import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_SCRIPT = ROOT / "scripts" / "generate_harness.py"
REACT_SCRIPT = ROOT / "scripts" / "observer_react.py"


def run_harness(*args: str):
    return subprocess.run(
        ["python3", str(HARNESS_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def run_react(*args: str):
    return subprocess.run(
        ["python3", str(REACT_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class ObserverReactTests(unittest.TestCase):
    def test_react_promotes_waiting_job_to_auto_execute(self):
        job_id = "observer-react-demo"
        harness = run_harness(job_id, "--preset", "implementation")
        state_file = ROOT / json.loads(harness.stdout)["state"]

        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["created_at"] = "2026-04-02T00:00:00+00:00"
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result = run_react(
            "--state-file", str(state_file),
            "--minutes-since-reply", "10",
            "--apply",
            "--seed", "1",
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["should_act"])
        self.assertEqual(payload["job_id"], job_id)

        updated = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertEqual(updated["status"], "auto_execute")
        self.assertFalse(updated["nudge"]["proposal_pending"])
        self.assertIsNotNone(updated["observer"]["last_auto_execute_at"])


if __name__ == "__main__":
    unittest.main()
