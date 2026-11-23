"""Exact integer helpers for the counterexample searcher.

Everything is Python int (arbitrary precision), so there is no overflow.
is_prime is deterministic below 3.3e24 (Miller-Rabin with the first 13 prime
bases, Sorenson-Webster 2015); above that it is a strong probable-prime test
and callers must say so.
"""
from __future__ import annotations

import math
import random

_SMALL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
DETERMINISTIC_BOUND = 3317044064679887385961981


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _SMALL:
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


def _rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    rng = random.Random(n)
    while True:
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g = r = q = 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g


def factor(n: int) -> dict[int, int]:
    """Prime factorization {p: e}. Trial division to 1000, then Pollard rho."""
    f: dict[int, int] = {}
    for p in range(2, 1000):
        if p * p > n:
            break
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m):
            f[m] = f.get(m, 0) + 1
            continue
        d = _rho(m)
        stack += [d, m // d]
    return dict(sorted(f.items()))


def mult_order(a: int, n: int) -> int:
    """Least k > 0 with a^k = 1 (mod n); requires gcd(a, n) = 1."""
    if math.gcd(a, n) != 1:
        raise ValueError("not coprime")
    if n == 1:
        return 1
    lam = carmichael_lambda(n)
    k = lam
    for p in factor(lam):
        while k % p == 0 and pow(a, k // p, n) == 1:
            k //= p
    return k


def carmichael_lambda(n: int) -> int:
    lam = 1
    for p, e in factor(n).items():
        if p == 2:
            v = 1 if e == 1 else 2 if e == 2 else 2 ** (e - 2)
        else:
            v = (p - 1) * p ** (e - 1)
        lam = lam * v // math.gcd(lam, v)
    return lam


def is_psp(n: int, base: int = 2) -> bool:
    """Fermat pseudoprime: composite n > 1 with base^(n-1) = 1 (mod n)."""
    return n > 1 and pow(base, n - 1, n) == 1 and not is_prime(n)


def is_carmichael(n: int) -> bool:
    """Korselt: n composite, squarefree, p - 1 | n - 1 for every prime p | n."""
    if n < 3 or n % 2 == 0 or is_prime(n):
        return False
    f = factor(n)
    return len(f) >= 2 and all(e == 1 and (n - 1) % (p - 1) == 0 for p, e in f.items())
