"""DISC-0004 candidate conjectures (M1.2), each with an independent check by impl_c.

Every candidate came out of engine.py (impl_a and impl_b agree to N = 10^4) and is
re-checked here by impl_c (linear sieve) to N_BIG. A candidate whose check fails
is REFUTED and stays in the record with its counterexample.

Levels (agreed with the CEO/ChatGPT 2026-11-22):
  L0 lead: pattern only.  L1: precise, A/B agree to 1e4, impl_c to 1e6, not a
  one-step consequence of a known formula, OEIS screen has no identity match for
  the statement itself, fully traceable.  L2 (M1.3): + critic, proof attempt, reviewer.
"""
from __future__ import annotations

from research.r001.batch.impl_c import C


def _sf(c, x):
    return c.is_squarefree(x)


def _a065301(c, n):
    return _sf(c, n) and _sf(c, c.sigma(n))


def check_all(n_big: int = 1_000_000) -> list[dict]:
    c = C(6 * n_big)
    out = []

    def add(cid, statement, source_lead, ok, counterexample=None, note="", triviality="", oeis=""):
        out.append({"id": cid, "statement": statement, "source_lead": source_lead,
                    "checked_to": n_big, "holds": ok, "counterexample": counterexample,
                    "note": note, "triviality": triviality, "oeis_screen": oeis})

    def first_fail(pred, start=1):
        for n in range(start, n_big + 1):
            if not pred(n):
                return n
        return None

    # C01
    bad = first_fail(lambda n: (c.sigma(c.sigma_odd(n)) == c.sigma_odd(c.sigma(n))) == (n % 2 == 1 and c.is_square(n)))
    add("C01", "sigma(sigma_odd(n)) = sigma_odd(sigma(n))  <=>  n is an odd square",
        "E-sigma(sigma_odd(n))=sigma_odd(sigma(n))", bad is None, bad,
        triviality="short argument expected (sigma(m) odd iff m is a square or twice a square), but the 'only if' for even n is not one step",
        oeis="set matches A016754 (odd squares), defined differently: cross match")

    # C02 / C03: structure of the non-A065301 solutions
    def c02(n):
        if c.rad(c.sigma(n)) != c.sigma(c.rad(n)) or _a065301(c, n):
            return True
        f = dict(c.fac(n))
        a = f.pop(2, 0)
        return a % 2 == 1 and a >= 3 and len(f) == 1 and list(f.values()) == [1]
    bad = first_fail(c02)
    add("C02", "if rad(sigma(n)) = sigma(rad(n)) then either n and sigma(n) are both squarefree (A065301) "
        "or n = 2^a * p with p an odd prime and a odd, a >= 3",
        "E-rad(sigma(n))=sigma(rad(n))", bad is None, bad,
        note="to 1e6 the exceptional solutions have a in {3, 5, 7}; A065301 is always contained (C02b)",
        triviality="containment of A065301 is one step; the classification of the other solutions is not",
        oeis="set is A065301 plus extras; no identity match for the full set")
    bad = first_fail(lambda n: not _a065301(c, n) or c.rad(c.sigma(n)) == c.sigma(c.rad(n)))
    add("C02b", "A065301 is contained in {n : rad(sigma(n)) = sigma(rad(n))}", "E-rad(sigma(n))=sigma(rad(n))",
        bad is None, bad, triviality="one step (rad fixes squarefree numbers): kept only as a sanity check, not counted as L1")

    def c03(n):
        if c.psi(c.sigma(n)) != c.sigma(c.psi(n)) or _a065301(c, n):
            return True
        f = dict(c.fac(n))
        a = f.pop(2, 0)
        return a % 2 == 1 and a >= 3
    bad = first_fail(c03)
    add("C03", "if psi(sigma(n)) = sigma(psi(n)) and n is not in A065301, then the 2-adic valuation of n is odd and >= 3",
        "E-psi(sigma(n))=sigma(psi(n))", bad is None, bad,
        note="examples 2088 = 2^3*3^2*29, 39688 = 2^3*11^2*41: odd part need not be squarefree",
        oeis="set is A065301 plus extras; no identity match")

    # C04 core / unitary sigma: extras are never squarefree
    bad = first_fail(lambda n: c.core(c.usigma(n)) != c.usigma(c.core(n)) or _a065301(c, n) or not _sf(c, n))
    add("C04", "if core(usigma(n)) = usigma(core(n)) and n is squarefree, then sigma(n) is squarefree (n in A065301)",
        "E-core(usigma(n))=usigma(core(n))", bad is None, bad,
        note="non-squarefree solutions exist (1764, 8820, 14400, ...): 51 up to 1e6",
        triviality="for squarefree n, usigma = sigma and core(n) = n, so this reduces to core(sigma(n)) = sigma(n): one step. NOT L1",
        oeis="cross match with A065301 on the squarefree part")

    # C05 / C06 Fermat
    fermat = {3, 5, 17, 257, 65537}
    bad = first_fail(lambda n: (c.phi(c.usigma(n)) == n) == (n == 1 or (n + 1) in fermat))
    add("C05", "phi(usigma(n)) = n  <=>  n = 1 or n + 1 is a Fermat prime", "F-phi(usigma(n))=n", bad is None, bad,
        note="solutions to 1e6: 1, 2, 4, 16, 256, 65536", oeis="5 terms only: too short for a meaningful OEIS screen")
    bad = first_fail(lambda n: (c.usigma(c.phi(n)) == n) == (n == 1 or n in fermat))
    add("C06", "usigma(phi(n)) = n  <=>  n = 1 or n is a Fermat prime", "F-usigma(phi(n))=n", bad is None, bad,
        note="solutions to 1e6: 1, 3, 5, 17, 257, 65537", oeis="too short for OEIS screen")

    # C07-C09 bounds through d(n)
    bad = first_fail(lambda n: n in (2, 6) or c.sigma(c.d(n)) <= n)
    add("C07", "sigma(d(n)) <= n for every n >= 1 except n = 2 and n = 6", "B-sigma(d(n))<=n", bad is None, bad,
        triviality="should follow from explicit bounds on d(n) (d(n) <= sqrt(3n)) plus a finite check")
    bad = first_fail(lambda n: n <= 360 or c.J2(c.d(n)) <= n)
    add("C08", "J2(d(n)) <= n for every n > 360 (the 25 exceptions are all <= 360)", "B-J2(d(n))<=n", bad is None, bad,
        triviality="same route as C07")
    bad = first_fail(lambda n: n == 2 or (c.psi(c.d(n)) <= n and c.usigma(c.d(n)) <= n))
    add("C09", "psi(d(n)) <= n and usigma(d(n)) <= n for every n except n = 2", "B-psi(d(n))<=n", bad is None, bad)

    # C10 refuted
    ex = [n for n in range(1, n_big + 1) if c.sigma_odd(c.phi(n)) > n]
    add("C10", "sigma_odd(phi(n)) <= n for all n except n = 8191 (the only exception up to 1e4)",
        "B-sigma_odd(phi(n))<=n", not ex[1:], ex[1] if len(ex) > 1 else None,
        note=f"{len(ex)} exceptions up to {n_big}: {ex[:8]} ... the 1e4 window was misleading")

    # C11 finite solution sets
    s1 = [n for n in range(1, n_big + 1) if c.d(c.psi(n)) == n]
    s2 = [n for n in range(1, n_big + 1) if c.psi(c.d(n)) == n]
    add("C11", "{n : d(psi(n)) = n} = {1, 2, 3, 4, 6} and {n : psi(d(n)) = n} = {1, 3, 4, 6, 12}",
        "F-d(psi(n))=n", s1 == [1, 2, 3, 4, 6] and s2 == [1, 3, 4, 6, 12], None,
        note=f"found {s1} and {s2} up to {n_big}", triviality="finiteness follows from d(m) = m^{o(1)}; the exact list needs an explicit bound")

    # C12 gpf / phi
    pow3 = lambda n: n % 3 == 0 and (n // 3) & (n // 3 - 1) == 0   # noqa: E731
    gpf = lambda x: c.fac(x)[-1][0] if x > 1 else 1               # noqa: E731
    bad = first_fail(lambda n: (gpf(c.phi(n)) == c.phi(gpf(n))) == (n in (1, 2) or pow3(n)))
    add("C12", "gpf(phi(n)) = phi(gpf(n))  <=>  n in {1, 2} or n = 3 * 2^k (k >= 0)", "E-gpf(phi(n))=phi(gpf(n))",
        bad is None, bad, triviality="elementary (phi(p) = p - 1 for the largest prime p of n)")

    # C13: new-looking sequence, not a conjecture
    s = [n for n in range(1, min(n_big, 200_000) + 1) if c.phi(c.usigma(n)) == c.usigma(c.phi(n))]
    add("C13", "the sequence {n : phi(usigma(n)) = usigma(phi(n))} (unitary analogue of A033632)",
        "E-phi(usigma(n))=usigma(phi(n))", True, None,
        note=f"terms up to 2e5: {s[:20]}", triviality="L0 only: a definition, not a statement",
        oeis="no identity match in the snapshot for its first terms")
    return out


LEVELS = {  # set after reading the checks; reasons are in the report
    "C01": "L1", "C02": "L1", "C02b": "L0", "C03": "L1", "C04": "L0", "C05": "L1", "C06": "L1",
    "C07": "L1", "C08": "L1", "C09": "L1", "C10": "REFUTED", "C11": "L1", "C12": "L1", "C13": "L0",
}
