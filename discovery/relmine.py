"""Relation mining across the offline OEIS (`python -m discovery.relmine`).

Looks for pairs of entries A, B such that, on every overlapping term (at least
--min-overlap of them),

    T(A)(n + r) = k * B(n + s)        k a nonzero rational constant

where T is one of the transforms in TRANSFORMS (identity, bisections,
partial sums, differences, binomial / inverse binomial, Euler / inverse Euler,
Moebius / inverse Moebius, INVERT, square under convolution), and neither
entry's text mentions the other's A-number. Such a pair is only a *lead* (L0):
matching terms prove nothing, the relation may still be known through a third
entry, and every lead must be proved by hand before it is used.

Method: the first terms of every entry are cached; windows of B (divided by
their gcd, sign fixed) are hashed at several start shifts; for every A and
every transform the same is done on T(A) and collisions are re-checked exactly
on the whole overlap.

First draft of the affine/partial-sum search by another thread (2026-11-27);
this version replaces the affine constant by the transform list.
"""
from __future__ import annotations

import argparse
import json
import pickle
import re
import sys
from collections import defaultdict
from fractions import Fraction
from math import comb, gcd
from pathlib import Path

from discovery.oeisdb import SRC

LINE = re.compile(r"^%(\w) (A\d{6}) ?(.*)$")
ANUM = re.compile(r"A\d{6}")
SKIP_KW = {"dead", "dumb", "cons", "frac", "word", "uned", "probation",
           "allocated", "recycled", "base"}
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "relmine"
CACHE = OUT / "terms.pkl"
MAXT = 80   # terms kept per entry
WIN = 14    # hashed window length


# ---------------------------------------------------------------- loading
def parse(text: str):
    data, refs, kw, off, name, anum = "", set(), set(), 0, "", None
    for raw in text.splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        tag, a, body = m.groups()
        anum = anum or a
        if tag in "STU":
            data += body.strip()
            continue
        if tag == "K":
            kw = set(body.replace(",", " ").split())
        elif tag == "O":
            try:
                off = int(body.split(",")[0])
            except ValueError:
                pass
        elif tag == "N":
            name = body
        refs.update(ANUM.findall(body))
    if not anum or kw & SKIP_KW:
        return None
    try:
        terms = [int(x) for x in data.strip(",").split(",") if x]
    except ValueError:
        return None
    refs.discard(anum)
    return anum, terms[:MAXT], off, refs, name


def load(src: Path = SRC, cache: Path = CACHE, rebuild: bool = False):
    if cache.exists() and not rebuild:
        return pickle.loads(cache.read_bytes())
    seqs = {}
    for i, f in enumerate(sorted((src / "seq").glob("A*/A*.seq"))):
        r = parse(f.read_text(encoding="utf-8", errors="replace"))
        if r and len(r[1]) >= 20:
            seqs[r[0]] = r[1:]
        if i % 50000 == 0:
            print(f"  read {i}", file=sys.stderr)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(pickle.dumps(seqs, protocol=pickle.HIGHEST_PROTOCOL))
    return seqs


# ------------------------------------------------------------- transforms
def psum(a):
    s, out = 0, []
    for x in a:
        s += x
        out.append(s)
    return out


def diff(a):
    return [y - x for x, y in zip(a, a[1:])]


def binom(a):
    return [sum(comb(n, k) * a[k] for k in range(n + 1)) for n in range(len(a))]


def invbinom(a):
    return [sum((-1) ** (n - k) * comb(n, k) * a[k] for k in range(n + 1)) for n in range(len(a))]


def euler(a):
    """a = a(1), a(2), ...; returns b(1), b(2), ... of prod (1-x^n)^(-a(n)) (b(0)=1 dropped)."""
    n = len(a)
    c = [0] * (n + 1)
    for i in range(1, n + 1):
        c[i] = sum(d * a[d - 1] for d in range(1, i + 1) if i % d == 0)
    b = [1] + [0] * n
    for i in range(1, n + 1):
        b[i] = sum(c[k] * b[i - k] for k in range(1, i + 1))
        if b[i] % i:
            return []
        b[i] //= i
    return b[1:]


