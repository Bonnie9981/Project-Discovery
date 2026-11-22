"""Implementation A — direct enumeration (DISC-0003).

Method:
- Representation counts: build a table for every n <= n_max by literally
  listing every run a, a+D, a+2D, ... (a >= 1) term by term, adding each
  running sum to the table, and stopping a run once its sum passes n_max.
  No algebra about k(2a+(k-1)D) is used.
- Odd-divisor count: test every d <= sqrt(n) for d | n and count the members
  of each divisor pair {d, n/d} that are odd.
- Divisor count: same pair enumeration, counting all members.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations

import math


def rep_table(n_max: int, D: int = 1, k_ok=None) -> list[int]:
    """t[n] = #{(a,k): a>=1, k>=1, k_ok(k), a + (a+D) + ... + (a+(k-1)D) = n} for 0 <= n <= n_max."""
    t = [0] * (n_max + 1)
    for a in range(1, n_max + 1):
        s, k, term = 0, 0, a
        while True:
            s += term
            k += 1
            if s > n_max:
                break
            if k_ok is None or k_ok(k):
                t[s] += 1
            term += D
            if D == 0 and term > n_max:  # D = 0 is not used, guard anyway
                break
    return t


def divisor_pairs(n: int):
    r = math.isqrt(n)
    for d in range(1, r + 1):
        if n % d == 0:
            yield d
            if d != n // d:
                yield n // d


def odd_divisor_count(n: int) -> int:
    return sum(1 for d in divisor_pairs(n) if d % 2 == 1)


def divisor_count(n: int) -> int:
    return sum(1 for _ in divisor_pairs(n))


def is_power_of_two(n: int) -> bool:
    while n % 2 == 0:
        n //= 2
    return n == 1


def domain(n_max: int) -> list[int]:
    return list(range(1, n_max + 1))
