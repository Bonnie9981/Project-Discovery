"""Check DISC-0029: compositions, largest parts and left-to-right maxima.

(1) A336482(n) = A102712(n) - A102712(n-1)   (n >= 1, A102712(0) = 0)
    refined: for each j >= 1, #{c |= n : the first part >= j equals j}
             = #{c |= n : max >= j} - #{c |= n-1 : max >= j}
(2) A119706(n) = A102712(n+1) - 2^n           (Mathar's 2025 conjecture)

Brute force over all compositions (as bit masks) for n <= N, plus the stored
OEIS terms when the offline snapshot is present.
"""
import sys
from pathlib import Path

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20


def compositions(n):
    """all compositions of n >= 1, via the n-1 cut bits"""
    for mask in range(1 << (n - 1)):
        parts, cur = [], 1
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(cur)
                cur = 1
            else:
                cur += 1
        parts.append(cur)
        yield parts


def records(c):
    r, m = 0, 0
    for x in c:
        if x > m:
            r, m = r + 1, x
    return r


def longest_ones(n, w):
    best = cur = 0
    for i in range(n):
        if w >> i & 1:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def first_ge_is(c, j):
    for x in c:
        if x >= j:
            return x == j
    return False


def fast(M):
    """L(n) = sum_j #{c |= n : max >= j} via N_j(n) = #{c |= n : all parts < j} (DP),
    and R(n) = sum_j B_j(n) with B_j(n) = sum_k N_j(k) C(n-k-j); checks the decomposition against the brute force."""
    C = [1] + [2 ** (m - 1) for m in range(1, M + 1)]
    L, R = [0] * (M + 1), [0] * (M + 1)
    for j in range(1, M + 1):
        Nj = [1] + [0] * M
        for n in range(1, M + 1):
            Nj[n] = sum(Nj[n - i] for i in range(1, min(j - 1, n) + 1))
        for n in range(1, M + 1):
            L[n] += C[n] - Nj[n]
            R[n] += sum(Nj[k] * C[n - k - j] for k in range(0, n - j + 1))
    return L, R


def main():
    L = {0: 0}
    R = {0: 0}
    for n in range(1, N + 2):
        cs = list(compositions(n))
        L[n] = sum(max(c) for c in cs)
        R[n] = sum(records(c) for c in cs)
        if n <= N:
            for j in range(1, n + 1):
                a = sum(1 for c in cs if max(c) >= j)
                b = 0 if n == 1 else sum(1 for c in compositions(n - 1) if max(c) >= j)
                assert sum(1 for c in cs if first_ge_is(c, j)) == a - b, (n, j)
    for n in range(1, N + 1):
        assert R[n] == L[n] - L[n - 1], n
        W = sum(longest_ones(n, w) for w in range(1 << n))
        assert W == L[n + 1] - 2 ** n, n
    out = "skipped (offline OEIS not fetched)"
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
        from discovery.relmine import parse
        from discovery.oeisdb import SRC
        got = []
        FL, FR = fast(80)
        assert FL[:N + 1] == [L[n] for n in range(N + 1)] and FR[:N + 1] == [R[n] for n in range(N + 1)]
        for n in range(1, 80):
            assert FR[n] == FL[n] - FL[n - 1], n
        for a, f in (("A102712", lambda n: FL[n]), ("A336482", lambda n: FR[n]),
                     ("A119706", lambda n: FL[n + 1] - 2 ** n)):
            p = SRC / "seq" / a[:4] / f"{a}.seq"
            _, terms, off, _, _ = parse(p.read_text())
            k = 0
            for i, v in enumerate(terms):
                n = off + i
                if n > 78:
                    break
                assert f(n) == v, (a, n)
                k += 1
            got.append(f"{a}:{k}")
        out = " ".join(got)
    except FileNotFoundError:
        pass
    print(f"n <= {N}: (1), refinement, (2) OK; OEIS terms compared: {out}")


if __name__ == "__main__":
    main()
