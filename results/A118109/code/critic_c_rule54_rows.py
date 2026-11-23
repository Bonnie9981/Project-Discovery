"""DISC-0015 critic: independent re-check of Rule 54 rows (A118109, A265225).

Written without reading l08's code paths into it (no imports from the repo).
Different methods from l08_rule54_rows.py:
- rows as Python big-int bitsets: new = c XOR ((c << 1) | (c >> 1)) (no rule-table lookup,
  no closed form);
- A118109 value computed arithmetically (sum of 10^i over ON bits), not by string join;
- formulas checked with exact integer arithmetic; g.f.s checked by power-series *division*
  (expanding numerator/denominator), not by multiplying the series by the denominator;
- Ianakiev's min-sum checked by a dynamic programme (min sum by count and residue), which
  reaches much larger n than enumerating subsets; both index readings a(n-1) and a(n) tested,
  plus the shifted reading "n+1 numbers from 1..2n+2".
Usage: python results/A118109/code/critic_c_rule54_rows.py [N] [M]
"""
import sys


def rows_bits(N):
    """Row t as an int; bit i <-> cell x = i - t ... normalised so bit 0 is the leftmost cell -t."""
    out, c = [], 1  # cell 0 at bit 0 of a width-1 row
    for t in range(N + 1):
        out.append(c)
        c <<= 1  # widen: now row t occupies bits 1..2t+1, new row will use bits 0..2t+2
        c = c ^ ((c << 1) | (c >> 1))
    return out


def value_dec(c, width):
    # bit 0 = leftmost cell -> most significant decimal digit
    v = 0
    for i in range(width):
        if (c >> i) & 1:
            v += 10 ** (width - 1 - i)
    return v


def series_div(num, den, n_terms):
    """Coefficients of num/den as a power series (den[0] = 1)."""
    assert den[0] == 1
    q = []
    r = list(num) + [0] * n_terms
    for k in range(n_terms):
        c = r[k]
        q.append(c)
        for j in range(1, len(den)):
            if k + j < len(r):
                r[k + j] -= c * den[j]
    return q


def poly(*factors):
    p = [1]
    for f in factors:
        out = [0] * (len(p) + len(f) - 1)
        for i, x in enumerate(p):
            for j, y in enumerate(f):
                out[i + j] += x * y
        p = out
    return p


def min_divisible_sum(k, top, mod):
    """Min sum of k distinct numbers from 1..top whose sum is divisible by mod (DP)."""
    INF = float("inf")
    dp = [[INF] * mod for _ in range(k + 1)]
    dp[0][0] = 0
    for v in range(1, top + 1):
        for c in range(min(k, v), 0, -1):
            prev = dp[c - 1]
            cur = dp[c]
            for r in range(mod):
                if prev[r] != INF:
                    s = prev[r] + v
                    rr = (r + v) % mod
                    if s < cur[rr]:
                        cur[rr] = s
    return dp[k][0]


def main(N, M):
    rows = rows_bits(N)
    a, tot, s = [], [], 0
    for t, c in enumerate(rows):
        w = 2 * t + 1
        assert c >> w == 0, "row wider than light cone"
        assert c & 1, "leftmost cell -t should be ON"
        a.append(value_dec(c, w))
        s += bin(c).count("1")
        tot.append(s)
    # spot values (hand-computed from the rule: 1, 111, 10001, 1110111)
    assert a[:4] == [1, 111, 10001, 1110111]
    assert tot[:5] == [1, 4, 6, 12, 15]
    for n in range(N + 1):
        assert 9999 * a[n] <= (10000 + 1100 * (n % 2)) * 100 ** n < 9999 * (a[n] + 1)  # Keller
        assert 4 * tot[n] == (n + 1) * (2 * n - (-1) ** n + 5)                          # Barker
        assert tot[n] == n + 1 + (n + 1) * ((n + 1) // 2)                               # Hurt
        assert tot[n] == (n + n % 2) * (n + 1) // 2 + n + 1                             # Veselovac
        if n >= 4:
            assert a[n] + 10000 * a[n - 4] == 10001 * a[n - 2]
        if n >= 5:
            assert tot[n] - tot[n - 1] - 2 * tot[n - 2] + 2 * tot[n - 3] + tot[n - 4] - tot[n - 5] == 0
    g1 = series_div([1, 111], poly([1, -1], [1, 1], [1, -100], [1, 100]), N + 1)
    g2 = series_div([1, 3], poly([1, -1], [1, -1], [1, -1], [1, 1], [1, 1]), N + 1)
    assert g1 == a and g2 == tot
    # Ianakiev
    n_minus_1 = n_same = 0
    for n in range(1, M + 1):
        m = min_divisible_sum(n, 2 * n, n)
        if m == tot[n - 1]:
            n_minus_1 += 1
        if m == tot[n]:
            n_same += 1
        # shifted reading: n+1 numbers from 1..2n+2, divisible by n+1  -> a(n)
        assert min_divisible_sum(n + 1, 2 * n + 2, n + 1) == tot[n]
    assert n_minus_1 == M and n_same == 0
    print(f"OK critic_c: 0 <= n <= {N} bitset rows give all A118109/A265225 formulas and g.f.s; "
          f"Ianakiev min-sum(n of 1..2n) = a(n-1) for 1 <= n <= {M}, never a(n); "
          f"'n+1 of 1..2n+2' reading gives a(n)")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    assert M + 1 <= N
    main(N, M)
