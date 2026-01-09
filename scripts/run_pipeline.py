import subprocess
import sys
from logger import get_logger
from alert_email import send_failure_email

logger = get_logger("pipeline")

PIPELINE_STEPS = [
    "ingest_worldbank.py",
    "ingest_fred.py",
    "transform_macro.py",
    "incremental_load.py",
    "data_quality.py",
    "export_analytics_tables.py"
]


def run_step(script_name):
    logger.info(f"Starting step: {script_name}")

    try:
        result = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.error(f"Step failed: {script_name}")
            logger.error(result.stderr)

            # EMAIL ALERT
            send_failure_email(script_name, result.stderr)

            raise RuntimeError(f"{script_name} failed")

        logger.info(f"Completed step: {script_name}")

    except Exception as e:
        logger.error(f"Fatal error in step: {script_name}")
        logger.error(str(e))

        # EMAIL ALERT (safety net)
        send_failure_email(script_name, str(e))

        raise


if __name__ == "__main__":
    logger.info("Pipeline execution started")

    try:
        for step in PIPELINE_STEPS:
            run_step(step)

        logger.info("Pipeline executed successfully")

    except Exception:
        logger.error("Pipeline execution failed")
        sys.exit(1)
