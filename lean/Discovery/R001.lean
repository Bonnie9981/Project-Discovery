import Mathlib

/-!
# R-001 formal results (DISC-0002)

Family: for a prime `p`, the statement `Q p` says `n^2 + n + p` is prime for all `n ≤ p - 2`.
-/

namespace Discovery.R001

/-- At `n = p - 1` the quadratic equals `p^2`. -/
theorem boundary_eq (p : ℕ) (hp : 1 ≤ p) : (p - 1) ^ 2 + (p - 1) + p = p ^ 2 := by
  obtain ⟨k, rfl⟩ : ∃ k, p = k + 1 := ⟨p - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  ring

/-- So no `p ≥ 2` can make `n^2 + n + p` prime at `n = p - 1`:
the range `n ≤ p - 2` in `Q p` is the longest possible. -/
theorem boundary_not_prime (p : ℕ) (hp : 2 ≤ p) :
    ¬ Nat.Prime ((p - 1) ^ 2 + (p - 1) + p) := by
  rw [boundary_eq p (by omega)]
  exact Nat.Prime.pow_not_prime (le_refl 2)

/-- Euler's polynomial: `n^2 + n + 41` is prime for `n = 0, …, 39`. -/
theorem euler41 : ∀ n < 40, Nat.Prime (n ^ 2 + n + 41) := by
  intro n hn
  interval_cases n <;> norm_num

/-- …and fails at `n = 40`, where it equals `41^2`. -/
theorem euler41_fails : ¬ Nat.Prime (40 ^ 2 + 40 + 41) := by
  norm_num

end Discovery.R001
