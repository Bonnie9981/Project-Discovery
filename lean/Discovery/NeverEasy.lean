/-!
# DISC-0018: three OEIS "a(n) is never ..." conjectures with one-line proofs

* A231897: a(n) = smallest m with wt(m^2) = n, "or -1 if no such m exists".
  Conjecture (2013): a(n) is never -1.
  Proof: wt((2^a - 1)^2) = a, because (2^a - 1)^2 = (2^(a-1) - 1) * 2^(a+1) + 1.
  (`wt_sq_two_pow_sub_one`, `a231897_exists`; also gives a(n) <= 2^n - 1.)

* A215462: number of ordered ways to write 2n = x + y with x, y odd nonprimes (1 counts).
  Conjecture (2012, "verified to 10^9"): a(n) is never 0 for n > 19.
  Proof: 2n = 9 + (2n-9), 25 + (2n-25) or 35 + (2n-35) according to 2n mod 6;
  the second summand is an odd multiple of 3 that is at least 9. (`a215462_pos`)

* A215461: number of ordered ways to write 2n = p + c, p odd prime, c odd nonprime.
  Conjecture (2012, "verified to 10^9"): a(n) is never 0 for n > 5.
  Proof: one of 2n-3, 2n-5, 2n-7 is a multiple of 3, and for n >= 6 it is at least 9. (`a215461_pos`)

Only core Lean is used (no Mathlib, no `native_decide`).  Primality is the plain
definition `IsPrime p := 2 <= p ∧ ∀ d, d ∣ p → d = 1 ∨ d = p`.
-/

namespace Discovery.NeverEasy

/-! ## Binary weight -/

/-- Number of 1's in the binary expansion (A000120). -/
def wt : Nat → Nat
  | 0 => 0
  | n + 1 => (n + 1) % 2 + wt ((n + 1) / 2)
decreasing_by omega

theorem wt_zero : wt 0 = 0 := by rw [wt]

theorem wt_double (x : Nat) : wt (2 * x) = wt x := by
  cases x with
  | zero => rfl
  | succ k =>
    have h : 2 * (k + 1) = (2 * k + 1) + 1 := by omega
    rw [h, wt]
    have h1 : (2 * k + 1 + 1) % 2 = 0 := by omega
    have h2 : (2 * k + 1 + 1) / 2 = k + 1 := by omega
    rw [h1, h2, Nat.zero_add]

theorem wt_double_add_one (x : Nat) : wt (2 * x + 1) = wt x + 1 := by
  rw [wt]
  have h1 : (2 * x + 1) % 2 = 1 := by omega
  have h2 : (2 * x + 1) / 2 = x := by omega
  rw [h1, h2, Nat.add_comm]

theorem wt_mul_two_pow (x k : Nat) : wt (x * 2 ^ k) = wt x := by
  induction k with
  | zero => rw [Nat.pow_zero, Nat.mul_one]
  | succ k ih =>
    have h : x * 2 ^ (k + 1) = 2 * (x * 2 ^ k) := by
      rw [Nat.pow_succ]; rw [Nat.mul_comm 2, Nat.mul_assoc]
    rw [h, wt_double, ih]

theorem wt_two_pow_sub_one (a : Nat) : wt (2 ^ a - 1) = a := by
  induction a with
  | zero => exact wt_zero
  | succ a ih =>
    have hp : 1 ≤ 2 ^ a := Nat.one_le_two_pow
    have h : 2 ^ (a + 1) - 1 = 2 * (2 ^ a - 1) + 1 := by
      rw [Nat.pow_succ]; omega
    rw [h, wt_double_add_one, ih]

/-- (2^(b+1) - 1)^2 = (2^b - 1) * 2^(b+2) + 1. -/
theorem sq_identity (b : Nat) :
    (2 ^ (b + 1) - 1) * (2 ^ (b + 1) - 1) = (2 ^ b - 1) * 2 ^ (b + 2) + 1 := by
  have hp : 1 ≤ 2 ^ b := Nat.one_le_two_pow
  obtain ⟨t, ht⟩ : ∃ t, 2 ^ b = t + 1 := ⟨2 ^ b - 1, by omega⟩
  have e1 : 2 ^ (b + 1) = 2 * (t + 1) := by rw [Nat.pow_succ, ht, Nat.mul_comm]
  have e2 : 2 ^ (b + 2) = 4 * (t + 1) := by
    rw [Nat.pow_succ, Nat.pow_succ, ht]; rw [Nat.mul_assoc, Nat.mul_comm]
  rw [e1, e2, ht]
  have l : 2 * (t + 1) - 1 = 2 * t + 1 := by omega
  have r : t + 1 - 1 = t := by omega
  rw [l, r]
  -- (2t+1)^2 = t * (4t + 4) + 1
  simp only [Nat.mul_add, Nat.add_mul, Nat.mul_one, Nat.one_mul]
  have a1 : 2 * t * (2 * t) = t * t * 4 := by
    simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
  have a2 : t * (4 * t) = t * t * 4 := by
    simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
  rw [a1, a2]
  omega

