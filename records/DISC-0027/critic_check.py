"""DISC-0027 critic: third independent check (standard library only, no repo imports).

Algorithm (different from A = 2^n bitmask brute force and B = window DP / transfer matrix):
recursive enumeration of 0/1 assignments vertex by vertex, pruning only on domination of
vertices whose neighbourhood is already fully decided, then a dict-based full check at the
leaves straight from the definitions (keys = frozenset of neighbours/closed nbhd in S).
Also: series expansion of the claimed g.f.s by exact long division, an independent
characteristic polynomial (Faddeev-LeVerrier over Fractions) of a transfer matrix built
here from the definition of identifying code via sliding windows, and b-file checks.

Usage: python records/DISC-0027/critic_check.py [NMAX]   (default 20)
"""
import sys
from fractions import Fraction
from pathlib import Path


def nbrs(n, cyc):
    adj = {v: set() for v in range(n)}
    for v in range(n - 1):
        adj[v].add(v + 1); adj[v + 1].add(v)
    if cyc and n >= 3:
        adj[0].add(n - 1); adj[n - 1].add(0)
    return adj


def is_ld(S, adj):
    seen = {}
    for v in adj:
        if v in S:
            continue
        key = frozenset(adj[v] & S)
        if not key or key in seen:
            return False
        seen[key] = v
    return True


def is_id(S, adj):
    seen = {}
    for v in adj:
        key = frozenset((adj[v] | {v}) & S)
        if not key or key in seen:
            return False
        seen[key] = v
    return True


def count(n, cyc, kind):
    adj = nbrs(n, cyc)
    check = is_ld if kind == "ld" else is_id
    closed = kind == "id"
    S = set()
    total = 0

    def dominated(v):
        if closed and v in S:
            return True
        if not closed and v in S:
            return True
        return bool(adj[v] & S)

    def rec(i):
        nonlocal total
        if i == n:
            total += check(S, adj)
            return
        for bit in (0, 1):
            if bit:
                S.add(i)
            # vertex i-1 has all neighbours decided once i is decided (except wrap vertex 0 on cycle)
            ok = True
            j = i - 1
            if j >= 1 or (j == 0 and not cyc):
                ok = dominated(j)
            if ok:
                rec(i + 1)
            if bit:
                S.discard(i)

    rec(0)
    return total


def series(num, den, N):
    """coefficients c[0..N] of num/den, den[0] == 1, integer lists (index = power)."""
    c = []
    for k in range(N + 1):
        s = num[k] if k < len(num) else 0
        for j in range(1, min(k, len(den) - 1) + 1):
            s -= den[j] * c[k - j]
        c.append(s)
    return c


GF_LD_P = ([0, 1, 2, 0, 2, 1], [1, -1, -1, 0, -1, -1])
GF_A001642 = ([0, 1, 2, 0, 4, 5], [1, -1, -1, 0, -1, -1])
GF_ID_P = ([0, 1, -1, 1, 2, 1, -1, -1], [1, -1, -1, 1, -1, -1, 0, 1])


def id_matrix():
    """8 states = last three letters; transition abc -> bcd allowed iff the 4-window abcd
    is consistent with the definition for an interior window: no 000 and (a or d)."""
    states = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    M = [[0] * 8 for _ in range(8)]
    for i, (a, b, c) in enumerate(states):
        for d in (0, 1):
            w = (a, b, c, d)
            if (b, c, d) == (0, 0, 0) or (a == 0 and d == 0):
                continue
            M[i][states.index((b, c, d))] = 1
    return M


def charpoly(M):
    """Faddeev-LeVerrier: coefficients of det(xI - M), highest power first."""
    n = len(M)
    I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    A = [[Fraction(x) for x in row] for row in M]
    coeffs = [Fraction(1)]
    Mk = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        Mk = [[sum(A[i][t] * Mk[t][j] for t in range(n)) + coeffs[-1] * I[i][j]
               for j in range(n)] for i in range(n)]
        AM = [[sum(A[i][t] * Mk[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        ck = -sum(AM[i][i] for i in range(n)) / k
        coeffs.append(ck)
    return [int(c) for c in coeffs]


def read_bfile(p):
    out = {}
    for line in Path(p).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        a, b = line.split()
        out[int(a)] = int(b)
    return out


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    ld_p = series(*GF_LD_P, 600)
    a1642 = series(*GF_A001642, 600)
    id_p = series(*GF_ID_P, 600)
    bad = []
    print("n  LD(P) gf | LD(C) A001642 | ID(P) gf | ID(C)")
    for n in range(1, N + 1):
        lp = count(n, False, "ld"); ip = count(n, False, "id")
        lc = count(n, True, "ld") if n >= 3 else None
        ic = count(n, True, "id") if n >= 3 else None
        print(n, lp, ld_p[n], "|", lc, a1642[n], "|", ip, id_p[n], "|", ic)
        if lp != ld_p[n]:
            bad.append(("LD_P", n))
        if ip != id_p[n]:
            bad.append(("ID_P", n))
        if n >= 5 and lc != a1642[n]:
            bad.append(("LD_C", n))
    print("mismatches:", bad)
    print("charpoly(M) high->low:", charpoly(id_matrix()))
    root = Path(__file__).resolve().parents[2]
    for name, seq in (("results/locating-dominating-path/b_ld_path.txt", ld_p),
                      ("results/identifying-code-path/b_id_path.txt", id_p)):
        bf = read_bfile(root / name)
        diff = [k for k in bf if bf[k] != seq[k]]
        print(name, "terms", min(bf), "..", max(bf), "mismatches", diff[:5])


if __name__ == "__main__":
    main()
