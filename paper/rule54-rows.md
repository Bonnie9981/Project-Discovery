# Rule 54 from a single ON cell: closed form of every row (A118109, A265225)

Chi Hsia, 2026. Proof and Lean 4 formalization generated with an LLM (Claude), attacked and
reviewed by separate AI agents, and machine-checked by Lean 4 in the repository's CI.
Nothing here is claimed to be new: the row pattern is visible in Wolfram's *A New Kind of
Science* (p. 55) and the decimal form is already in A118108. This note only supplies proofs
for the formulas that OEIS still marks as conjectures.

## Setup

Rule 54 maps the neighbourhoods 111, 110, ..., 000 to 0, 0, 1, 1, 0, 1, 1, 0. Checking the
eight cases, this is

  new(x) = old(x) XOR (old(x-1) OR old(x+1)).

Let R_t(x) be generation t, started from one ON cell at x = 0 on the infinite line.

**Lemma (rows).** R_t(x) = 1 exactly when |x| <= t and

- t even: x == t (mod 4);
- t odd: x != t+1 (mod 4).

So row t, read on the cells -t..t, is `1(0001)^(t/2)` for even t and `111(0111)^((t-1)/2)` for
odd t.

*Proof.* Induction on t; t = 0 is the seed. Assume the formula for row t and look at cell x.
Outside |x| <= t+1 everything is 0. Inside, the new value depends only on x mod 4 and on
whether x is at the edge, and the eight residue/edge cases check directly. For example, for
even t the ON cells are isolated and 4 apart, so a cell becomes ON iff it is ON or next to an
ON cell, giving the blocks `111` with one OFF cell at x == t+2 (mod 4); for odd t, an ON
cell with an ON neighbour turns OFF and an OFF cell with an ON neighbour turns ON, which
leaves exactly x == t+1 (mod 4) ON. (Lean: `C_step`, `row_eq`, proved by `omega`.) QED

Two consequences, both by comparing row t+2 with row t:

- cells -(t+2)..t-2 of row t+2 equal cells -t..t of row t (`shift`), and the last four cells
  are `0001` (t even) or `0111` (t odd) (`tail`);
- hence, for A118109 (the row read as a decimal numeral of 0/1 digits),
  a(t+2) = 10000*a(t) + e(t), with e = 1 (t even), 111 (t odd); a(0) = 1, a(1) = 111;
- and the number of ON cells is ones(t+2) = ones(t) + 1 or + 3, so
  ones(2k) = k+1 and ones(2k+1) = 3k+3.

## A118109

1. **a(n) = 10001*a(n-2) - 10000*a(n-4), n > 3.** Both a(n) - 10000*a(n-2) and
   a(n-2) - 10000*a(n-4) equal e(n), which depends only on the parity of n. (`a118109_rec`)
2. **G.f. (1+111*x)/((1-x)(1+x)(1-100*x)(1+100*x)).** The denominator is 1 - 10001*x^2 +
   10000*x^4, so this is item 1 together with a(0) = 1, a(1) = 111, a(2) = 10001, a(3) = 1110111.
3. **a(n) = floor((10000 + 1100*(n mod 2))*100^n/9999).** By induction with the step
   above, 9999*a(n) + e(n) = (10000 + 1100*(n mod 2))*100^n, and 0 < e(n) <= 111 < 9999.
   (`a118109_mul`, `a118109_floor`)

## A265225 (ON cells in rows 0..n)

Summing ones(t): a(2k) = 2k^2 + 3k + 1 = (2k+1)(k+1) and a(2k+1) = 2k^2 + 6k + 4 = (2k+2)(k+2)
(`a265225_even`, `a265225_odd`). Then, splitting by parity:

1. **a(n) = (n+1)*(2*n - (-1)^n + 5)/4** (`a265225_barker`).
2. **a(n) = a(n-1) + 2*a(n-2) - 2*a(n-3) - a(n-4) + a(n-5), n > 4** (`a265225_rec`), and the
   **g.f. (1+3*x)/((1-x)^3*(1+x)^2)**, whose denominator expands to
   1 - x - 2x^2 + 2x^3 + x^4 - x^5, with a(0..4) = 1, 4, 6, 12, 15 fixing the numerator.
3. **a(n) = n + 1 + (n+1)*floor((n+1)/2)** (`a265225_hurt`).
4. **a(n) = A093353(n) + n + 1**, where A093353 is defined by A093353(n) = (n + (n mod 2))*(n+1)/2 (its name in OEIS) (`a265225_veselovac`).

**Ianakiev's comment.** Choose n distinct numbers from 1..2n with sum divisible by n and
minimal. The comment says the minimum "seems" to equal a(n); it actually equals **a(n-1)**
(n = 1: the minimum is 1 = a(0), while a(1) = 4). Proof: the n-subsets of 1..2n have every
sum from n(n+1)/2 to n(3n+1)/2 (raise one element by 1 at a time). If n is odd, n | n(n+1)/2,
so the minimum is n(n+1)/2 = a(n-1). If n is even, n(n+1)/2 == n/2 (mod n), so the minimum is
n(n+1)/2 + n/2 = n(n+2)/2 <= n(3n+1)/2, which is again a(n-1) by the formula for odd index.
Equivalently, with n+1 numbers chosen from 1..2n+2 the minimum is exactly a(n).
(Paper proof only; brute force agrees for 1 <= n <= 11.)

## Checks

- Lean 4.15.0, core only (no Mathlib, no `native_decide`): `lean/Discovery/Rule54Rows.lean`.
  Every formula above except the two generating functions and Ianakiev's comment is a Lean
  theorem for all n; the g.f.s follow from the proved recurrences and initial terms.
- `results/A118109/code/l08_rule54_rows.py`: two row generators (rule-table simulation and the
  closed form) agree for n <= 300; all conjectured formulas, both g.f.s (series times
  denominator) and the DATA of A118109 and A265225 match.
