import logging
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.run_pipeline import build_stages, configure_logging, run_pipeline


def _completed(returncode=0, stdout="ok", stderr=""):
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


class BuildStagesTests(unittest.TestCase):
    def test_default_stages_include_simulate(self):
        stages = build_stages(skip_simulate=False, check_only=False)
        names = [name for name, _ in stages]
        self.assertIn("Simulating behavioural data", names)
        self.assertEqual(len(stages), 5)

    def test_skip_simulate_omits_that_stage(self):
        stages = build_stages(skip_simulate=True, check_only=False)
        names = [name for name, _ in stages]
        self.assertNotIn("Simulating behavioural data", names)
        self.assertEqual(len(stages), 4)

    def test_check_only_is_passed_to_data_preparation(self):
        stages = build_stages(skip_simulate=False, check_only=True)
        prepare_args = next(args for name, args in stages if "Preparing" in name)
        self.assertIn("--check-only", prepare_args)

    def test_stage_order_is_profile_simulate_prepare_engineer_load(self):
        stages = build_stages(skip_simulate=False, check_only=False)
        scripts = [args[0] for _, args in stages]
        self.assertEqual(scripts, [
            "src/profile_data.py", "src/simulate_data.py", "src/data_preparation.py",
            "src/feature_engineering.py", "src/load_database.py",
        ])


class RunPipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        configure_logging(Path(self.tmp.name) / "pipeline.log")

    def tearDown(self):
        logger = logging.getLogger("run_pipeline")
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        self.tmp.cleanup()

    def test_all_stages_succeed(self):
        with patch("subprocess.run", return_value=_completed(returncode=0)) as mock_run:
            success = run_pipeline(skip_simulate=True, check_only=False)
        self.assertTrue(success)
        self.assertEqual(mock_run.call_count, 4)

    def test_stops_after_first_failure(self):
        results = [_completed(returncode=0), _completed(returncode=1, stderr="boom")]
        with patch("subprocess.run", side_effect=results) as mock_run:
            success = run_pipeline(skip_simulate=True, check_only=False)
        self.assertFalse(success)
        self.assertEqual(mock_run.call_count, 2)

    def test_log_file_records_stage_outcomes(self):
        log_path = Path(self.tmp.name) / "pipeline.log"
        configure_logging(log_path)
        with patch("subprocess.run", return_value=_completed(returncode=0)):
            run_pipeline(skip_simulate=True, check_only=False)
        content = log_path.read_text()
        self.assertIn("Pipeline completed successfully", content)

    def test_failure_is_logged_with_exit_code(self):
        log_path = Path(self.tmp.name) / "pipeline.log"
        configure_logging(log_path)
        with patch("subprocess.run", return_value=_completed(returncode=1, stderr="bad data")):
            run_pipeline(skip_simulate=True, check_only=False)
        content = log_path.read_text()
        self.assertIn("FAILED", content)
        self.assertIn("exit code 1", content)


if __name__ == "__main__":
    unittest.main()
