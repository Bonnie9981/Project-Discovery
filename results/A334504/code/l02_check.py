"""R3-L02 (DISC-0009): numerical checks for the even-width half of OEIS A334504.

python results/A334504/code/l02_check.py [N_MAX]      (default N_MAX = 40)

Conjecture (A334504 FORMULA, Zabolotskii 2024, "It seems that"):
    a(2n+2) = A268754(n),  n >= 1,
where A334504(w) = eventual period of rule 26 on a ring of w cells from one live cell,
and A268754(n) = eventual period of rule 90 with null boundary on n cells from one
live cell at the left end (A268754 PROG / MATHEMATICA: tridiagonal 0/1 matrix, seed e_1).

Checks, for 1 <= n <= N_MAX (w = 2n + 2, m = n + 1):

  Way 1 (impl_b): (transient, period) of rule 26 on the ring of width w (Brent).
  Way 2 (own code, no import from the repo): null-boundary rule 90 on n cells from the
         left-end seed, first repeat by dictionary -> (transient, period).
  Claim:   period_26(w) == period_90null(n)  and  transient_26(w) == transient_90null(n) + 1.
  OEIS:    period_90null(n) == A268754(n) (54 terms copied from the entry, 2026-11-22).
  Lemma (structure, n <= 20, all t <= transient + 2*period): for t >= 1 the ring state is
         cells 0 and m dead, cells 1..m-1 = y_{t-1}, cells m+1..w-1 = mirror image,
         where y_0 = left-end seed and y_{k+1} = null-boundary rule 90 of y_k.
Standard library only (plus research/r002/impl_b.py for Way 1).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from research.r002 import impl_b  # noqa: E402

# OEIS A268754, offset 1 (read 2026-11-22 via the browser, entry DATA field).
A268754 = [1, 2, 1, 6, 4, 14, 1, 14, 12, 62, 8, 126, 28, 30, 1, 30, 28, 1022, 24, 126,
           124, 4094, 16, 2046, 252, 1022, 56, 32766, 60, 62, 1, 62, 60, 8190, 56,
           174762, 2044, 8190, 48, 2046, 252, 254, 248, 8190, 8188, 16777214, 32,
           4194302, 4092, 510, 504, 134217726, 2044, 2097150]


def null90(cells: tuple[int, ...]) -> tuple[int, ...]:
    n = len(cells)
    return tuple((cells[i - 1] if i > 0 else 0) ^ (cells[i + 1] if i + 1 < n else 0)
                 for i in range(n))


def way2(n: int) -> tuple[int, int]:
    y = tuple([1] + [0] * (n - 1))
    seen: dict[tuple[int, ...], int] = {}
    t = 0
    while y not in seen:
        seen[y] = t
        y = null90(y)
        t += 1
    return seen[y], t - seen[y]


def structure(n: int, steps: int) -> None:
    w, m = 2 * n + 2, n + 1
    mask = (1 << w) - 1
    x = impl_b._step(1, 26, w, mask)          # x_1
    y = tuple([1] + [0] * (n - 1))            # y_0
    for t in range(1, steps + 1):
        cells = [(x >> i) & 1 for i in range(w)]
        assert cells[0] == 0 and cells[m] == 0, (n, t)
        assert tuple(cells[1:m]) == y, (n, t)
        assert all(cells[w - i] == cells[i] for i in range(1, m)), (n, t)
        x = impl_b._step(x, 26, w, mask)
        y = null90(y)


def main(n_max: int = 40) -> None:
    rows = []
    for n in range(1, n_max + 1):
        w = 2 * n + 2
        t26, p26 = impl_b.orbit(26, w, 1, 10 ** 7)
        t90, p90 = way2(n)
        assert (t26, p26) == (t90 + 1, p90), (n, (t26, p26), (t90, p90))
        if n <= len(A268754):
            assert p90 == A268754[n - 1], (n, p90, A268754[n - 1])
        if n <= 20:
            structure(n, t26 + 2 * p26)
        rows.append((n, w, t26, p26))
    print(f"OK: 1 <= n <= {n_max}: period_26(2n+2) = period_90null(n) = A268754(n), "
          f"transient_26 = transient_90null + 1; structure lemma n <= {min(n_max, 20)}")
    print("first rows (n, w, T26, P26):", rows[:8])


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
