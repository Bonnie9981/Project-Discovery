"""DISC-0014: numerical checks for the FORMULA a(2n) = a(n) + 2n of OEIS A071052.

A071052(n) = number of 0's among the 2n+1 cells of row n of the Rule 150 triangle (A071036).
Method 1: simulate Rule 150 on a list (cells -n..n) from one ON cell.
Method 2: coefficients of (1+x+x^2)^n over GF(2), as an integer bit mask (carry-less product).
Usage: python research/r003/l07_a071052_even.py [N]
"""
import sys

DATA = [0,0,2,2,6,2,8,4,14,10,12,8,20,12,18,10,30,26,28,24,32,16,30,14,44,36,
        38,30,46,26,40,20,62,58,60,56,64,48,62,46,72,56,58,42,74,46,60,32,92,
        84,86,78,90,62,84,56,102,82,84,64,100,60,82,42,126,122,124]


def zeros_ca(N):
    out, row = [], [1]
    for n in range(N + 1):
        out.append(row.count(0))
        p = [0, 0] + row + [0, 0]
        row = [p[i - 1] ^ p[i] ^ p[i + 1] for i in range(1, len(p) - 1)]
    return out


def zeros_poly(N):
    out, m = [], 1
    for n in range(N + 1):
        out.append(2 * n + 1 - bin(m).count("1"))
        a, b, r = m, 0b111, 0
        while b:
            if b & 1:
                r ^= a
            a <<= 1
            b >>= 1
        m = r
    return out


def rows_ca(N):
    rows, row = [], [1]
    for n in range(N + 1):
        rows.append(row)
        p = [0, 0] + row + [0, 0]
        row = [p[i - 1] ^ p[i] ^ p[i + 1] for i in range(1, len(p) - 1)]
    return rows


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    z1, z2 = zeros_ca(N), zeros_poly(N)
    assert z1 == z2, "methods disagree"
    assert z1[:len(DATA)] == DATA, "DATA mismatch"
    rows = rows_ca(N)
    for n in range(N // 2 + 1):
        assert z1[2 * n] == z1[n] + 2 * n, n
        # H1 cell by cell: list index k <-> position k - n
        assert rows[2 * n][0::2] == rows[n] and not any(rows[2 * n][1::2]), n
    print(f"OK: 0 <= n <= {N // 2}: a(2n) = a(n) + 2n; cell-by-cell doubling holds; two methods agree to n = {N}; "
          f"{len(DATA)} DATA terms match")


if __name__ == "__main__":
    main()
