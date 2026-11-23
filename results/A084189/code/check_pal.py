"""DISC-0024: numeric checks for A084189 and A084352 (independent of the C searches).

1. List palindromes N < LIMIT that are p*q (p <= q primes), by trial division.
2. A046376 = those with p, q palindromic; A084352 terms = those with len(p) == len(q).
3. Compare min-digit values with the OEIS DATA lines, and check max <= 3.
Run: python3 check_pal.py [LIMIT]   (default 10**8, about a minute)
"""
import sys

A084189 = [int(x) for x in (
    "2,2,3,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,"
    "0,0,1,0,0,0,1,0,0,0,0,2,2,0,0,0,2,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0,0,0,"
    "0,0,1,1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1").split(",")]
A084352 = [int(x) for x in (
    "2,2,3,1,1,1,1,1,1,2,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,1,1,0,0,0,1,1,0,"
    "1,0,1,1,0,0,1,0,1,2,0,1,2,0,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,"
    "0,1,1,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1").split(",")]


def palindromes(limit):
    out = []
    L = 1
    while 10 ** (L - 1) < limit:
        h = (L + 1) // 2
        for half in range(10 ** (h - 1), 10 ** h):
            s = str(half)
            t = s + s[::-1][L % 2:]
            n = int(t)
            if n < limit:
                out.append(n)
        L += 1
    return sorted(out)


def semiprime_split(n):
    """Return (p, q) with p <= q primes and p*q == n, or None."""
    d = 2
    while d * d <= n:
        if n % d == 0:
            q = n // d
            # d is the least prime factor; n is semiprime iff q is prime
            e = 2
            while e * e <= q:
                if q % e == 0:
                    return None
                e += 1
            return (d, q) if q > 1 else None
        d += 1
    return None


def ispal(n):
    return str(n) == str(n)[::-1]


def main():
    limit = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
    seq189, seq352 = [], []
    for n in palindromes(limit):
        sp = semiprime_split(n)
        if not sp:
            continue
        p, q = sp
        m = min(int(c) for c in str(p) + str(q))
        if ispal(p) and ispal(q):
            seq189.append((n, m))
        if len(str(p)) == len(str(q)):
            seq352.append((n, m))
    v189 = [m for _, m in seq189]
    v352 = [m for _, m in seq352]
    assert v189[:len(A084189)] == A084189, "A084189 DATA mismatch"
    assert v352[:len(A084352)] == A084352, "A084352 DATA mismatch"
    print(f"limit {limit}: A046376 terms {len(seq189)}, max min-digit {max(v189)}; "
          f"palindromic brilliant {len(seq352)}, max min-digit {max(v352)}")
    assert max(v189) <= 3 and max(v352) <= 3
    print("DATA lines match; conjectures hold below the limit")


if __name__ == "__main__":
    main()
