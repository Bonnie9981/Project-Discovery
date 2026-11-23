"""Catalog of base-2 Fermat pseudoprimes (psp2) and Carmichael numbers.

Built by psp2.c (sieve + Montgomery 2^(n-1) mod n, exact for n < 2^63) or,
for small bounds, by pure Python. Every loaded catalog is checked against
the published counts below, and every member is re-checked with Python big
integers, so a bug in the C code cannot silently drop or add terms.
"""
from __future__ import annotations

import gzip
import subprocess
from pathlib import Path

from discovery.cxsearch import numth

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cx"
C_SRC = Path(__file__).with_name("psp2.c")

# Number of base-2 pseudoprimes below 10^k (OEIS A055550) and Carmichael
# numbers below 10^k (OEIS A055553).
PSP2_COUNT = {3: 3, 4: 22, 5: 78, 6: 245, 7: 750, 8: 2057, 9: 5597, 10: 14884}
CARM_COUNT = {3: 1, 4: 7, 5: 16, 6: 43, 7: 105, 8: 255, 9: 646, 10: 1547}


def python_psp2(limit: int) -> list[int]:
    """Slow reference implementation (independent of psp2.c)."""
    return [n for n in range(3, limit, 2) if pow(2, n - 1, n) == 1 and not numth.is_prime(n)]


def build_c(limit: int, out: Path, workers: int = 4) -> Path:
    exe = out.with_suffix(".bin")
    subprocess.run(["gcc", "-O3", "-o", str(exe), str(C_SRC)], check=True)
    step = -(-limit // workers)
    procs, parts = [], []
    for i in range(workers):
        lo, hi = i * step + 1, min((i + 1) * step, limit)
        part = out.with_name(f"{out.name}.part{i}")
        parts.append(part)
        procs.append(subprocess.Popen([str(exe), str(lo), str(hi)], stdout=part.open("w")))
    for p in procs:
        if p.wait():
            raise RuntimeError("psp2.c failed")
    with gzip.open(out, "wt") as f:
        for part in parts:
            f.write(part.read_text())
            part.unlink()
    exe.unlink()
    return out


def load(path: Path) -> list[int]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        return [int(l) for l in f if l.strip()]


def check(psp: list[int], limit: int) -> dict:
    """Recheck every member with Python ints and compare counts with OEIS."""
    assert psp == sorted(set(psp)), "catalog not strictly increasing"
    bad = [n for n in psp if not numth.is_psp(n, 2)]
    if bad:
        raise AssertionError(f"not psp2: {bad[:5]}")
    counts = {k: sum(1 for n in psp if n < 10 ** k) for k in PSP2_COUNT if 10 ** k <= limit}
    for k, c in counts.items():
        if c != PSP2_COUNT[k]:
            raise AssertionError(f"psp2 below 10^{k}: got {c}, OEIS A055550 says {PSP2_COUNT[k]}")
    carm = [n for n in psp if numth.is_carmichael(n)]
    for k in counts:
        c = sum(1 for n in carm if n < 10 ** k)
        if c != CARM_COUNT[k]:
            raise AssertionError(f"Carmichael below 10^{k}: got {c}, OEIS A055553 says {CARM_COUNT[k]}")
    return {"limit": limit, "psp2": len(psp), "carmichael": len(carm), "counts_checked": sorted(counts)}


def carmichael(psp: list[int]) -> list[int]:
    """Every Carmichael number is a psp2, so this list is complete up to the bound."""
    return [n for n in psp if numth.is_carmichael(n)]
