"""Checks for DISC-0031 (marked mesh patterns in 132-avoiding permutations).

Theorem: for k >= 1, sum_n [x^1] Q_{n,132}^{(0,0,k,0)}(x) t^n
         = t*(1 - P_k + t*P_k^2)/(1 - t*P_k)^3,  P_k = C_0 + C_1 t + ... + C_{k-1} t^(k-1).
k = 2, 3, 4 give A212338, A212339, A212341.  Also checks KRT Theorem 13 for
A212344 (5*C(n-3)) and A212345 (9*C(n-3)).

usage: python results/A212339/code/check_a212339.py [nmax_brute=11]
"""
import sys
from collections import Counter
from math import comb

N = 60  # series length for the exact/DP checks


def cat(m):
    return comb(2 * m, m) // (m + 1)


# ---------- implementation 1: brute force over 132-avoiding permutations ----------
def av132(n):
    def rec(p, rem):
        if not rem:
            yield p
            return
        for v in sorted(rem):
            # v must not play the role of "2" in a 132 with earlier p[i] < v < p[j], i < j
            ok = True
            lo_seen = False
            for x in p:
                if x < v:
                    lo_seen = True
                elif lo_seen:  # x > v after some smaller entry
                    ok = False
                    break
            if ok:
                yield from rec(p + [v], rem - {v})
    yield from rec([], frozenset(range(n)))


def brute(nmax):
    """dist[(quadrant, k)][n] = Counter of the statistic over S_n(132)."""
    out = {}
    for n in range(nmax + 1):
        perms = list(av132(n))
        assert len(perms) == cat(n)
        for k in (2, 3, 4):
            c3 = Counter(sum(1 for i in range(n) if sum(1 for j in range(i) if p[j] < p[i]) >= k) for p in perms)
            c2 = Counter(sum(1 for i in range(n) if sum(1 for j in range(i) if p[j] > p[i]) >= k) for p in perms)
            out.setdefault(('III', k), []).append(c3)
            out.setdefault(('II', k), []).append(c2)
    return out


# ---------- power series helpers (integer, length N) ----------
def mul(a, b):
    r = [0] * N
    for i, x in enumerate(a[:N]):
        if x:
            for j, y in enumerate(b[:N - i]):
                r[i + j] += x * y
    return r


def inv(a):
    assert a[0] == 1
    r = [0] * N
    r[0] = 1
    for n in range(1, N):
        r[n] = -sum(a[i] * r[n - i] for i in range(1, min(n, len(a) - 1) + 1))
    return r


def P(k):
    return [cat(a) for a in range(k)] + [0] * (N - k)


def gf_x1(k):
    """t*(1 - P + t*P^2)/(1 - t*P)^3 as a series."""
    p = P(k)
    tp = [0] + p[:N - 1]
    one_m_tp = [1 - tp[0]] + [-x for x in tp[1:]]
    num = [0] * N
    num[0] = 1
    for i in range(N):
        num[i] -= p[i]
    tp2 = [0] + mul(p, p)[:N - 1]
    for i in range(N):
        num[i] += tp2[i]
    num = [0] + num[:N - 1]
    d = inv(one_m_tp)
    return mul(num, mul(d, mul(d, d)))


# ---------- implementation 2: DP from the decomposition sigma = alpha n beta ----------
def dp_x1_full(k, nmax):
    """Q_n(x) from Q_n = sum_{a+b=n-1} x^[a>=k] Q_a Q_b (uses the decomposition of the proof)."""
    Q = [[1]]
    for n in range(1, nmax + 1):
        acc = [0] * (n + 1)
        for a in range(n):
            b = n - 1 - a
            sh = 1 if a >= k else 0
            for i, x in enumerate(Q[a]):
                for j, y in enumerate(Q[b]):
                    acc[i + j + sh] += x * y
        Q.append(acc)
    return Q


