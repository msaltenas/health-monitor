import json
import logging
import os
import sys
from pathlib import Path

import psutil


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "health-monitor.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def collect_metrics():
    """Collect CPU, memory, and disk utilization metrics."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(os.path.abspath(os.sep)).percent,
    }


def evaluate_health(metrics):
    """Classify machine health based on resource utilization."""
    thresholds = ("cpu_percent", "memory_percent", "disk_percent")
    critical = any(metrics[key] >= 90 for key in thresholds)
    return "CRITICAL" if critical else "HEALTHY"


def main():
    try:
        metrics = collect_metrics()
        status = evaluate_health(metrics)
        result = {"status": status, "metrics": metrics}
        print(json.dumps(result, indent=2))
        logging.info("Health check completed: %s", result)
        return 1 if status == "CRITICAL" else 0
    except Exception as exc:
        logging.exception("Health check failed")
        print(json.dumps({"status": "ERROR", "error": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
