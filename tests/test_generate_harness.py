import json
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
    def test_custom_harness_generation(self):
        job_id = "test-custom-harness"
        result = run_cmd(
            job_id,
            "--goal", "커스텀 작업",
            "--scope", "출력 파일 확인",
            "--tests", "파일 생성 확인",
            "--done", "세 파일 생성",
            "--artifacts", f"specs/{job_id}/plan.md, specs/{job_id}/spawn.md, .state/pipelines/{job_id}.json",
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["job_id"], job_id)
        self.assertTrue((ROOT / payload["plan"]).exists())
        self.assertTrue((ROOT / payload["spawn"]).exists())
        self.assertTrue((ROOT / payload["state"]).exists())

    def test_preset_generation(self):
        job_id = "test-research-harness"
        result = run_cmd(job_id, "--preset", "research")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["preset"], "research")

        plan_text = (ROOT / payload["plan"]).read_text(encoding="utf-8")
        state = json.loads((ROOT / payload["state"]).read_text(encoding="utf-8"))

        self.assertIn("리서치 작업 수행", plan_text)
        self.assertEqual(state["preset"], "research")
        self.assertIn(f"specs/{job_id}/results.md", state["artifacts"])


if __name__ == "__main__":
    unittest.main()
