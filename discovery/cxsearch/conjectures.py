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
    domain: str          # "psp2" | "carmichael" | "n"
    statement: str       # English, close to the entry's wording
    reading: str         # how we formalised it (ambiguities resolved here)
    test: Callable[[int], Optional[dict]]


def in_a215944(n):
    """Membership in A215944: psp2 with three prime factors (counted with
    multiplicity) divisible by a smaller psp2. Checked against the b-file."""
    f = numth.factor(n)
    if sum(f.values()) != 3:
        return False
    a, b, c = [p for p, e in f.items() for _ in range(e)]
    return any(d < n and numth.is_psp(d) for d in {a * b, a * c, b * c})


def _divisors(n):
    ds = [1]
    for p, e in numth.factor(n).items():
        ds = [d * p ** i for d in ds for i in range(e + 1)]
    return sorted(ds)


def coman_form(n):
    """Witness (p, A, B) with n = p*A*B, A = (m+1)p-m, B = (k+1)p-k, m, k >= 1,
    i.e. A, B = 1 (mod p-1) and A, B >= 2p-1. p, A, B need not be prime."""
    for p in _divisors(n):
        if p < 2 or p ** 3 > n:
            continue
        r = n // p
        for a in _divisors(r):
            b = r // a
            if a <= b and a >= 2 * p - 1 and (a - 1) % (p - 1) == 0 and (b - 1) % (p - 1) == 0:
                return (p, a, b)
    return None


def a215944(n):
    """Members of A215944 (squareful ones included) that violate the conjecture."""
    if not in_a215944(n) or coman_form(n):
        return None
    if n % 5461 == 0 and (n // 5461 + 13) % 42 == 0:
        return None  # the stated exception 5461*(42k-13)
    return {"n": n, "factors": numth.factor(n)}


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


def _vp_fact(x: int, p: int) -> int:
    s = 0
    while x:
        x //= p
        s += x
    return s


def a362070_value(n: int) -> int:
    """A362070: a(n) = sum_{r=1..K(n)} m_min(n, r), where m_min(n, r) is the least m
    with n | prod_{t=1..m} t(t+1)...(t+r-1) and K(n) is the Kempner number.
    Per prime power p^e || n the p-adic valuation of that product is
    v_p((m+r-1)!) + ... computed as sum_t [v_p((t+r-1)!) - v_p((t-1)!)]."""
    if n == 1:
        return 1
    fac = numth.factor(n)

    def kempner_pe(p, e):
        m = 0
        while True:
            m += p
            if _vp_fact(m, p) >= e:
                return m

    def f(p, e, r):
        s, m = 0, 0
        while s < e:
            m += 1
            s += _vp_fact(m + r - 1, p) - _vp_fact(m - 1, p)
        return m
    K = max(kempner_pe(p, e) for p, e in fac.items())
    return sum(max(f(p, e, r) for p, e in fac.items()) for r in range(1, K + 1))


def a362070(n: int):
    """a(n) != a(n+1)."""
    a, b = a362070_value(n), a362070_value(n + 1)
    return {"n": n, "a(n)": a, "a(n+1)": b} if a == b else None


def a134559_gcd(n: int) -> int:
    """gcd(P(n), n) with P(n) = prod_{k=0..ceil(n/2)-1} b_n(k), where b_n(k) is the
    sum of all u in [1, n] with n mod u = k (A134559, Ratajczak 2019 comment)."""
    K = (n + 1) // 2
    b = [0] * K
    for u in range(1, n + 1):
        r = n % u
        if r < K:
            b[r] += u
    pr = 1 % n
    for x in b:
        pr = pr * x % n
    from math import gcd
    return gcd(pr, n)


def _is_prime_small(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def a134559(n: int):
    """[gcd(P(n),n) = 1 and gcd(P(n+1),n+1) = 2]  <=>  n in A005383 minus {3, 5}."""
    sat = a134559_gcd(n) == 1 and a134559_gcd(n + 1) == 2
    in_a = n > 5 and _is_prime_small(n) and n % 2 == 1 and _is_prime_small((n + 1) // 2)
    if sat == in_a:
        return None
    return {"n": n, "satisfies": sat, "in_A005383": in_a,
            "gcd(P(n),n)": a134559_gcd(n), "gcd(P(n+1),n+1)": a134559_gcd(n + 1)}


def a073631(k: int):
    """A073631 (Adamchuk 2007 comment): nonsquarefree terms are multiples of 23^2.

    k is a term iff k is not prime and 3^(k-1) = 2^(k-1) (mod k). Square factors:
    divide out every p <= k^(1/3); the cofactor c has all prime factors > k^(1/3),
    so c is 1, a prime, p*q or p^2, and c has a square factor iff c is a perfect
    square. Trial division is slow above ~1e15; give big k as known squares.
    """
    from math import isqrt
    if k < 4 or pow(3, k - 1, k) != pow(2, k - 1, k):
        return None
    sq = []
    c = k
    p = 2
    while p * p * p <= k:
        if c % p == 0:
            e = 0
            while c % p == 0:
                c //= p
                e += 1
            if e >= 2:
                sq.append(p)
        p += 1
    r = isqrt(c)
    if c > 1 and r * r == c:
        sq.append(r)
    if not sq or k % 529 == 0:
        return None          # squarefree (so also covers k prime) or a multiple of 23^2
    return {"k": k, "square_factors": sq}

REGISTRY: dict[str, Conjecture] = {c.key: c for c in [
    Conjecture(
        "A215944", "psp2",
        "The only psp2 divisible by a smaller psp2 that can't be written as "
        "p*((m+1)p-m)*((n+1)p-n) are multiples of 5461 of the form 5461*(42k-13).",
        "Domain = the entry's own terms: psp2 with three prime factors counted with "
        "multiplicity, divisible by a smaller psp2. The form with natural m, n >= 1 "
        "means n = p*A*B with A, B = 1 (mod p-1) and A, B >= 2p-1 (p, A, B any naturals).",
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
    Conjecture(
        "A362070", "n",
        "The equation a(n) = a(n+1) has no solutions.",
        "a(n) exactly as in the entry's name (agrees with the 57 DATA terms and the entry's "
        "Maxima program). Refuted: a(1715) = a(1716) = 91 (DISC-0020).",
        a362070),
    Conjecture(
        "A134559", "n",
        "Consecutive n with gcd(P(n),n) = 1 and gcd(P(n+1),n+1) = 2 are consecutive "
        "elements of A005383 (save 3 and 5).",
        "Read as: the solution set equals A005383 minus {3, 5}. Refuted: 4933 is in "
        "A005383 but 4934 | P(4934) (DISC-0021); the solution set is always inside A005383.",
        a134559),
    Conjecture(
        "A073631", "n",
        "All nonsquarefree terms of A073631 (nonprimes k with k | 3^(k-1)-2^(k-1)) "
        "are multiples of 23^2.",
        "Conjecture of A. Adamchuk (2007) in the comments of A073631 and A130058. "
        "Refuted: 3842760169^2 is a term (3842760169 is a base-3/2 Wieferich prime, "
        "A376896); it is the least counterexample (DISC-0023).",
        a073631),
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