/-- wt((2^a - 1)^2) = a for every a. -/
theorem wt_sq_two_pow_sub_one (a : Nat) : wt ((2 ^ a - 1) * (2 ^ a - 1)) = a := by
  cases a with
  | zero => exact wt_zero
  | succ b =>
    rw [sq_identity]
    have h : (2 ^ b - 1) * 2 ^ (b + 2) + 1 = 2 * ((2 ^ b - 1) * 2 ^ (b + 1)) + 1 := by
      rw [Nat.pow_succ 2 (b + 1)]
      rw [Nat.mul_comm (2 ^ (b + 1)) 2, ← Nat.mul_assoc, Nat.mul_comm (2 ^ b - 1) 2,
        Nat.mul_assoc]
    rw [h, wt_double_add_one, wt_mul_two_pow, wt_two_pow_sub_one]

/-- A231897 is never -1: for every n some m has wt(m^2) = n, and one can take m <= 2^n - 1. -/
theorem a231897_exists (n : Nat) : ∃ m, m ≤ 2 ^ n - 1 ∧ wt (m * m) = n :=
  ⟨2 ^ n - 1, Nat.le_refl _, wt_sq_two_pow_sub_one n⟩

/-! ## Sums of two odd numbers -/

/-- `x` is not prime in the OEIS sense used by A215461/A215462 (1 counts as nonprime):
it is 1 or has a divisor strictly between 1 and x. -/
def NonPrime (x : Nat) : Prop := x = 1 ∨ ∃ d, 1 < d ∧ d < x ∧ x % d = 0

/-- Plain primality. -/
def IsPrime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d ∣ p → d = 1 ∨ d = p

theorem nonprime_of_three (x : Nat) (h9 : 9 ≤ x) (h3 : x % 3 = 0) : NonPrime x :=
  Or.inr ⟨3, by omega, by omega, h3⟩

theorem nonprime_of_five (x : Nat) (h9 : 9 ≤ x) (h5 : x % 5 = 0) : NonPrime x :=
  Or.inr ⟨5, by omega, by omega, h5⟩

/-- Every even number 2n with n > 19 (2n >= 40) is a sum of two odd nonprimes,
so A215462(n) > 0 for n > 19. -/
theorem a215462_pos (n : Nat) (hn : 19 < n) :
    ∃ x y, x + y = 2 * n ∧ x % 2 = 1 ∧ y % 2 = 1 ∧ NonPrime x ∧ NonPrime y := by
  have hm : (2 * n) % 6 = 0 ∨ (2 * n) % 6 = 2 ∨ (2 * n) % 6 = 4 := by omega
  rcases hm with h | h | h
  · exact ⟨9, 2 * n - 9, by omega, by omega, by omega,
      nonprime_of_three 9 (by omega) (by omega), nonprime_of_three _ (by omega) (by omega)⟩
  · -- 2n ≡ 2 (mod 6) and 2n ≥ 40 force 2n ≥ 44
    exact ⟨35, 2 * n - 35, by omega, by omega, by omega,
      nonprime_of_five 35 (by omega) (by omega), nonprime_of_three _ (by omega) (by omega)⟩
  · exact ⟨25, 2 * n - 25, by omega, by omega, by omega,
      nonprime_of_five 25 (by omega) (by omega), nonprime_of_three _ (by omega) (by omega)⟩

theorem dvd_le' {d p : Nat} (h : d ∣ p) (hp : 0 < p) : d ≤ p := Nat.le_of_dvd hp h

theorem prime_small (p : Nat) (hp : p = 3 ∨ p = 5 ∨ p = 7) : IsPrime p := by
  refine ⟨by omega, fun d hd => ?_⟩
  have hle : d ≤ p := Nat.le_of_dvd (by omega) hd
  have hmod : p % d = 0 := Nat.mod_eq_zero_of_dvd hd
  rcases hp with rfl | rfl | rfl
  all_goals
    (have : d = 0 ∨ d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 ∨ d = 5 ∨ d = 6 ∨ d = 7 := by omega
     rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp_all)

/-- Every even number 2n with n > 5 is p + c with p an odd prime (3, 5 or 7) and c an odd
nonprime, so A215461(n) > 0 for n > 5. -/
theorem a215461_pos (n : Nat) (hn : 5 < n) :
    ∃ p c, p + c = 2 * n ∧ p % 2 = 1 ∧ c % 2 = 1 ∧ IsPrime p ∧ NonPrime c := by
  have hm : (2 * n) % 3 = 0 ∨ (2 * n) % 3 = 1 ∨ (2 * n) % 3 = 2 := by omega
  rcases hm with h | h | h
  · exact ⟨3, 2 * n - 3, by omega, by omega, by omega, prime_small 3 (by omega),
      nonprime_of_three _ (by omega) (by omega)⟩
  · exact ⟨7, 2 * n - 7, by omega, by omega, by omega, prime_small 7 (by omega),
      nonprime_of_three _ (by omega) (by omega)⟩
  · exact ⟨5, 2 * n - 5, by omega, by omega, by omega, prime_small 5 (by omega),
      nonprime_of_three _ (by omega) (by omega)⟩

end Discovery.NeverEasy
