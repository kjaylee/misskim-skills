#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
SPECS = ROOT / "specs"
STATE = ROOT / ".state" / "pipelines"
PRESETS_PATH = TEMPLATES / "harness-presets.json"


def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def load_presets() -> Dict[str, Dict[str, str]]:
    if not PRESETS_PATH.exists():
        return {}
    return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))


def render(template: str, values: Dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def require(value: Optional[str], field: str) -> str:
    if value is None or not value.strip():
        raise SystemExit(f"필수 값 누락: {field}")
    return value.strip()


def default_artifacts(job_id: str) -> str:
    return f"specs/{job_id}/plan.md, specs/{job_id}/spawn.md, specs/{job_id}/spawn-ready.md, .state/pipelines/{job_id}.json"


def default_done(job_id: str) -> str:
    return f"{job_id} 관련 계획, 스폰 지시문, 상태 파일이 모두 생성되고 검증된다"


def build_redteam_block(values: Dict[str, str]) -> str:
    tpl = load_template("harness-redteam-template.md")
    return render(tpl, values).strip()


def merge_values(job_id: str, args: argparse.Namespace) -> Dict[str, str]:
    presets = load_presets()
    preset_values = presets.get(args.preset, {}) if args.preset else {}

    values = {
        "job_id": job_id,
        "goal": (args.goal or preset_values.get("goal") or "").strip(),
        "scope": (args.scope or preset_values.get("scope") or "").strip(),
        "tests": (args.tests or preset_values.get("tests") or "").strip(),
        "done": (args.done or preset_values.get("done") or default_done(job_id)).strip(),
        "artifacts": (args.artifacts or preset_values.get("artifacts") or default_artifacts(job_id)).strip(),
        "forbidden": (args.forbidden or preset_values.get("forbidden") or "보호 디렉토리 삭제 금지, 범위 밖 변경 금지").strip(),
        "state_summary": (args.state_summary or "초기 생성").strip(),
        "preset": (args.preset or "custom").strip(),
        "redteam_attack_1": (args.redteam_attack_1 or "범위가 커져서 원래 작업이 흔들릴 수 있음").strip(),
        "redteam_attack_2": (args.redteam_attack_2 or "검증이 약하면 빈 문서만 늘어날 수 있음").strip(),
        "redteam_defense": (args.redteam_defense or "범위, 테스트, 완료 조건, 산출물 경로를 강제해서 빈 작업을 줄인다").strip(),
        "redteam_decision": (args.redteam_decision or "위험 수용").strip(),
    }

    for key in [
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
    ]:
        values[key] = render(require(values[key], key), values)

    values["redteam_block"] = build_redteam_block(values)
    return values


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="미스 김 내부 하네스 생성기")
    p.add_argument("job_id")
    p.add_argument("--preset", choices=["research", "implementation", "refactor", "deploy"])
    p.add_argument("--goal")
    p.add_argument("--scope")
    p.add_argument("--tests")
    p.add_argument("--done")
    p.add_argument("--artifacts")
    p.add_argument("--forbidden")
    p.add_argument("--state-summary", default="초기 생성")
    p.add_argument("--redteam-attack-1")
    p.add_argument("--redteam-attack-2")
    p.add_argument("--redteam-defense")
    p.add_argument("--redteam-decision")
    return p


def main() -> None:
    p = build_parser()
    args = p.parse_args()

    job_id = require(args.job_id, "job_id")
    values = merge_values(job_id, args)

    spec_dir = SPECS / job_id
    spec_dir.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)

    plan_md = render(load_template("harness-plan-template.md"), values)
    spawn_md = render(load_template("harness-spawn-template.md"), values)
    spawn_ready_md = spawn_md

    plan_path = spec_dir / "plan.md"
    spawn_path = spec_dir / "spawn.md"
    spawn_ready_path = spec_dir / "spawn-ready.md"
    state_path = STATE / f"{job_id}.json"

    plan_path.write_text(plan_md + "\n", encoding="utf-8")
    spawn_path.write_text(spawn_md + "\n", encoding="utf-8")
    spawn_ready_path.write_text(spawn_ready_md + "\n", encoding="utf-8")

    payload = {
        "job_id": job_id,
        "status": "planned",
        "preset": values["preset"],
        "goal": values["goal"],
        "scope": values["scope"],
        "tests": values["tests"],
        "done": values["done"],
        "artifacts": values["artifacts"],
        "forbidden": values["forbidden"],
        "state_summary": values["state_summary"],
        "redteam": {
            "attack_1": values["redteam_attack_1"],
            "attack_2": values["redteam_attack_2"],
            "defense": values["redteam_defense"],
            "decision": values["redteam_decision"],
        },
        "spec_path": str(plan_path.relative_to(ROOT)),
        "spawn_path": str(spawn_path.relative_to(ROOT)),
        "spawn_ready_path": str(spawn_ready_path.relative_to(ROOT)),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "job_id": job_id,
        "preset": values["preset"],
        "plan": str(plan_path.relative_to(ROOT)),
        "spawn": str(spawn_path.relative_to(ROOT)),
        "spawn_ready": str(spawn_ready_path.relative_to(ROOT)),
        "state": str(state_path.relative_to(ROOT)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
