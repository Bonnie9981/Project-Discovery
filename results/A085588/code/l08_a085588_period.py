"""DISC-0016: OEIS A085588 (Rule 150 on a ring of n cells, eventual period of one ON cell).

Checks, for n = 2^D * m (m odd), s = A309786(n) = least s >= 1 with 2^s = +-1 (mod m):
  (1) the operator identity F^(2^D + P) = F^(2^D), P = 2^D (2^s - 1), on random configurations
      and on the single cell (method A: fast GF(2) operator powers via F^(2^j) = shift(-2^j)+1+shift(2^j));
  (2) a(n) | P, by computing a(n) two independent ways:
      method A: a(n) = least divisor d of P with F^(2^D+d) e = F^(2^D) e   (uses the theorem only as a bound)
      method B: brute-force simulation with a dictionary of seen states (no theory), when feasible;
  (3) the DATA terms of A085588 (copied from the live entry 2026-11-23);
  (4) the literal comment "2^D (2^s - 1) divides a(n)" fails, first at n = 4 and n = 13.
Run: python results/A085588/code/l08_a085588_period.py
"""
import random
from math import gcd


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rho(n):
    if n % 2 == 0:
        return 2
    c = 1
    while True:
        x = y = 2; d = 1
        while d == 1:
            x = (x * x + c) % n; y = (y * y + c) % n; y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d
        c += 1


def factorint(n, out=None):
    out = {} if out is None else out
    if n == 1:
        return out
    if is_prime(n):
        out[n] = out.get(n, 0) + 1
        return out
    d = rho(n)
    factorint(d, out); factorint(n // d, out)
    return out

DATA = [1,2,3,1,7,4,7,6,31,2,21,14,15,8,15,14,511,12,63,62,2047,4,1023,42,
        511,28,16383,30,31,16,31,30,4095,28,29127,1022,4095,24,1023,126,127,
        124,4095,4094,8388607,8,2097151,2046,255,84,67108863,1022,1048575,56,511,32766,
        536870911,60,17043521,62,63,32,63,62]  # n = 3..66


def split(n):
    D, m = 0, n
    while m % 2 == 0:
        m //= 2; D += 1
    return D, m


def sord(m):
    if m == 1:
        return 1
    s, p = 1, 2 % m
    while p not in (1, m - 1):
        p = p * 2 % m; s += 1
    return s


def rot(x, k, n):
    k %= n
    mask = (1 << n) - 1
    return ((x << k) | (x >> (n - k))) & mask if k else x


def step(x, n):  # one Rule 150 step on the ring
    return rot(x, 1, n) ^ x ^ rot(x, -1, n)


def power(x, k, n):
    """F^k x using F^(2^j) = shift(-2^j) + 1 + shift(2^j) over GF(2)."""
    j = 0
    while k:
        if k & 1:
            a = (1 << j) % n
            x = rot(x, a, n) ^ x ^ rot(x, -a, n)
        k >>= 1; j += 1
    return x


def period_A(n):
    D, m = split(n)
    s = sord(m)
    P = (1 << D) * ((1 << s) - 1)
    base = power(1, 1 << D, n)
    fac = factorint(P)
    d = P
    for q in fac:  # reduce d to the exact order
        while d % q == 0 and power(base, d // q, n) == base:
            d //= q
    return d, P


def period_B(n, limit=200000):
    seen, x, t = {}, 1, 0
    while x not in seen:
        if t > limit:
            return None
        seen[x] = t; x = step(x, n); t += 1
    return t - seen[x]


def main():
    rnd = random.Random(16)
    for n in range(1, 401):
        D, m = split(n); s = sord(m); P = (1 << D) * ((1 << s) - 1)
        for _ in range(3):
            x = rnd.getrandbits(n)
            assert power(x, (1 << D) + P, n) == power(x, 1 << D, n), n
        if n <= 120:  # power() itself vs plain stepping
            x = rnd.getrandbits(n); y = x
            for k in range(1, 70):
                y = step(y, n)
                assert y == power(x, k, n), (n, k)
    print("identity F^(2^D+P) = F^(2^D) on random configs: ok for n <= 400")
    lit_fail, b_checked = [], 0
    for n in range(3, 201):
        a, P = period_A(n)
        assert P % a == 0
        b = period_B(n)
        if b is not None:
            assert a == b, (n, a, b); b_checked += 1
        if n - 3 < len(DATA):
            assert a == DATA[n - 3], (n, a, DATA[n - 3])
        if a % P:
            lit_fail.append(n)
    print(f"a(n) | 2^D(2^s-1) for 3 <= n <= 200; brute force agrees on {b_checked} n; DATA (n<=66) matches")
    print("literal comment fails at", lit_fail[:12], "...", len(lit_fail), "of 198")
    print("a(4) =", period_A(4)[0], " a(13) =", period_A(13)[0])


if __name__ == "__main__":
    main()
