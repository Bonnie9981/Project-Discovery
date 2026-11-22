"""DISC-0011: rule 54, single seed, ring width w ≡ 2 or 3 (mod 4).

Checks for every w = 6, 7, 10, 11, ..., up to W:
  * method 1: bit simulation `research/r002/impl_b.py` + Brent -> (transient, period)
  * method 2: own list simulation (no repo import), first repeat via dict
  * both equal (T, 4), T = (w - 6)/2 (w ≡ 2) or (w - 7)/2 (w ≡ 3)
  * folded form: with d(i) = min(i, w - i) and m = w // 2 (= T + 3),
    lemma 1 (cone):  for t <= T, cell i is alive iff d(i) <= t and E(t, d(i))
    lemma 2 (defect ether): for k = 0..8, at time T + k cell i is alive iff
      E(T + k, d(i)) and not (d(i) == m and k % 4 == 1)
    (the one-cell "defect" sits at the centre d = m, i.e. the cell(s) farthest from the seed)

Run: python research/r003/l04_rule54_mod23.py [W]   (default 400)
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


def transient(w: int) -> int:
    return (w - 6) // 2 if w % 4 == 2 else (w - 7) // 2


def main(w_max: int) -> int:
    bad = []
    widths = [w for w in range(6, w_max + 1) if w % 4 in (2, 3)]
    for w in widths:
        T, m = transient(w), w // 2
        assert m == T + 3 and T % 2 == 0
        d = [min(i, w - i) for i in range(w)]
        a = impl_b.orbit(54, w, 1, 1 << 22)
        mu, lam, hist = list_orbit(w)
        if not (tuple(a) == (mu, lam) == (T, 4)):
            bad.append((w, "orbit", a, (mu, lam)))
            continue
        for t in range(0, T + 1):
            want = [int(d[i] <= t and ether(t, d[i])) for i in range(w)]
            if hist[t] != want:
                bad.append((w, "cone", t))
        cells = hist[T]
        for k in range(0, 9):
            want = [int(ether(T + k, d[i]) and not (d[i] == m and k % 4 == 1)) for i in range(w)]
            if cells != want:
                bad.append((w, "defect", k))
            cells = list_step(cells)
    if bad:
        print("FAIL", bad[:10])
        return 1
    print(f"OK: w ≡ 2, 3 (mod 4), 6 <= w <= {w_max} ({len(widths)} widths): "
          "(T, P) = (T(w), 4), folded cone and defect-ether lemmas hold")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 400))
