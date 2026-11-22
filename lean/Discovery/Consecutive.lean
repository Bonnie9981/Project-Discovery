import Mathlib.NumberTheory.Divisors
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# DISC-0003: sums of consecutive positive integers

`apSum D a k = a + (a + D) + ⋯ + (a + (k-1) D)`.
`reps D N` is the finite set of pairs `(a, k)` with `a ≥ 1`, `k ≥ 1` and `apSum D a k = N`
(both coordinates are automatically `≤ N`, see `mem_reps`).

* H1 `card_reps_one`: the number of ways to write `N` as a sum of one or more consecutive
  positive integers equals the number of odd divisors of `N` (OEIS A001227).
* H2 `card_reps_one_two_le`, `repsTwoLe_eq_empty_iff`: with at least two terms the count is
  `d_odd(N) - 1`, and it is `0` exactly when `N` is a power of two.
* H4 `card_reps_two`: sums of `k` terms with common difference 2 are counted by the divisors
  `d` of `N` with `d * d ≤ N`.
-/

namespace Discovery.Consecutive

open Finset

/-- `a + (a + D) + ⋯ + (a + (k-1) D)`. -/
def apSum (D a k : ℕ) : ℕ := ∑ i ∈ range k, (a + D * i)

/-- Representations of `N` as a sum of `k ≥ 1` terms of an arithmetic progression with
first term `a ≥ 1` and common difference `D`. -/
def reps (D N : ℕ) : Finset (ℕ × ℕ) :=
  (Icc 1 N ×ˢ Icc 1 N).filter (fun p => apSum D p.1 p.2 = N)

/-- The odd divisors of `N`. -/
def oddDivisors (N : ℕ) : Finset ℕ := N.divisors.filter Odd

theorem two_mul_apSum (D a k : ℕ) : 2 * apSum D a k + D * k = k * (2 * a + D * k) := by
  induction k with
  | zero => simp [apSum]
  | succ k ih =>
    have h : apSum D a (k + 1) = apSum D a k + (a + D * k) := by
      simp [apSum, sum_range_succ]
    rw [h]
    nlinarith [ih]

theorem mem_reps (D N a k : ℕ) :
    (a, k) ∈ reps D N ↔ 1 ≤ a ∧ 1 ≤ k ∧ apSum D a k = N := by
  constructor
  · intro h
    simp only [reps, mem_filter, mem_product, mem_Icc] at h
    exact ⟨h.1.1.1, h.1.2.1, h.2⟩
  · rintro ⟨ha, hk, hs⟩
    have e := two_mul_apSum D a k
    have h1 : D * k ≤ D * (k * k) := Nat.mul_le_mul_left D (Nat.le_mul_of_pos_left k hk)
    have h2 : a ≤ k * a := Nat.le_mul_of_pos_left a hk
    have h3 : k ≤ k * a := Nat.le_mul_of_pos_right k ha
    simp only [reps, mem_filter, mem_product, mem_Icc]
    refine ⟨⟨⟨ha, ?_⟩, ⟨hk, ?_⟩⟩, hs⟩ <;> nlinarith

/-- For `D = 1`: `(a, k)` is a representation iff `2 N = k (2 a + k - 1)`, stated without
subtraction. -/
theorem mem_reps_one (N a k : ℕ) :
    (a, k) ∈ reps 1 N ↔ 1 ≤ a ∧ 1 ≤ k ∧ 2 * N + k = k * (2 * a + k) := by
  rw [mem_reps]
  have e := two_mul_apSum 1 a k
  simp only [one_mul] at e
  constructor
  · rintro ⟨ha, hk, hs⟩
    exact ⟨ha, hk, by rw [← hs]; exact e⟩
  · rintro ⟨ha, hk, hs⟩
    exact ⟨ha, hk, by omega⟩

theorem mem_oddDivisors (N d : ℕ) : d ∈ oddDivisors N ↔ d ∣ N ∧ N ≠ 0 ∧ Odd d := by
  simp [oddDivisors, Nat.mem_divisors, and_assoc]

/-- Representation → odd divisor: the odd one of `k` and `2a + k - 1`. -/
def toDiv (p : ℕ × ℕ) : ℕ := if p.2 % 2 = 1 then p.2 else 2 * p.1 + p.2 - 1

