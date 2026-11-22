"""DISC-0005 candidate conjectures (R-002, elementary CA on a ring, single seed).

Each statement is about T_r(w) (transient) or P_r(w) (period) of rule r on a ring
of w cells started from one live cell. Candidates came from engine.py (impl_a,
impl_b, impl_c agree for all 256 rules, w <= 12; impl_b scan to w = 22). Here
every candidate is checked by impl_b (bit-parallel, Brent) AND impl_c (strings,
Floyd) up to w_big; the two must agree at every width or the check is INCONCLUSIVE.

v2pow(k) = largest power of 2 dividing k (OEIS A006519).
"""
from __future__ import annotations

from research.r002 import impl_b, impl_c

MAX_STEPS = 1 << 22


def v2pow(k: int) -> int:
    return k & -k


def is_pow2(k: int) -> bool:
    return k > 0 and k & (k - 1) == 0


# id -> (rule, quantity "T"/"P", formula(w) or None to skip w, w_min, statement, source)
CANDIDATES = {
    "R2-C01": (18, "T", lambda w: v2pow((w + 1) // 2), 1,
               "T_18(w) = v2pow(ceil(w/2)) for all w >= 1 (also rule 146 for w >= 3, by its own run)", "T-18"),
    "R2-C02": (146, "T", lambda w: v2pow((w + 1) // 2), 3,
               "T_146(w) = v2pow(ceil(w/2)) for w >= 3", "T-146"),
    "R2-C03": (126, "T", lambda w: v2pow(w // 2 + 1), 2,
               "T_126(w) = v2pow(floor(w/2) + 1) for w >= 2", "T-126"),
    "R2-C04": (26, "T", lambda w: 0 if w % 2 else v2pow(w // 2), 2,
               "T_26(w) = 0 for odd w >= 3 and v2pow(w/2) for even w", "T-26"),
    "R2-C05": (153, "T", lambda w: 0 if w % 2 else v2pow(w), 1,
               "T_153(w) = 0 for odd w and v2pow(w) for even w", "T-153"),
    "R2-C06": (105, "T", lambda w: v2pow(w // 3) if w % 3 == 0 else 0, 1,
               "T_105(w) = v2pow(w/3) if 3 | w, else 0", "T-105"),
    "R2-C07": (122, "T", lambda w: (w // 2 - 1) if w % 2 == 0 else (w if is_pow2(w + 1) else w - 2), 2,
               "T_122(w) = w/2 - 1 for even w; for odd w it is w when w+1 is a power of 2, else w-2", "T-122"),
    "R2-C08": (218, "T", lambda w: v2pow(w // 2) if w % 2 == 0 else (w - 2 if is_pow2(w - 1) else w - 1), 3,
               "T_218(w) = v2pow(w/2) for even w; for odd w >= 3 it is w-2 when w-1 is a power of 2, else w-1",
               "T-218"),
    # First written as 2*floor((w+1)/4), a misreading of the w <= 22 data; the check caught it at w = 7.
    "R2-C09": (94, "T", lambda w: 2 * (w // 4), 4,
               "T_94(w) = 2*floor(w/4) for w >= 4", "T-94"),
    "R2-C10": (54, "T", lambda w: {1: w - 3, 2: (w - 6) // 2, 3: (w - 7) // 2, 0: (w - 4) // 2}[w % 4], 6,
               "T_54(w) = w-3, (w-6)/2, (w-7)/2, (w-4)/2 for w = 1, 2, 3, 0 mod 4 (w >= 6)", "T-54"),
}

# Period relation: P_218(w) = 1 for odd w, P_218(w) = P_18(w) for even w.
RELATION = ("R2-C11", "P_218(w) = 1 for odd w and P_218(w) = P_18(w) for even w", "P-218")


def _both(rule: int, w: int):
    b = impl_b.orbit(rule, w, impl_b.single_seed(w), MAX_STEPS)
    c = impl_c.orbit(rule, w, impl_c.single_seed(w), MAX_STEPS)
    return b, c


def check_all(w_big: int = 30) -> list[dict]:
    out = []
    for cid, (rule, q, f, w_min, statement, src) in CANDIDATES.items():
        idx = 0 if q == "T" else 1
        cex, disagree, unresolved = None, [], []
        for w in range(w_min, w_big + 1):
            b, c = _both(rule, w)
            if b != c:
                disagree.append(w)
                continue
            if b is None:
                unresolved.append(w)
                continue
            if b[idx] != f(w):
                cex = {"w": w, "observed": b[idx], "formula": f(w)}
                break
        out.append(_entry(cid, statement, src, w_min, w_big, cex, disagree, unresolved, rule=rule))
    cid, statement, src = RELATION
    cex, disagree, unresolved = None, [], []
    for w in range(1, w_big + 1):
        b218, c218 = _both(218, w)
        b18, c18 = _both(18, w)
        if b218 != c218 or b18 != c18:
            disagree.append(w)
            continue
        if b218 is None or b18 is None:
            unresolved.append(w)
            continue
        want = 1 if w % 2 else b18[1]
        if b218[1] != want:
            cex = {"w": w, "observed": b218[1], "formula": want}
            break
    out.append(_entry(cid, statement, src, 1, w_big, cex, disagree, unresolved, rule=218))
    return out


def _entry(cid, statement, src, w_min, w_big, cex, disagree, unresolved, rule):
    if disagree:
        status = "INCONCLUSIVE"
    elif cex:
        status = "REFUTED"
    elif unresolved:
        status = "INCONCLUSIVE"
    else:
        status = "SUPPORTED_NOVELTY_UNCHECKED"
    return {"id": cid, "rule": rule, "statement": statement, "source_lead": src,
            "checked_widths": [w_min, w_big], "implementations": ["impl_b", "impl_c"],
            "holds": cex is None and not disagree and not unresolved, "counterexample": cex,
            "disagreements": disagree, "unresolved": unresolved, "status": status}
