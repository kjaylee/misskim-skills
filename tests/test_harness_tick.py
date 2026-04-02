import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_SCRIPT = ROOT / "scripts" / "generate_harness.py"
TICK_SCRIPT = ROOT / "scripts" / "harness_tick.py"


def run_harness(*args: str):
    return subprocess.run(
        ["python3", str(HARNESS_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def run_tick(*args: str):
    return subprocess.run(
        ["python3", str(TICK_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class HarnessTickTests(unittest.TestCase):
    def cleanup_job(self, job_id: str, payload: dict) -> None:
        state_path = ROOT / payload["state"]
        if state_path.exists():
            state_path.unlink()
        spec_dir = ROOT / "specs" / job_id
        if spec_dir.exists():
            shutil.rmtree(spec_dir)

    def test_tick_nudges_waiting_job(self):
        job_id = "test-tick-waiting-job"
        harness = run_harness(job_id, "--preset", "implementation")
        harness_payload = json.loads(harness.stdout)
        self.addCleanup(self.cleanup_job, job_id, harness_payload)
        state_file = ROOT / harness_payload["state"]

        result = run_tick(
            "--state-file", str(state_file),
            "--minutes-since-reply", "8",
            "--seed", "1",
            "--apply",
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["should_nudge"])

    def test_tick_does_not_nudge_active_job(self):
        job_id = "test-tick-active-job"
        harness = run_harness(job_id, "--preset", "implementation")
        harness_payload = json.loads(harness.stdout)
        self.addCleanup(self.cleanup_job, job_id, harness_payload)
        state_file = ROOT / harness_payload["state"]

        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["status"] = "active"
        state["nudge"]["proposal_pending"] = False
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result = run_tick(
            "--state-file", str(state_file),
            "--minutes-since-reply", "8",
            "--seed", "1",
            "--apply",
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["should_nudge"])
        self.assertEqual(payload["reason"], "대기 상태 아님")


if __name__ == "__main__":
    unittest.main()
