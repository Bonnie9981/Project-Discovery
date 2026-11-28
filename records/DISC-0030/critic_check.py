"""Critic's independent recheck for the open-locating / ladder batch (third implementation).

Standard library only; imports nothing from the repo. Run from anywhere:
    python records/DISC-0030/critic_check.py

Method (different from check_old.py / strip.py / transfer.py):
  * brute force over all subsets (small n) with bitmask codes;
  * a column DP that stores the S-bits of the last 4 columns and, when a column's
    neighbourhoods are complete, computes the actual codes (N(v)&S, N[v]&S) and
    compares them with every vertex at column distance <= 2.  This is exact because
    two equal NONEMPTY codes share a vertex x of S adjacent to (or equal to) both,
    so the two vertices are at distance <= 2, hence column distance <= 2.
    No "mask" lists, no templates, no Berlekamp-Massey.
  * cycles: the same DP with the first 4 bits kept in the state and the wrap-around
    codes checked at the end.
Kinds: 'old' (open nbhd, every v), 'ld' (open nbhd, only v not in S), 'id' (closed nbhd, every v).
"""
import itertools
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


# ---------- brute force ----------
def brute(adj, kind):
    n = len(adj)
    nb = [sum(1 << u for u in adj[v]) | ((1 << v) if kind == "id" else 0) for v in range(n)]
    tot = 0
    for S in range(1 << n):
        seen = set()
        ok = True
        for v in range(n):
            if kind == "ld" and S >> v & 1:
                continue
            c = nb[v] & S
            if c == 0 or c in seen:
                ok = False
                break
            seen.add(c)
        tot += ok
    return tot


def path_adj(n):
    return [[u for u in (v - 1, v + 1) if 0 <= u < n] for v in range(n)]


def cycle_adj(n):
    return [sorted({(v - 1) % n, (v + 1) % n}) for v in range(n)]


def ladder_adj(n):  # vertex (col j,row r) -> 2j+r
    return [[2 * j + 1 - r] + [2 * d + r for d in (j - 1, j + 1) if 0 <= d < n]
            for j in range(n) for r in range(2)]


# ---------- column DP for strips (w = 1: path, w = 2: ladder) ----------
def strip_count(n, w, kind):
    def nbrs(j, r):
        out = [(d, r) for d in (j - 1, j + 1) if 0 <= d < n]
        if w == 2:
            out.append((j, 1 - r))
        return out

    def code(j, r, bit):
        if kind == "ld" and bit(j, r):
            return None
        pts = nbrs(j, r) + ([(j, r)] if kind == "id" else [])
        return frozenset(p for p in pts if bit(*p))

    states = {(): 1}
    for c in range(n + 1):
        new = {}
        for st, cnt in states.items():
            for b in (range(1 << w) if c < n else [None]):
                win = st + ((b,) if b is not None else ())
                base = c - len(st)

                def bit(j, r, win=win, base=base):
                    return (win[j - base] >> r) & 1

                f = c - 1
                ok = True
                if f >= 0:
                    for r in range(w):
                        a = code(f, r, bit)
                        if a is None:
                            continue
                        if not a:
                            ok = False
                            break
                        others = [(f, s) for s in range(r)] + \
                                 [(j, s) for j in (f - 1, f - 2) if j >= 0 for s in range(w)]
                        for (j, s) in others:
                            o = code(j, s, bit)
                            if o is not None and o == a:
                                ok = False
                                break
                        if not ok:
                            break
                if ok:
                    key = win[-4:] if c < n else ()
                    new[key] = new.get(key, 0) + cnt
        states = new
    return states.get((), 0)


# ---------- cycle DP (OLD), n >= 9 ----------
def cycle_old(n):
    assert n >= 9
    tot = 0
    for pre in itertools.product((0, 1), repeat=4):
        def code_any(v, bits):
            return frozenset(u for u in ((v - 1) % n, (v + 1) % n) if bits[u])
        # prefix checks: vertices 1,2 finalized; compare (1,2) only (distance 1)
        b = dict(enumerate(pre))
        c1, c2 = code_any(1, b), code_any(2, b)
        if not c1 or not c2 or c1 == c2:
            continue
        states = {pre: 1}  # window = bits of the last 4 vertices
        for c in range(4, n):
            new = {}
            for win, cnt in states.items():
                for x in (0, 1):
                    w5 = win + (x,)
                    bb = {c - 4 + i: w5[i] for i in range(5)}
                    j = c - 1
                    a = code_any(j, bb)
                    ok = bool(a)
                    for k in (j - 1, j - 2):
                        if ok and k >= 1 and k - 1 >= c - 4:
                            if code_any(k, bb) == a:
                                ok = False
                        elif ok and k >= 1:  # k-1 is in the prefix
                            bk = dict(bb)
                            bk.update(enumerate(pre))
                            if code_any(k, bk) == a:
                                ok = False
                    if ok:
                        key = w5[1:]
                        new[key] = new.get(key, 0) + cnt
            states = new
        for win, cnt in states.items():
            bb = {n - 4 + i: win[i] for i in range(4)}
            bb.update(enumerate(pre))
            vs = [n - 3, n - 2, n - 1, 0, 1, 2]
            cs = {v: code_any(v, bb) for v in vs}
            if not cs[n - 1] or not cs[0]:
                continue
            bad = False
            for u, v in itertools.combinations(vs, 2):
                d = min((u - v) % n, (v - u) % n)
                if d <= 2 and cs[u] == cs[v]:
                    bad = True
            if not bad:
                tot += cnt
    return tot


