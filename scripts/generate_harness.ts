import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { requireValue, nowIso } from "./_observer_tooling";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const TEMPLATES = path.join(ROOT, "templates");
const SPECS = path.join(ROOT, "specs");
const STATE = path.join(ROOT, ".state", "pipelines");
const PRESETS_PATH = path.join(TEMPLATES, "harness-presets.json");
const OBSERVER_DEFAULTS_PATH = path.join(ROOT, "config", "observer-defaults.json");

type Preset = Record<string, string>;
type Presets = Record<string, Preset>;
type Values = Record<string, string>;

function loadTemplate(name: string): string {
  return readFileSync(path.join(TEMPLATES, name), "utf8");
}

function loadPresets(): Presets {
  if (!existsSync(PRESETS_PATH)) return {};
  return JSON.parse(readFileSync(PRESETS_PATH, "utf8")) as Presets;
}

function loadObserverDefaults(): Record<string, unknown> {
  if (!existsSync(OBSERVER_DEFAULTS_PATH)) {
    return {
      role: "equal-rank-5min-observer",
      enabled: true,
      interval_minutes: 5,
      model: "minimax-portal/MiniMax-M2.7",
      reason: "오 분 관찰자 모델은 minimax 사용",
      track: false,
      priority: 0,
    };
  }

  const payload = JSON.parse(readFileSync(OBSERVER_DEFAULTS_PATH, "utf8")) as {
    observer?: Record<string, unknown>;
  };
  return payload.observer ?? {};
}

function render(template: string, values: Values): string {
  return Object.entries(values).reduce((acc, [key, value]) => {
    return acc.replace(new RegExp(`{{${key}}}`, "g"), value);
  }, template);
}

function defaultArtifacts(jobId: string): string {
  return `specs/${jobId}/plan.md, specs/${jobId}/spawn.md, specs/${jobId}/spawn-ready.md, .state/pipelines/${jobId}.json`;
}

function defaultDone(jobId: string): string {
  return `${jobId} 관련 계획, 스폰 지시문, 상태 파일이 모두 생성되고 검증된다`;
}

function buildRedteamBlock(values: Values): string {
  const tpl = loadTemplate("harness-redteam-template.md");
  return render(tpl, values).trim();
}

function parseArgv(argv: string[]): Record<string, string | undefined> {
  const map: Record<string, string | undefined> = {};
  let index = 0;
  while (index < argv.length) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      index += 1;
      continue;
    }
    const key = token.slice(2).replace(/-/g, "_");
    const next = argv[index + 1];
    if (next !== undefined && !next.startsWith("--")) {
      map[key] = next;
      index += 2;
      continue;
    }
    map[key] = "true";
    index += 1;
  }
  return map;
}

function parseArgs() {
  const argv = process.argv.slice(2);
  const positional = argv[0] && !argv[0].startsWith("--") ? argv[0] : "";
  const parsed = parseArgv(argv);
  const preset = parsed.preset as "research" | "implementation" | "refactor" | "deploy" | undefined;
  if (
    preset !== undefined &&
    !["research", "implementation", "refactor", "deploy"].includes(preset)
  ) {
    throw new Error(`invalid choice for --preset: ${preset}`);
  }

  if (!preset && (parsed.goal || parsed.scope || parsed.tests || parsed.done || parsed.artifacts || parsed.forbidden)) {
    parsed.preset = "custom";
  }

  return {
    jobId: positional,
    preset,
    goal: parsed.goal,
    scope: parsed.scope,
    tests: parsed.tests,
    done: parsed.done,
    artifacts: parsed.artifacts,
    forbidden: parsed.forbidden,
    state_summary: parsed.state_summary ?? "초기 생성",
    redteam_attack_1: parsed.redteam_attack_1,
    redteam_attack_2: parsed.redteam_attack_2,
    redteam_defense: parsed.redteam_defense,
    redteam_decision: parsed.redteam_decision,
  };
}

