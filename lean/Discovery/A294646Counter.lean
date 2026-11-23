/-!
# DISC-0017: OEIS A294646, the conjecture "a(n) is never 2n-2" is false

A294646(n) = (1/2)^(2n) mod (2n+1), i.e. (entry comment) the smallest `k > 0` with
`k * 2^(2n) ≡ 1 (mod 2n+1)`.  The entry's comment (Israel & Ordowski, 2017) conjectures
"a(n) is never 2 or 2n or 2n-2".

Here we check in the kernel that for `n = 9814447404` (so `2n+1 = 19628894809 = 367 * 53484727`)
`(2n-2) * 2^(2n) ≡ 1 (mod 2n+1)`, hence `a(n) = 2n-2` (`a294646_counterexample`).
Equivalently `2n+1` divides `3 * 2^(2n) + 1` (`dvd_three_pow_add_one`).

`2^(2n) mod (2n+1)` is computed with binary exponentiation `powModAux`, proved equal to
`b ^ e % m` for every fuel value (`powModAux_eq`), so `decide` only evaluates small numbers.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A294646Counter

/-- Binary modular exponentiation with fuel. With fuel 0 it falls back to the definition. -/
def powModAux : Nat → Nat → Nat → Nat → Nat
  | 0, b, e, m => b ^ e % m
  | f + 1, b, e, m =>
    if e = 0 then 1 % m
    else if e % 2 = 1 then powModAux f (b * b % m) (e / 2) m * b % m
    else powModAux f (b * b % m) (e / 2) m

theorem mul_mod_mod' (a b m : Nat) : a * (b % m) % m = a * b % m := by
  rw [Nat.mul_mod, Nat.mod_mod, ← Nat.mul_mod]

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

/-- The witness: `n = 9814447404`, `2n+1 = 19628894809 = 367 * 53484727`. -/
def N : Nat := 9814447404

theorem modulus_factor : 2 * N + 1 = 367 * 53484727 := by decide

/-- Kernel check: `(2N-2) * 2^(2N) ≡ 1 (mod 2N+1)`. -/
theorem key : (2 * N - 2) * 2 ^ (2 * N) % (2 * N + 1) = 1 := by
  rw [Nat.mul_mod, ← powModAux_eq 64]
  decide

/-- Same fact in the form `2n+1 | 3 * 2^(2n) + 1`. -/
theorem dvd_three_pow_add_one : (3 * 2 ^ (2 * N) + 1) % (2 * N + 1) = 0 := by
  rw [Nat.add_mod, Nat.mul_mod, ← powModAux_eq 64]
  decide

/-- Inverses mod `m` are unique below `m`. -/
theorem inv_unique (m x c k : Nat) (hc : c < m) (hk : k < m)
    (h1 : c * x % m = 1) (h2 : k * x % m = 1) : k = c := by
  have : k % m = c % m := by
    calc k % m = k * (c * x % m) % m := by rw [h1, Nat.mul_one]
      _ = k * (c * x) % m := by rw [mul_mod_mod']
      _ = c * (k * x) % m := by rw [Nat.mul_left_comm]
      _ = c * (k * x % m) % m := by rw [mul_mod_mod']
      _ = c % m := by rw [h2, Nat.mul_one]
  rwa [Nat.mod_eq_of_lt hk, Nat.mod_eq_of_lt hc] at this

/-- `k` is A294646(n): the smallest `k > 0` with `k * 2^(2n) ≡ 1 (mod 2n+1)`. -/
def IsA294646 (n k : Nat) : Prop :=
  0 < k ∧ k * 2 ^ (2 * n) % (2 * n + 1) = 1 ∧
    ∀ j, 0 < j → j < k → j * 2 ^ (2 * n) % (2 * n + 1) ≠ 1

/-- The counterexample: A294646(9814447404) = 2 * 9814447404 - 2. -/
theorem a294646_counterexample : IsA294646 N (2 * N - 2) := by
  refine ⟨by decide, key, ?_⟩
  intro j hj hlt hj1
  have hN : N = 9814447404 := rfl
  have := inv_unique (2 * N + 1) (2 ^ (2 * N)) (2 * N - 2) j
    (by omega) (by omega) key hj1
  omega

end Discovery.A294646Counter
