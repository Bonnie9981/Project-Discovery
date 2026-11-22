"""Implementation B — per-length closed-form test and prime factorisation (DISC-0003).

Method:
- Representation counts: for each fixed length k, the AP a, a+D, ..., a+(k-1)D
  has sum k*a + D*k*(k-1)/2, so a representation of n with k terms exists iff
  n - D*k*(k-1)/2 is a positive multiple of k (and then it is unique). Loop over
  k while the smallest possible sum k + D*k*(k-1)/2 is <= n.
- Odd-divisor count: remove all factors 2, factor the odd part by trial
  division, return the product of (e_p + 1).
- Divisor count: product of (e_p + 1) over the full factorisation.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations


def rep_count(n: int, D: int = 1, k_ok=None) -> int:
    c, k = 0, 1
    while k + D * k * (k - 1) // 2 <= n:
        rest = n - D * k * (k - 1) // 2
        if rest % k == 0 and rest // k >= 1 and (k_ok is None or k_ok(k)):
            c += 1
        k += 1
    return c


def factorise(n: int) -> dict[int, int]:
    f: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def odd_divisor_count(n: int) -> int:
    out = 1
    for p, e in factorise(n).items():
        if p != 2:
            out *= e + 1
    return out


def divisor_count(n: int) -> int:
    out = 1
    for e in factorise(n).values():
        out *= e + 1
    return out


def is_power_of_two(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def domain(n_max: int) -> list[int]:
    out, n = [], 1
    while n <= n_max:
        out.append(n)
        n += 1
    return out