def inveuler(b):
    """Inverse of euler(): b = b(1), b(2), ... -> a(1), a(2), ..."""
    n = len(b)
    bb = [1] + list(b)
    c = [0] * (n + 1)
    for i in range(1, n + 1):
        c[i] = i * bb[i] - sum(c[k] * bb[i - k] for k in range(1, i))
    a = []
    for i in range(1, n + 1):
        s = sum(mob(i // d) * c[d] for d in range(1, i + 1) if i % d == 0)
        if s % i:
            return []
        a.append(s // i)
    return a


_MU = {}


def mob(n):
    if n not in _MU:
        m, k, r = n, 2, 1
        while k * k <= m:
            if m % k == 0:
                m //= k
                if m % k == 0:
                    _MU[n] = 0
                    return 0
                r = -r
            k += 1
        _MU[n] = -r if m > 1 else r
    return _MU[n]


def mobius(a):
    """b(n) = sum_{d|n} mu(n/d) a(d), a indexed from 1."""
    return [sum(mob(n // d) * a[d - 1] for d in range(1, n + 1) if n % d == 0)
            for n in range(1, len(a) + 1)]


def invmobius(a):
    return [sum(a[d - 1] for d in range(1, n + 1) if n % d == 0) for n in range(1, len(a) + 1)]


def invert(a):
    """1/(1 - x A(x)) with A(x) = sum a[i] x^i: b(n) = sum_{k=1..n} a[k-1] b(n-k)."""
    b = [1]
    for n in range(1, len(a) + 1):
        b.append(sum(a[k - 1] * b[n - k] for k in range(1, n + 1)))
    return b[1:]


def square(a):
    return [sum(a[i] * a[n - i] for i in range(n + 1)) for n in range(len(a))]


TRANSFORMS = {
    "id": lambda a: a,
    "bisect0": lambda a: a[0::2],
    "bisect1": lambda a: a[1::2],
    "psum": psum,
    "diff": diff,
    "binom": binom,
    "invbinom": invbinom,
    "euler": euler,
    "euler1": lambda a: euler(a[1:]),
    "inveuler": inveuler,
    "mobius": mobius,
    "invmobius": invmobius,
    "invert": invert,
    "square": square,
}


# ---------------------------------------------------------------- hashing
def key(w):
    """Window -> scalar normal form (divide by gcd, first nonzero positive) or None if poor."""
    g = 0
    for x in w:
        g = gcd(g, x)
    if g == 0:
        return None
    w = [x // g for x in w]
    if len(set(w)) < 8 or max(abs(x) for x in w) < 50:
        return None
    for x in w:
        if x:
            if x < 0:
                w = [-y for y in w]
            break
    return hash(tuple(w))


def scalar_fit(x, y):
    """k with x = k*y termwise, else None."""
    k = None
    for p, q in zip(x, y):
        if q == 0:
            if p != 0:
                return None
            continue
        f = Fraction(p, q)
        if k is None:
            k = f
        elif f != k:
            return None
    return k


def mine(seqs, transforms=None, shifts=4, rshifts=3, min_overlap=20, max_bucket=8):
    transforms = transforms or list(TRANSFORMS)
    idx = defaultdict(list)
    for b, (terms, off, refs, name) in seqs.items():
        for s in range(shifts + 1):
            w = terms[s:s + WIN]
            if len(w) == WIN:
                h = key(w)
                if h is not None:
                    idx[h].append((b, s))
    print(f"  index: {len(idx)} keys", file=sys.stderr)
    leads, seen = [], set()
    for n, (a, (terms, off, refs, name)) in enumerate(seqs.items()):
        for tn in transforms:
            try:
                t = TRANSFORMS[tn](terms)
            except (ZeroDivisionError, OverflowError):
                continue
            for r in range(rshifts):
                w = t[r:r + WIN]
                if len(w) < WIN:
                    break
                h = key(w)
                if h is None:
                    continue
                hits = idx.get(h, ())
                if len(hits) > max_bucket:
                    continue
                for b, s in hits:
                    if b == a or (a, b, tn, r - s) in seen:
                        continue
                    seen.add((a, b, tn, r - s))
                    lead = check(seqs, a, b, tn, t, r, s, min_overlap)
                    if lead:
                        leads.append(lead)
        if n % 50000 == 0:
            print(f"  mined {n}, leads {len(leads)}", file=sys.stderr)
    return leads


def check(seqs, a, b, tn, t, r, s, min_overlap):
    ta, oa, ra, na = seqs[a]
    tb, ob, rb, nb = seqs[b]
    if tn == "id" and r == s:
        # same index alignment: plain duplicates / scalar multiples; keep, flagged
        pass
    x, y = t[r:], tb[s:]
    m = min(len(x), len(y))
    if m < min_overlap:
        return None
    k = scalar_fit(x[:m], y[:m])
    if k is None:
        return None
    return {"a": a, "b": b, "transform": tn, "k": str(k),
            "r": r, "s": s, "offset_a": oa, "offset_b": ob, "overlap": m,
            "known": b in ra or a in rb, "name_a": na, "name_b": nb}


def cfinite_order(a, maxord=12):
    """Smallest order d <= maxord of a constant-coefficient linear recurrence that fits
    every term (Berlekamp-Massey over Q, checked on >= 2d+8 terms), else None."""
    a = [Fraction(x) for x in a]
    n = len(a)
    C, B, L, m, bb = [Fraction(1)], [Fraction(1)], 0, 1, Fraction(1)
    for i in range(n):
        d = a[i] + sum(C[j] * a[i - j] for j in range(1, L + 1))
        if d == 0:
            m += 1
            continue
        T = C[:]
        coef = d / bb
        C = C + [Fraction(0)] * (len(B) + m - len(C))
        for j, x in enumerate(B):
            C[j + m] -= coef * x
        if 2 * L <= i:
            L, B, bb, m = i + 1 - L, T, d, 1
        else:
            m += 1
    if L <= maxord and n >= 2 * L + 8:
        return L
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--min-overlap", type=int, default=20)
    ap.add_argument("--transforms", default="", help="comma list; default all")
    ap.add_argument("--rebuild", action="store_true", help="re-read the .seq files")
    ap.add_argument("--out", default=str(OUT / "leads.jsonl"))
    args = ap.parse_args(argv)
    seqs = load(rebuild=args.rebuild)
    print(f"  {len(seqs)} entries", file=sys.stderr)
    tr = [x for x in args.transforms.split(",") if x] or None
    leads = mine(seqs, tr, min_overlap=args.min_overlap)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        for lead in leads:
            f.write(json.dumps(lead, ensure_ascii=False) + "\n")
    unk = [x for x in leads if not x["known"]]
    print(f"{len(leads)} relations, {len(unk)} with no direct cross-reference -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
