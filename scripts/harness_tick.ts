import { readFileSync, writeFileSync } from "node:fs";
import { evaluateStateFile } from "./equal_rank_nudge_bot";

type Args = {
  stateFile: string;
  minutesSinceReply: number;
  seed?: number;
  apply: boolean;
};

function parseArgs(argv: string[]): Args {
  const toFind = (key: string): string | undefined => {
    const idx = argv.indexOf(`--${key}`);
    if (idx === -1 || idx + 1 >= argv.length) return undefined;
    return argv[idx + 1];
  };
  const has = (key: string): boolean => argv.includes(`--${key}`);

  const stateFile = toFind("state-file");
  if (!stateFile) {
    throw new Error("required argument missing: --state-file");
  }

  const minutes = Number(toFind("minutes-since-reply"));
  if (!Number.isFinite(minutes)) {
    throw new Error("required argument missing or invalid: --minutes-since-reply");
  }

  return {
    stateFile,
    minutesSinceReply: minutes,
    seed: toFind("seed") ? Number(toFind("seed")) : undefined,
    apply: has("apply"),
  };
}

function main(): void {
  const args = parseArgs(process.argv.slice(2));
  const payload = JSON.parse(readFileSync(args.stateFile, "utf8")) as Record<string, unknown>;
  const nudge = (payload.nudge as Record<string, unknown>) ?? {};
  const status = payload.status;

  if (!Object.prototype.hasOwnProperty.call(nudge, "proposal_pending")) {
    const shouldNudge = ["planned", "proposal_pending", "waiting_reply"].includes(String(status));
    nudge.proposal_pending = shouldNudge;
    const nextPayload = { ...payload, nudge };
    if (args.apply) {
      writeFileSync(args.stateFile, `${JSON.stringify(nextPayload, null, 2)}\n`, "utf8");
    }
  }

  const result = evaluateStateFile(args.stateFile, args.minutesSinceReply, args.seed, args.apply);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (import.meta.main) {
  main();
}
