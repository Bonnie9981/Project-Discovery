"""Ladder P_2 x P_n: locating-dominating sets and identifying codes.

Run from the repo root: python results/ladder-locating/code/check_ladder.py   (about 20 seconds)

1. brute force from the definitions (standard library only) for n <= 9;
2. the window DP of discovery/newseq/transfer.py for n <= 15;
3. the certified column transfer matrix of discovery/newseq/strip.py (vector identity);
all compared with the generating functions of paper/open-locating-and-ladders.md, Theorems 3-4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from discovery.newseq import strip as ST, transfer as T  # noqa: E402

GF = {  # numerator, denominator coefficient lists (constant term first); g.f. = x^s * P / Q
    "locating_dominating": (1, [3, 0, 7, 3, -5, -6, 2, -1, 1, 2, -3, 0, 1],
                            [1, -3, 0, -4, -7, 2, 2, -3, 1, 1, -2, 3, 1, -1]),
    "identifying_code": (2, [5, 19, 12, 3, -5, -22, -10, 6, 8],
                         [1, -2, -2, -6, -10, 4, 1, 6, 8, 2, -8]),
}


def series(s, P, Q, N):
    """Coefficients a(1..N) of x^s P/Q."""
    c = [0] * (N + 1)
    for i in range(N + 1 - s):
        v = (P[i] if i < len(P) else 0) - sum(Q[j] * c[i - j] for j in range(1, min(i, len(Q) - 1) + 1))
        c[i] = v  # Q[0] = 1
    return [0] * s + c[:N + 1 - s]


def ladder(n):
    return [{2 * c + 1 - r} | {2 * d + r for d in (c - 1, c + 1) if 0 <= d < n}
            for c in range(n) for r in range(2)]


def is_ld(adj, S):
    seen = set()
    for v in range(len(adj)):
        if v in S:
            continue
        t = frozenset(adj[v] & S)
        if not t or t in seen:
            return False
        seen.add(t)
    return True


def is_id(adj, S):
    seen = set()
    for v in range(len(adj)):
        t = frozenset((adj[v] | {v}) & S)
        if not t or t in seen:
            return False
        seen.add(t)
    return True


if __name__ == "__main__":
    for prop, test in (("locating_dominating", is_ld), ("identifying_code", is_id)):
        s, P, Q = GF[prop]
        a = series(s, P, Q, 60)  # a[n] for n = 0..60
        for n in range(1, 10):
            adj = ladder(n)
            b = sum(test(adj, {i for i in range(2 * n) if m >> i & 1}) for m in range(1 << (2 * n)))
            assert b == a[n], (prop, "brute", n, b, a[n])
        S = ST.Strip("ladder", prop)
        for n in range(1, 16):
            assert T.stats(ST.ladder(n), prop, S.nb)[0] == a[n], (prop, "window DP", n)
        coef, nfrom, counts, _ = ST.certify("ladder", prop, nterms=40)
        assert all(counts[n] == a[n] for n in counts), (prop, "column DP")
        assert coef == [-q for q in Q[1:]], (prop, "certified recurrence differs from Q")
        print(f"{prop}: brute n<=9, window DP n<=15, column DP n<={max(counts)} agree; "
              f"recurrence certified for n >= {nfrom}; a(1..10) = {a[1:11]}")
    print("all checks passed")
