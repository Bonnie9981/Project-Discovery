"""Implementation B — sieves over the whole range (DISC-0004 batch).

Method: nothing is factorised one number at a time.
- d, sigma, sigma2, sigma_odd, d_odd, d_square, usigma, d_unitary: divisor-sum
  sieves (for each divisor m, add its contribution to every multiple of m;
  unitary divisors are recognised by gcd(m, n/m) = 1).
- phi, psi, J2, rad, core, omega, Omega, sopf, sopfr, gpf, lpf, mu,
  liouville, carmichael: an Eratosthenes prime sieve, then each prime p
  updates its multiples (phi via n*(1-1/p), Omega via repeated division counts).
  Carmichael lambda is computed as the multiplicative order bound by
  brute-force search of the exponent of (Z/nZ)* for small n and by lcm of
  prime-power parts built from the sieve otherwise.
- r2 from Jacobi: r2 = 4 (d_1 - d_3); r4 from Jacobi: r4 = 8 * sum of divisors
  not divisible by 4; r3 from r3 = sum_z r2(n - z^2) using the sieved r2.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations

import math


def _primes_upto(n: int) -> list[int]:
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def _divisor_sum(n_max, f, unitary=False):
    t = [0] * (n_max + 1)
    for m in range(1, n_max + 1):
        v = f(m)
        if v == 0:
            continue
        for k in range(m, n_max + 1, m):
            if not unitary or math.gcd(m, k // m) == 1:
                t[k] += v
    return t


def _prime_power_parts(n_max, primes):
    """For every n, list of (p, e) built by the sieve (each prime visits its multiples)."""
    parts = [[] for _ in range(n_max + 1)]
    for p in primes:
        pk = p
        e = 1
        while pk <= n_max:
            for k in range(pk, n_max + 1, pk):
                if parts[k] and parts[k][-1][0] == p:
                    parts[k][-1] = (p, e)
                else:
                    parts[k].append((p, e))
            pk *= p
            e += 1
    return parts


def table(name: str, n_max: int) -> list[int]:
    N = n_max
    if name == "one":
        return [None] + [1] * N
    if name == "id":
        return [None] + list(range(1, N + 1))
    if name == "d":
        return [None] + _divisor_sum(N, lambda m: 1)[1:]
    if name == "d_odd":
        return [None] + _divisor_sum(N, lambda m: m % 2)[1:]
    if name == "sigma":
        return [None] + _divisor_sum(N, lambda m: m)[1:]
    if name == "sigma2":
        return [None] + _divisor_sum(N, lambda m: m * m)[1:]
    if name == "sigma_odd":
        return [None] + _divisor_sum(N, lambda m: m if m % 2 else 0)[1:]
    if name == "d_square":
        return [None] + _divisor_sum(N, lambda m: 1 if math.isqrt(m) ** 2 == m else 0)[1:]
    if name == "usigma":
        return [None] + _divisor_sum(N, lambda m: m, unitary=True)[1:]
    if name == "d_unitary":
        return [None] + _divisor_sum(N, lambda m: 1, unitary=True)[1:]
    if name in ("r2", "r3", "r4"):
        d1 = _divisor_sum(N, lambda m: 1 if m % 4 == 1 else (-1 if m % 4 == 3 else 0))
        r2 = [1] + [4 * x for x in d1[1:]]
        if name == "r2":
            return [None] + r2[1:]
        if name == "r4":
            s = _divisor_sum(N, lambda m: 0 if m % 4 == 0 else m)
            return [None] + [8 * x for x in s[1:]]
        r3 = [0] * (N + 1)
        for n in range(1, N + 1):
            z = 0
            tot = 0
            while z * z <= n:
                tot += r2[n - z * z] * (1 if z == 0 else 2)
                z += 1
            r3[n] = tot
        return [None] + r3[1:]

    primes = _primes_upto(N)
    parts = _prime_power_parts(N, primes)
    out = [None]
    for n in range(1, N + 1):
        pe = parts[n]
        if name == "phi":
            v = n
            for p, _ in pe:
                v = v // p * (p - 1)
        elif name == "psi":
            v = n
            for p, _ in pe:
                v = v // p * (p + 1)
        elif name == "J2":
            v = n * n
            for p, _ in pe:
                v = v // (p * p) * (p * p - 1)
        elif name == "rad":
            v = 1
            for p, _ in pe:
                v *= p
        elif name == "core":
            v = 1
            for p, e in pe:
                if e & 1:
                    v *= p
        elif name == "omega":
            v = len(pe)
        elif name == "Omega":
            v = sum(e for _, e in pe)
        elif name == "mu":
            v = 0 if any(e > 1 for _, e in pe) else (1 if len(pe) % 2 == 0 else -1)
        elif name == "liouville":
            v = 1 if sum(e for _, e in pe) % 2 == 0 else -1
        elif name == "sopf":
            v = sum(p for p, _ in pe)
        elif name == "sopfr":
            v = sum(p * e for p, e in pe)
        elif name == "gpf":
            v = pe[-1][0] if pe else 1
        elif name == "lpf":
            v = pe[0][0] if pe else 1
        elif name == "carmichael":
            v = _exponent_of_units(n) if n <= 200 else _carm_from_parts(pe)
        else:
            raise KeyError(name)
        out.append(v)
    return out


def _exponent_of_units(n: int) -> int:
    """Brute force: least m >= 1 with a^m = 1 mod n for all units a."""
    if n <= 2:
        return 1
    units = [a for a in range(1, n) if math.gcd(a, n) == 1]
    m = 1
    while True:
        if all(pow(a, m, n) == 1 for a in units):
            return m
        m += 1


def _carm_from_parts(pe) -> int:
    r = 1
    for p, e in pe:
        if p == 2:
            x = 1 if e == 1 else (2 if e == 2 else 1 << (e - 2))
        else:
            x = (p - 1) * p ** (e - 1)
        r = r * x // math.gcd(r, x)
    return r
