import { readFileSync, rmSync } from "node:fs";
import path from "node:path";
import { afterEach, describe, expect, it } from "bun:test";

const ROOT = process.cwd();
const generated: string[] = [];

function runNudge(args: string[]): Record<string, any> {
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "scripts/equal_rank_nudge_bot.ts", ...args],
    cwd: ROOT,
    stdout: "pipe",
    stderr: "pipe",
  });
  if (proc.exitCode !== 0) {
    throw new Error(new TextDecoder().decode(proc.stderr));
  }
  return JSON.parse(new TextDecoder().decode(proc.stdout));
}

function runHarness(args: string[]): Record<string, string> {
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "scripts/generate_harness.ts", ...args],
    cwd: ROOT,
    stdout: "pipe",
    stderr: "pipe",
  });
  if (proc.exitCode !== 0) throw new Error(new TextDecoder().decode(proc.stderr));
  return JSON.parse(new TextDecoder().decode(proc.stdout)) as Record<string, string>;
}

function register(statePath: string, specDir: string): void {
  generated.push(statePath);
  generated.push(specDir);
}

afterEach(() => {
  while (generated.length) {
    const rel = generated.pop();
    if (!rel) continue;
    const full = path.join(ROOT, rel);
    rmSync(full, { recursive: true, force: true });
  }
});

describe("equal_rank_nudge_bot", () => {
  it("nudges after five minutes", () => {
    const payload = runNudge(["--proposal-pending", "--minutes-since-reply", "6", "--seed", "1"]);
    expect(payload.should_nudge).toBe(true);
    expect(payload.message).not.toBeNull();
  });

  it("does not nudge before five minutes", () => {
    const payload = runNudge(["--proposal-pending", "--minutes-since-reply", "4"]);
    expect(payload.should_nudge).toBe(false);
    expect(payload.reason).toBe("오 분 미만");
  });

  it("does not nudge during cooldown", () => {
    const payload = runNudge([
      "--proposal-pending",
      "--minutes-since-reply",
      "9",
      "--last-nudge-minutes-ago",
      "10",
      "--cooldown-minutes",
      "30",
    ]);
    expect(payload.should_nudge).toBe(false);
    expect(payload.reason).toBe("쿨다운 중");
  });

  it("does not nudge on destructive risk", () => {
    const payload = runNudge([
      "--proposal-pending",
      "--minutes-since-reply",
      "12",
      "--risk",
      "destructive",
    ]);
    expect(payload.should_nudge).toBe(false);
    expect(payload.reason).toBe("파괴적 삭제 위험");
  });

  it("updates state file on apply", () => {
    const jobId = `state-linked-nudge-${Date.now()}`;
    const harness = runHarness([jobId, "--preset", "implementation"]);
    const statePath = harness.state;
    register(statePath, `specs/${jobId}`);

    const payload = runNudge([
      "--state-file",
      path.join(ROOT, statePath),
      "--minutes-since-reply",
      "7",
      "--seed",
      "1",
      "--apply",
    ]);
    expect(payload.should_nudge).toBe(true);

    const state = JSON.parse(readFileSync(path.join(ROOT, statePath), "utf8")) as Record<string, any>;
    expect(state.nudge.last_decision.reason).toBe("대기 상태 오 분 초과");
    expect(state.nudge.last_nudge_message).not.toBeNull();
    expect(state.nudge.last_nudge_minutes_ago).toBe(0);
  });
});
