"""Run the full DealMakers pipeline in one repeatable command.

Each stage is a real subprocess of the same scripts documented in the
README (profile -> simulate -> prepare -> engineer features -> load
database), so this orchestrates the existing pipeline rather than
reimplementing it. Every run is logged to both the console and a log file
with timestamps and durations, and the pipeline stops at the first stage
that fails instead of continuing on top of bad data.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

LOG_PATH = Path("data/processed/pipeline.log")
logger = logging.getLogger("run_pipeline")


def configure_logging(log_path: Path = LOG_PATH) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def build_stages(skip_simulate: bool, check_only: bool) -> list[tuple[str, list[str]]]:
    stages = [("Profiling raw data", ["src/profile_data.py"])]
    if not skip_simulate:
        stages.append(("Simulating behavioural data", ["src/simulate_data.py"]))
    prepare_args = ["src/data_preparation.py"]
    if check_only:
        prepare_args.append("--check-only")
    stages.append(("Preparing and validating data", prepare_args))
    stages.append(("Engineering opportunity features", ["src/feature_engineering.py"]))
    stages.append(("Loading the analytical database", ["src/load_database.py"]))
    return stages


def run_stage(name: str, args: list[str]) -> bool:
    logger.info("START: %s (%s)", name, " ".join(args))
    started = time.monotonic()
    result = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    duration = time.monotonic() - started

    for line in result.stdout.splitlines():
        logger.info("  %s", line)
    for line in result.stderr.splitlines():
        logger.warning("  %s", line)

    if result.returncode != 0:
        logger.error("FAILED: %s after %.1fs (exit code %d)", name, duration, result.returncode)
        return False

    logger.info("DONE: %s in %.1fs", name, duration)
    return True


def run_pipeline(skip_simulate: bool = False, check_only: bool = False) -> bool:
    stages = build_stages(skip_simulate, check_only)
    pipeline_started = time.monotonic()
    for name, args in stages:
        if not run_stage(name, args):
            logger.error("Pipeline stopped after %.1fs due to a failed stage.", time.monotonic() - pipeline_started)
            return False
    logger.info("Pipeline completed successfully in %.1fs.", time.monotonic() - pipeline_started)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full DealMakers data pipeline end to end.")
    parser.add_argument("--skip-simulate", action="store_true", help="Reuse existing behavioural CSVs instead of regenerating them.")
    parser.add_argument("--check-only", action="store_true", help="Validate data without writing cleaned CSV files.")
    parser.add_argument("--log-file", type=Path, default=LOG_PATH, help="Path to write the pipeline log (default: data/processed/pipeline.log).")
    args = parser.parse_args()

    configure_logging(args.log_file)
    success = run_pipeline(skip_simulate=args.skip_simulate, check_only=args.check_only)
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
