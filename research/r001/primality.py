"""Two independently written primality tests, used to cross-check each other."""
from __future__ import annotations


def is_prime_trial(n: int) -> bool:
    """Implementation A: plain trial division."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_prime_mr(n: int) -> bool:
    """Implementation B: Miller-Rabin with the first 13 prime bases (2..41).

    Deterministic for n < 3317044064679887385961981 (~3.3e24; Sorenson & Webster 2015).
    With only the first 12 bases the bound is 318665857834031151167461, which is itself
    a strong pseudoprime to bases 2..37 (found by the DISC-0002 critic). R-001 values stay < 1e11.
    """
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True
