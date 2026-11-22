"""Offline OEIS snapshot (layer 1 of the novelty check).

Files come from the official OEIS downloads (https://oeis.org/stripped.gz and
https://oeis.org/names.gz, CC BY-SA 4.0). They are NOT committed to git
(see .gitignore). Put them in data/oeis/raw/ and run

    python -m discovery.oeis_offline register

which writes data/oeis/manifest.json (size, SHA-256, registration time). Every
search reports the snapshot it used, so a record says exactly what was searched.

A snapshot only shows what OEIS contained on that date. "Not in the snapshot"
is NO_MATCH_IN_SCOPE, never evidence of novelty.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from discovery import novelty

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = ROOT / "data" / "oeis"
FILES = ("stripped.gz", "names.gz")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _open(path: Path):
    return gzip.open(path, "rt", encoding="utf-8", errors="replace") if path.suffix == ".gz" \
        else path.open(encoding="utf-8", errors="replace")


def parse_stripped(path: Path) -> dict[str, list[int]]:
    """Lines look like 'A000045 ,0,1,1,2,3,5,'. Comment lines start with '#'."""
    seqs: dict[str, list[int]] = {}
    with _open(path) as f:
        for line in f:
            if not line.startswith("A"):
                continue
            sid, _, rest = line.partition(" ")
            terms = [int(x) for x in rest.strip().strip(",").split(",") if x.strip().lstrip("-").isdigit()]
            seqs[sid] = terms
    return seqs


def parse_names(path: Path) -> dict[str, str]:
    names: dict[str, str] = {}
    with _open(path) as f:
        for line in f:
            if line.startswith("A"):
                sid, _, name = line.partition(" ")
                names[sid] = name.strip()
    return names


@dataclass
class Snapshot:
    seqs: dict[str, list[int]]
    names: dict[str, str] = field(default_factory=dict)
    sha256: str = ""
    registered_at: str | None = None

    @property
    def label(self) -> str:
        return f"sha256:{self.sha256[:12]}" + (f",{self.registered_at}" if self.registered_at else ",UNREGISTERED")

    def search(self, terms: list[int], max_matches: int = 50) -> list[dict]:
        rows = ((sid, self.names.get(sid, ""), ref) for sid, ref in self.seqs.items())
        return novelty.search_table(terms, rows, "oeis_offline", max_matches)


def load(d: Path = DEFAULT_DIR) -> Snapshot | None:
    raw = d / "raw"
    stripped = raw / "stripped.gz"
    if not stripped.exists():
        stripped = raw / "stripped"
        if not stripped.exists():
            return None
    names_p = next((p for p in (raw / "names.gz", raw / "names") if p.exists()), None)
    manifest = {}
    mp = d / "manifest.json"
    if mp.exists():
        manifest = json.loads(mp.read_text(encoding="utf-8"))
    digest = sha256(stripped)
    reg = manifest.get("files", {}).get(stripped.name, {})
    if reg and reg.get("sha256") != digest:
        raise RuntimeError(f"{stripped.name} does not match manifest.json; re-run register")
    return Snapshot(parse_stripped(stripped), parse_names(names_p) if names_p else {},
                    digest, manifest.get("registered_at") if reg else None)


_cache: dict[str, Snapshot | None] = {}


def load_default() -> Snapshot | None:
    if "default" not in _cache:
        _cache["default"] = load(DEFAULT_DIR)
    return _cache["default"]


def register(d: Path = DEFAULT_DIR, source: str = "https://oeis.org/") -> dict:
    raw = d / "raw"
    files = {}
    for p in sorted(raw.iterdir()) if raw.exists() else []:
        if p.is_file():
            files[p.name] = {"bytes": p.stat().st_size, "sha256": sha256(p),
                             "mtime_utc": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
                             .isoformat(timespec="seconds")}
    if "stripped.gz" not in files and "stripped" not in files:
        raise SystemExit(f"no stripped.gz in {raw}")
    m = {"source": source, "license": "CC BY-SA 4.0 (OEIS Foundation)",
         "registered_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "files": files}
    (d / "manifest.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    return m


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="discovery.oeis_offline")
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register", help="hash data/oeis/raw/* into manifest.json")
    s = sub.add_parser("search", help="search terms, e.g. 1,1,2,3,5,8")
    s.add_argument("terms")
    a = ap.parse_args(argv)
    if a.cmd == "register":
        print(json.dumps(register(a.dir), indent=2))
        return 0
    snap = load(a.dir)
    if snap is None:
        print("no snapshot", file=sys.stderr)
        return 2
    terms = [int(x) for x in a.terms.split(",")]
    print(json.dumps({"snapshot": snap.label, "matches": snap.search(terms)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
