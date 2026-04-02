import json
import shutil
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
    def cleanup_job(self, job_id: str, payload: dict) -> None:
        state_path = ROOT / payload["state"]
        if state_path.exists():
            state_path.unlink()
        spec_dir = ROOT / "specs" / job_id
        if spec_dir.exists():
            shutil.rmtree(spec_dir)

    def test_react_promotes_waiting_job_to_auto_execute(self):
        job_id = "observer-react-direct"
        harness = run_harness(job_id, "--preset", "implementation")
        harness_payload = json.loads(harness.stdout)
        self.addCleanup(self.cleanup_job, job_id, harness_payload)
        state_file = ROOT / harness_payload["state"]

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

    def test_react_scans_legacy_real_work_state(self):
        job_id = "observer-react-legacy"
        harness = run_harness(job_id, "--preset", "implementation")
        harness_payload = json.loads(harness.stdout)
        self.addCleanup(self.cleanup_job, job_id, harness_payload)
        state_file = ROOT / harness_payload["state"]

        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["created_at"] = "2026-04-02T00:00:00+00:00"
        state["observer"]["track"] = False
        state["observer"]["priority"] = 9999
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result = run_react("--apply", "--seed", "1")
        payload = json.loads(result.stdout)

        self.assertTrue(payload["should_act"])
        self.assertEqual(payload["job_id"], job_id)

        updated = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertEqual(updated["status"], "auto_execute")
        self.assertTrue(updated["observer"]["track"])
        self.assertEqual(updated["observer"]["track_migration_reason"], "legacy preset 자동 추적")


if __name__ == "__main__":
    unittest.main()
