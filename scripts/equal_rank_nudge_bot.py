#!/usr/bin/env python3
import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

MESSAGES = [
    "알아서 최선 판단 후 진행.",
    "확인 불필요. 범위 안에서 먼저 실행.",
    "오 분 지남. 가장 보수적이면서 생산적인 안으로 진행.",
]

BLOCK_REASONS = {
    "destructive": "파괴적 삭제 위험",
    "external_send": "외부 발신 위험",
    "permission": "권한 충돌",
    "contradiction": "요구사항 모순",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def decide(
    proposal_pending: bool,
    minutes_since_reply: int,
    cooldown_minutes: int,
    last_nudge_minutes_ago: Optional[int],
    risk: str,
    seed: Optional[int] = None,
):
    if not proposal_pending:
        return {
            "should_nudge": False,
            "reason": "대기 상태 아님",
            "message": None,
        }

    if minutes_since_reply < 5:
        return {
            "should_nudge": False,
            "reason": "오 분 미만",
            "message": None,
        }

    if risk in BLOCK_REASONS:
        return {
            "should_nudge": False,
            "reason": BLOCK_REASONS[risk],
            "message": None,
        }

    if last_nudge_minutes_ago is not None and last_nudge_minutes_ago < cooldown_minutes:
        return {
            "should_nudge": False,
            "reason": "쿨다운 중",
            "message": None,
        }

    chooser = random.Random(seed) if seed is not None else random
    message = chooser.choice(MESSAGES)
    return {
        "should_nudge": True,
        "reason": "대기 상태 오 분 초과",
        "message": message,
    }


def evaluate_state_file(
    state_file: Path,
    minutes_since_reply: int,
    seed: Optional[int],
    apply: bool,
):
    payload = json.loads(state_file.read_text(encoding="utf-8"))
    nudge = payload.get("nudge", {})
    result = decide(
        proposal_pending=bool(nudge.get("proposal_pending", False)),
        minutes_since_reply=minutes_since_reply,
        cooldown_minutes=int(nudge.get("cooldown_minutes", 30)),
        last_nudge_minutes_ago=nudge.get("last_nudge_minutes_ago"),
        risk=nudge.get("risk", "normal"),
        seed=seed,
    )

    payload["nudge"] = {
        **nudge,
        "last_checked_at": now_iso(),
        "last_minutes_since_reply": minutes_since_reply,
        "last_decision": result,
    }

    if apply and result["should_nudge"]:
        payload["nudge"]["last_nudge_at"] = now_iso()
        payload["nudge"]["last_nudge_message"] = result["message"]
        payload["nudge"]["last_nudge_minutes_ago"] = 0

    if apply:
        state_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "job_id": payload.get("job_id"),
        "state_file": str(state_file),
        **result,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="동급 권한 위임 리마인더")
    p.add_argument("--proposal-pending", action="store_true")
    p.add_argument("--minutes-since-reply", type=int, required=True)
    p.add_argument("--cooldown-minutes", type=int, default=30)
    p.add_argument("--last-nudge-minutes-ago", type=int)
    p.add_argument(
        "--risk",
        choices=["normal", "destructive", "external_send", "permission", "contradiction"],
        default="normal",
    )
    p.add_argument("--seed", type=int)
    p.add_argument("--state-file")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    if args.state_file:
        result = evaluate_state_file(
            state_file=Path(args.state_file),
            minutes_since_reply=args.minutes_since_reply,
            seed=args.seed,
            apply=args.apply,
        )
    else:
        result = decide(
            proposal_pending=args.proposal_pending,
            minutes_since_reply=args.minutes_since_reply,
            cooldown_minutes=args.cooldown_minutes,
            last_nudge_minutes_ago=args.last_nudge_minutes_ago,
            risk=args.risk,
            seed=args.seed,
        )

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
