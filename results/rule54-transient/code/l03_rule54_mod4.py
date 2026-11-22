"""DISC-0010: rule 54, single seed, ring width w ≡ 0 (mod 4).

Checks for every w = 4, 8, ..., W:
  * method 1: bit simulation `research/r002/impl_b.py` + Brent -> (transient, period)
  * method 2: own list simulation (no repo import), first repeat via dict
  * both equal ((w - 4) / 2, 4)
  * lemma 1 (light cone): for 2t + 4 <= w, cell i is alive iff
    (i <= t or w <= i + t) and E(t, i)
  * lemma 2 (ether): for T <= t <= T + 8, cell i is alive iff E(t, i)

Run: python results/rule54-transient/code/l03_rule54_mod4.py [W]   (default 400)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from research.r002 import impl_b  # noqa: E402


def ether(t: int, i: int) -> bool:
    if t % 2 == 0:
        return i % 4 == t % 4
    return i % 4 != (t + 1) % 4


def list_step(cells: list[int]) -> list[int]:
    w = len(cells)
    return [cells[i] ^ (cells[i - 1] | cells[(i + 1) % w]) for i in range(w)]


def list_orbit(w: int) -> tuple[int, int, list[list[int]]]:
    cells = [1] + [0] * (w - 1)
    seen: dict[tuple[int, ...], int] = {}
    hist: list[list[int]] = []
    t = 0
    while tuple(cells) not in seen:
        seen[tuple(cells)] = t
        hist.append(cells)
        cells = list_step(cells)
        t += 1
    mu = seen[tuple(cells)]
    return mu, t - mu, hist


def main(w_max: int) -> int:
    bad = []
    for w in range(4, w_max + 1, 4):
        T = (w - 4) // 2
        a = impl_b.orbit(54, w, 1, 1 << 22)
        mu, lam, hist = list_orbit(w)
        if not (tuple(a) == (mu, lam) == (T, 4)):
            bad.append((w, "orbit", a, (mu, lam)))
            continue
        for t in range(0, T + 1):
            want = [int((i <= t or w <= i + t) and ether(t, i)) for i in range(w)]
            if hist[t] != want:
                bad.append((w, "cone", t))
        cells = hist[T]
        for t in range(T, T + 9):
            if cells != [int(ether(t, i)) for i in range(w)]:
                bad.append((w, "ether", t))
            cells = list_step(cells)
    n = len(range(4, w_max + 1, 4))
    if bad:
        print("FAIL", bad[:10])
        return 1
    print(f"OK: w = 4, 8, ..., {w_max} ({n} widths): (T, P) = ((w-4)/2, 4), cone and ether lemmas hold")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 400))
