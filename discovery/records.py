"""Write a DISC-XXXX research record: report.md (for people) + result.json (for machines)."""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

RECORDS_DIR = Path(__file__).resolve().parent.parent / "records"


def git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True,
            cwd=Path(__file__).resolve().parent,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True,
            cwd=Path(__file__).resolve().parent,
        ).stdout.strip()
        return out + ("-dirty" if dirty else "")
    except Exception:  # noqa: BLE001
        return None


def existing_ids(records_dir: Path = RECORDS_DIR) -> set[str]:
    if not records_dir.exists():
        return set()
    return {p.name for p in records_dir.iterdir() if p.is_dir() and p.name.startswith("DISC-")}


def environment() -> dict:
    return {"python": sys.version.split()[0], "platform": platform.platform()}


def write_record(run_id: str, result: dict, report_md: str, records_dir: Path = RECORDS_DIR) -> Path:
    d = records_dir / run_id
    if d.exists():
        raise FileExistsError(f"{d} exists; records are never overwritten")
    d.mkdir(parents=True)
    (d / "result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    (d / "report.md").write_text(report_md, encoding="utf-8")
    return d
