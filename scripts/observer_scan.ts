import { existsSync, mkdirSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { evaluateStateFile } from "./equal_rank_nudge_bot";
import {
  buildActionPlanFromPayload,
  normalizeObserverHints,
  parseActionKind,
  parseNumber,
} from "./_observer_tooling";

type StatePayload = Record<string, unknown>;

type ScanResult = Record<string, unknown>;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const PIPELINES = path.join(ROOT, ".state", "pipelines");
const WAITING = new Set(["planned", "proposal_pending", "waiting_reply"]);
const EXCLUDED_TOKENS = new Set(["demo", "test", "sample", "데모", "테스트", "샘플"]);

function parseIso(value: unknown): Date | null {
  if (typeof value !== "string") return null;
  try {
    const date = new Date(value.replace("Z", "+00:00"));
    if (Number.isNaN(date.getTime())) return null;
    return date;
  } catch {
    return null;
  }
}

function ageMinutes(ts: Date | null): number | null {
  if (!ts) return null;
  const now = new Date();
  return Math.max(0, Math.floor((now.getTime() - ts.getTime()) / 60000));
}

function inferMinutesSinceReply(payload: StatePayload, statePath: string): number {
  const nudge = (payload.nudge as Record<string, unknown>) ?? {};
  const candidates: Array<unknown> = [
    nudge.last_user_reply_at,
    payload.updated_at,
    payload.created_at,
  ];
  for (const candidate of candidates) {
    const parsed = parseIso(candidate);
    const mins = ageMinutes(parsed);
    if (mins !== null) {
      return mins;
    }
  }

  const fallback = statSync(statePath).mtime;
  return ageMinutes(fallback) ?? 0;
}

function tokenize(value: unknown): string[] {
  if (value == null) return [];
  const text = String(value).toLowerCase();
  return text.split(/[^0-9a-z가-힣]+/g).filter(Boolean);
}

function isDemoTestSample(payload: StatePayload, statePath: string): boolean {
  const candidates = [
    payload.job_id,
    path.basename(statePath, ".json"),
    payload.spec_path,
    payload.spawn_path,
    payload.spawn_ready_path,
    payload.artifacts,
  ];
  for (const candidate of candidates) {
    const tokens = tokenize(candidate);
    if (tokens.some((token) => EXCLUDED_TOKENS.has(token))) return true;
  }
  return false;
}

function buildBaseResult(
  payload: StatePayload,
  stateFile: string,
  status: string,
  minutesSinceReply: number,
  observer: ReturnType<typeof normalizeObserverHints>,
): ScanResult {
  return {
    job_id: payload.job_id,
    state_file: stateFile,
    minutes_since_reply: minutesSinceReply,
    status,
    priority: observer.priority,
    observer_track: observer.track,
    action_plan: buildActionPlanFromPayload(payload, ROOT),
  };
}

function buildSkipResult(
  payload: StatePayload,
  stateFile: string,
  status: string,
  minutesSinceReply: number,
  observer: ReturnType<typeof normalizeObserverHints>,
  reason: string,
): ScanResult {
  return {
    ...buildBaseResult(payload, stateFile, status, minutesSinceReply, observer),
    should_nudge: false,
    reason,
    message: null,
  };
}

export function scan(apply: boolean, seed?: number) {
  if (!existsSync(PIPELINES)) {
    mkdirSync(PIPELINES, { recursive: true });
  }

  const files = readdirSync(PIPELINES)
    .filter((name) => name.endsWith(".json"))
    .sort();

  const results: ScanResult[] = [];

  for (const fileName of files) {
    const statePath = path.join(PIPELINES, fileName);
    const payload = JSON.parse(readFileSync(statePath, "utf8")) as StatePayload;
    const status = typeof payload.status === "string" ? payload.status : "planned";

    if (!WAITING.has(status)) continue;

    const observer = normalizeObserverHints(
      (payload.observer as Record<string, unknown> | undefined) ?? undefined,
      parseActionKind(payload.preset, "implementation"),
    );
    const minutes = inferMinutesSinceReply(payload, statePath);

    if (isDemoTestSample(payload, statePath)) {
      results.push(
        buildSkipResult(payload, statePath, status, minutes, observer, "데모/테스트/샘플 제외"),
      );
      continue;
    }

    if (!observer.track) {
      results.push(
        buildSkipResult(payload, statePath, status, minutes, observer, "observer.track 꺼짐"),
      );
      continue;
    }

    const decision = evaluateStateFile(statePath, minutes, seed, apply);
    results.push({
      ...buildBaseResult(payload, statePath, status, minutes, observer),
      ...decision,
    });
  }

  const eligible = results
    .filter((item) => item.should_nudge)
    .sort((left, right) => {
      const leftPriority = parseNumber(left.priority, 0);
      const rightPriority = parseNumber(right.priority, 0);
      if (leftPriority !== rightPriority) return rightPriority - leftPriority;
      const leftMinutes = parseNumber(left.minutes_since_reply, 0);
      const rightMinutes = parseNumber(right.minutes_since_reply, 0);
      if (leftMinutes !== rightMinutes) return rightMinutes - leftMinutes;
      return String(left.job_id ?? "").localeCompare(String(right.job_id ?? ""));
    });

  return {
    checked: results.length,
    eligible: eligible.length,
    top: eligible[0] ?? null,
    results,
  };
}

function parseArgs(argv: string[]): { apply: boolean; seed?: number } {
  const toFind = (key: string): string | undefined => {
    const idx = argv.indexOf(`--${key}`);
    if (idx === -1 || idx + 1 >= argv.length) return undefined;
    return argv[idx + 1];
  };
  const has = (key: string): boolean => argv.includes(`--${key}`);
  return {
    apply: has("apply"),
    seed: toFind("seed") ? Number(toFind("seed")) : undefined,
  };
}

function main(): void {
  const args = parseArgs(process.argv.slice(2));
  const result = scan(args.apply, args.seed);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (import.meta.main) {
  main();
}
