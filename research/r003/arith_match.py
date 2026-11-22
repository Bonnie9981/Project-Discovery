"""R-003 pilot (R3-A): number-theoretic formulas for ECA orbit sizes.

Bridges R-001 (arithmetic functions) and R-002 (elementary CA on a ring, single
seed). For every rule r and quantity Q in {T (transient), P (period)}, and every
residue class w = c (mod m), m in {1, 2, 4}, we look for an exact formula

    Q_r(w) = a * G(h(w)) + b      for all w in the class with W0 <= w <= W_FIT

with G an arithmetic function, h an index map, a in {1, 2, 1/2}, b in -3..3.
Formulas that fit are re-checked on W_FIT < w <= W_CHECK by a fresh simulation.
A fit on a finite range is a lead (L0), never a theorem.
"""
from __future__ import annotations

from math import gcd

W0, W_FIT, W_CHECK = 5, 22, 30


def oddpart(n: int) -> int:
    while n and n % 2 == 0:
        n //= 2
    return n


def v2pow(n: int) -> int:
    return n & -n


def ordmod(m: int) -> int:
    """Multiplicative order of 2 mod m (m odd); 1 for m = 1."""
    if m == 1:
        return 1
    k, x = 1, 2 % m
    while x != 1:
        x = x * 2 % m
        k += 1
    return k


def subord(m: int) -> int:
    """Smallest k >= 1 with 2^k = +-1 mod m (m odd); 1 for m <= 3."""
    if m <= 3:
        return 1
    k, x = 1, 2 % m
    while x not in (1, m - 1):
        x = x * 2 % m
        k += 1
    return k


G = {
    "n": lambda n: n,
    "oddpart": oddpart,
    "v2pow": v2pow,
    "ord2(oddpart)": lambda n: ordmod(oddpart(n)),
    "sord2(oddpart)": lambda n: subord(oddpart(n)),
    "2^sord2-1": lambda n: 2 ** subord(oddpart(n)) - 1,
    "2^ord2-1": lambda n: 2 ** ordmod(oddpart(n)) - 1,
    "n/gcd(n,3)": lambda n: n // gcd(n, 3),
    "1": lambda n: 1,
}
H = {
    "w": lambda w: w,
    "w/2": lambda w: w // 2 if w % 2 == 0 else None,
    "(w+1)/2": lambda w: (w + 1) // 2 if w % 2 else None,
    "(w-1)/2": lambda w: (w - 1) // 2 if w % 2 else None,
    "w+1": lambda w: w + 1,
    "w-1": lambda w: w - 1,
}
A = (1, 2, 0.5)
B = range(-3, 4)


def fits(values: dict[int, int], ws: list[int]) -> list[str]:
    out = []
    for gname, g in G.items():
        for hname, h in H.items():
            args = [h(w) for w in ws]
            if any(x is None or x <= 0 for x in args):
                continue
            gv = [g(x) for x in args]
            for a in A:
                for b in B:
                    if all(a * gv[i] + b == values[w] for i, w in enumerate(ws)):
                        out.append((a, gname, hname, b))
    return out


def search(orbits: dict[int, list], rules=range(256)) -> list[dict]:
    """orbits[r][w-1] = (T, P) for w = 1..W_FIT."""
    leads = []
    for r in rules:
        for qi, q in ((0, "T"), (1, "P")):
            vals = {w: orbits[r][w - 1][qi] for w in range(1, W_FIT + 1)}
            if len(set(vals[w] for w in range(W0, W_FIT + 1))) <= 2:
                continue                      # constant-ish: not interesting
            pieces = {}
            for m in (1, 2, 4):
                pieces = {}
                for c in range(m):
                    ws = [w for w in range(W0, W_FIT + 1) if w % m == c]
                    f = fits(vals, ws)
                    if not f:
                        break
                    pieces[c] = f
                else:
                    leads.append({"rule": r, "quantity": q, "modulus": m,
                                  "pieces": {c: f for c, f in pieces.items()}})
                    break
    return leads


LINEAR = {"n", "1"}


def show(f: tuple) -> str:
    a, g, h, b = f
    return f"{a:g}*{g}({h}){b:+d}"


def evaluate(f: tuple, w: int):
    a, g, h, b = f
    x = H[h](w)
    if x is None or x <= 0:
        return None
    return a * G[g](x) + b


def nontrivial(lead: dict) -> bool:
    """A lead is trivial when every residue class has a formula linear in w."""
    return not all(any(f[1] in LINEAR for f in fs) for fs in lead["pieces"].values())


def recheck(lead: dict, w_hi: int = W_CHECK, max_steps: int = 1 << 22) -> dict:
    """Keep, per residue class, the formulas that survive W_FIT < w <= w_hi,
    with both impl_b and impl_c simulating each width."""
    from research.r002 import impl_b, impl_c
    r, qi, m = lead["rule"], (0 if lead["quantity"] == "T" else 1), lead["modulus"]
    truth = {}
    for w in range(W_FIT + 1, w_hi + 1):
        ob = impl_b.orbit(r, w, impl_b.single_seed(w), max_steps)
        oc = impl_c.orbit(r, w, impl_c.single_seed(w), max_steps)
        if ob is None or oc is None or tuple(ob) != tuple(oc):
            raise RuntimeError(f"impl_b/impl_c disagree or time out: rule {r}, w {w}")
        truth[w] = ob[qi]
    kept = {}
    for c, fs in lead["pieces"].items():
        ws = [w for w in truth if w % m == c]
        kept[c] = [f for f in fs if all(evaluate(f, w) == truth[w] for w in ws)]
    return {"survives": all(kept.values()), "pieces": kept, "w_hi": w_hi}


def partial_leads(orbits: dict[int, list], full: list[dict], rules=range(256)) -> list[dict]:
    """Rule/quantity pairs with no full lead where, for m in {2, 4}, some residue
    classes (not all) have a non-linear formula. search() drops these."""
    done = {(l["rule"], l["quantity"]) for l in full}
    out = []
    for r in rules:
        for qi, q in ((0, "T"), (1, "P")):
            if (r, q) in done:
                continue
            vals = {w: orbits[r][w - 1][qi] for w in range(1, W_FIT + 1)}
            if len(set(vals[w] for w in range(W0, W_FIT + 1))) <= 2:
                continue
            for m in (2, 4):
                pieces = {}
                for c in range(m):
                    ws = [w for w in range(W0, W_FIT + 1) if w % m == c]
                    f = [x for x in fits(vals, ws) if x[1] not in LINEAR]
                    if f and not any(x[1] in LINEAR for x in fits(vals, ws)):
                        pieces[c] = f
                if pieces:
                    out.append({"rule": r, "quantity": q, "modulus": m, "pieces": pieces})
    return out
