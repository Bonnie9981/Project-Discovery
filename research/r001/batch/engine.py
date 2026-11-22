"""DISC-0004 batch engine: generate derived sequences, detect structure, screen against OEIS.

Pipeline (docs/RESEARCH_STANDARDS.md, M1.2 rules agreed 2026-11-22):
1. Base tables from impl_a and impl_b separately; every derived value is computed
   twice, once from each implementation's tables, and any disagreement drops the item.
2. Derived objects: compositions f(g(n)); commutator pairs f(g(n)) vs g(f(n)).
3. Detectors produce leads (Level 0): multiplicativity, sign/inequality with
   finite exception set, equality sets, residue classes with exceptions.
4. Each lead's sequence or set is looked up in the OEIS snapshot. A lead whose
   OEIS match is *definitional* (the OEIS name uses the same functions) is known.
5. Leads are scored; Level 1 needs impl_c to confirm to a larger range (run.py).
This file never decides novelty beyond the automatic statuses in discovery.novelty.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

from research.r001.batch import impl_a as A
from research.r001.batch import impl_b as B
from research.r001.batch.library import FUNCS, INNER, KEYWORDS, MONOTONE_BOUND, OUTER


@dataclass
class Lead:
    id: str
    kind: str
    statement: str
    objects: list[str]
    data: dict = field(default_factory=dict)
    oeis: list[dict] = field(default_factory=list)
    oeis_kind: str = "none"          # none | definitional | cross
    score: int = 0
    reasons: list[str] = field(default_factory=list)


class Tables:
    """Base function tables up to M from both implementations."""

    def __init__(self, n: int, m: int):
        self.n, self.m = n, m
        self.a: dict[str, list] = {}
        self.b: dict[str, list] = {}
        self.mismatch: list[str] = []
        for f in FUNCS:
            lim = n if f in ("r2", "r3", "r4") else m
            ta, tb = A.table(f, lim), B.table(f, lim)
            self.a[f], self.b[f] = ta, tb
            if ta != tb:
                self.mismatch.append(f)

    def compose(self, f: str, g: str):
        """f(g(n)) for n = 1..N from each implementation; None if values exceed M or disagree."""
        ga, gb, fa, fb = self.a[g], self.b[g], self.a[f], self.b[f]
        sa, sb = [None], [None]
        for i in range(1, self.n + 1):
            x, y = ga[i], gb[i]
            if x < 1 or y < 1 or x >= len(fa) or y >= len(fb):
                return None
            sa.append(fa[x])
            sb.append(fb[y])
        return sa if sa == sb else "DISAGREE"


# ----------------------------------------------------------------------------- OEIS

class OeisIndex:
    """Exact-window index over the snapshot: key = 6 consecutive terms at offsets 0..3."""

    def __init__(self, snap, width: int = 6):
        self.snap, self.width = snap, width
        self.idx: dict[tuple, list] = defaultdict(list)
        for sid, terms in snap.seqs.items():
            for off in range(0, 4):
                w = tuple(terms[off:off + width])
                if len(w) == width:
                    self.idx[w].append((sid, off))

    def lookup(self, q: list[int], min_len: int = 12) -> list[dict]:
        """q must match from one of the first 4 OEIS terms on; all of q (if shorter than
        min_len) or at least min_len terms must agree."""
        if len(q) < self.width:
            return []
        out = []
        for sid, off in self.idx.get(tuple(q[:self.width]), []):
            ref = self.snap.seqs[sid][off:]
            k = min(len(ref), len(q))
            if (k >= min_len or k == len(q)) and ref[:k] == q[:k]:
                out.append({"id": sid, "name": self.snap.names.get(sid, ""), "offset": off, "matched_terms": k})
        return out


def definitional(name: str, funcs: list[str]) -> bool:
    low = name.lower()
    return all(any(k.lower() in low for k in KEYWORDS.get(f, [f])) for f in funcs if f in KEYWORDS)


# ----------------------------------------------------------------------------- detectors

def is_multiplicative(s, n) -> bool:
    if s[1] != 1:
        return False
    for a in range(2, n + 1):
        for b in range(a + 1, n // a + 1):
            if math.gcd(a, b) == 1 and s[a * b] != s[a] * s[b]:
                return False
    return True


MULTIPLICATIVE = {"sigma", "phi", "psi", "rad", "core", "sigma_odd", "usigma", "d", "sigma2", "J2",
                  "d_odd", "d_unitary", "d_square", "mu", "liouville"}
# Sequences so common that a numerical match with them says little (primes, squarefree, ...).
COMMON = {"A000040", "A008578", "A015919", "A064555", "A000012", "A000027", "A005117", "A000961",
          "A000079", "A000290", "A001358", "A000430", "A246655", "A005408", "A005843", "A000035"}


def trivially_multiplicative(f: str, g: str) -> bool:
    # liouville is completely multiplicative and Omega completely additive, so
    # liouville(g(n)) is multiplicative for every multiplicative g.
    if f == "liouville" and g in MULTIPLICATIVE:
        return True
    # f(g(n)) is multiplicative by construction when f is (completely) determined
    # multiplicatively and g maps coprime n to coprime values (only rad/core here),
    # or f is completely multiplicative.
    return g in ("rad", "core") and f not in ("omega", "Omega", "sopf", "sopfr", "gpf", "lpf", "carmichael")


def run(n: int = 10_000, m_factor: int = 5, snap=None) -> dict:
    T = Tables(n, m_factor * n)
    idx = OeisIndex(snap) if snap is not None else None
    leads: list[Lead] = []
    seqs: dict[str, list] = {}
    dropped = {"out_of_range": [], "disagree": []}

    for g in INNER:
        for f in OUTER:
            if f == g:
                continue
            s = T.compose(f, g)
            key = f"{f}({g}(n))"
            if s is None:
                dropped["out_of_range"].append(key)
            elif s == "DISAGREE":
                dropped["disagree"].append(key)
            else:
                seqs[key] = s

    def oeis(lead: Lead, q: list[int], funcs: list[str]):
        if idx is None:
            return
        hits = idx.lookup(q)
        lead.oeis = hits[:5]
        if not hits:
            lead.oeis_kind = "none"
        elif any(definitional(h["name"], funcs) for h in hits):
            lead.oeis_kind = "definitional"
        else:
            lead.oeis_kind = "cross"

    # D1: multiplicative compositions
    for key, s in seqs.items():
        f, g = key.split("(")[0], key.split("(")[1]
        if len(set(s[1:])) >= 3 and is_multiplicative(s, n) and not trivially_multiplicative(f, g):
            L = Lead(f"M-{key}", "multiplicative", f"n -> {key} is multiplicative", [f, g])
            oeis(L, s[1:201], [f, g])
            leads.append(L)

    # D2: commutator pairs f(g(n)) vs g(f(n)): inequality / equality set
    for key, s in seqs.items():
        f, g = key.split("(")[0], key.split("(")[1]
        other = f"{g}({f}(n))"
        if other not in seqs or key > other:
            continue
        t = seqs[other]
        eq = [i for i in range(1, n + 1) if s[i] == t[i]]
        lt = [i for i in range(1, n + 1) if s[i] < t[i]]
        gt = [i for i in range(1, n + 1) if s[i] > t[i]]
        for lo_name, lo, hi_name, hi_list in ((key, lt, other, gt), (other, gt, key, lt)):
            if hi_list and len(hi_list) <= 30 and len(lo) > n // 10:
                L = Lead(f"I-{lo_name}<={hi_name}", "inequality_with_exceptions",
                         f"{lo_name} <= {hi_name} for all n except n in {hi_list} (n <= {n})",
                         [f, g], {"exceptions": hi_list, "equal_count": len(eq)})
                leads.append(L)
        if not lt or not gt:
            pass
        if 5 <= len(eq) <= n // 2:
            L = Lead(f"E-{key}={other}", "equality_set", f"{{n : {key} = {other}}}", [f, g],
                     {"count": len(eq), "first": eq[:200]})
            oeis(L, eq[:200], [f, g])
            leads.append(L)
        if not lt and gt or not gt and lt:
            big, small = (key, other) if gt else (other, key)
            L = Lead(f"I-{small}<={big}", "inequality", f"{small} <= {big} for all n <= {n}",
                     [f, g], {"equal_count": len(eq), "equal_first": eq[:20]})
            leads.append(L)

    # D3: composition vs n, with a finite or structured exception set
    ident = list(range(n + 1))
    for key, s in seqs.items():
        f, g = key.split("(")[0], key.split("(")[1]
        bf, bg = MONOTONE_BOUND.get(f), MONOTONE_BOUND.get(g)
        above = [i for i in range(1, n + 1) if s[i] > ident[i]]
        below = [i for i in range(1, n + 1) if s[i] < ident[i]]
        equal = [i for i in range(1, n + 1) if s[i] == ident[i]]
        for side, ex, rel in (("<=", above, "below"), (">=", below, "above")):
            trivial = (side == "<=" and bf == "down" and bg == "down") or (side == ">=" and bf == "up" and bg == "up")
            if trivial or not ex or len(ex) > 25:
                continue
            L = Lead(f"B-{key}{side}n", "bound_with_exceptions",
                     f"{key} {side} n for all n except {ex} (n <= {n})", [f, g],
                     {"exceptions": ex, "equal_count": len(equal)})
            leads.append(L)
        if 5 <= len(equal) <= n // 2:
            L = Lead(f"F-{key}=n", "fixed_points", f"{{n : {key} = n}}", [f, g],
                     {"count": len(equal), "first": equal[:200]})
            oeis(L, equal[:200], [f, g])
            leads.append(L)

    # D4: residue rules with finite exceptions: m | f(g(n)) for all but finitely many n
    for key, s in seqs.items():
        f, g = key.split("(")[0], key.split("(")[1]
        for mod in (2, 3, 4, 8, 12, 24):
            bad = [i for i in range(1, n + 1) if s[i] % mod]
            if 0 < len(bad) <= 20 and bad[-1] < n // 4:
                L = Lead(f"R-{mod}|{key}", "residue_with_exceptions",
                         f"{mod} divides {key} for all n except {bad} (n <= {n})", [f, g],
                         {"mod": mod, "exceptions": bad})
                leads.append(L)

    # sequences themselves: OEIS status of every composition
    seq_status = {}
    for key, s in seqs.items():
        f, g = key.split("(")[0], key.split("(")[1]
        L = Lead(f"S-{key}", "sequence", key, [f, g])
        oeis(L, s[1:201], [f, g])
        seq_status[key] = L.oeis_kind

    score(leads, seq_status)
    return {"n": n, "m": T.m, "base_mismatch": T.mismatch, "dropped": dropped,
            "n_sequences": len(seqs), "seq_status": seq_status, "leads": leads, "_seqs": seqs}


def score(leads: list[Lead], seq_status: dict) -> None:
    """Heuristic 0-100 ranking (never decides truth). Weights follow the agreed rubric."""
    for L in leads:
        sc, why = 0, []
        base = {"multiplicative": 40, "equality_set": 30, "fixed_points": 30, "bound_with_exceptions": 30,
                "inequality_with_exceptions": 35, "inequality": 25, "residue_with_exceptions": 20}[L.kind]
        sc += base
        why.append(f"kind {L.kind} +{base}")
        common = all(o["id"] in COMMON for o in L.oeis) if L.oeis else False
        if L.oeis_kind == "cross" and common:
            sc -= 20
            why.append("only matches a very common sequence (primes, squarefree, ...) -20")
        elif L.oeis_kind == "cross":
            sc += 30
            why.append("set/sequence matches an OEIS entry defined differently +30")
        elif L.oeis_kind == "definitional":
            sc -= 30
            why.append("OEIS entry defines it with the same functions -30 (known object)")
        ex = L.data.get("exceptions")
        if ex is not None:
            if len(ex) <= 3:
                sc += 10
                why.append("few exceptions +10")
        if set(L.objects) & {"Omega", "omega", "gpf", "sopfr", "d"}:
            sc -= 5
            why.append("small-valued inner/outer function -5")
        L.score, L.reasons = max(0, min(100, sc)), why
    leads.sort(key=lambda L: -L.score)
