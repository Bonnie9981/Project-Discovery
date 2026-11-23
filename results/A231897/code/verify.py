"""DISC-0018: checks for A231897 (never -1) and A215461/A215462 (never 0).

Two independent implementations for each of A215461/A215462:
  (1) sieve + convolution exactly as in the entries' FORMULA lines,
  (2) direct listing of odd splittings with trial-division primality.
Run: python3 results/A231897/code/verify.py
"""

A231897 = [0,1,3,5,13,11,21,39,45,75,155,217,331,181,627,923,1241,2505,3915,
           5221,6475,11309,15595,19637,31595]
A215461 = [0,0,2,2,2,0,4,4,2,4,6,4,4,6,8,6,12,6,4,16,10,8,14,12,8,12,16,10,18,
           16,8,24,14,10,28,16,14,22,20,12,26,24,12,26,28,10,30,28,18,36,24,18,
           32,30,22,32,28,18,34,36,10,44,38,18,48,32,26,40,42,32,38,36,22,44]
A215462 = [0,1,0,0,0,2,0,0,2,1,0,2,2,2,2,3,0,4,6,0,4,5,2,4,6,5,4,7,4,6,10,2,8,
           11,2,9,10,6,8,13,6,8,14,8,8,17,8,10,16,7,14,17,10,12,16,11,14,19,12,
           12,26,10,14,25,10,19,22,16,16,21,18,20,28,18,18,31,14,23,30,16]


def wt(x):
    return bin(x).count("1")


def check_a231897():
    for a in range(0, 3001):
        m = 2 ** a - 1
        assert wt(m * m) == a, a
    # brute force the first terms, and a(n) <= 2^n - 1
    for n, v in enumerate(A231897):
        m = 0
        while wt(m * m) != n:
            m += 1
        assert m == v, (n, m, v)
        assert v <= 2 ** n - 1
    print("A231897: wt((2^a-1)^2) = a for a <= 3000; first", len(A231897), "terms match")


def sieve(N):
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return s


def isprime_td(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True


def impl1(N):
    """Formula lines: p(i)=1 if 2i+1 prime, c(i)=1-p(i); sums over i+j=n-1."""
    s = sieve(2 * N + 2)
    p = [s[2 * i + 1] for i in range(N)]
    c = [1 - x for x in p]
    pc, cc = [], []
    for n in range(N):
        a = b = 0
        for i in range(n):
            j = n - 1 - i
            a += p[i] * c[j] + c[i] * p[j]
            b += c[i] * c[j]
        pc.append(a)
        cc.append(b)
    return pc, cc


def impl2(N):
    pc, cc = [], []
    for n in range(N):
        a = b = 0
        for x in range(1, 2 * n, 2):
            y = 2 * n - x
            px, py = isprime_td(x), isprime_td(y)
            a += (px and not py) or (py and not px)
            b += (not px) and (not py)
        pc.append(a)
        cc.append(b)
    return pc, cc


def zeros_fast(N):
    """Indices n < N with A215461(n)=0 / A215462(n)=0 (stop at first witness)."""
    s = sieve(2 * N + 2)
    z1, z2 = [], []
    for n in range(N):
        two = 2 * n
        f1 = f2 = False
        for x in range(1, two, 2):
            y = two - x
            if s[x] != s[y]:
                f1 = True
            if not s[x] and not s[y]:
                f2 = True
            if f1 and f2:
                break
        if not f1:
            z1.append(n)
        if not f2:
            z2.append(n)
    return z1, z2


def check_sums():
    N = 600
    a1, b1 = impl1(N)
    a2, b2 = impl2(N)
    assert a1 == a2 and b1 == b2
    assert a1[:len(A215461)] == A215461
    assert b1[:len(A215462)] == A215462
    z1 = [n for n in range(N) if a1[n] == 0]
    z2 = [n for n in range(N) if b1[n] == 0]
    print("A215461/A215462: two implementations agree for n <", N, "; DATA matches")
    print("  zeros of A215461 for n <", N, ":", z1)
    print("  zeros of A215462 for n <", N, ":", z2)
    Z1, Z2 = zeros_fast(200000)
    print("  zeros for n < 200000:", Z1, Z2)
    assert max(Z1) == 5 and max(Z2) == 19
    # the explicit witnesses used in the Lean proofs
    s = sieve(10 ** 6)
    for n in range(20, 500000):
        x = {0: 9, 2: 35, 4: 25}[(2 * n) % 6]
        y = 2 * n - x
        assert y % 2 == 1 and not s[y] and not s[x]
    for n in range(6, 500000):
        pr = {0: 3, 1: 7, 2: 5}[(2 * n) % 3]
        c = 2 * n - pr
        assert s[pr] and not s[c] and c % 2 == 1
    print("  Lean witnesses checked numerically for n < 500000")


if __name__ == "__main__":
    check_a231897()
    check_sums()
