"""DISC-0014 critic: third independent recomputation of A071052 and a(2n) = a(n) + 2n.

Does not import any project module. Two methods, both different from l07_a071052_even.py:
  M1: parity of trinomial coefficients via Lucas/Kummer: the multinomial n!/(a!b!c!) is odd
      iff a, b, c have pairwise disjoint binary digits. Coefficient of x^k in (1+x+x^2)^n
      mod 2 = number of such (a,b,c) with a+b+c = n, b+2c = k, mod 2.  (No simulation.)
  M2: dict-based Rule 150 simulation on absolute positions (no fixed window), also checks
      the row identity r_{2n}(2i) = r_n(i), r_{2n}(2i+1) = 0 cell by cell (H1).
  M3: A071053 = run-length transform of Jacobsthal 1,3,5,11,21,... (cross-check only).
Usage: python results/A071052/code/critic_c_a071052.py [N]
"""
import sys


def row_lucas(n):
    """Set of exponents k (0..2n) with odd coefficient in (1+x+x^2)^n."""
    bits = [1 << t for t in range(n.bit_length()) if n >> t & 1]
    par = {}
    # each set bit of n goes to exactly one of a (x^0), b (x^1), c (x^2)
    def rec(idx, k):
        if idx == len(bits):
            par[k] = par.get(k, 0) ^ 1
            return
        v = bits[idx]
        rec(idx + 1, k)          # to a
        rec(idx + 1, k + v)      # to b
        rec(idx + 1, k + 2 * v)  # to c
    rec(0, 0)
    return {k for k, p in par.items() if p}


def sim_rows(N):
    cur = {0}
    rows = [cur]
    for _ in range(N):
        cand = set()
        for i in cur:
            cand.update((i - 1, i, i + 1))
        cur = {i for i in cand if ((i - 1 in cur) + (i in cur) + (i + 1 in cur)) % 2}
        rows.append(cur)
    return rows


def jacobsthal_rlt(n):
    J = lambda L: (2 ** (L + 2) - (-1) ** (L + 2)) // 3  # 1,3,5,11,21 for L = 0..4
    prod, run = 1, 0
    while True:
        if n & 1:
            run += 1
        else:
            if run:
                prod *= J(run)
            run = 0
            if n == 0:
                break
        n >>= 1
    return prod


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    rows = sim_rows(N)
    z = []
    for n in range(N + 1):
        r = rows[n]
        assert all(-n <= i <= n for i in r), ("light cone", n)
        luc = {k - n for k in row_lucas(n)}  # shift exponent k to position k - n
        assert luc == r, ("M1 != M2", n)
        assert len(r) == jacobsthal_rlt(n), ("M3", n)
        z.append(2 * n + 1 - len(r))
    for n in range(N // 2 + 1):
        assert rows[2 * n] == {2 * i for i in rows[n]}, ("H1", n)
        assert z[2 * n] == z[n] + 2 * n, ("H3", n)
    print(f"OK N={N}: M1(Lucas)=M2(sim) rows, M3 counts; H1,H3 for n<={N // 2}; "
          f"first terms {z[:16]}")


if __name__ == "__main__":
    main()
