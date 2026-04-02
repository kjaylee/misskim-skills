import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { evaluateStateFile } from "./equal_rank_nudge_bot";
import { buildActionPlanFromPayload, parseNumber } from "./_observer_tooling";
import { scan } from "./observer_scan";

type ScanTop = {
  state_file: string;
  reason: string;
  message: string | null;
};

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

function nowIso(): string {
  return new Date().toISOString();
}

function readState(stateFile: string): Record<string, unknown> {
  return JSON.parse(readFileSync(stateFile, "utf8")) as Record<string, unknown>;
}

function buildResponse(
  payload: Record<string, unknown>,
  stateFile: string,
  top: ScanTop,
  shouldAct: boolean,
) {
  const actionPlan = buildActionPlanFromPayload(payload, ROOT);
  return {
    should_act: shouldAct,
    job_id: payload.job_id,
    reason: top.reason,
    message: shouldAct ? top.message : null,
    state_file: path.resolve(stateFile),
    spawn_ready_path: payload.spawn_ready_path,
    spawn_ready_json_path: payload.spawn_ready_json_path,
    action_plan: actionPlan,
  };
}

function promote(stateFile: string, top: ScanTop, apply: boolean) {
  const payload = readState(stateFile);
  payload.status = "auto_execute";
  payload.observer = (payload.observer as Record<string, unknown>) ?? {};
  (payload.observer as Record<string, unknown>).last_auto_execute_at = nowIso();
  (payload.observer as Record<string, unknown>).last_auto_execute_reason = top.reason;
  payload.nudge = (payload.nudge as Record<string, unknown>) ?? {};
  (payload.nudge as Record<string, unknown>).proposal_pending = false;

  if (apply) {
    writeFileSync(stateFile, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  }

  return buildResponse(payload, stateFile, top, true);
}

function reactOne(
  stateFile: string,
  minutesSinceReply: number,
  apply: boolean,
  seed?: number,
) {
  const top = evaluateStateFile(stateFile, minutesSinceReply, seed, apply);
  const payload = readState(stateFile);
  if (!top.should_nudge) {
    return buildResponse(payload, stateFile, top as ScanTop, false);
  }
  return promote(stateFile, top as ScanTop, apply);
}

function react(apply: boolean, seed?: number) {
  const result = scan(apply, seed);
  const top = result.top;
  if (!top) {
    return {
      should_act: false,
      reason: "eligible 없음",
      message: null,
      action_plan: null,
    };
  }
  return promote(String(top.state_file), top as ScanTop, apply);
}

function parseArgs(argv: string[]): {
  apply: boolean;
  seed?: number;
  stateFile?: string;
  minutesSinceReply: number;
} {
  const toFind = (key: string): string | undefined => {
    const idx = argv.indexOf(`--${key}`);
    if (idx === -1 || idx + 1 >= argv.length) return undefined;
    return argv[idx + 1];
  };
  const has = (key: string): boolean => argv.includes(`--${key}`);
  const minutesSinceReply = toFind("minutes-since-reply") ? Number(toFind("minutes-since-reply")) : 10;
  return {
    apply: has("apply"),
    seed: toFind("seed") ? Number(toFind("seed")) : undefined,
    stateFile: toFind("state-file"),
    minutesSinceReply: parseNumber(minutesSinceReply, 10),
  };
}

function main(): void {
  const args = parseArgs(process.argv.slice(2));
  const result = args.stateFile
    ? reactOne(args.stateFile, args.minutesSinceReply, args.apply, args.seed)
    : react(args.apply, args.seed);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (import.meta.main) {
  main();
}
