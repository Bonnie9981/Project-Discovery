"""DISC-0002 experiments (P0-07 drill). Run: python -m research.r001.drill [N]"""
from __future__ import annotations

import json
import math
import sys
import time

from discovery import verify
from discovery.records import environment, git_commit
from discovery.verify import Conjecture
from research.r001.primality import is_prime_mr, is_prime_trial


def q_holds(p: int, upto: int, is_prime) -> bool:
    return all(is_prime(n * n + n + p) for n in range(0, upto + 1))


def isqrt_p_over_3(p: int) -> int:
    return math.isqrt(p // 3)  # floor(sqrt(p/3)) for integer p


def conjectures(N: int) -> list[Conjecture]:
    primes = lambda: (p for p in range(2, N + 1) if is_prime_trial(p))
    return [
        Conjecture(
            "H1", "for every p >= 2: (p-1)^2 + (p-1) + p = p^2 (so it is not prime)",
            lambda: range(2, min(N, 10_000) + 1), f"2..{min(N, 10_000)}",
            lambda p: (p - 1) ** 2 + (p - 1) + p == p * p and not is_prime_trial(p * p),
            lambda p: pow(p - 1, 2) + p - 1 + p - pow(p, 2) == 0 and not is_prime_mr(p ** 2),
        ),
        Conjecture(
            "H2", "n^2 + n + 41 is prime for 0 <= n <= 39", lambda: range(0, 40), "0..39",
            lambda n: is_prime_trial(n * n + n + 41), lambda n: is_prime_mr(n * n + n + 41),
        ),
        Conjecture(
            "H4", f"for prime p <= {N}: Q_p holds  <=>  p in {{2,3,5,11,17,41}}",
            primes, f"primes <= {N}",
            lambda p: q_holds(p, p - 2, is_prime_trial) == (p in {2, 3, 5, 11, 17, 41}),
            lambda p: q_holds(p, p - 2, is_prime_mr) == (p in {2, 3, 5, 11, 17, 41}),
        ),
        Conjecture(
            "H5", f"for prime p <= {N}: Q_p holds  <=>  n^2+n+p prime for all n <= floor(sqrt(p/3))",
            primes, f"primes <= {N}",
            lambda p: q_holds(p, p - 2, is_prime_trial) == q_holds(p, isqrt_p_over_3(p), is_prime_trial),
            lambda p: q_holds(p, p - 2, is_prime_mr) == q_holds(p, isqrt_p_over_3(p), is_prime_mr),
        ),
    ]


def h3() -> dict:
    v = 40 * 40 + 40 + 41
    return {"id": "H3", "statement": "40^2+40+41 is not prime",
            "value": v, "trial": is_prime_trial(v), "mr": is_prime_mr(v),
            "status": verify.SUPPORTED_IN_RANGE if not is_prime_trial(v) and not is_prime_mr(v)
            else verify.REFUTED if is_prime_trial(v) and is_prime_mr(v) else verify.INCONCLUSIVE}


def main(N: int = 10_000) -> dict:
    t0 = time.time()
    out = {"params": {"N": N}, "git_commit": git_commit(), "env": environment(), "results": []}
    for c in conjectures(N):
        v = verify.check(c)
        out["results"].append({"id": c.id, "statement": c.statement, "domain": c.domain_desc, **v.as_dict()})
    out["results"].append(h3())
    out["seconds"] = round(time.time() - t0, 2)
    return out


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    print(json.dumps(main(N), indent=2, ensure_ascii=False))