/-- Odd divisor `d` → representation, using the complementary factor `2N/d` of `2N`. -/
def toRep (N d : ℕ) : ℕ × ℕ :=
  if d < 2 * (N / d) then ((2 * (N / d) + 1 - d) / 2, d) else ((d + 1 - 2 * (N / d)) / 2, 2 * (N / d))

/-- **H1.** The number of representations of `N` as a sum of consecutive positive integers
equals the number of odd divisors of `N`. -/
theorem card_reps_one (N : ℕ) : (reps 1 N).card = (oddDivisors N).card := by
  apply Finset.card_nbij' toDiv (toRep N)
  · -- toDiv lands in the odd divisors
    rintro ⟨a, k⟩ hp
    rw [mem_reps_one] at hp
    obtain ⟨ha, hk, hs⟩ := hp
    rw [mem_oddDivisors]
    simp only [toDiv]
    rcases Nat.even_or_odd' k with ⟨t, rfl | rfl⟩
    · -- k = 2t even: the odd factor is 2a + 2t - 1, and N = t (2a + 2t - 1)
      have ht : 1 ≤ t := by omega
      have hN : N = t * (2 * a + 2 * t - 1) := by
        obtain ⟨u, rfl⟩ : ∃ u, a = u + 1 := ⟨a - 1, by omega⟩
        obtain ⟨v, rfl⟩ : ∃ v, t = v + 1 := ⟨t - 1, by omega⟩
        have : 2 * (u + 1) + 2 * (v + 1) - 1 = 2 * u + 2 * v + 3 := by omega
        rw [this]; nlinarith
      have h2 : ¬ (2 * t) % 2 = 1 := by omega
      simp only [h2, if_false]
      refine ⟨⟨t, by rw [hN]; ring⟩, ?_, ⟨a + t - 1, by omega⟩⟩
      rw [hN]; apply Nat.mul_ne_zero <;> omega
    · -- k = 2t + 1 odd: N = (2t + 1)(a + t)
      have hN : N = (2 * t + 1) * (a + t) := by nlinarith
      have h2 : (2 * t + 1) % 2 = 1 := by omega
      simp only [h2, if_true]
      refine ⟨⟨a + t, hN⟩, ?_, ⟨t, rfl⟩⟩
      rw [hN]; apply Nat.mul_ne_zero <;> omega
  · -- toRep lands in the representations
    intro d hd
    rw [mem_oddDivisors] at hd
    obtain ⟨⟨q, rfl⟩, hN, ⟨t, rfl⟩⟩ := hd
    have hq : 1 ≤ q := by
      rcases Nat.eq_zero_or_pos q with h | h
      · simp [h] at hN
      · exact h
    have hdiv : (2 * t + 1) * q / (2 * t + 1) = q := by
      rw [Nat.mul_div_cancel_left q (by omega)]
    simp only [toRep, hdiv]
    split_ifs with hlt
    · -- k = 2t + 1, a = q - t
      have ha : (2 * q + 1 - (2 * t + 1)) / 2 = q - t := by omega
      rw [ha, mem_reps_one]
      refine ⟨by omega, by omega, ?_⟩
      obtain ⟨s, hs⟩ : ∃ s, q = t + s + 1 := ⟨q - t - 1, by omega⟩
      subst hs
      have : t + s + 1 - t = s + 1 := by omega
      rw [this]; ring
    · -- k = 2q, a = t + 1 - q
      have ha : (2 * t + 1 + 1 - 2 * q) / 2 = t + 1 - q := by omega
      rw [ha, mem_reps_one]
      refine ⟨by omega, by omega, ?_⟩
      obtain ⟨s, hs⟩ : ∃ s, t = q + s := ⟨t - q, by omega⟩
      subst hs
      have : q + s + 1 - q = s + 1 := by omega
      rw [this]; ring
  · -- toRep (toDiv p) = p
    rintro ⟨a, k⟩ hp
    rw [mem_reps_one] at hp
    obtain ⟨ha, hk, hs⟩ := hp
    simp only [toDiv]
    rcases Nat.even_or_odd' k with ⟨t, rfl | rfl⟩
    · have ht : 1 ≤ t := by omega
      have h2 : ¬ (2 * t) % 2 = 1 := by omega
      simp only [h2, if_false]
      obtain ⟨u, rfl⟩ : ∃ u, a = u + 1 := ⟨a - 1, by omega⟩
      have e1 : 2 * (u + 1) + 2 * t - 1 = 2 * (u + t) + 1 := by omega
      have hN : N = (2 * (u + t) + 1) * t := by
        obtain ⟨v, rfl⟩ : ∃ v, t = v + 1 := ⟨t - 1, by omega⟩
        nlinarith
      rw [e1, hN]
      simp only [toRep]
      rw [Nat.mul_div_cancel_left t (by omega : 0 < 2 * (u + t) + 1)]
      have hlt : ¬ 2 * (u + t) + 1 < 2 * t := by omega
      simp only [hlt, if_false, Prod.mk.injEq, and_true]
      omega
    · have h2 : (2 * t + 1) % 2 = 1 := by omega
      simp only [h2, if_true]
      have hN : N = (2 * t + 1) * (a + t) := by nlinarith
      rw [hN]
      simp only [toRep]
      rw [Nat.mul_div_cancel_left (a + t) (by omega : 0 < 2 * t + 1)]
      have hlt : 2 * t + 1 < 2 * (a + t) := by omega
      simp only [hlt, if_true, Prod.mk.injEq, and_true]
      omega
  · -- toDiv (toRep d) = d
    intro d hd
    rw [mem_oddDivisors] at hd
    obtain ⟨⟨q, rfl⟩, hN, ⟨t, rfl⟩⟩ := hd
    have hdiv : (2 * t + 1) * q / (2 * t + 1) = q := by
      rw [Nat.mul_div_cancel_left q (by omega)]
    simp only [toRep, hdiv]
    split_ifs with hlt
    · simp only [toDiv]
      have h2 : (2 * t + 1) % 2 = 1 := by omega
      simp [h2]
    · simp only [toDiv]
      have h2 : ¬ (2 * q) % 2 = 1 := by omega
      simp only [h2, if_false]
      omega

