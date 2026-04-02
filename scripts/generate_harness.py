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


def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def render(template: str, values: Dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def require(value: Optional[str], field: str) -> str:
    if value is None or not value.strip():
        raise SystemExit(f"필수 값 누락: {field}")
    return value.strip()


def main() -> None:
    p = argparse.ArgumentParser(description="미스 김 내부 하네스 생성기 최소안")
    p.add_argument("job_id")
    p.add_argument("--goal", required=True)
    p.add_argument("--scope", required=True)
    p.add_argument("--tests", required=True)
    p.add_argument("--done", required=True)
    p.add_argument("--artifacts", required=True)
    p.add_argument("--forbidden", default="보호 디렉토리 삭제 금지, 범위 밖 변경 금지")
    p.add_argument("--state-summary", default="초기 생성")
    args = p.parse_args()

    job_id = require(args.job_id, "job_id")
    values = {
        "job_id": job_id,
        "goal": require(args.goal, "goal"),
        "scope": require(args.scope, "scope"),
        "tests": require(args.tests, "tests"),
        "done": require(args.done, "done"),
        "artifacts": require(args.artifacts, "artifacts"),
        "forbidden": require(args.forbidden, "forbidden"),
        "state_summary": require(args.state_summary, "state_summary"),
    }

    spec_dir = SPECS / job_id
    spec_dir.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)

    plan_md = render(load_template("harness-plan-template.md"), values)
    spawn_md = render(load_template("harness-spawn-template.md"), values)

    plan_path = spec_dir / "plan.md"
    spawn_path = spec_dir / "spawn.md"
    state_path = STATE / f"{job_id}.json"

    plan_path.write_text(plan_md + "\n", encoding="utf-8")
    spawn_path.write_text(spawn_md + "\n", encoding="utf-8")

    payload = {
        "job_id": job_id,
        "status": "planned",
        "goal": values["goal"],
        "scope": values["scope"],
        "tests": values["tests"],
        "done": values["done"],
        "artifacts": values["artifacts"],
        "forbidden": values["forbidden"],
        "state_summary": values["state_summary"],
        "spec_path": str(plan_path.relative_to(ROOT)),
        "spawn_path": str(spawn_path.relative_to(ROOT)),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "job_id": job_id,
        "plan": str(plan_path.relative_to(ROOT)),
        "spawn": str(spawn_path.relative_to(ROOT)),
        "state": str(state_path.relative_to(ROOT)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
