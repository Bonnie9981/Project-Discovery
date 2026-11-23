/-!
# DISC-0022: a counterexample to the conjecture in A073631 / A130058

OEIS A073631: nonprimes `k` such that `k ∣ 3^(k-1) - 2^(k-1)`.
Conjecture (Alexander Adamchuk, 2007, in A073631 and A130058):
all nonsquarefree terms are multiples of `23^2`; also "it appears that 1 and 529
are the only perfect squares" in the sequence.

`q = 3842760169` is a Wieferich prime to base 3/2 (A376896), so `k = q^2` satisfies
`3^(k-1) ≡ 2^(k-1) (mod k)`. It is a perfect square, not squarefree, not prime,
and not a multiple of `529`. The same holds for `41975417117^2`.

We check the congruences by kernel computation with the binary exponentiation
`powModAux` (copied from `CxBatch1`), proved equal to `b ^ e % m` by `powModAux_eq`.
Primality of `q` is not needed: `k = q * q` with `q ≥ 2` is already nonprime and
nonsquarefree. Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A073631Counter

/-- Binary modular exponentiation with fuel. With fuel 0 it falls back to the definition. -/
def powModAux : Nat → Nat → Nat → Nat → Nat
  | 0, b, e, m => b ^ e % m
  | f + 1, b, e, m =>
    if e = 0 then 1 % m
    else if e % 2 = 1 then powModAux f (b * b % m) (e / 2) m * b % m
    else powModAux f (b * b % m) (e / 2) m

theorem pow_mod' (a k m : Nat) : (a % m) ^ k % m = a ^ k % m := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Nat.pow_succ, Nat.pow_succ, Nat.mul_mod, ih, Nat.mod_mod, ← Nat.mul_mod]

theorem powModAux_eq (f b e m : Nat) : powModAux f b e m = b ^ e % m := by
  induction f generalizing b e with
  | zero => rfl
  | succ f ih =>
    simp only [powModAux, ih]
    have hsplit : b ^ e = (b * b) ^ (e / 2) * b ^ (e % 2) := by
      rw [← Nat.pow_two, ← Nat.pow_mul, ← Nat.pow_add, Nat.div_add_mod]
    have hsq : (b * b % m) ^ (e / 2) % m = (b * b) ^ (e / 2) % m := by
      rw [pow_mod']
    split
    · subst ‹e = 0›; simp
    · split
      · rename_i h
        rw [hsq, hsplit, h, Nat.pow_one, Nat.mul_mod, Nat.mod_mod, ← Nat.mul_mod]
      · rename_i h
        have h0 : e % 2 = 0 := by omega
        rw [hsq, hsplit, h0, Nat.pow_zero, Nat.mul_one]

/-- `k` satisfies the defining divisibility of A073631: `k ∣ 3^(k-1) - 2^(k-1)`,
written as equality of residues (`3^(k-1) ≥ 2^(k-1)`, so this is the same thing). -/
def InSeq (k : Nat) : Prop := 3 ^ (k - 1) % k = 2 ^ (k - 1) % k

def q1 : Nat := 3842760169
def q2 : Nat := 41975417117

/-- `q1` is a Wieferich prime to base 3/2: `3^(q1-1) ≡ 2^(q1-1) (mod q1^2)`. -/
theorem wieferich_q1 : 3 ^ (q1 - 1) % (q1 * q1) = 2 ^ (q1 - 1) % (q1 * q1) := by
  rw [← powModAux_eq 40, ← powModAux_eq 40]; decide

theorem wieferich_q2 : 3 ^ (q2 - 1) % (q2 * q2) = 2 ^ (q2 - 1) % (q2 * q2) := by
  rw [← powModAux_eq 40, ← powModAux_eq 40]; decide

/-- `k = q1^2 = 14766805716452908561` satisfies the defining congruence of A073631. -/
set_option maxRecDepth 100000 in
theorem inSeq_q1_sq : InSeq (q1 * q1) := by
  unfold InSeq
  rw [← powModAux_eq 66, ← powModAux_eq 66]; decide

set_option maxRecDepth 100000 in
theorem inSeq_q2_sq : InSeq (q2 * q2) := by
  unfold InSeq
  rw [← powModAux_eq 74, ← powModAux_eq 74]; decide

/-- The counterexample: `k = q1 * q1` is in A073631 (nonprime because `1 < q1 < k`
and `q1 ∣ k`), it is a perfect square, it is divisible by the square `q1^2` with
`q1 ≥ 2` (so not squarefree), and it is not a multiple of `23^2 = 529`. -/
theorem a073631_counterexample :
    q1 * q1 = 14766805716452908561 ∧ InSeq (q1 * q1) ∧
    1 < q1 ∧ q1 < q1 * q1 ∧ (q1 * q1) % q1 = 0 ∧
    (q1 * q1) % 529 ≠ 0 := by
  refine ⟨by decide, inSeq_q1_sq, by decide, by decide, by decide, by decide⟩

theorem a073631_counterexample2 :
    q2 * q2 = 1761935642146136591689 ∧ InSeq (q2 * q2) ∧
    1 < q2 ∧ q2 < q2 * q2 ∧ (q2 * q2) % q2 = 0 ∧
    (q2 * q2) % 529 ≠ 0 := by
  refine ⟨by decide, inSeq_q2_sq, by decide, by decide, by decide, by decide⟩

/-- Sanity check against the DATA: `529 = 23^2` is a term. -/
theorem inSeq_529 : InSeq 529 := by
  unfold InSeq
  rw [← powModAux_eq 20, ← powModAux_eq 20]; decide

end Discovery.A073631Counter
