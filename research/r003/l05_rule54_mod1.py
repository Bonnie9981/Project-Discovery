"""DISC-0012: rule 54, single seed, ring width w ≡ 1 (mod 4).

Checks for every w = 9, 13, 17, ... up to W:
  * method 1: bit simulation `research/r002/impl_b.py` + Brent -> (transient, period)
  * method 2: own list simulation (no repo import), first repeat via dict
  * both equal (w - 3, 4)
  * folded form, d(i) = min(i, w - i), m = w // 2 (even):
    lemma 1 (cone): for t <= m - 2, cell i is alive iff d(i) <= t and E(t, d(i))
    lemma 2 (phase wall): for m - 2 <= t <= w + 8, cell i equals G(w, t, d(i)) where
      G = E(t, d)                          if d + t < w   (in front of the wall)
      G = N(t, d) xor defect(t, d)         if d + t >= w  (behind the wall)
      N(t, d) = E(t + 1, d + 3)            (the phase-shifted ether)
      defect  = (d == 0 and t % 4 == 2) or (d == m and t % 4 == m % 4)

Run: python research/r003/l05_rule54_mod1.py [W]   (default 400)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from research.r002 import impl_b  # noqa: E402


def ether(t: int, i: int) -> bool:
    if t % 2 == 0:
        return i % 4 == t % 4
    return i % 4 != (t + 1) % 4


def wall(w: int, t: int, d: int) -> bool:
    m = w // 2
    if d + t < w:
        return ether(t, d)
    defect = (d == 0 and t % 4 == 2) or (d == m and t % 4 == m % 4)
    return ether(t + 1, d + 3) != defect


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
    widths = [w for w in range(9, w_max + 1) if w % 4 == 1]
    for w in widths:
        T, m = w - 3, w // 2
        d = [min(i, w - i) for i in range(w)]
        a = impl_b.orbit(54, w, 1, 1 << 22)
        mu, lam, hist = list_orbit(w)
        if not (tuple(a) == (mu, lam) == (T, 4)):
            bad.append((w, "orbit", a, (mu, lam)))
            continue
        for t in range(0, m - 1):
            want = [int(d[i] <= t and ether(t, d[i])) for i in range(w)]
            if hist[t] != want:
                bad.append((w, "cone", t))
        cells = hist[m - 2]
        for t in range(m - 2, w + 9):
            want = [int(wall(w, t, d[i])) for i in range(w)]
            if cells != want:
                bad.append((w, "wall", t))
            cells = list_step(cells)
    if bad:
        print("FAIL", bad[:10])
        return 1
    print(f"OK: w ≡ 1 (mod 4), 9 <= w <= {w_max} ({len(widths)} widths): "
          "(T, P) = (w - 3, 4), folded cone and phase-wall lemmas hold")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 400))
