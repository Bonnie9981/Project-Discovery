import Mathlib

/-!
# R-001 formal results (DISC-0002)

Context (not formalised here): for a prime `p`, Q_p says `n^2 + n + p` is prime for all `n ≤ p - 2`.
The theorems below are H1 (boundary), H2 (Euler's 40 primes) and H3 (failure at n = 40).
-/

namespace Discovery.R001

/-- At `n = p - 1` the quadratic equals `p^2`. -/
theorem boundary_eq (p : ℕ) (hp : 1 ≤ p) : (p - 1) ^ 2 + (p - 1) + p = p ^ 2 := by
  obtain ⟨k, rfl⟩ : ∃ k, p = k + 1 := ⟨p - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  ring

/-- So no `p ≥ 2` can make `n^2 + n + p` prime at `n = p - 1`:
the range `n ≤ p - 2` in Q_p is the longest possible. -/
theorem boundary_not_prime (p : ℕ) (hp : 2 ≤ p) :
    ¬ Nat.Prime ((p - 1) ^ 2 + (p - 1) + p) := by
  rw [boundary_eq p (by omega)]
  intro h
  rw [sq] at h
  rcases Nat.prime_mul_iff.mp h with ⟨_, h1⟩ | ⟨_, h1⟩ <;> omega

/-- Euler's polynomial: `n^2 + n + 41` is prime for `n = 0, …, 39`. -/
theorem euler41 : ∀ n < 40, Nat.Prime (n ^ 2 + n + 41) := by
  intro n hn
  interval_cases n <;> norm_num

/-- …and fails at `n = 40`, where it equals `41^2`. -/
theorem euler41_fails : ¬ Nat.Prime (40 ^ 2 + 40 + 41) := by
  norm_num

end Discovery.R001
