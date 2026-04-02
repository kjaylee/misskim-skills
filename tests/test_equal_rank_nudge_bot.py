import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "equal_rank_nudge_bot.py"


def run_cmd(*args: str):
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class EqualRankNudgeBotTests(unittest.TestCase):
    def test_nudges_after_five_minutes(self):
        result = run_cmd(
            "--proposal-pending",
            "--minutes-since-reply", "6",
            "--seed", "1",
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["should_nudge"])
        self.assertIsNotNone(payload["message"])

    def test_no_nudge_before_five_minutes(self):
        result = run_cmd(
            "--proposal-pending",
            "--minutes-since-reply", "4",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "오 분 미만")

    def test_no_nudge_during_cooldown(self):
        result = run_cmd(
            "--proposal-pending",
            "--minutes-since-reply", "9",
            "--last-nudge-minutes-ago", "10",
            "--cooldown-minutes", "30",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "쿨다운 중")

    def test_no_nudge_on_destructive_risk(self):
        result = run_cmd(
            "--proposal-pending",
            "--minutes-since-reply", "12",
            "--risk", "destructive",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "파괴적 삭제 위험")


if __name__ == "__main__":
    unittest.main()