# ---------- exact polynomial identities with Barker's / Mathar's g.f.s ----------
def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def polypow(a, e):
    r = [1]
    for _ in range(e):
        r = polymul(r, a)
    return r


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def our_num_den(k):
    p = [cat(a) for a in range(k)]
    num = [1] + [0] * (2 * k)
    for i, x in enumerate(p):
        num[i] -= x
    for i, x in enumerate(polymul(p, p)):
        num[i + 1] += x
    num = [0] + num  # times t
    den = [1] + [-x for x in p]  # 1 - t*P
    return trim(num), trim(polypow(den, 3))


def check_exact():
    # A212338: g.f. x^3*(2+x)/(1-x-x^2)^3 (Mathar, stated as a formula in the entry)
    # A212339: Barker: x^4*(5+4x+4x^2)/((1-2x)^3*(1+x+x^2)^3)
    # A212341: Barker: x^5*(14+14x+20x^2+25x^3)/(1-x-x^2-2x^3-5x^4)^3
    targets = {
        2: ([0, 0, 0, 2, 1], polypow([1, -1, -1], 3)),
        3: ([0, 0, 0, 0, 5, 4, 4], polymul(polypow([1, -2], 3), polypow([1, 1, 1], 3))),
        4: ([0, 0, 0, 0, 0, 14, 14, 20, 25], polypow([1, -1, -1, -2, -5], 3)),
    }
    for k, (tn, td) in targets.items():
        n, d = our_num_den(k)
        assert trim(polymul(n, td)) == trim(polymul(tn, d)), k
    # Dale's signature for A212339: denominator 1 - 3t - 0t^2 - t^3 + 12t^4 + 3t^5 - t^6 - 18t^7 - 12t^8 - 8t^9
    sig = [3, 0, 1, -12, -3, 1, 18, 12, 8]
    assert trim(polypow([1, -1, -1, -2], 3)) == [1] + [-s for s in sig]


def check_oeis(series):
    try:
        sys.path.insert(0, '.')
        import sqlite3
        db = sqlite3.connect('data/oeis/index/oeisdb.sqlite')
    except Exception:
        return 'skipped'
    import pickle
    try:
        terms = pickle.load(open('data/relmine/terms.pkl', 'rb'))
    except Exception:
        terms = None
    out = []
    for a, s in series.items():
        if terms and a in terms:
            t, off = terms[a][0], terms[a][1]
        else:
            row = db.execute("select text from line where anum=? and tag in ('S','T','U')", (a,)).fetchall()
            if not row:
                out.append(a + ':skipped')
                continue
            t = [int(x) for x in ''.join(r[0] for r in row).split(',') if x]
            off = db.execute('select offset from seq where anum=?', (a,)).fetchone()[0]
        L = min(len(t), len(s) - off)
        assert all(t[i] == s[off + i] for i in range(L)), a
        out.append('%s:%d' % (a, L))
    return ' '.join(out)


def main():
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    br = brute(nb)
    series = {}
    for k, a in ((2, 'A212338'), (3, 'A212339'), (4, 'A212341')):
        g = gf_x1(k)
        Q = dp_x1_full(k, N - 1)
        for n in range(N):
            assert (Q[n][1] if len(Q[n]) > 1 else 0) == g[n], (k, n)
        for n in range(nb + 1):
            assert br[('III', k)][n][1] == g[n], (k, n)
            assert br[('III', k)][n][0] == Q[n][0]
        series[a] = g
    # KRT Theorem 13 for (0,3,0,0): x^(n-3) -> 5 C(n-3) (A212344), x^(n-4) -> 9 C(n-3) (A212345)
    for n in range(4, nb + 1):
        assert br[('II', 3)][n][n - 3] == 5 * cat(n - 3)
        assert br[('II', 3)][n][n - 4] == 9 * cat(n - 3)
    series['A212344'] = [0, 0, 0] + [5 * cat(n - 3) for n in range(3, N)]
    series['A212345'] = [0, 0, 0, 0] + [9 * cat(n - 3) for n in range(4, N)]
    check_exact()
    print('brute n <= %d, DP n < %d, exact g.f. identities (A212338/39/41, Dale signature) OK; OEIS terms: %s'
          % (nb, N, check_oeis(series)))


if __name__ == '__main__':
    main()
