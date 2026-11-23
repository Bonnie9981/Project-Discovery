"""DISC-0015: numerical checks for Rule 54 rows from one ON cell (OEIS A118109, A265225).

Method 1: simulate Rule 54 by looking up the bits of 54 (cells -n..n).
Method 2: build rows from the closed form (even row: ON at x = t mod 4; odd row: OFF at x = t+1 mod 4).
Checks the conjectured formulas of A118109 and A265225, the DATA copied from the live entries
(2026-11-23), and Ianakiev's comment in A265225 by brute force over n-subsets.
Usage: python results/A118109/code/l08_rule54_rows.py [N]
"""
import sys
from itertools import combinations

DATA_118109 = [1, 111, 10001, 1110111, 100010001, 11101110111, 1000100010001,
               111011101110111, 10001000100010001, 1110111011101110111,
               100010001000100010001, 11101110111011101110111,
               1000100010001000100010001, 111011101110111011101110111,
               10001000100010001000100010001, 1110111011101110111011101110111]
DATA_265225 = [1, 4, 6, 12, 15, 24, 28, 40, 45, 60, 66, 84, 91, 112, 120, 144, 153, 180, 190,
               220, 231, 264, 276, 312, 325, 364, 378, 420, 435, 480, 496, 544, 561, 612, 630,
               684, 703, 760, 780, 840, 861, 924, 946, 1012, 1035, 1104, 1128, 1200, 1225, 1300,
               1326, 1404, 1431]


def rows_sim(N):
    rows, row = [], [1]
    for n in range(N + 1):
        rows.append(row)
        p = [0, 0] + row + [0, 0]
        row = [(54 >> (4 * p[i - 1] + 2 * p[i] + p[i + 1])) & 1 for i in range(1, len(p) - 1)]
    return rows


def rows_closed(N):
    def on(t, x):
        return int((x - t) % 4 == 0) if t % 2 == 0 else int((x - t - 1) % 4 != 0)
    return [[on(t, x) for x in range(-t, t + 1)] for t in range(N + 1)]


def main(N):
    r1, r2 = rows_sim(N), rows_closed(N)
    assert r1 == r2, "simulation and closed form differ"
    a = [int("".join(map(str, r))) for r in r1]
    tot, s = [], 0
    for r in r1:
        s += sum(r)
        tot.append(s)
    assert a[:len(DATA_118109)] == DATA_118109
    assert tot[:len(DATA_265225)] == DATA_265225
    for n in range(N + 1):
        assert a[n] == (10000 + 1100 * (n % 2)) * 100 ** n // 9999          # Keller
        assert 4 * tot[n] == (n + 1) * (2 * n - (-1) ** n + 5)              # Barker
        assert tot[n] == n + 1 + (n + 1) * ((n + 1) // 2)                    # Hurt
        assert tot[n] == (n + n % 2) * (n + 1) // 2 + n + 1                  # Veselovac
        if n > 3:
            assert a[n] == 10001 * a[n - 2] - 10000 * a[n - 4]               # Barker
        if n > 4:
            assert tot[n] == tot[n-1] + 2*tot[n-2] - 2*tot[n-3] - tot[n-4] + tot[n-5]
    # g.f. checks: multiply series by the denominators and compare with the numerators
    def mul(p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, x in enumerate(p):
            for j, y in enumerate(q):
                out[i + j] += x * y
        return out
    den1 = mul(mul([1, -1], [1, 1]), mul([1, -100], [1, 100]))
    assert mul(a, den1)[:N + 1] == [1, 111] + [0] * (N - 1)
    den2 = mul(mul(mul([1, -1], [1, -1]), mul([1, -1], [1, 1])), [1, 1])
    assert mul(tot, den2)[:N + 1] == [1, 3] + [0] * (N - 1)
    # Ianakiev: min sum of n distinct numbers from 1..2n with n | sum equals a(n-1) (not a(n))
    K = min(11, N + 1)
    for n in range(1, K + 1):
        m = min(t for t in map(sum, combinations(range(1, 2 * n + 1), n)) if t % n == 0)
        assert m == tot[n - 1] and (n == 0 or m != tot[n])
    print(f"OK: 0 <= n <= {N}: simulation = closed form; A118109 and A265225 conjectured formulas, "
          f"recurrences and g.f.s hold; DATA match; Ianakiev min-sum = a(n-1) for 1 <= n <= {K}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 300)
