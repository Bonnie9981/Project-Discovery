"""DISC-0003 experiments. Run: python -m research.r001.disc0003.run [N_MAX] > experiment_data.json

Each hypothesis is checked by impl_a (direct enumeration) and impl_b (per-length
closed form + factorisation) through discovery.verify.check, with both domains
generated independently. impl_c (the Critic's) is added when present.
"""
from __future__ import annotations

import importlib
import json
import sys
import time

from discovery import verify
from discovery.records import environment, git_commit
from discovery.verify import Conjecture
from research.r001.disc0003 import impl_a as A
from research.r001.disc0003 import impl_b as B

try:  # the Critic's third implementation, optional
    C = importlib.import_module("research.r001.disc0003.impl_c")
except ImportError:  # pragma: no cover
    C = None

ODD = lambda k: k % 2 == 1          # noqa: E731
EVEN = lambda k: k % 2 == 0         # noqa: E731
TWO_LE = lambda k: k >= 2           # noqa: E731


def conjectures(n_max: int, d_max: int = 8) -> list[Conjecture]:
    tA = {key: A.rep_table(n_max, D, f) for key, D, f in (
        ("1", 1, None), ("1odd", 1, ODD), ("1even", 1, EVEN), ("1two", 1, TWO_LE), ("2", 2, None))}
    n5 = min(n_max, 10_000)  # H5 costs d_max times more per n
    tAD = {D: A.rep_table(n5, D) for D in range(1, d_max + 1)}
    dom_a = lambda: A.domain(n_max)   # noqa: E731
    dom_b = lambda: B.domain(n_max)   # noqa: E731

    def c3(name):
        return getattr(C, name) if C is not None and hasattr(C, name) else None

    def odd_small_a(n, small):
        return sum(1 for d in A.divisor_pairs(n) if d % 2 == 1 and ((d * d < 2 * n) == small))

    def odd_small_b(n, small):
        # enumerate odd divisors from the factorisation
        divs = [1]
        for p, e in B.factorise(n).items():
            if p != 2:
                divs = [d * p ** i for d in divs for i in range(e + 1)]
        return sum(1 for d in divs if (d * d < 2 * n) == small)

    def small_b(n):
        divs = [1]
        for p, e in B.factorise(n).items():
            divs = [d * p ** i for d in divs for i in range(e + 1)]
        return sum(1 for d in divs if d * d <= n)

    def general_a(n, D):
        return sum(1 for k in A.divisor_pairs(2 * n)
                   if (2 * n // k) >= 2 + (k - 1) * D and ((2 * n // k) - (k - 1) * D) % 2 == 0)

    def general_b(n, D):
        divs = [1]
        for p, e in B.factorise(2 * n).items():
            divs = [d * p ** i for d in divs for i in range(e + 1)]
        c = 0
        for k in divs:
            m = 2 * n // k
            if m - (k - 1) * D >= 2 and (m - (k - 1) * D) % 2 == 0:
                c += 1
        return c

    hc = c3("holds_h1")
    out = [
        Conjecture("H1", "R(N) = d_odd(N): #reps of N as a sum of >=1 consecutive positive integers "
                   "equals #odd divisors of N", dom_a, f"1..{n_max}",
                   lambda n: tA["1"][n] == A.odd_divisor_count(n),
                   lambda n: B.rep_count(n) == B.odd_divisor_count(n),
                   holds_c=hc, domain_b=dom_b),
        Conjecture("H2a", "#reps with >=2 terms = d_odd(N) - 1", dom_a, f"1..{n_max}",
                   lambda n: tA["1two"][n] == A.odd_divisor_count(n) - 1,
                   lambda n: B.rep_count(n, 1, TWO_LE) == B.odd_divisor_count(n) - 1,
                   holds_c=c3("holds_h2a"), domain_b=dom_b),
        Conjecture("H2b", "N has no rep with >=2 terms  <=>  N is a power of 2", dom_a, f"1..{n_max}",
                   lambda n: (tA["1two"][n] == 0) == A.is_power_of_two(n),
                   lambda n: (B.rep_count(n, 1, TWO_LE) == 0) == B.is_power_of_two(n),
                   holds_c=c3("holds_h2b"), domain_b=dom_b),
        Conjecture("H3", "#reps with an odd number k of terms = #{odd d | N : d^2 < 2N}, and with even k "
                   "= #{odd d | N : d^2 > 2N}", dom_a, f"1..{n_max}",
                   lambda n: tA["1odd"][n] == odd_small_a(n, True) and tA["1even"][n] == odd_small_a(n, False),
                   lambda n: B.rep_count(n, 1, ODD) == odd_small_b(n, True)
                   and B.rep_count(n, 1, EVEN) == odd_small_b(n, False),
                   holds_c=c3("holds_h3"), domain_b=dom_b),
        Conjecture("H4", "R_2(N) (common difference 2) = #{d | N : d^2 <= N} = ceil(tau(N)/2)", dom_a,
                   f"1..{n_max}",
                   lambda n: tA["2"][n] == sum(1 for d in A.divisor_pairs(n) if d * d <= n)
                   and tA["2"][n] == (A.divisor_count(n) + 1) // 2,
                   lambda n: B.rep_count(n, 2) == -(-B.divisor_count(n) // 2)
                   and B.rep_count(n, 2) == small_b(n),
                   holds_c=c3("holds_h4"), domain_b=dom_b),
        Conjecture("H5", f"for 1 <= D <= {d_max}: R_D(N) = #{{k | 2N : 2N/k - (k-1)D is even and >= 2}}",
                   lambda: A.domain(n5), f"1..{n5}, D=1..{d_max}",
                   lambda n: all(tAD[D][n] == general_a(n, D) for D in range(1, d_max + 1)),
                   lambda n: all(B.rep_count(n, D) == general_b(n, D) for D in range(1, d_max + 1)),
                   holds_c=c3("holds_h5"), domain_b=lambda: B.domain(n5)),
        Conjecture("H6", "(naive extrapolation, expected false) R_2(N) <= R_1(N) for every N", dom_a,
                   f"1..{n_max}",
                   lambda n: tA["2"][n] <= tA["1"][n],
                   lambda n: B.rep_count(n, 2) <= B.rep_count(n, 1),
                   holds_c=c3("holds_h6"), domain_b=dom_b),
        Conjecture("H7", "(characterises the H6 counterexamples) R_2(N) > R_1(N)  <=>  4 | N", dom_a,
                   f"1..{n_max}",
                   lambda n: (tA["2"][n] > tA["1"][n]) == (n % 4 == 0),
                   lambda n: (B.rep_count(n, 2) > B.rep_count(n, 1)) == (n % 4 == 0),
                   holds_c=c3("holds_h7"), domain_b=dom_b),
    ]
    return out


# Extension sequences for the novelty layer: name -> (D, k filter, description)
EXTENSIONS = {
    "E1": (1, TWO_LE, "N as a sum of >= 2 consecutive positive integers"),
    "E2": (1, ODD, "... with an odd number of terms"),
    "E3": (1, EVEN, "... with an even number of terms"),
    "E4": (1, lambda k: k >= 3, "... with >= 3 terms"),
    "E5": (1, lambda k: k <= 3, "... with at most 3 terms"),
    "E6": (2, None, "AP with common difference 2, >= 1 term"),
    "E7": (2, TWO_LE, "AP with common difference 2, >= 2 terms"),
    "E8": (3, None, "AP with common difference 3"),
    "E9": (3, TWO_LE, "AP with common difference 3, >= 2 terms"),
    "E10": (4, None, "AP with common difference 4"),
    "E11": (5, None, "AP with common difference 5"),
    "E12": (6, None, "AP with common difference 6"),
    "E13": (1, lambda k: k >= 2 and all(k % p for p in range(2, int(k ** 0.5) + 1)),
            "consecutive integers, prime number of terms"),
}
EXT_TERMS = 80


def extension_sequences() -> dict:
    out = {}
    for key, (D, f, desc) in EXTENSIONS.items():
        ta = A.rep_table(EXT_TERMS, D, f)[1:]
        tb = [B.rep_count(n, D, f) for n in range(1, EXT_TERMS + 1)]
        out[key] = {"D": D, "description": desc, "terms_from_n1": ta, "impl_agree": ta == tb}
    return out


def main(n_max: int = 100_000) -> dict:
    t0 = time.time()
    out = {"params": {"n_max": n_max, "d_max": 8, "ext_terms": EXT_TERMS}, "git_commit": git_commit(),
           "env": environment(), "results": []}
    for c in conjectures(n_max):
        v = verify.check(c, stop_at_first_counterexample=True)
        out["results"].append({"id": c.id, "statement": c.statement, "domain": c.domain_desc, **v.as_dict()})
    out["extensions"] = extension_sequences()
    out["seconds"] = round(time.time() - t0, 2)
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    print(json.dumps(main(n), indent=2, ensure_ascii=False))
