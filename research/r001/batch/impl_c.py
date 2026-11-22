"""Implementation C — the Critic's check, linear (Euler) sieve of smallest prime factors.

Method: one linear sieve computes spf[x] for x <= M (each composite is struck
exactly once by its least prime, unlike the Eratosthenes sieve in impl_b).
Each function value is then computed on demand by peeling primes off with
spf and applying the prime-power rule. Used to push candidates from 10^4 to
10^5..10^6. Does not import impl_a, impl_b or any sibling module.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations

import math
from array import array


class C:
    def __init__(self, m: int):
        self.m = m
        spf = array("i", [0]) * (m + 1)
        primes: list[int] = []
        for i in range(2, m + 1):
            if spf[i] == 0:
                spf[i] = i
                primes.append(i)
            si = spf[i]
            for p in primes:
                if p > si or p * i > m:
                    break
                spf[p * i] = p
        self.spf = spf

    def fac(self, x: int) -> list[tuple[int, int]]:
        out = []
        spf = self.spf
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            out.append((p, e))
        return out

    # functions ---------------------------------------------------------
    def sigma(self, x):
        r = 1
        for p, e in self.fac(x):
            r *= (p ** (e + 1) - 1) // (p - 1)
        return r

    def sigma_odd(self, x):
        r = 1
        for p, e in self.fac(x):
            if p != 2:
                r *= (p ** (e + 1) - 1) // (p - 1)
        return r

    def usigma(self, x):
        r = 1
        for p, e in self.fac(x):
            r *= p ** e + 1
        return r

    def phi(self, x):
        r = 1
        for p, e in self.fac(x):
            r *= (p - 1) * p ** (e - 1)
        return r

    def psi(self, x):
        r = 1
        for p, e in self.fac(x):
            r *= (p + 1) * p ** (e - 1)
        return r

    def rad(self, x):
        r = 1
        for p, _ in self.fac(x):
            r *= p
        return r

    def core(self, x):
        r = 1
        for p, e in self.fac(x):
            if e & 1:
                r *= p
        return r

    def d(self, x):
        r = 1
        for _, e in self.fac(x):
            r *= e + 1
        return r

    def J2(self, x):
        r = 1
        for p, e in self.fac(x):
            r *= (p * p - 1) * p ** (2 * e - 2)
        return r

    def is_squarefree(self, x):
        return all(e == 1 for _, e in self.fac(x))

    def is_square(self, x):
        return math.isqrt(x) ** 2 == x
