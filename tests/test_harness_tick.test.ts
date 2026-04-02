import { readFileSync, writeFileSync, rmSync } from "node:fs";
import path from "node:path";
import { afterEach, describe, expect, it } from "bun:test";

const ROOT = process.cwd();
const generated: string[] = [];

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

function runTick(args: string[]): Record<string, any> {
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "scripts/harness_tick.ts", ...args],
    cwd: ROOT,
    stdout: "pipe",
    stderr: "pipe",
  });
  if (proc.exitCode !== 0) throw new Error(new TextDecoder().decode(proc.stderr));
  return JSON.parse(new TextDecoder().decode(proc.stdout));
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

describe("harness_tick", () => {
  it("nudges waiting job", () => {
    const jobId = `tick-waiting-job-${Date.now()}`;
    const harness = runHarness([jobId, "--preset", "implementation"]);
    const statePath = harness.state;
    register(statePath, `specs/${jobId}`);

    const payload = runTick([
      "--state-file",
      path.join(ROOT, statePath),
      "--minutes-since-reply",
      "8",
      "--seed",
      "1",
      "--apply",
    ]);
    expect(payload.should_nudge).toBe(true);
  });

  it("does not nudge active job", () => {
    const jobId = `tick-active-job-${Date.now()}`;
    const harness = runHarness([jobId, "--preset", "implementation"]);
    const statePath = harness.state;
    register(statePath, `specs/${jobId}`);

    const state = JSON.parse(readFileSync(path.join(ROOT, statePath), "utf8")) as Record<string, any>;
    state.status = "active";
    state.nudge.proposal_pending = false;
    writeFileSync(path.join(ROOT, statePath), `${JSON.stringify(state, null, 2)}\n`, "utf8");

    const payload = runTick([
      "--state-file",
      path.join(ROOT, statePath),
      "--minutes-since-reply",
      "8",
      "--seed",
      "1",
      "--apply",
    ]);
    expect(payload.should_nudge).toBe(false);
    expect(payload.reason).toBe("대기 상태 아님");
  });
});
