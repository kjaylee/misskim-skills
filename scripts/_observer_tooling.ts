import { existsSync, readFileSync, writeFileSync } from "node:fs";

export type JsonPayload = Record<string, unknown>;

export type DecisionResult = {
  should_nudge: boolean;
  reason: string;
  message: string | null;
};

export type EvaluateStateResult = {
  job_id?: string;
  state_file: string;
} & DecisionResult;

export const MESSAGES = [
  "알아서 최선 판단 후 진행.",
  "확인 불필요. 범위 안에서 먼저 실행.",
  "오 분 지남. 가장 보수적이면서 생산적인 안으로 진행.",
] as const;

export const BLOCK_REASONS: Record<string, string> = {
  destructive: "파괴적 삭제 위험",
  external_send: "외부 발신 위험",
  permission: "권한 충돌",
  contradiction: "요구사항 모순",
};

const WAITING_STATUSES = new Set(["planned", "proposal_pending", "waiting_reply"]);

export function requireValue(value: string | undefined, field: string): string {
  if (!value || !value.trim()) {
    throw new Error(`필수 값 누락: ${field}`);
  }
  return value.trim();
}

export function nowIso(): string {
  return new Date().toISOString();
}

export function readJson<T = JsonPayload>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

export function writeJson(path: string, payload: JsonPayload): void {
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

export function parseBoolean(value: unknown, defaultValue = false): boolean {
  if (typeof value === "boolean") return value;
  if (value == null) return defaultValue;
  if (typeof value === "number") return Boolean(value);
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase();
    if (["1", "true", "yes", "y", "on"].includes(normalized)) return true;
    if (["0", "false", "no", "n", "off", ""].includes(normalized)) return false;
  }
  return defaultValue;
}

export function parseNumber(value: unknown, defaultValue = 0): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : defaultValue;
}

export function decideNudge(input: {
  proposalPending: boolean;
  minutesSinceReply: number;
  cooldownMinutes: number;
  lastNudgeMinutesAgo?: number | null;
  risk: string;
  seed?: number;
}): DecisionResult {
  const { proposalPending, minutesSinceReply, cooldownMinutes, lastNudgeMinutesAgo, risk, seed } = input;

  if (!proposalPending) {
    return { should_nudge: false, reason: "대기 상태 아님", message: null };
  }

  if (minutesSinceReply < 5) {
    return { should_nudge: false, reason: "오 분 미만", message: null };
  }

  if (risk in BLOCK_REASONS) {
    return { should_nudge: false, reason: BLOCK_REASONS[risk], message: null };
  }

  if (lastNudgeMinutesAgo != null && lastNudgeMinutesAgo < cooldownMinutes) {
    return { should_nudge: false, reason: "쿨다운 중", message: null };
  }

  const messages = Array.from(MESSAGES);
  const idx = seed === undefined ? Math.floor(Math.random() * messages.length) : Math.abs(seed) % messages.length;
  return {
    should_nudge: true,
    reason: "대기 상태 오 분 초과",
    message: messages[idx],
  };
}

export function evaluateStateFile(
  stateFile: string,
  args: { minutesSinceReply: number; seed?: number; apply: boolean },
): EvaluateStateResult {
  const payload = readJson<Record<string, unknown>>(stateFile);
  const nudge = (payload.nudge as Record<string, unknown>) ?? {};
  const status = typeof payload.status === "string" ? payload.status : "proposal_pending";
  const proposalPending = Boolean(
    (nudge.proposal_pending as boolean | undefined) ?? WAITING_STATUSES.has(status),
  );
  const decision = decideNudge({
    proposalPending,
    minutesSinceReply: args.minutesSinceReply,
    cooldownMinutes: parseNumber((nudge.cooldown_minutes as number | undefined) ?? 30),
    lastNudgeMinutesAgo: nudge.last_nudge_minutes_ago as number | null | undefined,
    risk: typeof nudge.risk === "string" ? nudge.risk : "normal",
    seed: args.seed,
  });

  const nextNudge: Record<string, unknown> = {
    ...nudge,
    last_checked_at: nowIso(),
    last_minutes_since_reply: args.minutesSinceReply,
    last_decision: decision,
  };

  if (args.apply && decision.should_nudge) {
    nextNudge.last_nudge_at = nowIso();
    nextNudge.last_nudge_message = decision.message;
    nextNudge.last_nudge_minutes_ago = 0;
  }

  if (args.apply) {
    writeJson(stateFile, { ...payload, nudge: nextNudge });
  }

  return {
    job_id: (payload.job_id as string | undefined) ?? undefined,
    state_file: stateFile,
    ...decision,
  };
}
