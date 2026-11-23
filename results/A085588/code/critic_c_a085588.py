"""DISC-0016 critic: independent recomputation of OEIS A085588 (rule 150 on a ring of n cells).

Written without reading l08_a085588_period.py (only its DATA list was copied, as the
reference to compare against).  Standard library only.

Method 1 (algebra, no Frobenius shortcut): a ring state is a polynomial in
F2[x]/(x^n - 1); one rule-150 step is multiplication by T = x^-1 + 1 + x = x^(n-1) + 1 + x.
T^k is computed by plain square-and-multiply of GF(2) polynomials (carryless products),
so the identity T^(2^D+P) = T^(2^D) is tested as a polynomial identity, which is the
same as the operator identity on every state.  The exact eventual period of the seed
is found as the least divisor d of P with T^(K+d) = T^K (K = n); this is valid because
the equality T^(K+P) = T^K is checked directly first.

Method 2 (no theory): literal cell-by-cell simulation with a dict of seen states, for
n where the period is small enough.

Also: s = A309786(n) through the OEIS formula a(2n) = a(n), a(2n-1) = A003558(n-1),
with A003558(k) = least j >= 1 with 2^j == +-1 (mod 2k+1), computed by brute force.
"""
import random
import sys

DATA = [1,2,3,1,7,4,7,6,31,2,21,14,15,8,15,14,511,12,63,62,2047,4,1023,42,
        511,28,16383,30,31,16,31,30,4095,28,29127,1022,4095,24,1023,126,127,
        124,4095,4094,8388607,8,2097151,2046,255,84,67108863,1022,1048575,56,511,32766,
        536870911,60,17043521,62,63,32,63,62]  # n = 3..66, copied from the entry


# ---------- GF(2)[x]/(x^n - 1) ----------
def clmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def red(a, n):
    mask = (1 << n) - 1
    while a >> n:
        a = (a & mask) ^ (a >> n)
    return a


def mulmod(a, b, n):
    return red(clmul(a, b), n)


def powmod(a, k, n):
    r = 1
    while k:
        if k & 1:
            r = mulmod(r, a, n)
        a = mulmod(a, a, n)
        k >>= 1
    return r


def T(n):
    return red((1 << (n - 1)) | 1 | (1 << 1), n)


# ---------- factoring (own code) ----------
def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def brent(n):
    if n % 2 == 0:
        return 2
    rng = random.Random(n)
    while True:
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def primes_of(n, out):
    for p in range(2, 10000):
        while n % p == 0:
            out.add(p)
            n //= p
    if n == 1:
        return out
    if is_prime(n):
        out.add(n)
        return out
    d = brent(n)
    primes_of(d, out)
    primes_of(n // d, out)
    return out


# ---------- sequences ----------
def A003558(k):
    q = 2 * k + 1
    if q == 1:
        return 1
    j, v = 1, 2 % q
    while v != 1 and v != q - 1:
        j += 1
        v = v * 2 % q
    return j


def A309786(n):  # via OEIS formula only
    while n % 2 == 0:
        n //= 2
    return A003558((n + 1) // 2 - 1)


def two_adic(n):
    D = 0
    while n % 2 == 0:
        n //= 2
        D += 1
    return D, n


def period_alg(n):
    """Return (a(n), preperiod, P, identity_holds)."""
    D, m = two_adic(n)
    s = A309786(n)
    P = 2 ** D * (2 ** s - 1)
    t = T(n)
    ident = powmod(t, 2 ** D + P, n) == powmod(t, 2 ** D, n)
    K = n
    base = powmod(t, K, n)
    assert mulmod(base, powmod(t, P, n), n) == base, n  # T^(K+P) = T^K directly
    p = P
    for q in sorted(primes_of(P, set())):
        while p % q == 0 and mulmod(base, powmod(t, p // q, n), n) == base:
            p //= q
    # exact preperiod: least k with T^(k+p) = T^k
    tp = powmod(t, p, n)
    k, cur = 0, 1
    while mulmod(cur, tp, n) != cur:
        cur = mulmod(cur, t, n)
        k += 1
    return p, k, P, ident


def period_sim(n, cap):
    """Literal simulation of cells; returns eventual period or None."""
    state = tuple(1 if i == 0 else 0 for i in range(n))
    seen = {state: 0}
    for step in range(1, cap + 1):
        state = tuple(state[i - 1] ^ state[i] ^ state[(i + 1) % n] for i in range(n))
        if state in seen:
            return step - seen[state]
        seen[state] = step
    return None


def carryless_A115770(k):
    return clmul(11, k) == 7 * k


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    bad_div, bad_ident, bad_pre, lit_fail, fixed, sim_ok = [], [], [], [], [], 0
    for n in range(3, N + 1):
        a, pre, P, ident = period_alg(n)
        D, _ = two_adic(n)
        if n - 3 < len(DATA):
            assert a == DATA[n - 3], ("DATA mismatch", n, a, DATA[n - 3])
        if P % a:
            bad_div.append(n)
        if not ident:
            bad_ident.append(n)
        if pre > 2 ** D:
            bad_pre.append(n)
        if a % P:
            lit_fail.append(n)
        if a == n:
            fixed.append(n)
        if a <= 50000 and n <= 60:
            b = period_sim(n, 200000)
            assert b == a, ("sim mismatch", n, a, b)
            sim_ok += 1
    print(f"n=3..{N}: DATA n<=66 match; brute-force simulation agrees on {sim_ok} n")
    print(f"a(n) not dividing P: {bad_div}; identity T^(2^D+P)!=T^(2^D): {bad_ident}; preperiod>2^D: {bad_pre}")
    print(f"literal comment (P | a(n)) fails for {len(lit_fail)} n: {lit_fail[:12]} ...")
    print(f"a(n)=n: {fixed}; all in A115770 (11 (x) k = 7k): {all(carryless_A115770(k) for k in fixed)}")
    odd_parts = sorted({two_adic(k)[1] for k in fixed})
    print(f"odd parts of a(n)=n: {odd_parts}")
    print(f"A309786(1..20): {[A309786(i) for i in range(1, 21)]}")
    a4, a13 = period_alg(4), period_alg(13)
    print(f"a(4)={a4[0]} P={a4[2]}; a(13)={a13[0]} P={a13[2]}")


if __name__ == "__main__":
    main()
