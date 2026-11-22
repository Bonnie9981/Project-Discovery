"""Literature search evidence (layer 3: manual / browser searches).

Every search done by hand or through a browser is appended to
records/DISC-XXXX/search_evidence.jsonl. Entries are never edited; a correction
is a new entry. A screenshot or search page is not a substitute for the source:
for any candidate match, record the paper's abstract/DOI/full-text link too.

    python -m discovery.evidence add DISC-0003 --platform OEIS \
        --query "1,2,2,2,3" --scope "OEIS full-text search" \
        --url "https://oeis.org/search?q=1,2,2,2,3" --found "A001227" \
        --limits "only OEIS; no journals"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from discovery.records import RECORDS_DIR

REQUIRED = ("search_id", "research_id", "searched_at_utc", "platform", "query", "scope",
            "results", "evidence", "coverage_limits", "searched_by")


def _path(research_id: str, records_dir: Path) -> Path:
    return records_dir / research_id / "search_evidence.jsonl"


def entries(research_id: str, records_dir: Path = RECORDS_DIR) -> list[dict]:
    p = _path(research_id, records_dir)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate(e: dict) -> list[str]:
    errs = [f"missing {k}" for k in REQUIRED if e.get(k) in (None, "", [])]
    if not isinstance(e.get("evidence"), list):
        errs.append("evidence must be a list of URLs/file paths")
    return errs


def add(research_id: str, platform: str, query: str, scope: str, results: list[str],
        evidence: list[str], coverage_limits: str, searched_by: str,
        records_dir: Path = RECORDS_DIR) -> dict:
    d = records_dir / research_id
    if not d.is_dir():
        raise FileNotFoundError(f"{d} does not exist")
    n = len(entries(research_id, records_dir)) + 1
    e = {
        "search_id": f"{research_id}-S{n:03d}",
        "research_id": research_id,
        "searched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "platform": platform,
        "query": query,
        "scope": scope,
        "results": results or ["(no results)"],
        "evidence": evidence,
        "coverage_limits": coverage_limits,
        "searched_by": searched_by,
    }
    errs = validate(e)
    if errs:
        raise ValueError("; ".join(errs))
    with _path(research_id, records_dir).open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="discovery.evidence")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("research_id")
    a.add_argument("--platform", required=True)
    a.add_argument("--query", required=True)
    a.add_argument("--scope", required=True)
    a.add_argument("--found", action="append", default=[], help="candidate match (repeatable)")
    a.add_argument("--url", action="append", default=[], help="evidence URL or file (repeatable)")
    a.add_argument("--limits", required=True, help="what this search could not cover")
    a.add_argument("--by", default="claude-in-chrome")
    sub.add_parser("check", help="validate all search_evidence.jsonl files")
    args = ap.parse_args(argv)
    if args.cmd == "add":
        print(json.dumps(add(args.research_id, args.platform, args.query, args.scope, args.found,
                             args.url, args.limits, args.by), ensure_ascii=False, indent=2))
        return 0
    bad = 0
    for p in sorted(RECORDS_DIR.glob("DISC-*/search_evidence.jsonl")):
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for err in validate(json.loads(line)):
                print(f"FAIL {p.parent.name} line {i}: {err}")
                bad += 1
    print(f"{bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
