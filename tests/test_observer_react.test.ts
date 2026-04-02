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

function runReact(args: string[]): Record<string, any> {
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "scripts/observer_react.ts", ...args],
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

describe("observer_react", () => {
  it("promotes waiting job to auto_execute and returns action plan", () => {
    const jobId = `observer-react-demo-${Date.now()}`;
    const harness = runHarness([jobId, "--preset", "implementation"]);
    const statePath = harness.state;
    register(statePath, `specs/${jobId}`);

    const statePathAbs = path.join(ROOT, statePath);
    const state = JSON.parse(readFileSync(statePathAbs, "utf8")) as Record<string, any>;
    state.created_at = "2026-04-02T00:00:00+00:00";
    writeFileSync(statePathAbs, `${JSON.stringify(state, null, 2)}\n`, "utf8");

    const payload = runReact([
      "--state-file",
      statePathAbs,
      "--minutes-since-reply",
      "10",
      "--apply",
      "--seed",
      "1",
    ]);
    expect(payload.should_act).toBe(true);
    expect(payload.job_id).toBe(jobId);
    expect(payload.spawn_ready_path).toBe(`specs/${jobId}/spawn-ready.md`);
    expect(payload.spawn_ready_json_path).toBe(`specs/${jobId}/spawn-ready.json`);
    expect(payload.action_plan.actionKind).toBe("implementation");
    expect(payload.action_plan.runtimeHint).toBe("subagent");
    expect(payload.action_plan.sessionHint).toBe("isolated");
    expect(payload.action_plan.spawnReadyPath).toBe(`specs/${jobId}/spawn-ready.md`);
    expect(payload.action_plan.spawnReadyJsonPath).toBe(`specs/${jobId}/spawn-ready.json`);
    expect(payload.action_plan.recommendedCommand).toContain(`specs/${jobId}/spawn-ready.md`);

    const updated = JSON.parse(readFileSync(statePathAbs, "utf8")) as Record<string, any>;
    expect(updated.status).toBe("auto_execute");
    expect(updated.nudge.proposal_pending).toBe(false);
    expect(updated.observer.last_auto_execute_at).toBeDefined();
  });
});
