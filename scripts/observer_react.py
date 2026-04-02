#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from observer_scan import scan
from equal_rank_nudge_bot import evaluate_state_file


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def promote(state_file: Path, top: Dict[str, Any], apply: bool) -> Dict[str, Any]:
    payload = json.loads(state_file.read_text(encoding="utf-8"))
    payload["status"] = "auto_execute"
    payload.setdefault("observer", {})
    payload["observer"]["last_auto_execute_at"] = now_iso()
    payload["observer"]["last_auto_execute_reason"] = top["reason"]
    payload.setdefault("nudge", {})
    payload["nudge"]["proposal_pending"] = False

    if apply:
        state_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "should_act": True,
        "job_id": payload.get("job_id"),
        "reason": top["reason"],
        "message": top["message"],
        "state_file": str(state_file),
        "spawn_ready_path": payload.get("spawn_ready_path"),
    }


def react(apply: bool, seed: Optional[int] = None) -> Dict[str, Any]:
    result = scan(apply=apply, seed=seed)
    top = result.get("top")
    if not top:
        return {
            "should_act": False,
            "reason": "eligible 없음",
            "message": None,
        }

    return promote(Path(top["state_file"]), top, apply)


def react_one(state_file: Path, minutes_since_reply: int, apply: bool, seed: Optional[int] = None) -> Dict[str, Any]:
    top = evaluate_state_file(
        state_file=state_file,
        minutes_since_reply=minutes_since_reply,
        seed=seed,
        apply=apply,
    )
    if not top.get("should_nudge"):
        return {
            "should_act": False,
            "reason": top["reason"],
            "message": None,
            "state_file": str(state_file),
        }
    return promote(state_file, top, apply)


def main() -> None:
    p = argparse.ArgumentParser(description="오 분 관찰자 반응기")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--seed", type=int)
    p.add_argument("--state-file")
    p.add_argument("--minutes-since-reply", type=int, default=10)
    args = p.parse_args()

    if args.state_file:
        result = react_one(Path(args.state_file), args.minutes_since_reply, args.apply, args.seed)
    else:
        result = react(apply=args.apply, seed=args.seed)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
