"""Count special vertex subsets of standard graph families (`python -m discovery.newseq.graphsets`).

For each family G_n and each property P, brute force over all 2^|V| subsets
(numpy, |V| <= MAXV) gives three sequences: number of subsets with P, minimum
size of such a subset, number of subsets of minimum size. Each sequence is
looked up in the offline OEIS; those not found are printed as leads.

All properties are "hitting" or "covering" conditions on bitmasks, so they
vectorise: a subset S satisfies "S meets M" iff (S & M) != 0.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import deque

import numpy as np

MAXV = 20


# ---------- families: n -> adjacency list ----------
def path(n): return {i: {j for j in (i - 1, i + 1) if 0 <= j < n} for i in range(n)}
def cycle(n): return {i: {(i - 1) % n, (i + 1) % n} for i in range(n)} if n >= 3 else None


def product(g, h):
    """Cartesian product."""
    V = [(a, b) for a in g for b in h]
    ix = {v: i for i, v in enumerate(V)}
    return {ix[(a, b)]: {ix[(a2, b)] for a2 in g[a]} | {ix[(a, b2)] for b2 in h[b]} for a, b in V}


def strong(g, h):
    V = [(a, b) for a in g for b in h]
    ix = {v: i for i, v in enumerate(V)}
    return {ix[(a, b)]: {ix[(a2, b2)] for a2 in g[a] | {a} for b2 in h[b] | {b}} - {ix[(a, b)]}
            for a, b in V}


def circulant(n, steps):
    if n < 2 * max(steps) + 1:
        return None
    return {i: {(i + s) % n for s in steps} | {(i - s) % n for s in steps} for i in range(n)}


def moebius(n):
    if n < 3:
        return None
    g = circulant(2 * n, [1])
    for i in range(2 * n):
        g[i].add((i + n) % (2 * n))
    return g


def gpetersen(n, k=2):
    if n < 2 * k + 1:
        return None
    g = {i: set() for i in range(2 * n)}
    def e(a, b): g[a].add(b); g[b].add(a)
    for i in range(n):
        e(i, (i + 1) % n); e(i, n + i); e(n + i, n + (i + k) % n)
    return g


def wheel(n):
    if n < 3:
        return None
    g = cycle(n); g[n] = set(range(n))
    for i in range(n): g[i].add(n)
    return g


def fan(n):
    g = path(n); g[n] = set(range(n))
    for i in range(n): g[i].add(n)
    return g


def triangular_strip(n):  # ladder with one diagonal per square (2 x n triangular grid)
    g = product(path(2), path(n))
    # vertex index (a,b) -> a*n+b ; add (0,b)-(1,b+1)
    for b in range(n - 1):
        g[b].add(n + b + 1); g[n + b + 1].add(b)
    return g


def knight(rows, n):
    V = [(r, c) for r in range(rows) for c in range(n)]
    ix = {v: i for i, v in enumerate(V)}
    mv = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    return {ix[(r, c)]: {ix[(r + a, c + b)] for a, b in mv if (r + a, c + b) in ix} for r, c in V}


FAMILIES = {
    "path": path,
    "cycle": cycle,
    "ladder": lambda n: product(path(2), path(n)),
    "prism": lambda n: product(path(2), cycle(n)) if n >= 3 else None,
    "moebius": moebius,
    "grid3": lambda n: product(path(3), path(n)),
    "king2": lambda n: strong(path(2), path(n)),
    "king3": lambda n: strong(path(3), path(n)),
    "tri_strip": triangular_strip,
    "gpetersen2": gpetersen,
    "wheel": wheel,
    "fan": fan,
    "c_1_2": lambda n: circulant(n, [1, 2]),
    "c_1_3": lambda n: circulant(n, [1, 3]),
    "torus3": lambda n: product(cycle(3), cycle(n)) if n >= 3 else None,
    "knight3": lambda n: knight(3, n),
    "knight2": lambda n: knight(2, n),
    "sq_path": lambda n: circulant_path(n, 2),
    "cube_path": lambda n: circulant_path(n, 3),
}


def circulant_path(n, k):  # k-th power of the path
    return {i: {j for j in range(i - k, i + k + 1) if 0 <= j < n and j != i} for i in range(n)}


# ---------- properties ----------
def dist(g):
    n = len(g)
    D = [[-1] * n for _ in range(n)]
    for s in range(n):
        D[s][s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in g[u]:
                if D[s][w] < 0:
                    D[s][w] = D[s][u] + 1
                    q.append(w)
    return D


def subset_or(masks):
    """Array over all subsets S of OR_{v in S} masks[v]."""
    a = np.zeros(1, dtype=np.int64)
    for m in masks:
        a = np.concatenate([a, a | m])
    return a


def subset_sum(vals):
    a = np.zeros(1, dtype=np.int64)
    for x in vals:
        a = np.concatenate([a, a + x])
    return a


def popcount(a):
    a = a.copy(); c = np.zeros_like(a)
    while a.any():
        c += a & 1; a >>= 1
    return c


def hits_all(S, masks):
    ok = np.ones(len(S), dtype=bool)
    for m in set(masks):
        ok &= (S & m) != 0
    return ok


def properties(g):
    n = len(g)
    full = (1 << n) - 1
    S = np.arange(1 << n, dtype=np.int64)
    opn = [sum(1 << w for w in g[v]) for v in range(n)]
    cl = [opn[v] | (1 << v) for v in range(n)]
    OP, CL = subset_or(opn), subset_or(cl)
    indep = (OP & S) == 0
    dom = CL == full
    tdom = OP == full
    P = {
        "independent": indep,
        "dominating": dom,
        "total_dominating": tdom,
        "independent_dominating": indep & dom,
        "vertex_cover": hits_all(S, [(1 << u) | (1 << v) for u in g for v in g[u] if u < v]),
        "efficient_dominating": dom & (subset_sum([bin(c).count("1") for c in cl]) == n),
        "total_perfect": tdom & (subset_sum([bin(c).count("1") for c in opn]) == n),
    }
    pairs = list(itertools.combinations(range(n), 2))
    P["identifying_code"] = dom & hits_all(S, [cl[u] ^ cl[v] for u, v in pairs])
    P["open_locating"] = tdom & hits_all(S, [opn[u] ^ opn[v] for u, v in pairs])
    P["locating_dominating"] = dom & hits_all(S, [(cl[u] ^ cl[v]) | (1 << u) | (1 << v) for u, v in pairs])
    D = dist(g)
    if all(D[0][v] >= 0 for v in range(n)):
        res = [sum(1 << x for x in range(n) if D[x][u] != D[x][v]) for u, v in pairs]
        P["resolving"] = hits_all(S, res)
    cnt = [popcount(S & c) for c in cl]
    P["double_dominating"] = np.all([c >= 2 for c in cnt], axis=0)
    ocnt = [popcount(S & o) for o in opn]
    inS = [((S >> v) & 1) == 1 for v in range(n)]
    P["2_dominating"] = np.all([inS[v] | (ocnt[v] >= 2) for v in range(n)], axis=0)
    P["perfect_dominating"] = np.all([inS[v] | (ocnt[v] == 1) for v in range(n)], axis=0)
    return S, P


def run(nmax=None):
    out = []
    for fam, f in FAMILIES.items():
        rows = {}
        for n in range(1, 40):
            g = f(n)
            if g is None:
                continue
            if len(g) > MAXV:
                break
            S, P = properties(g)
            pc = None
            for name, ok in P.items():
                cnt = int(ok.sum())
                if pc is None:
                    pc = popcount(S)
                if cnt:
                    m = int(pc[ok].min())
                    nm = int((pc[ok] == m).sum())
                else:
                    m = nm = 0
                rows.setdefault(name, []).append((n, cnt, m, nm))
            print(f"  {fam} n={n} |V|={len(g)}", file=sys.stderr)
        for name, r in rows.items():
            out.append({"family": fam, "property": name, "n": [x[0] for x in r],
                        "count": [x[1] for x in r], "min": [x[2] for x in r], "nmin": [x[3] for x in r]})
    return out


if __name__ == "__main__":
    res = run()
    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else "graphsets.json", "w"))
