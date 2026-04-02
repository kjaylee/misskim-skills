#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from equal_rank_nudge_bot import evaluate_state_file


WAITING_STATUSES = {"planned", "proposal_pending", "waiting_reply"}


def main() -> None:
    p = argparse.ArgumentParser(description="하네스 상태 파일 틱 처리기")
    p.add_argument("--state-file", required=True)
    p.add_argument("--minutes-since-reply", type=int, required=True)
    p.add_argument("--seed", type=int)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    state_file = Path(args.state_file)
    payload = json.loads(state_file.read_text(encoding="utf-8"))

    nudge = payload.get("nudge", {})
    status = payload.get("status", "planned")

    if "proposal_pending" not in nudge:
        nudge["proposal_pending"] = status in WAITING_STATUSES
        payload["nudge"] = nudge
        if args.apply:
            state_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = evaluate_state_file(
        state_file=state_file,
        minutes_since_reply=args.minutes_since_reply,
        seed=args.seed,
        apply=args.apply,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
