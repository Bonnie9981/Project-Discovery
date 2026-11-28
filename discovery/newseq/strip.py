"""Certified transfer-matrix counts on strips P_n x H (ladders, 3 x n grids, ...).

A strip graph has columns 0..n-1, each with the same w vertices (index c*w + r),
and edges only between columns at distance <= 1, the same in every column.
A hitting property (see transfer.masks_for) is "S meets every mask". Away from
both ends the masks are translates of a fixed finite set (the interior masks).

The DP processes columns left to right with state = bits of the last K columns.
For t >= t0 the step V_t -> V_{t+1} is one fixed linear map M (interior masks
only), so V_t = M^(t-t0) V_{t0}. The count for size n is a fixed linear
function of V_{n-1-c} (the last c columns are finished with the right-end
masks). Hence, if the vector identity  V_{k+r} = sum_i coef_i V_{k+r-i}
holds for ONE k >= t0, it holds for all later k (apply M), and the counts obey
the same recurrence from n = k + r + 1 + c on. `certify` checks exactly that.
"""
from __future__ import annotations

from discovery.newseq.transfer import berlekamp_massey, masks_for


def ladder(n):
    """P_2 x P_n, vertex c*2 + r."""
    g = {}
    for c in range(n):
        for r in range(2):
            v = 2 * c + r
            g[v] = {2 * c + 1 - r} | {2 * d + r for d in (c - 1, c + 1) if 0 <= d < n}
    return g


def grid3(n):
    """P_3 x P_n, vertex c*3 + r."""
    g = {}
    for c in range(n):
        for r in range(3):
            g[3 * c + r] = ({3 * c + s for s in (r - 1, r + 1) if 0 <= s < 3}
                            | {3 * d + r for d in (c - 1, c + 1) if 0 <= d < n})
    return g


STRIPS = {"ladder": (ladder, 2), "grid3": (grid3, 3)}


def _cols(m, w):
    return {x // w for x in m}


def setup(family, prop, nbig=40):
    """Interior mask templates (relative to their max column), K, and end sizes."""
    f, w = STRIPS[family]
    M = masks_for(f(nbig), prop)
    span = max(max(_cols(m, w)) - min(_cols(m, w)) for m in M)
    K = span + 1
    mid = nbig // 2
    tmpl = sorted({tuple(sorted((x // w - mid) * w + x % w for x in m)) for m in M
                   if max(_cols(m, w)) == mid})
    # a mask is "interior" if it equals a translate of a template
    def is_interior(m, n):
        hi = max(_cols(m, w))
        return tuple(sorted((x // w - hi) * w + x % w for x in m)) in tmpl_set
    tmpl_set = set(tmpl)
    # how many columns at each end carry non-template masks
    lo_c = max([max(_cols(m, w)) for m in M if not is_interior(m, nbig) and min(_cols(m, w)) < mid] + [-1]) + 1
    hi_c = nbig - min([max(_cols(m, w)) for m in M if not is_interior(m, nbig) and max(_cols(m, w)) >= mid] + [nbig])
    return f, w, K, tmpl, lo_c, hi_c


class Strip:
    def __init__(self, family, prop):
        self.f, self.w, self.K, self.tmpl, self.lo, self.hi = setup(family, prop)
        self.prop = prop
        self.nb = self.w * self.K  # state bits: last K columns

    def _step(self, V, masks_at):
        """Append one column; masks_at: list of masks (as relative offsets, 0 = new column's
        first vertex at bit 0 of the newest column)."""
        w, nb = self.w, self.nb
        out = {}
        for st, c in V.items():
            for col in range(1 << w):
                s2 = ((st << w) | col) & ((1 << nb) - 1)
                ok = True
                for m in masks_at:
                    # offset o = (dc)*w + r with dc <= 0; bit position = (-dc)*w + r
                    if not any((s2 >> ((-(o // w)) * w + o % w)) & 1 for o in m):
                        ok = False
                        break
                if ok:
                    out[s2] = out.get(s2, 0) + c
        return out

    def interior_vectors(self, T):
        """V_t for t = 0..T-1 using the actual left-end masks then templates."""
        w = self.w
        g = self.f(T + self.hi + 2 * self.K + 5)
        M = masks_for(g, self.prop)
        by = {}
        for m in M:
            hi = max(x // w for x in m)
            by.setdefault(hi, []).append(m)
        V, out = {0: 1}, []
        for t in range(T):
            rel = [tuple((x // w - t) * w + x % w for x in m) for m in by.get(t, [])]
            V = self._step(V, rel)
            out.append(V)
        return out

    def count(self, n, V=None):
        """Exact count for size n (n >= lo + hi + K), finishing with the right-end masks."""
        w = self.w
        g = self.f(n)
        M = masks_for(g, self.prop)
        by = {}
        for m in M:
            by.setdefault(max(x // w for x in m), []).append(m)
        start = n - self.hi - self.K
        if V is None:
            V = self.interior_vectors(start)[-1] if start > 0 else {0: 1}
        for t in range(max(start, 0), n):
            rel = [tuple((x // w - t) * w + x % w for x in m) for m in by.get(t, [])]
            V = self._step(V, rel)
        return sum(V.values())


def certify(family, prop, nterms=80, t0=None):
    """Return (coef, n_from, first terms) after checking the vector identity once."""
    S = Strip(family, prop)
    t0 = t0 if t0 is not None else S.lo + S.K
    # the step must be the fixed interior map from t0 on: every template is checked at t0
    big = S.f(t0 + S.hi + 2 * S.K + 10)
    at_t0 = {tuple(sorted((x // S.w - t0) * S.w + x % S.w for x in m)) for m in masks_for(big, S.prop)
             if max(x // S.w for x in m) == t0}
    assert at_t0 == set(S.tmpl), "t0 is not yet in the interior"
    Vs = S.interior_vectors(nterms + S.hi + 2 * S.K + 5)
    nmin = S.lo + S.hi + 2 * S.K
    counts = {n: S.count(n, Vs[n - S.hi - S.K - 1]) for n in range(nmin, nmin + nterms)}
    seq = [counts[n] for n in sorted(counts)]
    coef = berlekamp_massey(seq)
    r = len(coef)
    assert 2 * r + 4 < len(seq), "not enough terms for this order"
    k = t0
    keys = set(Vs[k + r])
    for i in range(r):
        keys |= set(Vs[k + r - 1 - i])
    for s in keys:
        lhs = Vs[k + r].get(s, 0)
        rhs = sum(coef[i] * Vs[k + r - 1 - i].get(s, 0) for i in range(r))
        if lhs != rhs:
            return None
    # V_t identity for t >= t0 + r  ==> counts identity for n with n - hi - K - 1 >= t0 + r
    return [int(c) if c.denominator == 1 else c for c in coef], t0 + r + S.hi + S.K + 1, counts, S
