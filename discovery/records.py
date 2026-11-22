"""Write a DISC-XXXX research record: report.md (for people) + result.json (for machines).

Every record carries ``provenance()``: git commit, which source files were
changed or untracked at run time, Python and package versions, the Lean
toolchain and Mathlib revision, and SHA-256 of any data snapshot used.
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS_DIR = ROOT / "records"
# Paths whose changes affect results. Untracked files here make the run "dirty".
CODE_PATHS = ("discovery", "research", "lean", "config", "requirements.txt")
PACKAGES = ("numpy", "scipy", "sympy", "pytest")


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True, cwd=ROOT).stdout


def dirty_files() -> list[str] | None:
    """Modified or untracked files under CODE_PATHS (records/ and data/ are outputs, not code)."""
    try:
        out = _git("status", "--porcelain", "--untracked-files=all", "--", *CODE_PATHS)
    except Exception:  # noqa: BLE001
        return None
    files = []
    for line in out.splitlines():
        path = line[3:].strip()
        if "__pycache__" in path or path.endswith(".pyc") or "/.lake/" in path or path.startswith("lean/.lake"):
            continue
        files.append(path)
    return files


def git_commit() -> str | None:
    try:
        out = _git("rev-parse", "HEAD").strip()
    except Exception:  # noqa: BLE001
        return None
    return out + ("-dirty" if dirty_files() else "")


def existing_ids(records_dir: Path = RECORDS_DIR) -> set[str]:
    if not records_dir.exists():
        return set()
    return {p.name for p in records_dir.iterdir() if p.is_dir() and p.name.startswith("DISC-")}


def environment() -> dict:
    return {"python": sys.version.split()[0], "platform": platform.platform()}


def _lean_versions() -> dict:
    out: dict = {}
    tc = ROOT / "lean" / "lean-toolchain"
    if tc.exists():
        out["toolchain"] = tc.read_text(encoding="utf-8").strip()
    man = ROOT / "lean" / "lake-manifest.json"
    if man.exists():
        for p in json.loads(man.read_text(encoding="utf-8")).get("packages", []):
            if p.get("name") == "mathlib":
                out["mathlib_rev"] = p.get("rev")
    return out


def _data_snapshots() -> dict:
    out = {}
    for m in (ROOT / "data").glob("*/manifest.json"):
        try:
            files = json.loads(m.read_text(encoding="utf-8")).get("files", {})
            out[m.parent.name] = {k: v.get("sha256") for k, v in files.items()}
        except ValueError:
            out[m.parent.name] = "unreadable manifest"
    return out


def provenance(params: dict | None = None) -> dict:
    pkgs = {}
    for name in PACKAGES:
        try:
            pkgs[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            pass
    return {
        "git_commit": git_commit(),
        "dirty_files": dirty_files(),
        "env": environment(),
        "packages": pkgs,
        "lean": _lean_versions(),
        "data_snapshots": _data_snapshots(),
        "params": params or {},
    }


def write_record(run_id: str, result: dict, report_md: str, records_dir: Path = RECORDS_DIR,
                 max_mb: float | None = None) -> Path:
    from discovery.limits import Budget
    limit = (max_mb if max_mb is not None else Budget.default().max_record_mb) * 1024 * 1024
    body = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    size = len(body.encode("utf-8")) + len(report_md.encode("utf-8"))
    if size > limit:
        raise ValueError(f"record is {size} bytes, over max_record_mb; store raw data elsewhere and hash it")
    d = records_dir / run_id
    if d.exists():
        raise FileExistsError(f"{d} exists; records are never overwritten")
    d.mkdir(parents=True)
    (d / "result.json").write_text(body, encoding="utf-8")
    (d / "report.md").write_text(report_md, encoding="utf-8")
    return d
