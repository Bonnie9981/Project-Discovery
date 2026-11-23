"""DISC-0024: check of the A276674 conjecture "if x - lambda(x) = 2m > 0 then x <= 4m",
i.e. lambda(x) <= x/2 whenever x - lambda(x) is even and positive (lambda = Carmichael, A002322).
Also checks the first DATA terms of A276674.  Run: python3 check276674.py [N]  (default 10**6)
"""
import sys
from math import gcd

DATA = [21, 28, 45, 46, 51, 64, 65, 77, 82, 85, 91, 106, 111, 126, 129, 133, 136, 148, 155, 166]


def main():
    N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 6
    spf = list(range(N + 1))
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    lam = [0, 1] + [0] * (N - 1)
    for x in range(2, N + 1):
        y, l = x, 1
        while y > 1:
            p, e = spf[y], 0
            while y % p == 0:
                y //= p
                e += 1
            if p == 2:
                lp = 1 if e == 1 else (2 if e == 2 else 2 ** (e - 2))
            else:
                lp = (p - 1) * p ** (e - 1)
            l = l * lp // gcd(l, lp)
        lam[x] = l
    for x in range(1, N + 1):
        n = x - lam[x]
        if n > 0 and n % 2 == 0:
            assert x <= 2 * n, x
    M = 200
    hit = set(x - lam[x] for x in range(1, min(N, M * M) + 1))
    seq = [n for n in range(1, M) if n not in hit]
    assert seq[:len(DATA)] == DATA, seq[:25]
    print(f"x <= {N}: x - lambda(x) = 2m > 0 always has x <= 4m; DATA matches")


if __name__ == "__main__":
    main()
