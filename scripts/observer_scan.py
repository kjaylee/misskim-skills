#!/usr/bin/env python3
# DEPRECATED: Python implementation is preserved for compatibility.
# Use scripts/observer_scan.ts for active execution.
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from equal_rank_nudge_bot import evaluate_state_file

ROOT = Path(__file__).resolve().parents[1]
PIPELINES = ROOT / ".state" / "pipelines"
WAITING = {"planned", "proposal_pending", "waiting_reply"}
EXCLUDED_TOKENS = {"demo", "test", "sample", "데모", "테스트", "샘플"}


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


def parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off", ""}:
            return False
    return default


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def tokenize(value: Any) -> List[str]:
    if value is None:
        return []
    text = str(value).lower()
    return [token for token in re.split(r"[^0-9a-z가-힣]+", text) if token]


def is_demo_test_sample(payload: Dict[str, Any], state_path: Path) -> bool:
    candidates = [
        payload.get("job_id"),
        state_path.stem,
        payload.get("spec_path"),
        payload.get("spawn_path"),
        payload.get("spawn_ready_path"),
        payload.get("artifacts"),
    ]
    for candidate in candidates:
        tokens = tokenize(candidate)
        if any(token in EXCLUDED_TOKENS for token in tokens):
            return True
    return False


def build_skip_result(
    payload: Dict[str, Any],
    state_file: Path,
    status: str,
    minutes_since_reply: int,
    priority: int,
    track: bool,
    reason: str,
) -> Dict[str, Any]:
    return {
        "job_id": payload.get("job_id"),
        "state_file": str(state_file),
        "should_nudge": False,
        "reason": reason,
        "message": None,
        "minutes_since_reply": minutes_since_reply,
        "status": status,
        "priority": priority,
        "observer_track": track,
    }


def scan(apply: bool, seed: Optional[int]) -> Dict[str, Any]:
    PIPELINES.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = []

    for state_file in sorted(PIPELINES.glob("*.json")):
        payload = json.loads(state_file.read_text(encoding="utf-8"))
        status = payload.get("status", "planned")
        if status not in WAITING:
            continue

        observer = payload.get("observer", {})
        track = parse_bool(observer.get("track"), default=False)
        priority = parse_int(observer.get("priority"), default=0)
        minutes = infer_minutes_since_reply(payload, state_file)

        if is_demo_test_sample(payload, state_file):
            results.append(
                build_skip_result(
                    payload=payload,
                    state_file=state_file,
                    status=status,
                    minutes_since_reply=minutes,
                    priority=priority,
                    track=track,
                    reason="데모/테스트/샘플 제외",
                )
            )
            continue

        if not track:
            results.append(
                build_skip_result(
                    payload=payload,
                    state_file=state_file,
                    status=status,
                    minutes_since_reply=minutes,
                    priority=priority,
                    track=track,
                    reason="observer.track 꺼짐",
                )
            )
            continue

        result = evaluate_state_file(
            state_file=state_file,
            minutes_since_reply=minutes,
            seed=seed,
            apply=apply,
        )
        result["minutes_since_reply"] = minutes
        result["status"] = status
        result["priority"] = priority
        result["observer_track"] = track
        results.append(result)

    eligible = [r for r in results if r.get("should_nudge")]
    eligible.sort(
        key=lambda x: (
            -parse_int(x.get("priority"), default=0),
            -parse_int(x.get("minutes_since_reply"), default=0),
            str(x.get("job_id") or ""),
        )
    )

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
