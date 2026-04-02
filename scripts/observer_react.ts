import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { evaluateStateFile } from "./equal_rank_nudge_bot";
import { scan } from "./observer_scan";
import { parseNumber } from "./_observer_tooling";

type ScanTop = {
  state_file: string;
  reason: string;
  message: string | null;
};

function nowIso(): string {
  return new Date().toISOString();
}

function promote(stateFile: string, top: ScanTop, apply: boolean) {
  const payload = JSON.parse(readFileSync(stateFile, "utf8")) as Record<string, unknown>;
  payload.status = "auto_execute";
  payload.observer = (payload.observer as Record<string, unknown>) ?? {};
  (payload.observer as Record<string, unknown>).last_auto_execute_at = nowIso();
  (payload.observer as Record<string, unknown>).last_auto_execute_reason = top.reason;
  payload.nudge = (payload.nudge as Record<string, unknown>) ?? {};
  (payload.nudge as Record<string, unknown>).proposal_pending = false;

  if (apply) {
    writeFileSync(stateFile, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  }

  return {
    should_act: true,
    job_id: payload.job_id,
    reason: top.reason,
    message: top.message,
    state_file: path.resolve(stateFile),
    spawn_ready_path: (payload as Record<string, unknown>).spawn_ready_path,
  };
}

function reactOne(
  stateFile: string,
  minutesSinceReply: number,
  apply: boolean,
  seed?: number,
) {
  const top = evaluateStateFile(stateFile, minutesSinceReply, seed, apply);
  if (!top.should_nudge) {
    return {
      should_act: false,
      reason: top.reason,
      message: null,
      state_file: stateFile,
    };
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