/-- Representations with at least two terms. -/
def repsTwoLe (N : ℕ) : Finset (ℕ × ℕ) := (reps 1 N).filter (fun p => 2 ≤ p.2)

/-- **H2a.** With at least two terms the count is `d_odd(N) - 1` (for `N ≥ 1`). -/
theorem card_reps_one_two_le (N : ℕ) (hN : 1 ≤ N) :
    (repsTwoLe N).card = (oddDivisors N).card - 1 := by
  have hsplit : reps 1 N = insert (N, 1) (repsTwoLe N) := by
    ext ⟨a, k⟩
    simp only [repsTwoLe, mem_insert, mem_filter, Prod.mk.injEq]
    constructor
    · intro h
      by_cases hk : 2 ≤ k
      · exact Or.inr ⟨h, hk⟩
      · left
        rw [mem_reps_one] at h
        obtain ⟨ha, hk1, hs⟩ := h
        have : k = 1 := by omega
        subst this
        omega
    · rintro (⟨rfl, rfl⟩ | ⟨h, _⟩)
      · rw [mem_reps_one]; omega
      · exact h
  have hnot : (N, 1) ∉ repsTwoLe N := by simp [repsTwoLe]
  rw [← card_reps_one, hsplit, card_insert_of_not_mem hnot]
  rfl

