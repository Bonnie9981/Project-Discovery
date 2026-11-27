"""DISC-0026 Critic: independent exhaustive search for A372430's reverse conjecture.

Self-contained (standard library only; no project imports).
Condition on k >= 1: for every j with bit (j-1) of k equal to 1, prime(j) divides k.

Method (differs from a372430_dfs.c): one global search over ALL k < 2^N with
leading zeros allowed (no per-length loop, no forced top prime). Bits are fixed
from position N down to 1 with an explicit stack; M = product of prime(j) over
fixed 1-bits. When the block [lo, lo+2^r) contains at most LEAF multiples of M,
the multiples are listed and each is checked against the definition written
from scratch (binary indices from the reversed bin() string, prime indices by
direct divisibility). Also: brute force for small k, and a check of 4100 and
2^87 + 2^49 by trial-division factorisation.
Run: python3 critic_a372430_search.py N [BRUTE]
"""
import sys
import time


def first_primes(n):
    ps = []
    c = 2
    while len(ps) < n:
        if all(c % p for p in ps if p * p <= c):
            ps.append(c)
        c += 1
    return ps


def binary_indices(k):
    s = bin(k)[2:][::-1]
    return {i + 1 for i, ch in enumerate(s) if ch == "1"}


def satisfies(k, P):
    if k < 1:
        return False
    return all(k % P[j - 1] == 0 for j in binary_indices(k))


def search(N, P, LEAF=4):
    hits, nodes = [], 0
    stack = [(N, 0, 1)]  # (undecided low bits r, prefix value v, modulus M)
    while stack:
        r, v, M = stack.pop()
        nodes += 1
        lo = v << r
        hi = lo + (1 << r)  # exclusive
        first = -(-lo // M) * M
        if first >= hi:
            continue
        if (hi - 1 - first) // M + 1 <= LEAF or r == 0:
            for k in range(first, hi, M):
                if satisfies(k, P):
                    hits.append(k)
            continue
        stack.append((r - 1, v << 1, M))
        stack.append((r - 1, (v << 1) | 1, M * P[r - 1]))
    return sorted(hits), nodes


def factor(n):
    f, d = [], 2
    while d * d <= n:
        while n % d == 0:
            f.append(d)
            n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    P = first_primes(max(N, 130))
    k = 2 ** 87 + 2 ** 49
    print("k =", k, "bin indices", sorted(binary_indices(k)),
          "factor(2^38+1) =", factor(2 ** 38 + 1),
          "prime(50), prime(88) =", P[49], P[87], "ok =", satisfies(k, P))
    print("4100 bin indices", sorted(binary_indices(4100)), "factor", factor(4100),
          "ok =", satisfies(4100, P))
    if B:
        t = time.time()
        print("brute k <=", B, ":", [x for x in range(1, B + 1) if satisfies(x, P)],
              f"{time.time()-t:.1f}s")
    t = time.time()
    hits, nodes = search(N, P)
    print(f"search k < 2^{N}: hits={hits} nodes={nodes} {time.time()-t:.1f}s")


if __name__ == "__main__":
    main()
