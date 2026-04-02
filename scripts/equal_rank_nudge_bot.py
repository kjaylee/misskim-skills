#!/usr/bin/env python3
import argparse
import json
import random
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


def main() -> None:
    p = argparse.ArgumentParser(description="동급 권한 위임 리마인더 최소판")
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
    args = p.parse_args()

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
