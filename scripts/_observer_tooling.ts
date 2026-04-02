import { existsSync, readFileSync, writeFileSync } from "node:fs";

export type JsonPayload = Record<string, unknown>;
export const ACTION_KINDS = ["research", "implementation", "refactor", "deploy"] as const;
export const RUNTIME_HINTS = ["main", "subagent"] as const;
export const SESSION_HINTS = ["main", "isolated"] as const;

export type ActionKind = (typeof ACTION_KINDS)[number];
export type RuntimeHint = (typeof RUNTIME_HINTS)[number];
export type SessionHint = (typeof SESSION_HINTS)[number];

export type ObserverHints = {
  role: string;
  enabled: boolean;
  interval_minutes: number;
  model: string;
  reason: string;
  track: boolean;
  priority: number;
  action_kind: ActionKind;
  runtime_hint: RuntimeHint;
  session_hint: SessionHint;
};

export type ActionPlan = {
  actionKind: ActionKind;
  runtimeHint: RuntimeHint;
  sessionHint: SessionHint;
  spawnReadyPath: string | null;
  spawnReadyJsonPath: string | null;
  recommendedCommand: string;
};

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

function parseChoice<T extends string>(
  value: unknown,
  allowed: readonly T[],
  defaultValue: T,
): T {
  if (typeof value !== "string") return defaultValue;
  const normalized = value.trim().toLowerCase();
  return (allowed as readonly string[]).includes(normalized)
    ? (normalized as T)
    : defaultValue;
}

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
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`);
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

export function parseActionKind(value: unknown, defaultValue: ActionKind = "implementation"): ActionKind {
  return parseChoice(value, ACTION_KINDS, defaultValue);
}

export function parseRuntimeHint(value: unknown, defaultValue: RuntimeHint = "subagent"): RuntimeHint {
  return parseChoice(value, RUNTIME_HINTS, defaultValue);
}

export function parseSessionHint(value: unknown, defaultValue: SessionHint = "isolated"): SessionHint {
  return parseChoice(value, SESSION_HINTS, defaultValue);
}

export function defaultRuntimeHint(actionKind: ActionKind): RuntimeHint {
  if (actionKind === "research" || actionKind === "deploy") return "main";
  return "subagent";
}

export function defaultSessionHint(actionKind: ActionKind): SessionHint {
  if (actionKind === "research" || actionKind === "deploy") return "main";
  return "isolated";
}

export function normalizeObserverHints(
  observer: Record<string, unknown> | undefined,
  fallbackActionKind: ActionKind = "implementation",
): ObserverHints {
  const actionKind = parseActionKind(observer?.action_kind, fallbackActionKind);
  return {
    role: String(observer?.role ?? "equal-rank-5min-observer"),
    enabled: parseBoolean(observer?.enabled, true),
    interval_minutes: parseNumber(observer?.interval_minutes, 5),
    model: String(observer?.model ?? "minimax-portal/MiniMax-M2.7"),
    reason: String(observer?.reason ?? "오 분 관찰자 모델은 minimax 사용"),
    track: parseBoolean(observer?.track, false),
    priority: parseNumber(observer?.priority, 0),
    action_kind: actionKind,
    runtime_hint: parseRuntimeHint(observer?.runtime_hint, defaultRuntimeHint(actionKind)),
    session_hint: parseSessionHint(observer?.session_hint, defaultSessionHint(actionKind)),
  };
}

function shellQuote(value: string): string {
  if (!value) return "''";
  return `'${value.replace(/'/g, `'\\''`)}'`;
}

export function buildRecommendedCommand(
  root: string,
  spawnReadyPath: string | null,
  runtimeHint: RuntimeHint,
): string {
  const cdRoot = `cd ${shellQuote(root)}`;
  if (!spawnReadyPath) return cdRoot;

  const catPrompt = `cat ${shellQuote(spawnReadyPath)}`;
  if (runtimeHint === "subagent") {
    return `${cdRoot} && codex exec --full-auto "$(${catPrompt})"`;
  }
  return `${cdRoot} && ${catPrompt}`;
}

export function buildActionPlanFromPayload(payload: Record<string, unknown>, root: string): ActionPlan {
  const presetActionKind = parseActionKind(payload.preset, "implementation");
  const observer = normalizeObserverHints(
    (payload.observer as Record<string, unknown> | undefined) ?? undefined,
    presetActionKind,
  );
  const spawnReadyPath = typeof payload.spawn_ready_path === "string" ? payload.spawn_ready_path : null;
  const spawnReadyJsonPath =
    typeof payload.spawn_ready_json_path === "string" ? payload.spawn_ready_json_path : null;

  return {
    actionKind: observer.action_kind,
    runtimeHint: observer.runtime_hint,
    sessionHint: observer.session_hint,
    spawnReadyPath,
    spawnReadyJsonPath,
    recommendedCommand: buildRecommendedCommand(root, spawnReadyPath, observer.runtime_hint),
  };
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
