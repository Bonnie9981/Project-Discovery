# A counterexample to the conjecture in OEIS A362070

Chi Hsia, November 2026. Written with an LLM (Claude); the two values are checked in Lean 4.

## The sequence

For `n ≥ 1` and `k ≥ 1` let `m_min(n, k)` be the least `m ≥ 1` such that `n` divides
`∏_{t=1..m} t(t+1)⋯(t+k−1)`, and let `K(n)` be the Kempner number (least `K` with `n | K!`).
A362070 is `a(n) = Σ_{r=1..K(n)} m_min(n, r)`.
The entry (Ratajczak, 2023) conjectures that `a(n) = a(n+1)` has no solutions.

## The counterexample

`a(1715) = a(1716) = 91`.

**n = 1716 = 2^2·3·11·13.** `K(1716) = 13`. For `r ≤ 13` the product
`∏_{t=1..m} t⋯(t+r−1)` contains the factor 13 only once its last block reaches 13,
i.e. only when `m + r − 1 ≥ 13`; at that point the factors 4, 3, 11 are present too.
So `m_min(1716, r) = 14 − r` and `a(1716) = 13 + 12 + ⋯ + 1 = 91`.

**n = 1715 = 5·7^3.** `K(1715) = 21` (`7^3 | 21!` and not `20!`). The values
`m_min(1715, r)` for `r = 1, …, 21` are

`21, 13, 7, 6, 5, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1`,

whose sum is 91. (For example `r = 2`: the power of 7 in `∏_{t=1..m} t(t+1)` is
`v_7(m!) + v_7((m+1)!)`, which first reaches 3 at `m = 13`.)

## Checks

- Lean 4 (core only, no `native_decide`): `Discovery.A362070Counter.a362070_counterexample`
  states the definition literally, proves that it defines a single value, and checks by kernel
  computation that `a(1715) = 91` and `a(1716) = 91`
  ([source](https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/A362070Counter.lean)).
- The Maxima program in the entry itself returns `a(1715) = a(1716) = 91`.
- Two further independent programs (the definition with big integers; a sieve using
  per-prime valuations) agree with the entry's DATA for `n ≤ 57` and give the same values.
- A sieve over all `n ≤ 10^10` finds no other `n` with `a(n) = a(n+1)`; so 1715 is the least
  solution and the only one below `10^10`.

Code: <https://github.com/Bonnie9981/Project-Discovery/tree/main/results/A362070/code>.
