# A085588: the eventual period divides 2^A007814(n) * (2^A309786(n) - 1)

Chi Hsia, November 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked; see the AI-use note at the end.

## Statement

Let F be one step of the elementary cellular automaton Rule 150, new(i) = old(i-1) XOR old(i) XOR old(i+1), on a ring of n cells. A085588(n) is the eventual period of the orbit of a single ON cell. Write n = 2^D * m with m odd (D = A007814(n)) and let s = A309786(n), the least s >= 1 with 2^s == +-1 (mod m).

**Theorem.** For every ring state x, F^(2^D + 2^D*(2^s-1))(x) = F^(2^D)(x). Hence every orbit is periodic after at most 2^D steps and its eventual period divides 2^D*(2^s-1). In particular

a(n) divides 2^A007814(n) * (2^A309786(n) - 1).

This is the direction that holds. The comment in the entry (Aug 2024) states the opposite divisibility, "2^A007814(n) * (2^A309786(n) - 1) divides a(n)", which is false: a(4) = 2 while 2^2 * (2^1 - 1) = 4, and a(13) = 21 while 2^0 * (2^6 - 1) = 63. The b-file has 174 such n <= 1000; they agree with the n the comment lists as having a(n) != 2^A007814(n) * (2^A309786(n) - 1).

## Proof

Write G_a(x)(i) = x(i-a) XOR x(i) XOR x(i+a), so F = G_1.

1. G_a(G_a(x)) = G_{2a}(x): in the double sum x(i-a) and x(i+a) appear twice and x(i) three times. By induction F^(2^j) = G_{2^j}. (Equivalently (x^-1 + 1 + x)^(2^j) = x^(-2^j) + 1 + x^(2^j) over GF(2).)
2. 2^D + 2^D*(2^s-1) = 2^(D+s). If 2^s = 1 + c*m then 2^(D+s) = 2^D + c*n; if 2^s = c*m - 1 then 2^(D+s) = -2^D + c*n. On the ring, G_a depends only on a modulo n and G_a = G_{-a}. So F^(2^(D+s)) = G_{2^(D+s)} = G_{2^D} = F^(2^D).
3. If p is the eventual period and F^(K+p)(x) = F^K(x), F^(K+P)(x) = F^K(x) with P = 2^D*(2^s-1), then r = P mod p also satisfies F^(K+r)(x) = F^K(x); minimality of p forces r = 0. QED

The argument is the Frobenius argument that the entry attributes to Martin, Odlyzko and Wolfram (Theorem 3.5, Rule 90); nothing new is claimed beyond correcting the comment and providing a checked proof. Only s with m | 2^s - 1 or m | 2^s + 1 is used, not minimality.

## On the second comment (a(n) = n only if n is in A115770)

Not proved here. Partial facts: by the theorem, a(n) = n implies m | 2^s - 1. Every n = 2^i * (2^j - 1) with j >= 3 is in A115770 (for k = 2^j - 1 the carryless product 11 (x) k = k XOR 2k XOR 8k equals 7k), and for n <= 1000 the n with a(n) = n are exactly 7, 14, 15, 28, 30, 31, ... , all of that form. Proving "a(n) = n implies the odd part of n is 2^j - 1" would suffice (it is not equivalent: A115770 also contains 455, 903, 910, ...), and is not done here. The comment says the converse first fails at 445; 445 is not in A115770, and the first such n appears to be 455 (a(455) = 4095).

## Checks

- Lean 4 (core only, no Mathlib): `lean/Discovery/A085588Period.lean`, theorems `a085588_dvd` (single cell) and `any_state_dvd` (any state), for all n; axioms used: propext, Quot.sound.
- `results/A085588/code/l08_a085588_period.py`: the identity on random states for n <= 400; a(n) by two different algorithms (exact order using fast operator powers; plain simulation with a table of seen states) for n <= 200, matching the DATA; the literal comment fails first at n = 4 and 13.
- All 998 b-file terms (n = 3..1000) satisfy a(n) | 2^D*(2^s-1) (checked in a browser with `results/A085588/code/bfile_check.js`).
- An independent critic script (`results/A085588/code/critic_c_a085588.py`, plain powers in GF(2)[x]/(x^n-1)) agrees for n <= 200.

## AI-use note

The proof, the Lean formalization and the checking programs were produced with Claude (Anthropic) under the author's direction, attacked and reviewed by separate AI agents (records/DISC-0016/critic.md, review.md), and machine-checked by Lean 4 in the repository's CI. The author is responsible for the submission.
