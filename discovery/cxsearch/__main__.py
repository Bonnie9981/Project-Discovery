"""CLI: python -m discovery.cxsearch {list,catalog,scan} ..."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from discovery.cxsearch import catalog, conjectures

DEFAULT_CATALOG = catalog.DATA / "psp2_1e10.txt.gz"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m discovery.cxsearch")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    c = sub.add_parser("catalog", help="build (C) or check a psp2 catalog")
    c.add_argument("--build", type=float, help="build psp2 below this bound with psp2.c")
    c.add_argument("--path", type=Path, default=DEFAULT_CATALOG)
    s = sub.add_parser("scan")
    s.add_argument("keys", nargs="*")
    s.add_argument("--path", type=Path, default=DEFAULT_CATALOG)
    s.add_argument("--limit", type=float, default=1e10)
    s.add_argument("--nmax", type=int, default=300, help="range for domain 'n'")
    s.add_argument("--keep", type=int, default=5)
    a = ap.parse_args(argv)

    if a.cmd == "list":
        for k, cj in conjectures.REGISTRY.items():
            print(f"{k:10} {cj.domain:10} {cj.statement}")
        return 0
    if a.cmd == "catalog":
        if a.build:
            catalog.build_c(int(a.build), a.path)
        psp = catalog.load(a.path)
        print(json.dumps(catalog.check(psp, _limit(a.path))))
        return 0
    psp = catalog.load(a.path)
    limit = int(a.limit)
    psp = [n for n in psp if n < limit]
    carm = catalog.carmichael(psp)
    for k in a.keys or list(conjectures.REGISTRY):
        dom = conjectures.REGISTRY[k].domain
        members = {"psp2": psp, "carmichael": carm, "n": range(1, a.nmax + 1)}[dom]
        lim = a.nmax if dom == "n" else limit
        print(json.dumps(conjectures.scan(k, members, lim, keep=a.keep)))
    return 0


def _limit(path: Path) -> int:
    """Bound encoded in the file name, e.g. psp2_1e10.txt.gz -> 10**10."""
    tag = path.name.split("_")[1].split(".")[0]
    return int(float(tag))


if __name__ == "__main__":
    raise SystemExit(main())
