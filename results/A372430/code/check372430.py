"""DISC-0026: independent checks for the A372430 conjecture (binary indices subset of prime indices).

1. Brute force k <= 10^6 (the entry says 4100 is the only one up to 10^7).
2. All k < 2^LMAX with at most 4 one-bits, by direct enumeration of bit positions.
3. Verify the counterexample 2^87 + 2^49 directly.
Run: python3 check372430.py [LMAX]   (default 120)
"""
import sys
from itertools import combinations


def primes(n):
    out, x = [], 2
    while len(out) < n:
        if all(x % p for p in out if p * p <= x):
            out.append(x)
        x += 1
    return out


def good(k, P):
    j = 1
    while k >> (j - 1):
        if (k >> (j - 1)) & 1 and k % P[j - 1]:
            return False
        j += 1
    return True


def main():
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    P = primes(L + 1)
    brute = [k for k in range(1, 10 ** 6 + 1) if good(k, P)]
    print("brute force k <= 10^6:", brute)
    found = []
    for s in range(1, 5):
        for pos in combinations(range(1, L + 1), s):
            k = sum(1 << (j - 1) for j in pos)
            if all(k % P[j - 1] == 0 for j in pos):
                found.append(k)
    print(f"<= 4 one-bits, k < 2^{L}:", sorted(found))
    k = 2 ** 87 + 2 ** 49
    assert good(k, P) and P[49] == 229 and P[87] == 457
    print("2^87 + 2^49 =", k, "binary indices {50, 88}, prime(50) = 229, prime(88) = 457: OK")


if __name__ == "__main__":
    main()
