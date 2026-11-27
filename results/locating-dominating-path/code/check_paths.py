"""Check the counts of locating-dominating sets and identifying codes in paths and cycles.

Only the Python standard library is used. Run: python check_paths.py

Three independent ways of counting, compared for every n checked:
  A. brute force over all subsets S of the vertices, straight from the graph definitions;
  B. the 0/1-word rules proved in the write-up (gaps between ones for LD sets,
     rules (a)(b)(c) and an 8-state transfer matrix for identifying codes);
  C. the claimed recurrences / generating functions.
"""
from itertools import combinations, product

NMAX = 20  # brute force is 2^n subsets


# ---------- A: definitions ----------
def path(n):
    return [{j for j in (i - 1, i + 1) if 0 <= j < n} for i in range(n)]


def cycle(n):
    return [{(i - 1) % n, (i + 1) % n} for i in range(n)]


def is_ld(adj, S):
    """every vertex outside S has a neighbour in S, and different ones see different sets."""
    seen = set()
    for v in range(len(adj)):
        if v in S:
            continue
        t = frozenset(adj[v] & S)
        if not t or t in seen:
            return False
        seen.add(t)
    return True


def is_id(adj, S):
    """N[v] & S is nonempty and different for every vertex v (N[v] = v and its neighbours)."""
    seen = set()
    for v in range(len(adj)):
        t = frozenset((adj[v] | {v}) & S)
        if not t or t in seen:
            return False
        seen.add(t)
    return True


def brute(graph, test, n):
    adj = graph(n)
    return sum(test(adj, {i for i in range(n) if m >> i & 1}) for m in range(1 << n))


# ---------- B: word rules ----------
def ld_word_path(w):
    n = len(w)
    ones = [i for i, b in enumerate(w) if b]
    if not ones:
        return False
    g = [ones[0]] + [b - a - 1 for a, b in zip(ones, ones[1:])] + [n - 1 - ones[-1]]
    if g[0] > 1 or g[-1] > 1 or any(x > 2 for x in g[1:-1]):
        return False
    big = [g[0] == 1] + [x == 2 for x in g[1:-1]] + [g[-1] == 1]
    return not any(big[i] and big[i + 1] for i in range(len(big) - 1))


def id_word_path(w):
    n = len(w)
    if n < 3:
        return n == 1 and w[0] == 1
    a = all(w[j] or w[j + 3] for j in range(n - 3))
    b = w[2] and w[n - 3]
    c = (w[0] or w[1]) and (w[-1] or w[-2]) and all(w[j] or w[j + 1] or w[j + 2] for j in range(n - 2))
    return bool(a and b and c)


def id_transfer(n):
    """8-state transfer matrix on the last three letters (n >= 3)."""
    st = list(product((0, 1), repeat=3))
    ok = lambda p, q: p[1:] == q[:2] and (p[0] or q[2]) and (p[1] or p[2] or q[2])
    vec = [1 if (p[0] or p[1]) and p[2] else 0 for p in st]       # w1 v w2, w3 = 1
    for _ in range(n - 3):
        vec = [sum(vec[i] for i, p in enumerate(st) if ok(p, q)) for q in st]
    return sum(v for v, q in zip(vec, st) if q[0] and (q[1] or q[2]))  # w_{n-2} = 1, w_{n-1} v w_n


# ---------- C: claimed formulas ----------
def rec(init, coef, N):
    a = list(init)
    while len(a) < N:
        a.append(sum(c * a[-1 - i] for i, c in enumerate(coef)))
    return a


LD_PATH = rec([1, 3, 4, 9, 15], [1, 1, 0, 1, 1], 60)               # n = 1, 2, ...
A001642 = rec([1, 3, 4, 11, 21], [1, 1, 0, 1, 1], 60)              # n = 1, 2, ... (its own %S)
ID_PATH = rec([1, 0, 2, 3, 7, 8, 13], [1, 1, -1, 1, 1, 0, -1], 60)  # n = 1, 2, ...

if __name__ == "__main__":
    for n in range(1, NMAX + 1):
        words = list(product((0, 1), repeat=n))
        ldp = (brute(path, is_ld, n), sum(map(ld_word_path, words)), LD_PATH[n - 1])
        idp = (brute(path, is_id, n), sum(map(id_word_path, words)),
               id_transfer(n) if n >= 3 else ID_PATH[n - 1], ID_PATH[n - 1])
        assert len(set(ldp)) == 1, ("LD path", n, ldp)
        assert len(set(idp)) == 1, ("ID path", n, idp)
        if n >= 3:
            c = brute(cycle, is_ld, n)
            assert (c == A001642[n - 1]) == (n != 4), ("LD cycle", n, c)
        print(f"n={n:2d}  LD(P_n)={ldp[0]:6d}  ID(P_n)={idp[0]:5d}" + (f"  LD(C_n)={c:6d}" if n >= 3 else ""))
    for n in range(NMAX + 1, 40):  # transfer matrix vs recurrence beyond brute force
        assert id_transfer(n) == ID_PATH[n - 1]
    print("all checks passed; LD(C_n) = A001642(n) for 3 <= n <= %d except n = 4" % NMAX)