function mergeValues(jobId: string, args: ReturnType<typeof parseArgs>): Values {
  const presets = loadPresets();
  const presetValues = args.preset ? presets[args.preset] ?? {} : {};

  const values: Values = {
    job_id: jobId,
    goal: (args.goal ?? presetValues.goal ?? "").trim(),
    scope: (args.scope ?? presetValues.scope ?? "").trim(),
    tests: (args.tests ?? presetValues.tests ?? "").trim(),
    done: (args.done ?? presetValues.done ?? defaultDone(jobId)).trim(),
    artifacts: (args.artifacts ?? presetValues.artifacts ?? defaultArtifacts(jobId)).trim(),
    forbidden: (args.forbidden ?? presetValues.forbidden ?? "보호 디렉토리 삭제 금지, 범위 밖 변경 금지").trim(),
    state_summary: args.state_summary.trim(),
    preset: (args.preset ?? "custom").trim(),
    redteam_attack_1: (args.redteam_attack_1 ?? "범위가 커져서 원래 작업이 흔들릴 수 있음").trim(),
    redteam_attack_2: (args.redteam_attack_2 ?? "검증이 약하면 빈 문서만 늘어날 수 있음").trim(),
    redteam_defense: (args.redteam_defense ?? "범위, 테스트, 완료 조건, 산출물 경로를 강제해서 빈 작업을 줄인다").trim(),
    redteam_decision: (args.redteam_decision ?? "위험 수용").trim(),
  };

  for (const key of [
    "goal",
    "scope",
    "tests",
    "done",
    "artifacts",
    "forbidden",
    "state_summary",
    "redteam_attack_1",
    "redteam_attack_2",
    "redteam_defense",
    "redteam_decision",
  ] as const) {
    values[key] = render(requireValue(values[key], key), values);
  }

  values.redteam_block = buildRedteamBlock(values);
  return values;
}

function main(): void {
  const args = parseArgs();
  const jobId = requireValue(args.jobId, "job_id");

  const values = mergeValues(jobId, args);

  const specDir = path.join(SPECS, jobId);
  mkdirSync(specDir, { recursive: true });
  mkdirSync(STATE, { recursive: true });

  const planMd = render(loadTemplate("harness-plan-template.md"), values);
  const spawnMd = render(loadTemplate("harness-spawn-template.md"), values);
  const spawnReadyMd = spawnMd;

  const planPath = path.join(specDir, "plan.md");
  const spawnPath = path.join(specDir, "spawn.md");
  const spawnReadyPath = path.join(specDir, "spawn-ready.md");
  const statePath = path.join(STATE, `${jobId}.json`);

  writeFileSync(planPath, `${planMd}\n`, "utf8");
  writeFileSync(spawnPath, `${spawnMd}\n`, "utf8");
  writeFileSync(spawnReadyPath, `${spawnReadyMd}\n`, "utf8");

  const observerDefaults = loadObserverDefaults();
  const payload = {
    job_id: jobId,
    status: "proposal_pending",
    preset: values.preset,
    goal: values.goal,
    scope: values.scope,
    tests: values.tests,
    done: values.done,
    artifacts: values.artifacts,
    forbidden: values.forbidden,
    state_summary: values.state_summary,
    redteam: {
      attack_1: values.redteam_attack_1,
      attack_2: values.redteam_attack_2,
      defense: values.redteam_defense,
      decision: values.redteam_decision,
    },
    spec_path: path.relative(ROOT, planPath),
    spawn_path: path.relative(ROOT, spawnPath),
    spawn_ready_path: path.relative(ROOT, spawnReadyPath),
    observer: {
      role: String(observerDefaults.role ?? "equal-rank-5min-observer"),
      enabled: Boolean(observerDefaults.enabled ?? true),
      interval_minutes: Number(observerDefaults.interval_minutes ?? 5),
      model: String(observerDefaults.model ?? "minimax-portal/MiniMax-M2.7"),
      reason: String(observerDefaults.reason ?? "오 분 관찰자 모델은 minimax 사용"),
      track: Boolean(observerDefaults.track ?? false),
      priority: Number(observerDefaults.priority ?? 0),
    },
    nudge: {
      proposal_pending: true,
      minutes_threshold: 5,
      cooldown_minutes: 30,
      last_nudge_minutes_ago: null,
      risk: "normal",
      last_nudge_at: null,
      last_nudge_message: null,
    },
    created_at: nowIso(),
  };

  writeFileSync(statePath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

  process.stdout.write(
    JSON.stringify(
      {
        job_id: jobId,
        preset: values.preset,
        plan: path.relative(ROOT, planPath),
        spawn: path.relative(ROOT, spawnPath),
        spawn_ready: path.relative(ROOT, spawnReadyPath),
        state: path.relative(ROOT, statePath),
      },
      null,
      2,
    ) + "\n",
  );
}

if (import.meta.main) {
  main();
}
