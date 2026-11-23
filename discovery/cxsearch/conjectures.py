"""Registry of conjectures the searcher can test, one predicate each.

A predicate takes one member of the domain (a psp2, a Carmichael number, or
an index n) and returns None when the conjecture holds for it, or a short
dict describing why it fails. A failure found here is only a candidate: it
must be re-checked by an independent implementation and against the OEIS
entry text (someone may already have reported it) before it is called a
counterexample.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from discovery.cxsearch import numth


@dataclass(frozen=True)
class Conjecture:
    key: str             # "A215944" or "A215944#2"
    domain: str          # "psp2" | "carmichael"
    statement: str       # English, close to the entry's wording
    reading: str         # how we formalised it (ambiguities resolved here)
    test: Callable[[int], Optional[dict]]


def _three_primes(n):
    f = numth.factor(n)
    if len(f) != 3 or any(e != 1 for e in f.values()):
        return None
    return sorted(f)


def in_a215944(n):
    """Membership in A215944: psp2 with three prime factors (counted with
    multiplicity) divisible by a smaller psp2. Checked against the b-file."""
    f = numth.factor(n)
    if sum(f.values()) != 3:
        return False
    a, b, c = [p for p, e in f.items() for _ in range(e)]
    return any(d < n and numth.is_psp(d) for d in {a * b, a * c, b * c})


def a215944(n):
    ps = _three_primes(n)
    if ps is None:
        return None
    p, q, r = ps
    smaller = [d for d in (p * q, p * r, q * r) if numth.is_psp(d)]
    if not smaller:
        return None
    if (q - 1) % (p - 1) == 0 and (r - 1) % (p - 1) == 0:
        return None  # n = p*((m+1)p-m)*((k+1)p-k) with m, k >= 1
    if n % 5461 == 0 and (n // 5461 + 13) % 42 == 0:
        return None  # the stated exception 5461*(42k-13)
    return {"n": n, "factors": ps, "psp_divisors": smaller}


def a321790(k):
    """Semiprime psp2 k: the least base a > 2 with a^(k-1) != 1 (mod k) is < lpf(k)."""
    f = numth.factor(k)
    if sum(f.values()) != 2:
        return None
    p = min(f)
    a = 3
    while a < p and pow(a, k - 1, k) == 1:
        a += 1
    return None if a < p else {"n": k, "factors": sorted(f), "least_base": a}


def a058128(n):
    """Even n: a(n) = (n^n - n)/(n-1)^2 satisfies n^a = n (mod a) (prime or weak psp)."""
    if n % 2 or n < 2:
        return None
    a = (n ** n - n) // (n - 1) ** 2
    return None if pow(n, a, a) == n % a else {"n": n}


def a218483_mod40(n):
    return {"n": n} if n % 40 == 15 else None


def a218010(n):
    return {"n": n} if (5 * n - 1) % 24 == 0 else None


REGISTRY: dict[str, Conjecture] = {c.key: c for c in [
    Conjecture(
        "A215944", "psp2",
        "The only psp2 divisible by a smaller psp2 that can't be written as "
        "p*((m+1)p-m)*((n+1)p-n) are multiples of 5461 of the form 5461*(42k-13).",
        "Domain = the entry's own domain: psp2 n = p*q*r with three distinct primes "
        "p < q < r and one of pq, pr, qr a psp2. The form with natural m, n means "
        "(p-1) | (q-1) and (p-1) | (r-1) with p the least prime factor.",
        a215944),
    Conjecture(
        "A218483#1", "psp2",
        "There are no pseudoprimes to base 2 of the form 40n+15.",
        "psp2 n with n = 15 (mod 40).",
        a218483_mod40),
    Conjecture(
        "A321790", "psp2",
        "If the psp2 k is semiprime, then the least base a > 2 with a^(k-1) != 1 (mod k) is < lpf(k).",
        "Semiprime = two prime factors with multiplicity (p^2 included).",
        a321790),
    Conjecture(
        "A058128", "n",
        "For even n, a(n) = (n^n-n)/(n-1)^2 is prime or a weak Fermat pseudoprime to base n.",
        "Tested as n^a(n) = n (mod a(n)), which every prime satisfies too.",
        a058128),
    Conjecture(
        "A218010", "carmichael",
        "No Carmichael number m has (5m-1)/24 an integer.",
        "Carmichael m with 5m = 1 (mod 24). Already refuted in the entry "
        "(3380740301, Greathouse 2014); kept as a pipeline self-test.",
        a218010),
]}


def scan(key: str, members: list[int], limit: int, keep: int = 20) -> dict:
    c = REGISTRY[key]
    fails = []
    total = 0
    for n in members:
        total += 1
        r = c.test(n)
        if r is not None:
            fails.append(r)
    return {"key": key, "domain": c.domain, "limit": limit, "checked": total,
            "failures": len(fails), "first": fails[:keep]}
