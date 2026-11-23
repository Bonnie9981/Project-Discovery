# A counterexample to Ratajczak's conjecture in OEIS A134559

Chi Hsia, November 2026. Written with an LLM (Claude); the counterexample is checked in Lean 4.

## The conjecture

For `n ≥ 1` and `0 ≤ k ≤ ⌈n/2⌉ − 1` let `b_n(k)` be the sum of all `u` with `1 ≤ u ≤ n`
and `n mod u = k` (equivalently `b_n(k) = T(n−k, k+1)`, the sum of the divisors of `n−k`
that are `≥ k+1`), and let `P(n) = ∏_{k=0}^{⌈n/2⌉−1} b_n(k)`.
A comment in A134559 (Ratajczak, 2019) conjectures that the `n` with

    gcd(P(n), n) = 1   and   gcd(P(n+1), n+1) = 2                      (*)

are exactly the terms of A005383 (primes `p` with `(p+1)/2` prime) other than 3 and 5.
It was checked for 2000 consecutive integers.

## The counterexample

`p = 4933` is prime and `(p+1)/2 = 2467` is prime, so `4933` is in A005383.
But `b_4934(134)` is the sum of the divisors of `4934 − 134 = 4800` that exceed 134, namely

    150 + 160 + 192 + 200 + 240 + 300 + 320 + 400 + 480 + 600 + 800 + 960 + 1200 + 1600 + 2400 + 4800 = 14802 = 6 · 2467,

and `b_4934(0) = σ(4934) = 7404` is even. Hence `4934 | P(4934)`, so
`gcd(P(4934), 4934) = 4934 ≠ 2` and `4933` does not satisfy (*).
It is the smallest such prime. Up to `1.5 · 10^5` the terms of A005383 (without 3, 5) that fail (*)
are 4933, 6997, 11113, 48673, 50341, 54217, 92941; for 54217 the failure is on the other side,
`gcd(P(54217), 54217) = 54217`, which the comment itself names as the way the conjecture could fail.

## The other half is true

**Lemma.** Let `N ≥ 2` and `N/2 < m ≤ 2N/3`. Then `k = N − m` is an admissible index and `b_N(k) = m`.

*Proof.* `k < N/2`, so `k ≤ ⌈N/2⌉ − 1`. A number `u ≤ N` has `N mod u = k` iff `u > k` and `u | m`.
`u = m` qualifies since `m > N/2 > k`. Any other divisor of `m` is at most `m/2 ≤ N − m = k`
(this is `m ≤ 2N/3`), so it does not qualify. ∎

So if `d ≥ 2` divides `N` and `d ≤ N/6`, the interval `(N/2, 2N/3]` (length `N/6`) contains a
multiple `m` of `d`, and `d | b_N(N − m) | P(N)`; thus `d | gcd(P(N), N)`.

**Theorem.** Every `n` satisfying (*) is in A005383 and differs from 3 and 5.

*Proof.* For `n < 36` this is a direct check. Let `n ≥ 36`.
If `n` were composite, its least prime factor `q ≤ √n ≤ n/6` would divide `gcd(P(n), n)`; so `n` is prime.
Let `N = n + 1`, even. If `4 | N` then `4 ≤ N/6` divides `gcd(P(N), N)`, which is not 2; so `N = 2M`
with `M` odd. If `M` were composite, its least prime factor `q ≤ √(N/2) ≤ N/6` would divide
`gcd(P(N), N)` together with 2; so `M = (n+1)/2` is prime. ∎

So the solutions of (*) form a subset of A005383, but a proper one.

## Checks

- Lean 4 (core only, no `native_decide`): `Discovery.A134559Counter.a134559_counterexample`
  states `b` and `P` literally and checks by kernel computation that 4933 and 2467 are prime and
  `gcd(P(4934), 4934) = 4934`
  ([source](https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/A134559Counter.lean)).
- A C program using the `n mod u` definition scans all `n ≤ 1.5 · 10^5`: it finds no `n` outside
  A005383 satisfying (*), and exactly the seven failures listed above. A separate Python program using
  the divisor form `T(n−k, k+1)` recomputes the three cases `n + 1 = 4934, 6998, 11114`.
  An independent reviewer's program (antidiagonal recursion) reproduces the full scan and extends it
  to `3 · 10^5`, adding the failures 161221, 172573, 242533.

Code: <https://github.com/Bonnie9981/Project-Discovery/tree/main/results/A134559/code>.
