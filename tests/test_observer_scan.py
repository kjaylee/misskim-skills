import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_SCRIPT = ROOT / "scripts" / "generate_harness.py"
SCAN_SCRIPT = ROOT / "scripts" / "observer_scan.py"


def run_harness(*args: str):
    return subprocess.run(
        ["python3", str(HARNESS_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def run_scan(*args: str):
    return subprocess.run(
        ["python3", str(SCAN_SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class ObserverScanTests(unittest.TestCase):
    def make_job(
        self,
        job_id: str,
        *,
        track: bool,
        priority: int,
        created_at: str,
    ) -> Path:
        harness = run_harness(job_id, "--preset", "implementation")
        payload = json.loads(harness.stdout)
        self.addCleanup(self.cleanup_job, job_id, payload)

        state_file = ROOT / payload["state"]
        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["created_at"] = created_at
        state.setdefault("observer", {})
        state["observer"]["track"] = track
        state["observer"]["priority"] = priority
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return state_file

    def cleanup_job(self, job_id: str, payload: dict) -> None:
        state_path = ROOT / payload["state"]
        if state_path.exists():
            state_path.unlink()
        spec_dir = ROOT / "specs" / job_id
        if spec_dir.exists():
            shutil.rmtree(spec_dir)

    def find_result(self, payload: dict, job_id: str) -> dict:
        for item in payload["results"]:
            if item.get("job_id") == job_id:
                return item
        self.fail(f"결과에서 job_id를 찾지 못함: {job_id}")

    def test_scan_ignores_demo_test_sample_jobs_by_default(self):
        self.make_job(
            "observer-scan-demo",
            track=True,
            priority=1000,
            created_at="2026-04-01T00:00:00+00:00",
        )

        payload = json.loads(run_scan("--seed", "1").stdout)
        demo_result = self.find_result(payload, "observer-scan-demo")

        self.assertFalse(demo_result["should_nudge"])
        self.assertEqual(demo_result["reason"], "데모/테스트/샘플 제외")
        eligible_job_ids = {item["job_id"] for item in payload["results"] if item.get("should_nudge")}
        self.assertNotIn("observer-scan-demo", eligible_job_ids)

    def test_scan_requires_observer_track_true(self):
        self.make_job(
            "observer-real-untracked",
            track=False,
            priority=900,
            created_at="2026-04-01T00:00:00+00:00",
        )

        payload = json.loads(run_scan("--seed", "1").stdout)
        result = self.find_result(payload, "observer-real-untracked")

        self.assertFalse(result["should_nudge"])
        self.assertEqual(result["reason"], "observer.track 꺼짐")
        self.assertFalse(result["observer_track"])

    def test_scan_prioritizes_priority_before_age(self):
        self.make_job(
            "observer-real-older",
            track=True,
            priority=900,
            created_at="2026-04-01T00:00:00+00:00",
        )
        self.make_job(
            "observer-real-priority",
            track=True,
            priority=1000,
            created_at="2026-04-02T03:50:00+00:00",
        )

        payload = json.loads(run_scan("--seed", "1").stdout)

        self.assertGreaterEqual(payload["eligible"], 2)
        self.assertIsNotNone(payload["top"])
        self.assertEqual(payload["top"]["job_id"], "observer-real-priority")
        self.assertEqual(payload["top"]["priority"], 1000)
        self.assertGreaterEqual(payload["top"]["minutes_since_reply"], 5)


if __name__ == "__main__":
    unittest.main()
