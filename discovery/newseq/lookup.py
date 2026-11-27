"""Is a term list already in the offline OEIS? (`discovery.newseq.lookup`)

Loads the %S/%T/%U terms of every entry in data/oeis/oeisdata into one string
and searches for the query as a contiguous run of terms (any offset). Also
tries the query with leading terms dropped, so a different starting index or
a different first term does not hide a match.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from discovery.oeisdb import SRC

LINE = re.compile(r"^%([STU]) (A\d{6}) ?(.*)$")


@lru_cache(maxsize=1)
def corpus(src: Path = SRC) -> tuple[str, list[int], list[str]]:
    parts, starts, anums, pos = [], [], [], 0
    for f in sorted((src / "seq").glob("A*/A*.seq")):
        data = "".join(m.group(3).strip() for raw in f.read_text(encoding="utf-8", errors="replace").splitlines()
                       if (m := LINE.match(raw)))
        s = "," + data.strip(",") + ",\n"
        parts.append(s)
        starts.append(pos)
        anums.append(f.stem)
        pos += len(s)
    return "".join(parts), starts, anums


def find(terms: list[int], minlen: int = 6, maxdrop: int = 3) -> list[str]:
    """A-numbers whose terms contain terms[d:] for some d <= maxdrop (keeping >= minlen terms)."""
    import bisect
    text, starts, anums = corpus()
    hits = set()
    for d in range(maxdrop + 1):
        q = terms[d:]
        if len(q) < minlen:
            break
        pat = "," + ",".join(map(str, q)) + ","
        i = text.find(pat)
        while i != -1:
            hits.add(anums[bisect.bisect_right(starts, i) - 1])
            i = text.find(pat, i + 1)
        if hits:
            break
    return sorted(hits)
