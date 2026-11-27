"""Transfer-matrix counting of hitting-set families on banded graphs.

Every property in graphsets that we prove things about is "S meets every mask
in a list" (domination: N[v]; identifying: N[u] xor N[v]; ...). On a graph whose
vertices 0..n-1 can be ordered so that every needed mask lies in a window of W
consecutive vertices (paths, ladders, path powers) or in such a window modulo n
(cycles, prisms), the number of such S, refined by |S|, is computed by a DP
that remembers only the last W bits (plus, for wrap-around masks, the first W
bits). This is implementation B; graphsets.py (brute force) is implementation A.
"""
from __future__ import annotations

import itertools
from fractions import Fraction



def masks_for(g, prop):
    n = len(g)
    opn = [frozenset(g[v]) for v in range(n)]
    cl = [opn[v] | {v} for v in range(n)]
    pairs = list(itertools.combinations(range(n), 2))
    if prop == "dominating":
        M = cl
    elif prop == "total_dominating":
        M = opn
    elif prop == "identifying_code":
        M = cl + [cl[u] ^ cl[v] for u, v in pairs]
    elif prop == "locating_dominating":
        M = cl + [(cl[u] ^ cl[v]) | {u, v} for u, v in pairs]
    elif prop == "open_locating":
        M = opn + [opn[u] ^ opn[v] for u, v in pairs]
    else:
        raise ValueError(prop)
    M = set(M)
    if frozenset() in M:
        return None  # impossible
    # keep only minimal masks
    return [m for m in M if not any(o < m for o in M)]


def count_by_size(g, prop, W):
    """dict size -> number of S of that size satisfying prop (DP, window W)."""
    n = len(g)
    M = masks_for(g, prop)
    if M is None:
        return {}
    at = [[] for _ in range(n)]
    wrap = []
    for m in M:
        lo, hi = min(m), max(m)
        if hi - lo < W:
            at[hi].append(m)
        else:
            assert all(x < W or x >= n - W for x in m), (m, W)
            wrap.append(m)
    assert n >= 2 * W or not wrap
    # state: (prefix bits of first min(W,n) vertices as int, last W bits as int) -> {size: count}
    st = {(0, 0): {0: 1}}
    for t in range(n):
        new = {}
        for (pre, last), sizes in st.items():
            for b in (0, 1):
                l2 = ((last << 1) | b) & ((1 << W) - 1)
                p2 = pre | (b << t) if t < W else pre
                # bit of vertex x (t-W < x <= t) is (l2 >> (t-x)) & 1
                if not all(any((l2 >> (t - x)) & 1 for x in m) for m in at[t]):
                    continue
                if t == n - 1 and wrap:
                    def bit(x):
                        return (p2 >> x) & 1 if x < W else (l2 >> (t - x)) & 1
                    if not all(any(bit(x) for x in m) for m in wrap):
                        continue
                key = (p2 if wrap_needed(n, W, M) else 0, l2)
                d = new.setdefault(key, {})
                for s, c in sizes.items():
                    d[s + b] = d.get(s + b, 0) + c
        st = new
    tot = {}
    for sizes in st.values():
        for s, c in sizes.items():
            tot[s] = tot.get(s, 0) + c
    return tot


def wrap_needed(n, W, M):
    return any(max(m) - min(m) >= W for m in M)


def stats(g, prop, W):
    d = count_by_size(g, prop, W)
    if not d:
        return 0, 0, 0
    m = min(d)
    return sum(d.values()), m, d[m]


def berlekamp_massey(seq):
    """Minimal linear recurrence over Q: returns c with a(n) = sum c[i] a(n-1-i)."""
    s = [Fraction(x) for x in seq]
    C, B = [Fraction(1)], [Fraction(1)]
    L, m, b = 0, 1, Fraction(1)
    for n in range(len(s)):
        d = s[n] + sum(C[i] * s[n - i] for i in range(1, L + 1))
        if d == 0:
            m += 1
            continue
        T = C[:]
        coef = d / b
        C = C + [Fraction(0)] * (len(B) + m - len(C))
        for i in range(len(B)):
            C[i + m] -= coef * B[i]
        if 2 * L <= n:
            L, B, b, m = n + 1 - L, T, d, 1
        else:
            m += 1
    return [-x for x in C[1:L + 1]]
