import { existsSync, rmSync, readFileSync } from "node:fs";
import path from "node:path";
import { afterEach, describe, expect, it } from "bun:test";

const ROOT = process.cwd();
const generated: string[] = [];

function runGenerate(args: string[]): Record<string, string> {
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "scripts/generate_harness.ts", ...args],
    cwd: ROOT,
    stdout: "pipe",
    stderr: "pipe",
  });
  if (proc.exitCode !== 0) {
    throw new Error(new TextDecoder().decode(proc.stderr));
  }
  return JSON.parse(new TextDecoder().decode(proc.stdout)) as Record<string, string>;
}

function register(pathRel: string): void {
  generated.push(pathRel);
}

afterEach(() => {
  while (generated.length) {
    const rel = generated.pop();
    if (!rel) continue;
    const full = path.join(ROOT, rel);
    if (existsSync(full)) {
      rmSync(full, { recursive: true, force: true });
    }
  }
});

describe("generate_harness", () => {
  it("creates custom harness artifacts", () => {
    const jobId = `test-custom-harness-${Date.now()}`;
    const payload = runGenerate([
      jobId,
      "--goal",
      "커스텀 작업",
      "--scope",
      "출력 파일 확인",
      "--tests",
      "파일 생성 확인",
      "--done",
      "세 파일 생성",
      "--artifacts",
      `specs/${jobId}/plan.md, specs/${jobId}/spawn.md, specs/${jobId}/spawn-ready.md, .state/pipelines/${jobId}.json`,
    ]);

    register(payload.state);
    const specDir = `specs/${jobId}`;
    register(specDir);

    expect(payload.job_id).toBe(jobId);
    const state = JSON.parse(readFileSync(path.join(ROOT, payload.state), "utf8")) as Record<string, any>;
    expect(existsSync(path.join(ROOT, payload.plan))).toBe(true);
    expect(existsSync(path.join(ROOT, payload.spawn))).toBe(true);
    expect(existsSync(path.join(ROOT, payload.spawn_ready))).toBe(true);
    expect(existsSync(path.join(ROOT, payload.state))).toBe(true);
    expect(state.observer.track).toBe(false);
    expect(state.observer.priority).toBe(0);
  });

  it("generates preset harness", () => {
    const jobId = `test-research-harness-${Date.now()}`;
    const payload = runGenerate([jobId, "--preset", "research"]);

    register(payload.state);
    const specDir = `specs/${jobId}`;
    register(specDir);

    const planText = readFileSync(path.join(ROOT, payload.plan), "utf8");
    const spawnReadyText = readFileSync(path.join(ROOT, payload.spawn_ready), "utf8");
    const state = JSON.parse(readFileSync(path.join(ROOT, payload.state), "utf8")) as Record<string, any>;

    expect(payload.preset).toBe("research");
    expect(planText).toContain("리서치 작업 수행");
    expect(state.preset).toBe("research");
    expect(state.artifacts).toContain(`specs/${jobId}/results.md`);
    expect(spawnReadyText).toContain("레드팀");
    expect(spawnReadyText).toContain("실행 원칙");
    expect(state.status).toBe("proposal_pending");
    expect(state.observer.model).toBe("minimax-portal/MiniMax-M2.7");
    expect(state.observer.interval_minutes).toBe(5);
    expect(state.observer.track).toBe(false);
    expect(state.observer.priority).toBe(0);
    expect(state.nudge.proposal_pending).toBe(true);
    expect(state.nudge.minutes_threshold).toBe(5);
  });
});
