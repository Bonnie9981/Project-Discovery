"""Implementation A — per-number trial-division factorisation (DISC-0004 batch).

Method: every n is factorised on its own by trial division, and each function
is evaluated from that factorisation with its textbook prime-power formula,
or by direct enumeration where the definition is a count:
- r2, r3: count lattice points by enumerating x, y (, z) directly.
- r4: Dirichlet-free count, r4 = sum_{a+b=n} r2(a) r2(b) (convolution of the
  directly counted r2 with itself).
No sieve is used anywhere.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations

import math


def factor(n: int) -> list[tuple[int, int]]:
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


def _prod(xs):
    r = 1
    for x in xs:
        r *= x
    return r


def _sigma_k(f, k):
    return _prod((p ** (k * (e + 1)) - 1) // (p ** k - 1) for p, e in f)


def _carmichael(f):
    parts = []
    for p, e in f:
        if p == 2:
            parts.append(1 if e == 1 else 2 if e == 2 else 2 ** (e - 2))
        else:
            parts.append((p - 1) * p ** (e - 1))
    r = 1
    for x in parts:
        r = r * x // math.gcd(r, x)
    return r


def value(name: str, n: int) -> int:
    f = factor(n)
    if name == "one":
        return 1
    if name == "id":
        return n
    if name == "d":
        return _prod(e + 1 for _, e in f)
    if name == "d_odd":
        return _prod(e + 1 for p, e in f if p != 2)
    if name == "sigma":
        return _sigma_k(f, 1)
    if name == "sigma2":
        return _sigma_k(f, 2)
    if name == "sigma_odd":
        return _sigma_k([(p, e) for p, e in f if p != 2], 1)
    if name == "phi":
        return _prod((p - 1) * p ** (e - 1) for p, e in f)
    if name == "psi":
        return _prod((p + 1) * p ** (e - 1) for p, e in f)
    if name == "J2":
        return _prod((p * p - 1) * p ** (2 * (e - 1)) for p, e in f)
    if name == "omega":
        return len(f)
    if name == "Omega":
        return sum(e for _, e in f)
    if name == "mu":
        return 0 if any(e > 1 for _, e in f) else (-1) ** len(f)
    if name == "liouville":
        return (-1) ** sum(e for _, e in f)
    if name == "rad":
        return _prod(p for p, _ in f)
    if name == "core":
        return _prod(p for p, e in f if e % 2 == 1)
    if name == "carmichael":
        return _carmichael(f)
    if name == "sopf":
        return sum(p for p, _ in f)
    if name == "sopfr":
        return sum(p * e for p, e in f)
    if name == "gpf":
        return max((p for p, _ in f), default=1)
    if name == "lpf":
        return min((p for p, _ in f), default=1)
    if name == "usigma":
        return _prod(p ** e + 1 for p, e in f)
    if name == "d_unitary":
        return 2 ** len(f)
    if name == "d_square":
        return _prod(e // 2 + 1 for _, e in f)
    raise KeyError(name)


LATTICE = ("r2", "r3", "r4")


def lattice_table(name: str, n_max: int) -> list[int]:
    """t[n] for 0 <= n <= n_max, by enumerating integer points."""
    r = math.isqrt(n_max)
    t2 = [0] * (n_max + 1)
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            s = x * x + y * y
            if s <= n_max:
                t2[s] += 1
    if name == "r2":
        return t2
    if name == "r3":
        t3 = [0] * (n_max + 1)
        for z in range(-r, r + 1):
            z2 = z * z
            for s in range(0, n_max - z2 + 1):
                if t2[s]:
                    t3[s + z2] += t2[s]
        return t3
    if name == "r4":
        t4 = [0] * (n_max + 1)
        nz = [(a, v) for a, v in enumerate(t2) if v]
        for a, va in nz:
            for b, vb in nz:
                if a + b > n_max:
                    break
                t4[a + b] += va * vb
        return t4
    raise KeyError(name)


def table(name: str, n_max: int) -> list[int]:
    """[None, f(1), ..., f(n_max)] (index 0 unused for arithmetic functions)."""
    if name in LATTICE:
        t = lattice_table(name, n_max)
        return [None] + t[1:]
    return [None] + [value(name, n) for n in range(1, n_max + 1)]
