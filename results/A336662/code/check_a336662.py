"""Checks for DISC-0032: always-turning walks vs Manhattan walks without contacts.

A189722(m): m-edge self-avoiding walks on Z^2 that turn 90 degrees at every
            vertex, first turn to the left.
A336662(k): k-step self-avoiding walks on the Manhattan lattice with no
            non-contiguous adjacencies.
A337353(n): n-step self-avoiding walks on Z^2 with no two consecutive steps
            in the same direction.
Claims: A336662(k) = 2*A189722(k+1) (k >= 1); A337353(n) = 4*A336662(n-1) (n >= 1);
A337353(n) = 8*A189722(n) (n >= 2).
Also checks the midpoint map of the proof on every walk (n small): q starts
with E, obeys the Manhattan orientation, and W is a SAW iff q is a SAW without contacts.

usage: python results/A336662/code/check_a336662.py [nmax=18]
"""
import sys

E, N, W, S = (1, 0), (0, 1), (-1, 0), (0, -1)
LEFT = {E: N, N: W, W: S, S: E}
RIGHT = {v: k for k, v in LEFT.items()}


def always_turn(m):
    """Count m-edge always-turning SAWs with first edge E and first turn L (A189722)."""
    if m < 2:
        return None
    cnt = 0
    def rec(pos, d, seen, left):
        nonlocal cnt
        if left == 0:
            cnt += 1
            return
        for nd in (LEFT[d], RIGHT[d]):
            p = (pos[0] + nd[0], pos[1] + nd[1])
            if p not in seen:
                seen.add(p)
                rec(p, nd, seen, left - 1)
                seen.discard(p)
    # first edge E from origin, then a left turn (N)
    seen = {(0, 0), (1, 0), (1, 1)}
    rec((1, 1), N, seen, m - 2)
    return cnt


def manhattan_ok(p, d):
    # row y runs east if y even, west if odd; column x runs north if x even, south if odd
    x, y = p
    if d in (E, W):
        return d == (E if y % 2 == 0 else W)
    return d == (N if x % 2 == 0 else S)


def manhattan_nocontact(k):
    cnt = 0
    def rec(path, seen, left):
        nonlocal cnt
        if left == 0:
            cnt += 1
            return
        x, y = path[-1]
        for d in (E, N, W, S):
            if not manhattan_ok((x, y), d):
                continue
            p = (x + d[0], y + d[1])
            if p in seen:
                continue
            # no contact with any earlier vertex other than the current one
            if any((p[0] + a, p[1] + b) in seen and (p[0] + a, p[1] + b) != (x, y) for a, b in (E, N, W, S)):
                continue
            seen.add(p)
            path.append(p)
            rec(path, seen, left - 1)
            path.pop()
            seen.discard(p)
    rec([(0, 0)], {(0, 0)}, k)
    return cnt


def no_repeat_dir(n):
    cnt = 0
    def rec(pos, d, seen, left):
        nonlocal cnt
        if left == 0:
            cnt += 1
            return
        for nd in (E, N, W, S):
            if nd == d:
                continue
            p = (pos[0] + nd[0], pos[1] + nd[1])
            if p not in seen:
                seen.add(p)
                rec(p, nd, seen, left - 1)
                seen.discard(p)
    rec((0, 0), None, {(0, 0)}, n)
    return cnt


def midpoint_check(m):
    """For every m-edge always-turning walk (any turns, first edge E, first turn L,
    self-avoiding or not), build q from doubled midpoints and check:
    q has unit steps, and W is self-avoiding iff q is self-avoiding with no
    non-contiguous adjacency. Returns number of walks checked."""
    from itertools import product
    n_ok = 0
    for turns in product('LR', repeat=m - 2):
        ts = ('L',) + turns
        d, v = E, (0, 0)
        verts = [v]
        edges = []
        for i in range(m):
            if i > 0:
                d = LEFT[d] if ts[i - 1] == 'L' else RIGHT[d]
            nv = (v[0] + d[0], v[1] + d[1])
            edges.append((v, nv))
            v = nv
            verts.append(v)
        p = [(a[0] + b[0], a[1] + b[1]) for a, b in edges]
        q = [((x - p[0][0] + y - p[0][1]) // 2, (x - p[0][0] - (y - p[0][1])) // 2) for x, y in p]
        assert all(abs(q[i + 1][0] - q[i][0]) + abs(q[i + 1][1] - q[i][1]) == 1 for i in range(len(q) - 1))
        # q is a walk on the Manhattan lattice from the origin whose first step is E
        assert q[0] == (0, 0) and q[1] == (1, 0)
        assert all(manhattan_ok(q[i], (q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1])) for i in range(len(q) - 1))
        saw_w = len(set(verts)) == len(verts)
        qs = set(q)
        ok_q = len(qs) == len(q) and not any(
            abs(q[i][0] - q[j][0]) + abs(q[i][1] - q[j][1]) == 1 for i in range(len(q)) for j in range(i + 2, len(q)))
        assert saw_w == ok_q, (ts,)
        n_ok += 1
    return n_ok


def oeis_terms(a):
    try:
        import pickle
        d = pickle.load(open('data/relmine/terms.pkl', 'rb'))
        return d[a][0], d[a][1]
    except Exception:
        return None


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    at = {m: always_turn(m) for m in range(2, nmax + 2)}
    mh = {k: manhattan_nocontact(k) for k in range(0, nmax + 1)}
    nr = {n: no_repeat_dir(n) for n in range(0, nmax + 1)}
    for k in range(1, nmax + 1):
        assert mh[k] == 2 * at[k + 1], k
    for n in range(1, nmax + 1):
        assert nr[n] == 4 * mh[n - 1], n
        assert nr[n] != 4 * mh[n], n  # the formula a(n) = 4*A336662(n) in A337353 fails for every n >= 1
        if n >= 2:
            assert nr[n] == 8 * at[n], n
    checked = sum(midpoint_check(m) for m in range(2, min(nmax, 16) + 1))
    msg = []
    for a, mine in (('A189722', at), ('A336662', mh), ('A337353', nr)):
        t = oeis_terms(a)
        if t is None:
            msg.append(a + ':skipped')
            continue
        terms, off = t
        idx = [n for n in mine if n - off >= 0 and n - off < len(terms)]
        assert all(terms[n - off] == mine[n] for n in idx), a
        msg.append('%s:%d' % (a, len(idx)))
    # relation on all stored OEIS terms
    t1, t2, t3 = oeis_terms('A189722'), oeis_terms('A336662'), oeis_terms('A337353')
    if t1 and t2 and t3:
        (m_, om), (b_, ob), (c_, oc) = t1, t2, t3
        M = lambda n: m_[n - om]
        B = lambda n: b_[n - ob]
        Cc = lambda n: c_[n - oc]
        r1 = [k for k in range(max(1, ob), ob + len(b_)) if om <= k + 1 < om + len(m_)]
        assert all(B(k) == 2 * M(k + 1) for k in r1)
        r2 = [n for n in range(max(1, oc), oc + len(c_)) if ob <= n - 1 < ob + len(b_)]
        assert all(Cc(n) == 4 * B(n - 1) for n in r2)
        assert all(Cc(n) != 4 * B(n) for n in r2 if n < ob + len(b_))
        msg.append('relations on stored terms: k<=%d, n<=%d' % (r1[-1], r2[-1]))
    print('brute n <= %d OK; midpoint map checked on %d walks; OEIS %s' % (nmax, checked, ' '.join(msg)))


if __name__ == '__main__':
    main()
