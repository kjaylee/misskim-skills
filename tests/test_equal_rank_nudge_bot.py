import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUDGE_SCRIPT = ROOT / "scripts" / "equal_rank_nudge_bot.py"
HARNESS_SCRIPT = ROOT / "scripts" / "generate_harness.py"


def run_nudge(*args: str):
    return subprocess.run(
        ["python3", str(NUDGE_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def run_harness(*args: str):
    return subprocess.run(
        ["python3", str(HARNESS_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class EqualRankNudgeBotTests(unittest.TestCase):
    def test_nudges_after_five_minutes(self):
        result = run_nudge(
            "--proposal-pending",
            "--minutes-since-reply", "6",
            "--seed", "1",
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["should_nudge"])
        self.assertIsNotNone(payload["message"])

    def test_no_nudge_before_five_minutes(self):
        result = run_nudge(
            "--proposal-pending",
            "--minutes-since-reply", "4",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "오 분 미만")

    def test_no_nudge_during_cooldown(self):
        result = run_nudge(
            "--proposal-pending",
            "--minutes-since-reply", "9",
            "--last-nudge-minutes-ago", "10",
            "--cooldown-minutes", "30",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "쿨다운 중")

    def test_no_nudge_on_destructive_risk(self):
        result = run_nudge(
            "--proposal-pending",
            "--minutes-since-reply", "12",
            "--risk", "destructive",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "파괴적 삭제 위험")

    def test_state_file_integration(self):
        job_id = "state-linked-nudge"
        harness = run_harness(job_id, "--preset", "implementation")
        state_file = ROOT / json.loads(harness.stdout)["state"]

        result = run_nudge(
            "--state-file", str(state_file),
            "--minutes-since-reply", "7",
            "--seed", "1",
            "--apply",
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["should_nudge"])

        state = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertEqual(state["nudge"]["last_decision"]["reason"], "대기 상태 오 분 초과")
        self.assertIsNotNone(state["nudge"]["last_nudge_message"])
        self.assertEqual(state["nudge"]["last_nudge_minutes_ago"], 0)


if __name__ == "__main__":
    unittest.main()
