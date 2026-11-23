# A counterexample to Coman's conjecture in OEIS A215944

Chi Hsia, 2026. Written with an LLM (Claude); the counterexample is checked in Lean 4 (core only).

**Conjecture (A215944, M. Coman, 2012).** The only Fermat pseudoprimes to base 2 (psp2) divisible by a smaller psp2 that cannot be written as p*((m+1)*p-m)*((n+1)*p-n), with m, n, p natural numbers, are multiples of 5461 of the form 5461*(42k-13).

**Counterexample.** N = 3048841 = 61 * 151 * 331 (it is a(36) in the b-file).

1. N is a psp2: 2^(N-1) == 1 (mod N). (Orders of 2: 60 mod 61, 15 mod 151, 30 mod 331; N-1 = 3048840 = 60 * 50814.)
2. N is divisible by the smaller psp2 49981 = 151 * 331 (A214305): 49980 is divisible by 15 and 30.
3. N is not of the stated form. Write N = p*A*B with A = p + m(p-1), B = p + n(p-1), m, n >= 1. Then A, B >= 2p-1 > p, so p^3 < N and p <= 145; p divides N, hence p = 61 (p = 1 gives the product 1). Then A*B = 49981 with A, B == 1 (mod 60) and A, B >= 121. The only divisors of 49981 = 151*331 are 1, 151, 331, 49981, and 151 == 31 (mod 60). Contradiction. (The argument does not need p, A, B to be prime.)
4. N is not a multiple of 5461 = 43 * 127.

**Smallest.** Among the 798 terms of A215944 below 10^10 (our list agrees with the b-file in count and sum), 211 violate the conjecture (including 5654273717 = 1093^2*4733, divisible by the psp 1093^2); 3048841 is the least. Allowing any number of prime factors, no psp2 below 3048841 violates it either.

**Reproduce.** `python -m discovery.cxsearch scan A215944` in https://github.com/Bonnie9981/Project-Discovery (psp2 list to 10^10 checked against A055550). Lean: `lean/Discovery/CxBatch1.lean`, theorem `a215944_counterexample`.

PARI check: `N=3048841; [factor(N), Mod(2,N)^(N-1), Mod(2,49981)^49980]`.
