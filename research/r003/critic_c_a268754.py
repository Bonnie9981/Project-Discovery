"""DISC-0013 critic: third, self-contained check of the A268754 odd-index FORMULA.

Method (no simulation loop, no cycle detection, no repo imports):
  * Closed form.  The null-boundary rule-90 wire of n cells with a seed in cell 1 is the
    mirror-symmetric ring Z/N, N = 2n+2, seeded at {+1, -1}.  On the infinite line rule 90
    from one cell gives C(t, (t+d)/2) mod 2 at offset d; summing over the images
    d = j - s + mN (s = +-1) gives cell j at time t directly.  C(t,k) mod 2 by Lucas
    (k & ~t == 0).  So any state x_t is computed in O(n * t / N) without iterating.
  * Least eventual period, verified rather than searched.  A candidate p is taken from the
    entry's DATA (widths <= 54) or from the FORMULA (2 a(n)).  With T = width (the
    transient of a linear map on n bits is <= n), p is an eventual period iff
    x_{T+p} == x_T, and it is the least one iff additionally x_{T+p/q} != x_T for every
    prime q | p (the least period divides every period).
  * Death: 0 is fixed and the transient is <= n, so the wire ever dies iff x_n == 0.

Checks (printed):
  1. for every width w <= 54: DATA[w] is the least eventual period (closed form);
  2. for 1 <= n <= N_MAX: 2*a(n) (non-exception) / 1 (exception) is the least eventual
     period of width 2n+1, a(n) itself verified the same way;
  3. for 1 <= n <= D_MAX: x_n == 0 iff n+1 is a power of two.
  4. the spread lemma at a few random large times (t up to 10^6), closed form only.

Run: python research/r003/critic_c_a268754.py [N_MAX] [D_MAX]   (defaults 40, 1000)
"""
from __future__ import annotations

import random
import sys

DATA = [1, 2, 1, 6, 4, 14, 1, 14, 12, 62, 8, 126, 28, 30, 1, 30, 28, 1022, 24, 126, 124,
        4094, 16, 2046, 252, 1022, 56, 32766, 60, 62, 1, 62, 60, 8190, 56, 174762, 2044,
        8190, 48, 2046, 252, 254, 248, 8190, 8188, 16777214, 32, 4194302, 4092, 510, 504,
        134217726, 2044, 2097150]  # A268754(1..54), as transcribed in DISC-0009/0013


def binom_odd(t: int, k: int) -> bool:
    return 0 <= k <= t and (k & ~t) == 0


def state(n: int, t: int) -> tuple[int, ...]:
    """Cells 1..n of the wire at time t, closed form via images on Z/(2n+2)."""
    big = 2 * n + 2
    out = []
    for j in range(1, n + 1):
        v = 0
        for s in (1, -1):
            d0 = j - s
            # all d = d0 + m*big with |d| <= t and d = t (mod 2)
            m_lo = -((t + d0) // big) - 1
            m_hi = (t - d0) // big + 1
            for m in range(m_lo, m_hi + 1):
                d = d0 + m * big
                if abs(d) <= t and (t + d) % 2 == 0 and binom_odd(t, (t + d) // 2):
                    v ^= 1
        out.append(v)
    return tuple(out)


def primes_of(p: int) -> list[int]:
    out, q = [], 2
    while q * q <= p:
        if p % q == 0:
            out.append(q)
            while p % q == 0:
                p //= q
        q += 1
    if p > 1:
        out.append(p)
    return out


def is_least_period(w: int, p: int) -> bool:
    base = state(w, w)
    if state(w, w + p) != base:
        return False
    return all(state(w, w + p // q) != base for q in primes_of(p))


def main() -> int:
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    bad: list = []
    for w, p in enumerate(DATA, 1):
        if not is_least_period(w, p):
            bad.append(("data", w, p))
    print(f"[1] DATA 1..{len(DATA)} least eventual periods: {'OK' if not bad else bad}")
    nb = len(bad)
    biggest = 0
    for n in range(1, nmax + 1):
        a = DATA[n - 1]
        pow2 = (n + 1) & n == 0
        want = 1 if pow2 else 2 * a
        if pow2 and a != 1:
            bad.append(("exc a(n)", n, a))
        if not is_least_period(2 * n + 1, want):
            bad.append(("formula", n, want))
        biggest = max(biggest, want)
    print(f"[2] a(2n+1) = 2a(n) / 1, n <= {nmax}, largest {biggest}: "
          f"{'OK' if len(bad) == nb else bad[nb:]}")
    nb = len(bad)
    for n in range(1, dmax + 1):
        dead = not any(state(n, n))
        if dead != ((n + 1) & n == 0):
            bad.append(("dies", n))
    print(f"[3] dies iff n+1 = 2^k, n <= {dmax}: {'OK' if len(bad) == nb else bad[nb:]}")
    nb = len(bad)
    rng = random.Random(13)
    for _ in range(40):
        n = rng.randint(1, 60)
        t = rng.randint(0, 10 ** 6)
        y, z = state(n, t), state(2 * n + 1, 2 * t + 1)
        spread = tuple(y[i // 2] if i % 2 == 1 else 0 for i in range(2 * n + 1))
        if z != spread:
            bad.append(("spread", n, t))
    print(f"[4] spread lemma, 40 random (n <= 60, t <= 1e6): "
          f"{'OK' if len(bad) == nb else bad[nb:]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
