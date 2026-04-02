import json
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
    def test_scan_finds_waiting_job(self):
        job_id = "observer-scan-demo"
        harness = run_harness(job_id, "--preset", "implementation")
        state_file = ROOT / json.loads(harness.stdout)["state"]

        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["created_at"] = "2026-04-02T00:00:00+00:00"
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result = run_scan("--apply", "--seed", "1")
        payload = json.loads(result.stdout)
        self.assertGreaterEqual(payload["checked"], 1)
        self.assertGreaterEqual(payload["eligible"], 1)
        self.assertIsNotNone(payload["top"])


if __name__ == "__main__":
    unittest.main()
