# Independent recount for DISC-0032 (no project imports).
"""Independent recount written by the critic for DISC-0032 (brute force, explicit midpoint bijection and reflection); imports nothing from the project."""
import sys
from itertools import product
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
DIRS = [(1,0),(0,1),(-1,0),(0,-1)]

def all_turning_saws(n):
    """All n-step SAWs on Z^2 from origin, any first direction, turning at every vertex.
    Returned as tuples of vertices."""
    out = []
    def go(path, d):
        if len(path) == n + 1:
            out.append(tuple(path)); return
        x, y = path[-1]
        for nd in DIRS:
            if d is not None and (nd[0]*d[0] + nd[1]*d[1]) != 0:  # forbid straight AND reversal
                continue
            p = (x+nd[0], y+nd[1])
            if p in path: continue
            path.append(p); go(path, nd); path.pop()
    go([(0,0)], None)
    return out

def no_same_dir(n):
    c = 0
    def go(path, d):
        nonlocal c
        if len(path) == n + 1: c += 1; return
        x, y = path[-1]
        for nd in DIRS:
            if nd == d: continue
            p = (x+nd[0], y+nd[1])
            if p in path: continue
            path.append(p); go(path, nd); path.pop()
    go([(0,0)], None); return c

def manh_walks(n, conv):
    """contact-free SAWs on a Manhattan lattice; conv=(a,b): row y goes east iff (y+a) even,
    column x goes north iff (x+b) even. Returns list of vertex tuples."""
    a, b = conv
    out = []
    def allowed(x, y):
        return [(1,0) if (y+a) % 2 == 0 else (-1,0), (0,1) if (x+b) % 2 == 0 else (0,-1)]
    def go(path):
        if len(path) == n + 1: out.append(tuple(path)); return
        x, y = path[-1]
        for d in allowed(x, y):
            p = (x+d[0], y+d[1])
            if p in path: continue
            # contact: p adjacent to any path vertex except the last one
            if any(abs(p[0]-u[0]) + abs(p[1]-u[1]) == 1 for u in path[:-1]): continue
            path.append(p); go(path); path.pop()
    go([(0,0)]); return out

def mid_map(W):
    # doubled midpoints, then (a,b)->((a+b)/2,(a-b)/2) relative to first
    P = [(W[i][0]+W[i+1][0], W[i][1]+W[i+1][1]) for i in range(len(W)-1)]
    x0, y0 = P[0]
    return tuple(((x-x0)+(y-y0))//2 for x, y in P), tuple(((x-x0)-(y-y0))//2 for x, y in P)

res = {}
for n in range(1, NMAX+1):
    at = all_turning_saws(n)
    nsd = no_same_dir(n)
    ms = {c: manh_walks(n, c) for c in [(0,0),(1,0),(0,1),(1,1)]}
    cnts = {c: len(v) for c, v in ms.items()}
    assert len(set(cnts.values())) == 1, (n, cnts)
    res[n] = (len(at), nsd, cnts[(0,0)])
# A189722(m) = (# all always-turning SAWs with m steps)/8 for m >= 2
A189722 = {m: res[m][0] // 8 for m in range(2, NMAX+1)}
for m in range(2, NMAX+1): assert res[m][0] % 8 == 0
A336662 = {0: 1, **{n: res[n][2] for n in res}}
A337353 = {0: 1, **{n: res[n][1] for n in res}}
print('A189722', [A189722[m] for m in sorted(A189722)])
print('A336662', [A336662[k] for k in sorted(A336662)])
print('A337353', [A337353[k] for k in sorted(A337353)])
for k in range(1, NMAX):
    assert A336662[k] == 2*A189722[k+1], k
for n in range(1, NMAX+1):
    assert A337353[n] == 4*A336662[n-1], ('4*A336662(n-1)', n)
for n in range(2, NMAX+1):
    assert A337353[n] == 8*A189722[n]
bad = [n for n in range(0, NMAX+1) if A337353[n] != 4*A336662[n]]
print('A337353(n) != 4*A336662(n) at n =', bad[:5], '... count', len(bad))
# Explicit bijection check: image of normalised always-turning SAWs (first E, first turn L)
# under the midpoint map == set of contact-free Manhattan walks (conv (0,0)) starting east.
for m in range(2, min(NMAX, 13)+1):
    norm = [W for W in all_turning_saws(m) if W[1] == (1,0) and W[2] == (1,1)]
    img = set()
    for W in norm:
        xs, ys = mid_map(W)
        img.add(tuple(zip(xs, ys)))
    target = set(w for w in manh_walks(m-1, (0,0)) if m-1 == 0 or w[1] == (1,0))
    assert len(img) == len(norm) and img == target, m
    # reflection x<->y maps east-starting onto north-starting
    north = set(w for w in manh_walks(m-1, (0,0)) if w[1] == (0,1))
    assert set(tuple((y, x) for x, y in w) for w in target) == north, m
print('explicit bijection + reflection OK for m <=', min(NMAX, 13))
