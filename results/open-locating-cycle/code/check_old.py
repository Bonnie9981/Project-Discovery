"""Open-locating-dominating (OLD) sets in paths and cycles: brute force vs formulas.

Standard library only. Run: python check_old.py

S is OLD if N(v) & S is nonempty and different for every vertex v (N(v) = neighbours, v itself excluded).
Claims checked for n <= NMAX:
  cycles: OLD(C_n) = A001609(n) for odd n >= 3, A001609(n/2)^2 for even n >= 6, OLD(C_4) = 0;
  paths:  OLD(P_2k) = A000930(k)^2 (k >= 1), OLD(P_2k+1) = A000930(k+3)*A000930(k-2) (k >= 2).
A001609 and A000930 are rebuilt here from their recurrences (OEIS offsets 1 and 0).
"""
NMAX = 20


def path(n):
    return [{j for j in (i - 1, i + 1) if 0 <= j < n} for i in range(n)]


def cycle(n):
    return [{(i - 1) % n, (i + 1) % n} for i in range(n)]


def is_old(adj, S):
    seen = set()
    for v in range(len(adj)):
        t = frozenset(adj[v] & S)
        if not t or t in seen:
            return False
        seen.add(t)
    return True


def brute(graph, n):
    adj = graph(n)
    return sum(is_old(adj, {i for i in range(n) if m >> i & 1}) for m in range(1 << n))


def A000930(k):  # a(0)=a(1)=a(2)=1, a(n)=a(n-1)+a(n-3)
    a = [1, 1, 1]
    while len(a) <= k:
        a.append(a[-1] + a[-3])
    return a[k]


def A001609(n):  # a(1)=a(2)=1, a(3)=4, a(n)=a(n-1)+a(n-3)
    a = [None, 1, 1, 4]
    while len(a) <= n:
        a.append(a[-1] + a[-3])
    return a[n]


def old_cycle(n):
    if n == 4:
        return 0
    return A001609(n) if n % 2 else A001609(n // 2) ** 2


def old_path(n):
    k = n // 2
    if n % 2 == 0:
        return A000930(k) ** 2
    return A000930(k + 3) * A000930(k - 2) if k >= 2 else brute(path, n)


if __name__ == "__main__":
    for n in range(1, NMAX + 1):
        p = brute(path, n)
        assert p == old_path(n), ("path", n, p, old_path(n))
        line = f"n={n:2d}  OLD(P_n)={p:5d}"
        if n >= 3:
            c = brute(cycle, n)
            assert c == old_cycle(n), ("cycle", n, c, old_cycle(n))
            line += f"  OLD(C_n)={c:5d}"
        print(line)
    print("all checks passed")
