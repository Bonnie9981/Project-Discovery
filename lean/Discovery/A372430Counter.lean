/-!
# DISC-0026: a second number whose binary indices are prime indices (A372430)

OEIS A372430 (Gus Wiseman, 2024), comment:
"Conjecture: The only number whose binary indices are a subset of its prime indices
is 4100 ... Verified up to 10,000,000."

Binary index j of k: bit j-1 of k is 1.  Prime index m of k: prime(m) divides k.

Counterexample: k = 2^87 + 2^49 = 154742504911235484315811840.
Its binary indices are {50, 88}; prime(50) = 229 and prime(88) = 457 both divide k
(2^38 + 1 = 5 * 229 * 457 * 525313).

Everything is checked by the kernel; only core Lean is used.
`isPrimeB` is trial division, proved equivalent to the usual definition.
-/

namespace Discovery.A372430Counter

def IsPrime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d ∣ p → d = 1 ∨ d = p

/-- Trial division: no divisor among 2 .. n-1. -/
def isPrimeB (n : Nat) : Bool :=
  decide (2 ≤ n) && (List.range (n - 2)).all (fun d => n % (d + 2) != 0)

theorem isPrimeB_iff (n : Nat) : isPrimeB n = true ↔ IsPrime n := by
  unfold isPrimeB IsPrime
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range,
    bne_iff_ne, ne_eq]
  constructor
  · rintro ⟨h2, hall⟩
    refine ⟨h2, fun d hd => ?_⟩
    have hdpos : 0 < d := Nat.pos_of_ne_zero (by rintro rfl; simp at hd; omega)
    have hdle : d ≤ n := Nat.le_of_dvd (by omega) hd
    rcases Nat.lt_or_ge d 2 with h | h
    · left; omega
    · rcases Nat.lt_or_ge d n with h' | h'
      · exfalso
        have := hall (d - 2) (by omega)
        have e : d - 2 + 2 = d := by omega
        rw [e] at this
        exact this (Nat.mod_eq_zero_of_dvd hd)
      · right; omega
  · rintro ⟨h2, hdiv⟩
    refine ⟨h2, fun d hd hmod => ?_⟩
    rcases hdiv (d + 2) (Nat.dvd_of_mod_eq_zero hmod) with h | h <;> omega

/-- Number of primes below n. -/
def primesBelow (n : Nat) : Nat := ((List.range n).filter isPrimeB).length

/-- The counterexample. -/
def k : Nat := 2 ^ 87 + 2 ^ 49

theorem k_value : k = 154742504911235484315811840 := by decide

set_option maxRecDepth 100000 in
/-- 229 is the 50th prime and 457 is the 88th prime. -/
theorem prime_229 : IsPrime 229 := (isPrimeB_iff 229).mp (by rfl)
set_option maxRecDepth 100000 in
theorem prime_457 : IsPrime 457 := (isPrimeB_iff 457).mp (by rfl)
set_option maxRecDepth 100000 in
theorem count_229 : primesBelow 229 = 49 := by rfl
set_option maxRecDepth 100000 in
theorem count_457 : primesBelow 457 = 87 := by rfl

/-- The only 1-bits of k are bits 49 and 87 (binary indices 50 and 88). -/
theorem k_bits : ∀ i, i < 88 → (k.testBit i = true ↔ i = 49 ∨ i = 87) := by decide
theorem k_lt : k < 2 ^ 88 := by decide

/-- prime(50) and prime(88) divide k. -/
theorem dvd_229 : 229 ∣ k := Nat.dvd_of_mod_eq_zero (by decide)
theorem dvd_457 : 457 ∣ k := Nat.dvd_of_mod_eq_zero (by decide)

/-- Counterexample to the A372430 conjecture: k ≠ 4100 and every binary index of k
is a prime index of k. -/
theorem a372430_counterexample :
    k ≠ 4100 ∧ k < 2 ^ 88 ∧
    (∀ i, i < 88 → k.testBit i = true → i = 49 ∨ i = 87) ∧
    IsPrime 229 ∧ primesBelow 229 = 49 ∧ 229 ∣ k ∧
    IsPrime 457 ∧ primesBelow 457 = 87 ∧ 457 ∣ k :=
  ⟨by decide, k_lt, fun i hi h => (k_bits i hi).mp h,
    prime_229, count_229, dvd_229, prime_457, count_457, dvd_457⟩

set_option maxRecDepth 100000 in
/-- Sanity check against the entry: 4100 = 2^12 + 2^2, prime(3) = 5 and prime(13) = 41. -/
example : 4100 = 2 ^ 12 + 2 ^ 2 ∧ 4100 % 5 = 0 ∧ 4100 % 41 = 0 ∧
    primesBelow 5 = 2 ∧ primesBelow 41 = 12 := by decide

end Discovery.A372430Counter