/-- **H2b.** `N ≥ 1` is a sum of two or more consecutive positive integers iff `N` is not a
power of two. -/
theorem repsTwoLe_eq_empty_iff (N : ℕ) (hN : 1 ≤ N) :
    repsTwoLe N = ∅ ↔ ∃ m, N = 2 ^ m := by
  rw [← card_eq_zero, card_reps_one_two_le N hN]
  obtain ⟨m, c, hc, hNc⟩ := Nat.exists_eq_two_pow_mul_odd (n := N) (by omega : N ≠ 0)
  have hc0 : c ≠ 0 := by rintro rfl; simp at hc
  have h1 : 1 ∈ oddDivisors N := by
    rw [mem_oddDivisors]; exact ⟨one_dvd N, by omega, odd_one⟩
  constructor
  · intro h
    -- only one odd divisor, so the odd part `c` equals 1
    have hle : (oddDivisors N).card ≤ 1 := by omega
    have hcmem : c ∈ oddDivisors N := by
      rw [mem_oddDivisors]; exact ⟨⟨2 ^ m, by rw [hNc]; ring⟩, by omega, hc⟩
    have : c = 1 := Finset.card_le_one.mp hle c hcmem 1 h1
    exact ⟨m, by rw [hNc, this, mul_one]⟩
  · rintro ⟨j, rfl⟩
    have : oddDivisors (2 ^ j) = {1} := by
      ext d
      simp only [mem_oddDivisors, mem_singleton]
      constructor
      · rintro ⟨hd, -, hodd⟩
        rw [Nat.dvd_prime_pow Nat.prime_two] at hd
        obtain ⟨i, -, rfl⟩ := hd
        rcases i with _ | i
        · rfl
        · exfalso
          have hev : Even (2 ^ (i + 1)) := Nat.even_pow.mpr ⟨even_two, by omega⟩
          exact (Nat.not_even_iff_odd.mpr hodd) hev
      · rintro rfl; exact ⟨one_dvd _, by positivity, odd_one⟩
    rw [this]; rfl

/-- Divisors `d` of `N` with `d * d ≤ N`. -/
def smallDivisors (N : ℕ) : Finset ℕ := N.divisors.filter (fun d => d * d ≤ N)

/-- **H4.** Sums of an arithmetic progression with common difference 2 and positive first
term: their number equals the number of divisors `d` of `N` with `d * d ≤ N`. -/
theorem card_reps_two (N : ℕ) : (reps 2 N).card = (smallDivisors N).card := by
  have key : ∀ a k, (a, k) ∈ reps 2 N ↔ 1 ≤ a ∧ 1 ≤ k ∧ N = k * (a + k - 1) := by
    intro a k
    rw [mem_reps]
    have e := two_mul_apSum 2 a k
    constructor
    · rintro ⟨ha, hk, hs⟩
      refine ⟨ha, hk, ?_⟩
      obtain ⟨v, rfl⟩ : ∃ v, k = v + 1 := ⟨k - 1, by omega⟩
      have : a + (v + 1) - 1 = a + v := by omega
      rw [this]; nlinarith
    · rintro ⟨ha, hk, hs⟩
      refine ⟨ha, hk, ?_⟩
      obtain ⟨v, rfl⟩ : ∃ v, k = v + 1 := ⟨k - 1, by omega⟩
      have : a + (v + 1) - 1 = a + v := by omega
      rw [this] at hs; nlinarith
  apply Finset.card_nbij' (fun p => p.2) (fun d => (N / d + 1 - d, d))
  · rintro ⟨a, k⟩ hp
    rw [key] at hp
    obtain ⟨ha, hk, hs⟩ := hp
    simp only [Finset.mem_coe, smallDivisors, mem_filter, Nat.mem_divisors]
    refine ⟨⟨⟨a + k - 1, hs⟩, ?_⟩, ?_⟩
    · rw [hs]; apply Nat.mul_ne_zero <;> omega
    · rw [hs]; exact Nat.mul_le_mul_left k (by omega)
  · intro d hd
    simp only [Finset.mem_coe, smallDivisors, mem_filter, Nat.mem_divisors] at hd
    obtain ⟨⟨⟨q, rfl⟩, hN⟩, hle⟩ := hd
    have hd0 : 0 < d := by
      rcases Nat.eq_zero_or_pos d with h | h
      · simp [h] at hN
      · exact h
    have hdq : d ≤ q := Nat.le_of_mul_le_mul_left hle hd0
    rw [key, Nat.mul_div_cancel_left q hd0]
    refine ⟨by omega, by omega, ?_⟩
    have : q + 1 - d + d - 1 = q := by omega
    rw [this]
  · rintro ⟨a, k⟩ hp
    rw [key] at hp
    obtain ⟨ha, hk, hs⟩ := hp
    simp only [Prod.mk.injEq, and_true]
    rw [hs, Nat.mul_div_cancel_left _ (by omega)]
    omega
  · intro d _
    rfl

end Discovery.Consecutive
