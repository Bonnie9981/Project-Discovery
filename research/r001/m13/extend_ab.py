"""M1.3: re-check C01 and C02 with implementations A and B (C already did 1e6).

Run: python -m research.r001.m13.extend_ab [N]
"""
from __future__ import annotations

import json
import sys

from research.r001.batch import impl_a, impl_b


def is_sqfree_a(x: int) -> bool:
    return impl_a.value("core", x) == x if x > 0 else False


def main(n: int) -> dict:
    out = {}
    # implementation A, number by number
    va = lambda f, x: impl_a.value(f, x)   # noqa: E731
    c01a = [k for k in range(1, n + 1) if (va("sigma", va("sigma_odd", k)) == va("sigma_odd", va("sigma", k)))
            != (k % 2 == 1 and int(k ** 0.5) ** 2 == k)]
    sol_a = [k for k in range(1, n + 1) if va("rad", va("sigma", k)) == va("sigma", va("rad", k))]
    # implementation B, sieved tables (sigma(k) <= 5k for k <= 1e6, so 5n suffices for the inner values)
    m = 5 * n
    sig, sodd, rad = impl_b.table("sigma", m), impl_b.table("sigma_odd", m), impl_b.table("rad", m)
    c01b = [k for k in range(1, n + 1) if (sig[sodd[k]] == sodd[sig[k]]) != (k % 2 == 1 and int(k ** 0.5) ** 2 == k)]
    sol_b = [k for k in range(1, n + 1) if rad[sig[k]] == sig[rad[k]]]
    out["n"] = n
    out["C01_failures_a"], out["C01_failures_b"] = c01a, c01b
    out["C02_solution_sets_equal"] = sol_a == sol_b
    out["C02_solutions"] = len(sol_a)
    bad = []
    for k in sol_a:
        if is_sqfree_a(k) and is_sqfree_a(va("sigma", k)):
            continue
        f = {}
        x = k
        while x % 2 == 0:
            x //= 2
            f[2] = f.get(2, 0) + 1
        a = f.get(2, 0)
        if not (a % 2 == 1 and a >= 3 and x > 1 and va("rad", x) == x and impl_a.value("d", x) == 2):
            bad.append(k)
    out["C02_failures"] = bad
    return out


if __name__ == "__main__":
    print(json.dumps(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6)))
