import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return "unknown"


def log_run(results_dir: str | Path, name: str, config: dict, metrics: dict, notes: str = "") -> Path:
    """Append one row to <results_dir>/runs.csv linking a run's config, metrics and Git commit.

    runs.csv is small and meant to be committed, so the team has a shared run log.
    """
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / "runs.csv"
    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "name": name,
        "git_commit": _git_commit(),
        "config": json.dumps(config, sort_keys=True),
        "metrics": json.dumps(metrics, sort_keys=True),
        "notes": notes,
    }
    new_file = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        if new_file:
            writer.writeheader()
        writer.writerow(row)
    return path
