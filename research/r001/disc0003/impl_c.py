"""Implementation C — the Critic's third implementation (DISC-0003).

Method (deliberately different from impl_a and impl_b):

- Representation counts R_D^{cond}(N): coefficient extraction from the
  generating function  sum_k  x^{s0(k)} / (1 - x^k),  s0(k) = k + D*k*(k-1)/2
  (the smallest k-term sum).  For each admissible length k the coefficients of
  x^{s0}/(1-x^k) are 1 exactly at s0, s0+k, s0+2k, ...; we add them into
  per-filter tables with a stride-k sieve.  impl_a iterates over the first term
  a and accumulates running sums; impl_b, for each single n, tests whether
  n - D*k(k-1)/2 is a positive multiple of k.  Neither builds a stride sieve.
- Odd-divisor counts, the H3 split (d^2 < 2N vs d^2 > 2N), #{d | N : d^2 <= N}
  and tau(N): divisor sieves (loop over d, mark all multiples of d), not trial
  division (impl_a) and not prime factorisation (impl_b).  For the d^2 < 2N
  split the sieve starts the "small" range at the first multiple m with
  2m > d^2.
- Power of two: membership in an explicitly generated set {1, 2, 4, ...}.
- H5 right-hand side: a sieve over k marking every even multiple M = 2N of k,
  then testing the parity / size condition on M/k - (k-1)D.

All tables are built lazily up to the largest n requested (rebuilt with
doubling), so each holds_* call is O(1) after the build.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations

D_MAX = 8
_cache: dict = {"n": 0}
_cache5: dict = {"n": 0}


def gf_table(n_max: int, D: int, k_ok=None) -> list[int]:
    """Coefficients 0..n_max of sum_{k>=1, k_ok(k)} x^{k + D k(k-1)/2} / (1 - x^k)."""
    t = [0] * (n_max + 1)
    k = 1
    while True:
        s0 = k + D * k * (k - 1) // 2
        if s0 > n_max:
            break
        if k_ok is None or k_ok(k):
            for s in range(s0, n_max + 1, k):
                t[s] += 1
        k += 1
    return t


def _build(n_max: int) -> None:
    c = {"n": n_max}
    c["R1"] = gf_table(n_max, 1)
    c["R1two"] = gf_table(n_max, 1, lambda k: k >= 2)
    c["R1odd"] = gf_table(n_max, 1, lambda k: k % 2 == 1)
    c["R1even"] = gf_table(n_max, 1, lambda k: k % 2 == 0)
    c["R2"] = gf_table(n_max, 2)
    dodd = [0] * (n_max + 1)
    small = [0] * (n_max + 1)   # odd d | m with d^2 < 2m
    large = [0] * (n_max + 1)   # odd d | m with d^2 > 2m
    for d in range(1, n_max + 1, 2):
        lim = d * d // 2         # m > lim  <=>  2m > d^2 (d odd, so d^2 = 2m impossible)
        for m in range(d, n_max + 1, d):
            dodd[m] += 1
            if m > lim:
                small[m] += 1
            else:
                large[m] += 1
    tau = [0] * (n_max + 1)
    sq = [0] * (n_max + 1)      # d | m with d^2 <= m
    for d in range(1, n_max + 1):
        for m in range(d, n_max + 1, d):
            tau[m] += 1
        for m in range(d * d, n_max + 1, d):
            sq[m] += 1
    pw = set()
    p = 1
    while p <= n_max:
        pw.add(p)
        p *= 2
    c.update(dodd=dodd, small=small, large=large, tau=tau, sq=sq, pw=pw)
    _cache.clear()
    _cache.update(c)


def _ensure(n: int) -> dict:
    if n > _cache["n"]:
        _build(max(n, 2 * _cache["n"], 1024))
    return _cache


def _build5(n_max: int) -> None:
    c = {"n": n_max}
    for D in range(1, D_MAX + 1):
        c[("L", D)] = gf_table(n_max, D)
        rhs = [0] * (n_max + 1)
        M_max = 2 * n_max
        for k in range(1, M_max + 1):
            # multiples M of k that are even; M = 2N
            for M in range(k, M_max + 1, k):
                if M % 2:
                    continue
                q = M // k - (k - 1) * D
                if q >= 2 and q % 2 == 0:
                    rhs[M // 2] += 1
        c[("R", D)] = rhs
    _cache5.clear()
    _cache5.update(c)


def _ensure5(n: int) -> dict:
    if n > _cache5["n"]:
        _build5(max(n, 2 * _cache5["n"], 512))
    return _cache5


def holds_h1(n: int) -> bool:
    c = _ensure(n)
    return c["R1"][n] == c["dodd"][n]


def holds_h2a(n: int) -> bool:
    c = _ensure(n)
    return c["R1two"][n] == c["dodd"][n] - 1


def holds_h2b(n: int) -> bool:
    c = _ensure(n)
    return (c["R1two"][n] == 0) == (n in c["pw"])


def holds_h3(n: int) -> bool:
    c = _ensure(n)
    return c["R1odd"][n] == c["small"][n] and c["R1even"][n] == c["large"][n]


def holds_h4(n: int) -> bool:
    c = _ensure(n)
    return c["R2"][n] == c["sq"][n] and 2 * c["R2"][n] in (c["tau"][n], c["tau"][n] + 1)


def holds_h5(n: int) -> bool:
    c = _ensure5(n)
    return all(c[("L", D)][n] == c[("R", D)][n] for D in range(1, D_MAX + 1))


def holds_h6(n: int) -> bool:
    c = _ensure(n)
    return c["R2"][n] <= c["R1"][n]
