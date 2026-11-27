"""Screen generated sequences against the offline OEIS (`python -m discovery.newseq.screen FILE`).

FILE is the JSON written by a generator: a list of rows with "family",
"property", "n" and one or more term lists. A term list is a lead when it is
not trivial (enough distinct values, not all small) and `lookup.find` finds
no entry containing it.
"""
from __future__ import annotations

import json
import sys

from discovery.newseq.lookup import find

STATS = ("count", "min", "nmin")


def interesting(t: list[int]) -> bool:
    nz = [x for x in t if x]
    return len(t) >= 7 and len(set(t)) >= 5 and max(map(abs, t)) >= 10 and len(nz) >= 6


def main(path):
    rows = json.load(open(path))
    leads = []
    for r in rows:
        for st in STATS:
            t = r.get(st)
            if not t or not interesting(t):
                continue
            # drop leading zeros/ones so a different offset still matches
            k = 0
            while k < len(t) and abs(t[k]) <= 1:
                k += 1
            hits = find(t[k:], minlen=6, maxdrop=3)
            if not hits:
                leads.append({"family": r["family"], "property": r["property"], "stat": st,
                              "n0": r["n"][0], "terms": t})
                print(r["family"], r["property"], st, r["n"][0], t)
    json.dump(leads, open(path.replace(".json", "_leads.json"), "w"))
    print(f"{len(leads)} leads", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
