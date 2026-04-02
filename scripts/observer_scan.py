#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from equal_rank_nudge_bot import evaluate_state_file

ROOT = Path(__file__).resolve().parents[1]
PIPELINES = ROOT / ".state" / "pipelines"
WAITING = {"planned", "proposal_pending", "waiting_reply"}


def parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def age_minutes(ts: Optional[datetime]) -> Optional[int]:
    if ts is None:
        return None
    now = datetime.now(timezone.utc)
    delta = now - ts.astimezone(timezone.utc)
    return max(0, int(delta.total_seconds() // 60))


def infer_minutes_since_reply(payload: Dict[str, Any], state_path: Path) -> int:
    nudge = payload.get("nudge", {})
    candidates = [
        parse_iso(nudge.get("last_user_reply_at")),
        parse_iso(payload.get("updated_at")),
        parse_iso(payload.get("created_at")),
    ]
    for c in candidates:
        mins = age_minutes(c)
        if mins is not None:
            return mins
    stat = state_path.stat()
    fallback = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
    return age_minutes(fallback) or 0


def scan(apply: bool, seed: Optional[int]) -> Dict[str, Any]:
    PIPELINES.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = []

    for state_file in sorted(PIPELINES.glob("*.json")):
        payload = json.loads(state_file.read_text(encoding="utf-8"))
        status = payload.get("status", "planned")
        if status not in WAITING:
            continue

        minutes = infer_minutes_since_reply(payload, state_file)
        result = evaluate_state_file(
            state_file=state_file,
            minutes_since_reply=minutes,
            seed=seed,
            apply=apply,
        )
        result["minutes_since_reply"] = minutes
        result["status"] = status
        results.append(result)

    eligible = [r for r in results if r.get("should_nudge")]
    eligible.sort(key=lambda x: x.get("minutes_since_reply", 0), reverse=True)

    return {
        "checked": len(results),
        "eligible": len(eligible),
        "top": eligible[0] if eligible else None,
        "results": results,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="오 분 관찰자 스캔 러너")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--seed", type=int)
    args = p.parse_args()

    print(json.dumps(scan(apply=args.apply, seed=args.seed), ensure_ascii=False))


if __name__ == "__main__":
    main()
