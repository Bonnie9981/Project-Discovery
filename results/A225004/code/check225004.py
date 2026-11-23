"""DISC-0024: numeric check of A225004 and A340896 (largest multiple of n with fewer than 2*d(n) divisors).

Brute force: for n <= N, scan every multiple k*n with k <= n^2 (far past the claimed bound k | n),
keep the largest with d(k*n) < 2*d(n).  Check it equals n * max{m | n : d(n*m) < 2 d(n)},
that it divides n^2, and that it matches the OEIS DATA line.
Run: python3 check225004.py [N]   (default 150)
"""
import sys

DATA = [1, 4, 9, 16, 25, 18, 49, 64, 81, 50, 121, 48, 169, 98, 75, 256, 289, 162, 361, 100, 147]


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    M = N ** 3
    d = [0] * (M + 1)
    for i in range(1, M + 1):
        for j in range(i, M + 1, i):
            d[j] += 1
    seq = []
    for n in range(1, N + 1):
        best = max(k * n for k in range(1, n * n + 1) if d[k * n] < 2 * d[n])
        formula = n * max(m for m in range(1, n + 1) if n % m == 0 and d[n * m] < 2 * d[n])
        assert best == formula, (n, best, formula)
        assert (n * n) % best == 0, n
        seq.append(best)
        # A340896: n^2 is in row n  <=>  n is a prime power (1 included)
        npf = sum(1 for p in range(2, n + 1) if n % p == 0 and all(p % r for r in range(2, p)))
        assert (d[n * n] < 2 * d[n]) == (npf <= 1), n
    assert seq[:len(DATA)] == DATA
    print(f"n <= {N}: brute force (multiples up to n^3) = formula, a(n) | n^2, DATA matches; A340896 n^2-in-row-n <=> prime power")


if __name__ == "__main__":
    main()
