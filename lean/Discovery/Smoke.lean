import Mathlib

/-! P0-03 smoke test: Lean + Mathlib compile and the kernel accepts a proof. -/

theorem Discovery.smoke_infinitely_many_primes (n : ℕ) : ∃ p, n ≤ p ∧ Nat.Prime p :=
  Nat.exists_infinite_primes n
