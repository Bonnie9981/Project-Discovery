"""Check the 4-part-partition / integer-triangle relations (DISC-0028).

(1) brute force: enumerate partitions of n into 4 parts and integer triangles of
    perimeter n-1, check the five difference identities for n <= N;
(2) the bijection (a,a,c,d) <-> (x,y,z) = (c, a, a+d-1) itself, checked one by one;
(3) generating functions: exact rational g.f. from y1+2y2+3y3+4y4 = n (proof.md)
    against Colin Barker's conjectured g.f.s; check_gf_exact proves equality by
    integer-polynomial cross-multiplication, check_gf compares 120 coefficients
    only as an extra sanity check;
(4) the terms stored in the OEIS entries (offline snapshot), if available.
"""
import sys
from fractions import Fraction
from pathlib import Path

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200


def parts4(n):
    """[sum a, sum b, sum c, sum d, count] over a>=b>=c>=d>=1, a+b+c+d=n."""
    S = [0] * 5
    for d in range(1, n // 4 + 1):
        for c in range(d, (n - d) // 3 + 1):
            for b in range(c, (n - c - d) // 2 + 1):
                a = n - b - c - d
                S[0] += a; S[1] += b; S[2] += c; S[3] += d; S[4] += 1
    return S


def tri(m):
    """[sum x, sum y, sum z, count] over x<=y<=z, x+y>z, x+y+z=m."""
    S = [0] * 4
    for x in range(1, m // 3 + 1):
        for y in range(x, (m - x) // 2 + 1):
            z = m - x - y
            if x + y > z:
                S[0] += x; S[1] += y; S[2] += z; S[3] += 1
    return S


def check_identities():
    P = {n: parts4(n) for n in range(0, N + 1)}
    for n in range(1, N + 1):
        p, q, t = P[n], P[n - 1], tri(n - 1)
        assert p[2] - q[2] == t[0], n            # A308758 vs A307686
        assert p[1] - q[1] == t[1], n            # A308759 vs A308096
        assert p[3] - q[3] == t[2] - t[1] + t[3], n  # A308733 vs A307966-A308096+A005044
        assert p[0] - q[0] == q[4] + t[1], n     # A308760 vs A026810(n-1)+A308096
        assert p[4] - q[4] == t[3], n            # count version (already in A005044)
    return P


def check_bijection():
    for n in range(1, N + 1):
        src = {(a, c, d) for d in range(1, n + 1) for c in range(d, n + 1)
               for a in range(c, n + 1) if 2 * a + c + d == n}
        dst = {(x, y, z) for x in range(1, n) for y in range(x, n) for z in range(y, n)
               if x + y + z == n - 1 and x + y > z}
        img = {(c, a, a + d - 1) for a, c, d in src}
        assert img == dst and len(img) == len(src), n


# ---- power series helpers (lists of Fractions, truncated to M terms)
def mul(p, q, M):
    r = [Fraction(0)] * M
    for i, x in enumerate(p[:M]):
        if x:
            for j, y in enumerate(q[:M - i]):
                r[i + j] += x * y
    return r


def inv_1m(k, M, power=1):
    """series of 1/(1-x^k)^power"""
    s = [Fraction(0)] * M
    for i in range(0, M, k):
        s[i] = Fraction(1)
    out = [Fraction(1)] + [Fraction(0)] * (M - 1)
    for _ in range(power):
        out = mul(out, s, M)
    return out


def poly(coeffs, M):
    r = [Fraction(0)] * M
    for i, c in enumerate(coeffs):
        if i < M:
            r[i] = Fraction(c)
    return r


def ratio(num, den_factors, M):
    """num(x) / prod (1 - x^k)^e  for den given as {k: e} with (1+x)=(1-x^2)/(1-x) etc. handled by caller"""
    s = poly(num, M)
    for k, e in den_factors.items():
        s = mul(s, inv_1m(k, M, e), M)
    return s


def check_gf(M=120):
    # exact g.f. from the parametrisation (proof.md):
    # F = x^4/((1-x)(1-x^2)(1-x^3)(1-x^4)); Y_i = F*x^i/(1-x^i) (i=1,2,3), Y_4 = F/(1-x^4)
    F = ratio([0, 0, 0, 0, 1], {1: 1, 2: 1, 3: 1, 4: 1}, M)
    Y = {i: mul(F, ratio([0] * i + [1], {i: 1}, M), M) for i in (1, 2, 3)}
    Y[4] = mul(F, inv_1m(4, M), M)
    add = lambda *s: [sum(t) for t in zip(*s)]
    D, C = Y[4], add(Y[4], Y[3])
    B = add(C, Y[2])
    A = add(B, Y[1])
    # Barker's g.f.s. Denominator (1-x)^5 (1+x)^3 (1+x^2)^2 (1+x+x^2)^k rewritten with
    # (1+x) = (1-x^2)/(1-x), (1+x^2) = (1-x^4)/(1-x^2), (1+x+x^2) = (1-x^3)/(1-x):
    # (1-x)^5(1+x)^3(1+x^2)^2(1+x+x^2)^2 = (1-x^4)^2 (1-x^3)^2 (1-x^2)^1 (1-x)^0 ... computed below
    def barker(num, k3):  # k3 = exponent of (1+x+x^2)
        # (1-x)^5 (1+x)^3 (1+x^2)^2 (1+x+x^2)^k3
        # = (1-x)^(5-3-k3) (1-x^2)^(3-2) (1-x^4)^2 (1-x^3)^k3
        e1 = 5 - 3 - k3
        s = ratio(num, {2: 1, 4: 2, 3: k3}, M)
        if e1 >= 0:
            s = mul(s, inv_1m(1, M, e1), M)
        else:
            s = mul(s, poly([1, -1] if e1 == -1 else [1, -2, 1], M), M)
        return s
    x4 = [0, 0, 0, 0]
    claims = {
        "A308733": (D, barker(x4 + [1], 1)),
        "A308758": (C, barker(x4 + [1, 1, 1, 1, 1, 1, 1], 2)),
        "A308759": (B, barker(x4 + [1, 1, 2, 2, 3, 2, 2], 2)),
        "A308760": (A, barker(x4 + [1, 2, 4, 5, 6, 4, 3], 2)),
        "A308775": (add(A, B, C, D), barker(x4 + [4, 5, 8, 8, 10, 7, 6], 2)),
    }
    # triangle sums: by Theorem 1, Tx(m) = C(m+1)-C(m), Ty(m) = B(m+1)-B(m),
    # Tz(m) = D(m+1)-D(m) + Ty(m) - count(m), count = A005044 with the classical
    # g.f. x^3/((1-x^2)(1-x^3)(1-x^4)); all rational, so the same degree argument applies.
    cnt = ratio([0, 0, 0, 1], {2: 1, 3: 1, 4: 1}, M)
    dif = lambda S: [S[m + 1] - S[m] for m in range(M - 1)] + [None]
    Tx, Ty = dif(C), dif(B)
    Tz = [None if dd is None else dd + y - k for dd, y, k in zip(dif(D), Ty, cnt)]
    def barker3(num):  # x^3 num / ((1-x)^4 (1+x)^3 (1+x^2)^2 (1+x+x^2)^2)
        s = ratio(num, {2: 1, 4: 2, 3: 2}, M)
        return mul(s, poly([1, -1], M), M)  # (1-x)^(4-3-2) = (1-x)^(-1) -> times (1-x)
    for name, ours, num in (("A307686", Tx, [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]),
                            ("A308096", Ty, [0, 0, 0, 1, 1, 2, 2, 3, 2, 2]),
                            ("A307966", Tz, [0, 0, 0, 1, 1, 2, 2, 4, 3, 3])):
        claims[name] = (ours[:M - 1], barker3(num)[:M - 1])
    for m in range(M - 1):
        assert [Tx[m], Ty[m], Tz[m], cnt[m]] == tri(m), m
    # series agreement here is only a sanity check; the proof is check_gf_exact()
    for k, (ours, theirs) in claims.items():
        assert ours == theirs, k
    # brute-force values agree with the series
    for n in range(M):
        assert [A[n], B[n], C[n], D[n]] == parts4(n)[:4], n
    return claims


# ---- exact polynomial identities (no truncation argument needed)
def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return r


def padd(*ps):
    r = [0] * max(len(p) for p in ps)
    for p in ps:
        for i, x in enumerate(p):
            r[i] += x
    return r


def pscale(p, c):
    return [c * x for x in p]


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def one_minus(k):
    return [1] + [0] * (k - 1) + [-1]


def xpow(k):
    return [0] * k + [1]


def pdiv_exact(p, q):
    """p / q for polynomials, asserting zero remainder."""
    p, q = trim(p), trim(q)
    out = [0] * (len(p) - len(q) + 1)
    p = list(p)
    for i in range(len(out) - 1, -1, -1):
        c = Fraction(p[i + len(q) - 1], q[-1])
        assert c.denominator == 1
        out[i] = int(c)
        for j, y in enumerate(q):
            p[i + j] -= out[i] * y
    assert not any(p), "not divisible"
    return out


def check_gf_exact():
    """Every g.f. as N/Q0^2 with Q0 = (1-x)(1-x^2)(1-x^3)(1-x^4); compare with Barker by
    cross-multiplication as polynomials."""
    Q0 = pmul(pmul(one_minus(1), one_minus(2)), pmul(one_minus(3), one_minus(4)))
    # F = x^4/Q0 ; Y_i = x^(4+i)/(Q0 (1-x^i)) = x^(4+i) * (Q0/(1-x^i)) / Q0^2 ; Y_4 = x^4 (Q0/(1-x^4)) / Q0^2
    Y = {i: pmul(xpow(4 + i), pdiv_exact(Q0, one_minus(i))) for i in (1, 2, 3)}
    Y[4] = pmul(xpow(4), pdiv_exact(Q0, one_minus(4)))
    D = Y[4]; C = padd(D, Y[3]); B = padd(C, Y[2]); A = padd(B, Y[1])
    den = pmul(Q0, Q0)
    # triangle g.f.s: Tx = (1-x)/x * C, Ty = (1-x)/x * B, Tz = (1-x)/x * D + Ty - cnt,
    # cnt = x^3/((1-x^2)(1-x^3)(1-x^4)) = x^3 (1-x) Q0 / Q0^2
    shift = lambda N: (lambda M: (assert_zero(M[0]), M[1:])[1])(pmul(one_minus(1), N))
    Tx, Ty = shift(C), shift(B)
    cnt = pmul(pmul(xpow(3), one_minus(1)), Q0)
    Tz = padd(shift(D), Ty, pscale(cnt, -1))
    fac = {1: one_minus(1), 2: one_minus(2), 3: one_minus(3), 4: one_minus(4)}
    # Barker denominators, as products of (1-x^k):
    # (1-x)^5 (1+x)^3 (1+x^2)^2 (1+x+x^2)^k3 = (1-x)^(2-k3) (1-x^2) (1-x^4)^2 (1-x^3)^k3
    def bden(k3, top):  # top = 5 (partitions) or 4 (triangles)
        e1 = top - 3 - k3
        d = pmul(fac[2], pmul(fac[4], fac[4]))
        for _ in range(k3):
            d = pmul(d, fac[3])
        return d, e1
    def same(ourN, num, k3, top):
        d, e1 = bden(k3, top)
        lhs, rhs = pmul(ourN, d), pmul(num, den)
        # e1 = exponent of (1-x) in Barker's denominator: move it to the other side
        for _ in range(max(e1, 0)):
            lhs = pmul(lhs, fac[1])
        for _ in range(max(-e1, 0)):
            rhs = pmul(rhs, fac[1])
        return trim(lhs) == trim(rhs)
    x4 = [0, 0, 0, 0]; x3 = [0, 0, 0]
    tests = {
        "A308733": (D, x4 + [1], 1, 5),
        "A308758": (C, x4 + [1, 1, 1, 1, 1, 1, 1], 2, 5),
        "A308759": (B, x4 + [1, 1, 2, 2, 3, 2, 2], 2, 5),
        "A308760": (A, x4 + [1, 2, 4, 5, 6, 4, 3], 2, 5),
        "A308775": (padd(A, B, C, D), x4 + [4, 5, 8, 8, 10, 7, 6], 2, 5),
        "A307686": (Tx, x3 + [1, 1, 1, 1, 1, 1, 1], 2, 4),
        "A308096": (Ty, x3 + [1, 1, 2, 2, 3, 2, 2], 2, 4),
        "A307966": (Tz, x3 + [1, 1, 2, 2, 4, 3, 3], 2, 4),
    }
    for k, (N, num, k3, top) in tests.items():
        assert same(N, num, k3, top), k
    return list(tests)


def assert_zero(x):
    assert x == 0


def check_oeis():
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
        from discovery.relmine import parse
        from discovery.oeisdb import SRC
    except Exception:
        return "skipped (no repo modules)"
    col = {"A308760": 0, "A308759": 1, "A308758": 2, "A308733": 3, "A026810": 4}
    tcol = {"A307686": 0, "A308096": 1, "A307966": 2, "A005044": 3}
    out = []
    for a, i in list(col.items()) + list(tcol.items()):
        f = SRC / "seq" / a[:4] / f"{a}.seq"
        if not f.exists():
            return "skipped (offline OEIS not fetched)"
        _, terms, off, _, _ = parse(f.read_text())
        fn = parts4 if a in col else tri
        for k, v in enumerate(terms):
            n = off + k
            if n > N:
                break
            assert fn(n)[i] == v, (a, n)
        out.append(f"{a}:{len(terms)}")
    return " ".join(out)


if __name__ == "__main__":
    check_identities()
    check_bijection()
    check_gf()
    check_gf_exact()
    print(f"identities and bijection: n <= {N} OK; g.f.s of A308733/58/59/60/75 equal Barker's (exact polynomial identities); triangle g.f.s A307686/A308096/A307966 too; OEIS terms:", check_oeis())
