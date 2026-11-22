"""DISC-0013: numerical checks for the odd-index FORMULA of OEIS A268754.

python research/r003/l06_a268754_odd.py [N_MAX] [DIES_MAX]   (defaults 40, 2000)

A268754(n) = least eventual period of null-boundary rule 90 on n cells, seed = one live
cell at the left end (entry PROG/MATHEMATICA). FORMULA of the entry (no proof given):
    a(2n+1) = 2 a(n),  except when n = 2^k - 1, where a(n) = a(2n+1) = 1.

  Way 1: wire as a bitmask, update ((y<<1)^(y>>1)) & mask (entry's Python), Brent.
  Way 2: own code, independent encoding: the symmetric ring of N = 2n+2 cells
         (Z/N, step c_i <- c_{i-1} xor c_{i+1}) started from cells {1, N-1}; first
         repeat found with a dictionary.  (Null-boundary wire = mirror-symmetric ring.)
  Checks for 1 <= n <= N_MAX: Way1 == Way2 for widths n and 2n+1; the FORMULA;
         Way1 == the 54 DATA terms copied from the entry (read 2026-11-22).
  Spread lemma (n <= 30, t <= 2*(transient+period)): the (2n+1)-wire at time 2t+1 equals
         the n-wire at time t with bit i moved to bit 2i+1.
  Dies (n <= DIES_MAX): the wire reaches 0 within n steps iff n+1 is a power of two
         (Way 1 only; the Lean proof covers all n).
Standard library only.
"""
from __future__ import annotations

import sys

OEIS = [1, 2, 1, 6, 4, 14, 1, 14, 12, 62, 8, 126, 28, 30, 1, 30, 28, 1022, 24, 126, 124,
        4094, 16, 2046, 252, 1022, 56, 32766, 60, 62, 1, 62, 60, 8190, 56, 174762, 2044,
        8190, 48, 2046, 252, 254, 248, 8190, 8188, 16777214, 32, 4194302, 4092, 510, 504,
        134217726, 2044, 2097150]


def step1(n: int, y: int) -> int:
    return ((y << 1) ^ (y >> 1)) & ((1 << n) - 1)


def way1(n: int) -> tuple[int, int]:
    """(transient, period) by Brent's algorithm."""
    power = lam = 1
    tort, hare = 1, step1(n, 1)
    while tort != hare:
        if power == lam:
            tort, power, lam = hare, power * 2, 0
        hare = step1(n, hare)
        lam += 1
    mu, tort, hare = 0, 1, 1
    for _ in range(lam):
        hare = step1(n, hare)
    while tort != hare:
        tort, hare, mu = step1(n, tort), step1(n, hare), mu + 1
    return mu, lam


def way2(n: int) -> tuple[int, int]:
    big = 2 * n + 2
    cells = [0] * big
    cells[1] = cells[big - 1] = 1
    seen: dict[tuple[int, ...], int] = {}
    t = 0
    while True:
        key = tuple(cells)
        if key in seen:
            return seen[key], t - seen[key]
        seen[key] = t
        cells = [cells[i - 1] ^ cells[(i + 1) % big] for i in range(big)]
        t += 1


def spread(y: int) -> int:
    out, i = 0, 0
    while y >> i:
        if (y >> i) & 1:
            out |= 1 << (2 * i + 1)
        i += 1
    return out


def main() -> int:
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    bad = []
    for n in range(1, nmax + 1):
        a, b = way1(n), way1(2 * n + 1)
        if a != way2(n) or b != way2(2 * n + 1):
            bad.append(("way1!=way2", n))
        pow2 = (n + 1) & n == 0
        want = 1 if pow2 else 2 * a[1]
        if b[1] != want or (pow2 and a[1] != 1):
            bad.append(("formula", n, a, b))
        for w, (_, p) in ((n, a), (2 * n + 1, b)):
            if w <= len(OEIS) and OEIS[w - 1] != p:
                bad.append(("oeis", w, p))
        if n <= 30:
            y, z = 1, step1(2 * n + 1, 1)
            for _ in range(2 * (a[0] + a[1]) + 2):
                if z != spread(y):
                    bad.append(("spread", n))
                    break
                y, z = step1(n, y), step1(2 * n + 1, step1(2 * n + 1, z))
    for n in range(1, dmax + 1):
        y, died = 1, False
        for _ in range(n + 1):
            if y == 0:
                died = True
                break
            y = step1(n, y)
        if died != ((n + 1) & n == 0):
            bad.append(("dies", n))
    if bad:
        print("FAIL", bad[:10])
        return 1
    print(f"OK: 1 <= n <= {nmax}: a(2n+1) = 2a(n) unless n = 2^k-1 (then both 1); "
          f"way1 == way2; matches 54 OEIS terms; spread lemma n <= 30; "
          f"dies iff n+1 = 2^k for n <= {dmax}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
