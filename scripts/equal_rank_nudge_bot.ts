import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import {
  BLOCK_REASONS,
  DecisionResult,
  decideNudge,
  nowIso,
  parseNumber,
  requireValue,
} from "./_observer_tooling";

type StatePayload = Record<string, unknown>;

function decide(
  proposalPending: boolean,
  minutesSinceReply: number,
  cooldownMinutes: number,
  lastNudgeMinutesAgo: number | null | undefined,
  risk: string,
  seed?: number,
): DecisionResult {
  return decideNudge({
    proposalPending,
    minutesSinceReply,
    cooldownMinutes,
    lastNudgeMinutesAgo,
    risk,
    seed,
  });
}

export function evaluateStateFile(
  stateFile: string,
  minutesSinceReply: number,
  seed: number | undefined,
  apply: boolean,
) {
  const payload = JSON.parse(readFileSync(stateFile, "utf8")) as StatePayload;
  const nudge = (payload.nudge as Record<string, unknown>) ?? {};
  const status = typeof payload.status === "string" ? payload.status : "proposal_pending";
  const proposalPending = Boolean(
    (nudge.proposal_pending as boolean | undefined) ?? ["planned", "proposal_pending", "waiting_reply"].includes(status),
  );

  const result = decide(
    proposalPending,
    minutesSinceReply,
    parseNumber(nudge.cooldown_minutes, 30),
    (nudge.last_nudge_minutes_ago as number | null | undefined) ?? null,
    typeof nudge.risk === "string" ? nudge.risk : "normal",
    seed,
  );

  const nextNudge = {
    ...nudge,
    last_checked_at: nowIso(),
    last_minutes_since_reply: minutesSinceReply,
    last_decision: result,
  };
  const nextPayload = { ...payload, nudge: nextNudge };

  if (apply && result.should_nudge) {
    nextPayload.nudge = {
      ...nextNudge,
      last_nudge_at: nowIso(),
      last_nudge_message: result.message,
      last_nudge_minutes_ago: 0,
    };
  }

  if (apply) {
    writeFileSync(stateFile, `${JSON.stringify(nextPayload, null, 2)}\n`, "utf8");
  }

  return {
    job_id: nextPayload.job_id as string | undefined,
    state_file: path.resolve(stateFile),
    ...result,
  };
}

function parseArgs(): {
  proposalPending: boolean;
  minutesSinceReply?: number;
  cooldownMinutes: number;
  lastNudgeMinutesAgo?: number;
  risk: keyof typeof BLOCK_REASONS | "normal";
  seed?: number;
  stateFile?: string;
  apply: boolean;
} {
  const argv = process.argv.slice(2);
  const toFind = (key: string): string | undefined => {
    const idx = argv.indexOf(`--${key}`);
    if (idx === -1 || idx + 1 >= argv.length) return undefined;
    return argv[idx + 1];
  };
  const has = (key: string): boolean => argv.includes(`--${key}`);

  const risk = (toFind("risk") ?? "normal") as keyof typeof BLOCK_REASONS | "normal";
  if (!["normal", "destructive", "external_send", "permission", "contradiction"].includes(risk)) {
    throw new Error(`invalid risk: ${risk}`);
  }

  return {
    proposalPending: has("proposal-pending"),
    minutesSinceReply: toFind("minutes-since-reply") ? Number(toFind("minutes-since-reply")) : undefined,
    cooldownMinutes: toFind("cooldown-minutes") ? Number(toFind("cooldown-minutes")) : 30,
    lastNudgeMinutesAgo: toFind("last-nudge-minutes-ago")
      ? Number(toFind("last-nudge-minutes-ago"))
      : undefined,
    risk,
    seed: toFind("seed") ? Number(toFind("seed")) : undefined,
    stateFile: toFind("state-file"),
    apply: has("apply"),
  };
}

function main(): void {
  const args = parseArgs();
  requireValue(typeof args.minutesSinceReply === "number" && Number.isFinite(args.minutesSinceReply) ? String(args.minutesSinceReply) : undefined, "minutes_since_reply");

  if (args.stateFile) {
    const result = evaluateStateFile(
      args.stateFile,
      args.minutesSinceReply ?? 0,
      args.seed,
      args.apply,
    );
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }

  const result = decide(
    args.proposalPending,
    args.minutesSinceReply ?? 0,
    args.cooldownMinutes,
    args.lastNudgeMinutesAgo,
    args.risk,
    args.seed,
  );

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (import.meta.main) {
  main();
}
