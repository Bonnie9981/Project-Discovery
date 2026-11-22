"""DISC-0005 engine: all 256 elementary CA on a ring, single live cell.

1. Agreement: impl_a, impl_b, impl_c give the same (transient, period) for every
   rule and every width w <= W_CHECK.
2. Scan: (T_r(w), P_r(w)) for w = 1..W with impl_b.
3. Symmetry sanity checks (known theorems, so a failure means a bug):
   mirror(r) has the same orbit sizes; complement(r) started from the complemented
   seed has the same orbit sizes as r from the seed.
4. OEIS screen of every non-trivial period / transient sequence (per mirror class).
5. Damage spreading: flip one cell of a random state, Hamming distance after S steps.
"""
from __future__ import annotations

import random
from collections import defaultdict

from research.r002 import impl_a, impl_b, impl_c


def mirror(r: int) -> int:
    return sum(((r >> p) & 1) << int(format(p, "03b")[::-1], 2) for p in range(8))


def complement(r: int) -> int:
    return sum((1 - ((r >> (7 - p)) & 1)) << p for p in range(8))


def agreement(w_check: int = 12) -> list[tuple]:
    bad = []
    for r in range(256):
        for w in range(1, w_check + 1):
            a = impl_a.orbit(r, w, impl_a.single_seed(w), 1 << 20)
            b = impl_b.orbit(r, w, impl_b.single_seed(w), 1 << 20)
            c = impl_c.orbit(r, w, impl_c.single_seed(w), 1 << 20)
            if not a == b == c:
                bad.append((r, w, a, b, c))
    return bad


def scan(w_max: int) -> dict[int, list]:
    return {r: [impl_b.orbit(r, w, 1, 1 << w) for w in range(1, w_max + 1)] for r in range(256)}


def symmetry_failures(data: dict[int, list], w_sym: int = 14) -> list[tuple]:
    bad = []
    for r in range(256):
        if data[r] != data[mirror(r)]:
            bad.append(("mirror", r))
        for w in range(1, w_sym + 1):
            anti = ((1 << w) - 1) ^ 1
            if impl_b.orbit(complement(r), w, anti, 1 << w) != data[r][w - 1]:
                bad.append(("complement", r, w))
                break
    return bad


def trivial(seq) -> bool:
    """Eventually constant from the middle on, or at most two distinct values."""
    return len(set(seq)) <= 2 or len(set(seq[len(seq) // 2:])) == 1


def oeis_screen(data: dict[int, list], idx) -> list[dict]:
    groups: dict[tuple, list[int]] = defaultdict(list)
    for r in range(256):
        if r != min(r, mirror(r)):
            continue
        groups[("P", tuple(x[1] for x in data[r]))].append(r)
        groups[("T", tuple(x[0] for x in data[r]))].append(r)
    out = []
    for (q, seq), rules in sorted(groups.items(), key=lambda kv: (kv[1][0], kv[0][0])):
        if trivial(seq):
            continue
        hits = []
        if idx is not None:
            for drop in range(4):
                hits += [h["id"] for h in idx.lookup(list(seq[drop:]), min_len=16)]
        out.append({"quantity": q, "rules": rules, "terms": list(seq),
                    "oeis": sorted(set(hits)),
                    "oeis_status": ("SOURCE_UNAVAILABLE" if idx is None else
                                    "MATCH_FOUND" if hits else "NO_MATCH_IN_SCOPE")})
    return out


def damage(width: int = 64, steps: int = 64, trials: int = 8, seed: int = 2026) -> dict[int, float]:
    rng = random.Random(seed)
    inits = [rng.getrandbits(width) for _ in range(trials)]
    out = {}
    for r in range(256):
        tot = 0
        for x in inits:
            y = x ^ 1
            d = impl_b.evolve(r, width, x, steps) ^ impl_b.evolve(r, width, y, steps)
            tot += bin(d).count("1")
        out[r] = round(tot / (trials * width), 4)
    return out
