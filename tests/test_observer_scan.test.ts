import { readFileSync, rmSync, writeFileSync } from "node:fs";
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

function runScan(seed: number): Record<string, any> {
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "scripts/observer_scan.ts", "--seed", String(seed)],
    cwd: ROOT,
    stdout: "pipe",
    stderr: "pipe",
  });
  if (proc.exitCode !== 0) throw new Error(new TextDecoder().decode(proc.stderr));
  return JSON.parse(new TextDecoder().decode(proc.stdout));
}

function makeJob(opts: {
  jobId: string;
  preset?: "research" | "implementation" | "refactor" | "deploy";
  track: boolean;
  priority: number;
  createdAt: string;
}) {
  const payload = runHarness([opts.jobId, "--preset", opts.preset ?? "implementation"]);
  const statePath = payload.state;
  const stateFull = path.join(ROOT, statePath);
  const state = JSON.parse(readFileSync(stateFull, "utf8")) as Record<string, any>;
  state.created_at = opts.createdAt;
  state.observer ??= {};
  state.observer.track = opts.track;
  state.observer.priority = opts.priority;
  writeFileSync(stateFull, `${JSON.stringify(state, null, 2)}\n`, "utf8");
  register(statePath, `specs/${opts.jobId}`);
  return statePath;
}

function register(statePath: string, specDir: string): void {
  generated.push(statePath);
  generated.push(specDir);
}

function findResult(payload: Record<string, any>, jobId: string): Record<string, any> {
  const found = payload.results.find((item: any) => item.job_id === jobId);
  if (!found) throw new Error(`missing job_id in results: ${jobId}`);
  return found;
}

afterEach(() => {
  while (generated.length) {
    const rel = generated.pop();
    if (!rel) continue;
    const full = path.join(ROOT, rel);
    rmSync(full, { recursive: true, force: true });
  }
});

describe("observer_scan", () => {
  it("ignores demo test sample jobs by default", () => {
    const jobId = `observer-scan-demo-${Date.now()}`;
    makeJob({ jobId, track: true, priority: 1000, createdAt: "2026-04-01T00:00:00+00:00" });
    const payload = runScan(1);
    const result = findResult(payload, jobId);
    expect(result.should_nudge).toBe(false);
    expect(result.reason).toBe("데모/테스트/샘플 제외");
    expect(result.action_plan.spawnReadyJsonPath).toBe(`specs/${jobId}/spawn-ready.json`);
    const eligibleIds = new Set(
      payload.results.filter((item: any) => item.should_nudge).map((item: any) => item.job_id),
    );
    expect(eligibleIds.has(jobId)).toBe(false);
  });

  it("requires observer_track true", () => {
    const jobId = `observer-real-untracked-${Date.now()}`;
    makeJob({ jobId, track: false, priority: 900, createdAt: "2026-04-01T00:00:00+00:00" });
    const payload = runScan(1);
    const result = findResult(payload, jobId);
    expect(result.should_nudge).toBe(false);
    expect(result.reason).toBe("observer.track 꺼짐");
    expect(result.observer_track).toBe(false);
    expect(result.action_plan.actionKind).toBe("implementation");
  });

  it("prioritizes priority before age and returns action plan on top", () => {
    const olderJob = `observer-real-older-${Date.now()}`;
    const priorityJob = `observer-real-priority-${Date.now()}`;
    makeJob({ jobId: olderJob, track: true, priority: 900, createdAt: "2026-04-01T00:00:00+00:00" });
    makeJob({ jobId: priorityJob, track: true, priority: 1000, createdAt: "2026-04-02T03:50:00+00:00" });

    const payload = runScan(1);
    const tracked = payload.results.filter((item: any) =>
      [olderJob, priorityJob].includes(item.job_id),
    );

    expect(tracked.length).toBe(2);
    const sorted = [...tracked].sort((a: any, b: any) => {
      if (a.priority !== b.priority) return b.priority - a.priority;
      if (a.minutes_since_reply !== b.minutes_since_reply) return b.minutes_since_reply - a.minutes_since_reply;
      return String(a.job_id).localeCompare(String(b.job_id));
    });
    expect(sorted[0].job_id).toBe(priorityJob);
    expect(sorted[0].priority).toBe(1000);
    expect(sorted[0].minutes_since_reply).toBeGreaterThanOrEqual(5);
    expect(payload.top.job_id).toBe(priorityJob);
    expect(payload.top.action_plan.actionKind).toBe("implementation");
    expect(payload.top.action_plan.runtimeHint).toBe("subagent");
    expect(payload.top.action_plan.sessionHint).toBe("isolated");
    expect(payload.top.action_plan.spawnReadyPath).toBe(`specs/${priorityJob}/spawn-ready.md`);
    expect(payload.top.action_plan.spawnReadyJsonPath).toBe(`specs/${priorityJob}/spawn-ready.json`);
    expect(payload.top.action_plan.recommendedCommand).toContain(`specs/${priorityJob}/spawn-ready.md`);
  });
});
