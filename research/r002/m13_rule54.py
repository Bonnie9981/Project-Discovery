"""M1.3: three-implementation check of R2-C10 (rule 54) to a larger width.

Run: python -m research.r002.m13_rule54 [W]
"""
from __future__ import annotations

import json
import sys

from research.r002 import impl_a, impl_b, impl_c


def formula(w: int) -> int:
    return {1: w - 3, 2: (w - 6) // 2, 3: (w - 7) // 2, 0: (w - 4) // 2}[w % 4]


def main(w_max: int) -> dict:
    bad, periods = [], set()
    for w in range(6, w_max + 1):
        a = impl_a.orbit(54, w, impl_a.single_seed(w), 1 << 22)
        b = impl_b.orbit(54, w, 1, 1 << 22)
        c = impl_c.orbit(54, w, impl_c.single_seed(w), 1 << 22)
        if not (a == b == c and a[0] == formula(w) and a[1] == 4):
            bad.append({"w": w, "a": a, "b": b, "c": c, "formula": formula(w)})
        periods.add(a[1])
    return {"w_range": [6, w_max], "failures": bad, "periods_seen": sorted(periods)}


if __name__ == "__main__":
    print(json.dumps(main(int(sys.argv[1]) if len(sys.argv) > 1 else 300)))