# ---------- formulas ----------
def narayana(N):  # A000930, offset 0
    a = [1, 1, 1]
    while len(a) <= N:
        a.append(a[-1] + a[-3])
    return a


def a1609(N):  # A001609, offset 1 (index 0 unused)
    a = [None, 1, 1, 4]
    while len(a) <= N:
        a.append(a[-1] + a[-3])
    return a


def gf_series(s, P, Q, N):
    c = []
    for i in range(N + 1):
        v = (P[i] if i < len(P) else 0) - sum(Q[j] * c[i - j] for j in range(1, min(i, len(Q) - 1) + 1))
        c.append(v)
    return ([0] * s + c)[:N + 1]


LD_GF = (1, [3, 0, 7, 3, -5, -6, 2, -1, 1, 2, -3, 0, 1], [1, -3, 0, -4, -7, 2, 2, -3, 1, 1, -2, 3, 1, -1])
ID_GF = (2, [5, 19, 12, 3, -5, -22, -10, 6, 8], [1, -2, -2, -6, -10, 4, 1, 6, 8, 2, -8])


def read_b(rel):
    d = {}
    with open(os.path.join(ROOT, rel)) as fh:
        for line in fh:
            if line.strip() and not line.startswith("#"):
                k, v = line.split()
                d[int(k)] = int(v)
    return d


def main():
    A = narayana(600)
    L = a1609(600)

    def f_cycle(n):
        if n == 4:
            return 0
        return L[n] if n % 2 else L[n // 2] ** 2

    def f_path(n):
        if n in (1, 3):
            return 0
        if n % 2 == 0:
            return A[n // 2] ** 2
        k = n // 2
        return A[k + 3] * A[k - 2]

    # 1. brute force
    for n in range(3, 19):
        assert brute(cycle_adj(n), "old") == f_cycle(n), ("cycle brute", n)
    for n in range(1, 19):
        assert brute(path_adj(n), "old") == f_path(n), ("path brute", n)
    print("brute: OLD(C_n) n=3..18, OLD(P_n) n=1..18 match formulas")
    ld = gf_series(*LD_GF, 80)
    idc = gf_series(*ID_GF, 80)
    for n in range(1, 9):
        assert brute(ladder_adj(n), "ld") == ld[n], ("ld brute", n)
        assert brute(ladder_adj(n), "id") == idc[n], ("id brute", n)
    print("brute: LD, ID of ladders n=1..8 match g.f.")

    # 2. DPs
    for n in range(9, 41):
        assert cycle_old(n) == f_cycle(n), ("cycle dp", n)
    for n in range(9, 13):
        assert cycle_old(n) == brute(cycle_adj(n), "old")
    for n in range(1, 61):
        assert strip_count(n, 1, "old") == f_path(n), ("path dp", n)
    for n in range(1, 61):
        assert strip_count(n, 2, "ld") == ld[n], ("ld dp", n)
        assert strip_count(n, 2, "id") == idc[n], ("id dp", n)
    for n in range(1, 9):
        assert strip_count(n, 2, "ld") == brute(ladder_adj(n), "ld")
        assert strip_count(n, 2, "id") == brute(ladder_adj(n), "id")
    print("DP: OLD(C_n) n<=40, OLD(P_n) n<=60, LD/ID ladders n<=60 match formulas / g.f.")

    # 3. b-files
    checks = [("results/open-locating-cycle/b_old_cycle.txt", f_cycle),
              ("results/open-locating-path/b_old_path.txt", f_path),
              ("results/ladder-locating/b_ld_ladder.txt", None),
              ("results/ladder-identifying/b_id_ladder.txt", None)]
    ldb = gf_series(*LD_GF, 600)
    idb = gf_series(*ID_GF, 600)
    for rel, f in checks:
        b = read_b(rel)
        keys = sorted(b)
        assert keys == list(range(keys[0], keys[0] + len(keys))), (rel, "gaps")
        g = f if f else (lambda n, rel=rel: (ldb if "locating/" in rel and "ld_" in rel else idb)[n])
        bad = [n for n in keys if b[n] != g(n)]
        print(f"{rel}: n={keys[0]}..{keys[-1]}, mismatches vs independent formula: {bad[:5]}")
        assert not bad
    print("all critic checks passed")


if __name__ == "__main__":
    main()
