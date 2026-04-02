import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_harness.py"


def run_cmd(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class GenerateHarnessTests(unittest.TestCase):
    def cleanup_job(self, job_id: str, payload: dict) -> None:
        state_path = ROOT / payload["state"]
        if state_path.exists():
            state_path.unlink()
        spec_dir = ROOT / "specs" / job_id
        if spec_dir.exists():
            shutil.rmtree(spec_dir)

    def test_custom_harness_generation(self):
        job_id = "test-custom-harness"
        result = run_cmd(
            job_id,
            "--goal", "커스텀 작업",
            "--scope", "출력 파일 확인",
            "--tests", "파일 생성 확인",
            "--done", "세 파일 생성",
            "--artifacts", f"specs/{job_id}/plan.md, specs/{job_id}/spawn.md, specs/{job_id}/spawn-ready.md, .state/pipelines/{job_id}.json",
        )
        payload = json.loads(result.stdout)
        self.addCleanup(self.cleanup_job, job_id, payload)
        state = json.loads((ROOT / payload["state"]).read_text(encoding="utf-8"))

        self.assertEqual(payload["job_id"], job_id)
        self.assertTrue((ROOT / payload["plan"]).exists())
        self.assertTrue((ROOT / payload["spawn"]).exists())
        self.assertTrue((ROOT / payload["spawn_ready"]).exists())
        self.assertTrue((ROOT / payload["state"]).exists())
        self.assertFalse(state["observer"]["track"])
        self.assertEqual(state["observer"]["priority"], 0)

    def test_preset_generation(self):
        job_id = "test-research-harness"
        result = run_cmd(job_id, "--preset", "research")
        payload = json.loads(result.stdout)
        self.addCleanup(self.cleanup_job, job_id, payload)
        self.assertEqual(payload["preset"], "research")

        plan_text = (ROOT / payload["plan"]).read_text(encoding="utf-8")
        spawn_ready_text = (ROOT / payload["spawn_ready"]).read_text(encoding="utf-8")
        state = json.loads((ROOT / payload["state"]).read_text(encoding="utf-8"))

        self.assertIn("리서치 작업 수행", plan_text)
        self.assertEqual(state["preset"], "research")
        self.assertIn(f"specs/{job_id}/results.md", state["artifacts"])
        self.assertIn("레드팀", spawn_ready_text)
        self.assertIn("실행 원칙", spawn_ready_text)
        self.assertEqual(state["status"], "proposal_pending")
        self.assertEqual(state["observer"]["model"], "minimax-portal/MiniMax-M2.7")
        self.assertEqual(state["observer"]["interval_minutes"], 5)
        self.assertTrue(state["observer"]["track"])
        self.assertEqual(state["observer"]["priority"], 0)
        self.assertTrue(state["nudge"]["proposal_pending"])
        self.assertEqual(state["nudge"]["minutes_threshold"], 5)

    def test_implementation_preset_enables_observer_tracking(self):
        job_id = "test-implementation-harness"
        result = run_cmd(job_id, "--preset", "implementation")
        payload = json.loads(result.stdout)
        self.addCleanup(self.cleanup_job, job_id, payload)
        state = json.loads((ROOT / payload["state"]).read_text(encoding="utf-8"))

        self.assertEqual(payload["preset"], "implementation")
        self.assertTrue(state["observer"]["track"])
        self.assertEqual(state["observer"]["priority"], 0)


if __name__ == "__main__":
    unittest.main()
