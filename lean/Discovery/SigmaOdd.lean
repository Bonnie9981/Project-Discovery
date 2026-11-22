import Mathlib.NumberTheory.ArithmeticFunction
import Mathlib.Data.Nat.Factorization.Induction
import Mathlib.Algebra.GeomSum
import Mathlib.Algebra.GCDMonoid.Nat
import Mathlib.Data.Finset.NatDivisors
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.IntervalCases

/-!
# DISC-0006 / C01: `σ(σ_odd n) = σ_odd(σ n)`

`sigmaOdd n` = sum of the odd divisors of `n` (equals `σ` of the odd part, `sigmaOdd_two_pow_mul`).
Conjecture C01: for `n ≥ 1`, `σ(σ_odd n) = σ_odd(σ n)` iff `n` is an odd perfect square.

Proved here:
* `odd_sigma_iff_isSquare`: for odd `m`, `σ m` is odd iff `m` is a square.
* `c01_odd`: C01 for every odd `n`.
* `c01_even_of_not_abundant`: no even solution `n = 2^a m` (`a ≥ 1`, `m` odd) when
  `q = 2^(a+1) - 1` satisfies `σ q ≤ 2q`.
* `c01_even_of_oddPart_square`: no even solution when the odd part of `σ m` is a square.
* `c01_of_not_two_pow_eleven_dvd`: C01 holds for every `n > 0` with `2^11 ∤ n`.

Not proved: even `n` with `v₂(n) ≥ 11` where neither hypothesis above applies
(`2^12 - 1 = 4095` is abundant, so `v₂(n) = 11` is the first open exponent).
-/

namespace Discovery.SigmaOdd

open ArithmeticFunction Finset

/-- Sum of the odd divisors of `n`. -/
def sigmaOdd (n : ℕ) : ℕ := ∑ d ∈ n.divisors.filter Odd, d

theorem sum_range_pow_mod_two (p : ℕ) (hp : Odd p) (N : ℕ) :
    (∑ k ∈ range N, p ^ k) % 2 = N % 2 := by
  induction N with
  | zero => simp
  | succ N ih =>
    rw [sum_range_succ, Nat.add_mod, ih]
    have : p ^ N % 2 = 1 := by
      rw [Nat.pow_mod, Nat.odd_iff.mp hp, one_pow]
      norm_num
    rw [this]
    omega

theorem isSquare_prime_pow_iff {p n : ℕ} (hp : p.Prime) : IsSquare (p ^ n) ↔ Even n := by
  constructor
  · rintro ⟨r, hr⟩
    have hdvd : r ∣ p ^ n := ⟨r, hr⟩
    obtain ⟨k, -, rfl⟩ := (Nat.dvd_prime_pow hp).1 hdvd
    rw [← pow_add] at hr
    exact ⟨k, Nat.pow_right_injective hp.two_le hr⟩
  · rintro ⟨k, rfl⟩
    exact ⟨p ^ k, by rw [pow_add]⟩

theorem isSquare_mul_of_coprime {a b : ℕ} (hab : a.Coprime b) :
    IsSquare (a * b) ↔ IsSquare a ∧ IsSquare b := by
  constructor
  · rintro ⟨c, hc⟩
    have hu : IsUnit (gcd a b) := by
      rw [Nat.isUnit_iff]; exact hab
    have hu' : IsUnit (gcd b a) := by
      rw [Nat.isUnit_iff]; exact hab.symm
    have h2 : a * b = c ^ 2 := by rw [hc, sq]
    have h2' : b * a = c ^ 2 := by rw [mul_comm, h2]
    obtain ⟨d, hd⟩ := exists_eq_pow_of_mul_eq_pow hu h2
    obtain ⟨e, he⟩ := exists_eq_pow_of_mul_eq_pow hu' h2'
    exact ⟨⟨d, by rw [hd, sq]⟩, ⟨e, by rw [he, sq]⟩⟩
  · rintro ⟨ha, hb⟩
    exact ha.mul hb

/-- For odd `m`, `σ(m)` is odd iff `m` is a perfect square. -/
theorem odd_sigma_iff_isSquare (m : ℕ) (hm : Odd m) : Odd (σ 1 m) ↔ IsSquare m := by
  induction m using Nat.recOnPrimeCoprime with
  | h0 => exact absurd hm (by decide)
  | hp p n hp =>
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · rw [pow_zero, isMultiplicative_sigma.map_one]
      simp
    have hpo : Odd p := hm.of_dvd_nat (dvd_pow_self p hn.ne')
    rw [sigma_one_apply_prime_pow hp, isSquare_prime_pow_iff hp, Nat.odd_iff,
      sum_range_pow_mod_two p hpo, ← Nat.odd_iff, Nat.odd_add_one, Nat.not_odd_iff_even]
  | h a b _ _ hab iha ihb =>
    obtain ⟨hao, hbo⟩ := Nat.odd_mul.1 hm
    rw [isMultiplicative_sigma.map_mul_of_coprime hab, Nat.odd_mul, iha hao, ihb hbo,
      isSquare_mul_of_coprime hab]

theorem sigma_two_pow (k : ℕ) : σ 1 (2 ^ k) = 2 ^ (k + 1) - 1 := by
  rw [sigma_one_apply_prime_pow Nat.prime_two, Nat.geomSum_eq (le_refl 2)]
  simp

theorem sigma_two_pow_mul (k t : ℕ) (ht : Odd t) :
    σ 1 (2 ^ k * t) = (2 ^ (k + 1) - 1) * σ 1 t := by
  have hc : (2 ^ k).Coprime t := Nat.Coprime.pow_left k (Nat.coprime_two_left.2 ht)
  rw [isMultiplicative_sigma.map_mul_of_coprime hc, sigma_two_pow]

theorem sigmaOdd_two_pow_mul (k t : ℕ) (ht : Odd t) : sigmaOdd (2 ^ k * t) = σ 1 t := by
  rw [sigmaOdd, sigma_one_apply]
  congr 1
  ext d
  have ht0 : t ≠ 0 := by rintro rfl; exact absurd ht (by decide)
  have h0 : 2 ^ k * t ≠ 0 := mul_ne_zero (pow_ne_zero _ two_ne_zero) ht0
  simp only [mem_filter, Nat.mem_divisors]
  constructor
  · rintro ⟨⟨hd, -⟩, hdo⟩
    have hc : d.Coprime (2 ^ k) := Nat.Coprime.pow_right k (Nat.coprime_two_right.2 hdo)
    exact ⟨hc.dvd_of_dvd_mul_left hd, ht0⟩
  · rintro ⟨hd, -⟩
    exact ⟨⟨Dvd.dvd.mul_left hd _, h0⟩, ht.of_dvd_nat hd⟩

theorem sigma_pos' {n : ℕ} (hn : 0 < n) : 0 < σ 1 n := by
  rw [sigma_one_apply]
  exact Finset.sum_pos (fun d hd => Nat.pos_of_mem_divisors hd)
    ⟨1, Nat.mem_divisors.2 ⟨one_dvd n, hn.ne'⟩⟩

theorem sigma_odd_eq (n : ℕ) (hn : Odd n) : sigmaOdd n = σ 1 n := by
  have := sigmaOdd_two_pow_mul 0 n hn
  simpa using this

theorem two_pow_succ_sub_one_mod_four {a : ℕ} (ha : 1 ≤ a) : (2 ^ (a + 1) - 1) % 4 = 3 := by
  obtain ⟨c, rfl⟩ := Nat.exists_eq_add_of_le ha
  have : 2 ^ (1 + c + 1) = 4 * 2 ^ c := by ring
  rw [this]
  have : 0 < 2 ^ c := Nat.pos_pow_of_pos c (by norm_num)
  omega

/-- **C01, odd `n`**: for odd `n`, `σ(σ_odd n) = σ_odd(σ n)` iff `n` is a perfect square. -/
theorem c01_odd (n : ℕ) (hn : Odd n) :
    σ 1 (sigmaOdd n) = sigmaOdd (σ 1 n) ↔ IsSquare n := by
  rw [sigma_odd_eq n hn, ← odd_sigma_iff_isSquare n hn]
  have hn0 : 0 < n := hn.pos
  obtain ⟨b, t, ht, hs⟩ := Nat.exists_eq_two_pow_mul_odd (sigma_pos' hn0).ne'
  rw [hs, sigma_two_pow_mul b t ht, sigmaOdd_two_pow_mul b t ht]
  have htpos : 0 < σ 1 t := sigma_pos' ht.pos
  constructor
  · intro h
    have h1 : 2 ^ (b + 1) - 1 = 1 := by
      have := Nat.eq_of_mul_eq_mul_right htpos (h.trans (one_mul _).symm)
      exact this
    have hb : b = 0 := by
      rcases Nat.eq_zero_or_pos b with hb | hb
      · exact hb
      · have : 2 ^ 2 ≤ 2 ^ (b + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
        omega
    subst hb
    simpa using ht
  · intro h
    have hb : b = 0 := by
      rcases Nat.eq_zero_or_pos b with hb | hb
      · exact hb
      · exfalso
        have : Even (2 ^ b * t) := (Nat.even_pow.2 ⟨even_two, hb.ne'⟩).mul_right t
        exact (Nat.not_even_iff_odd.2 h) this
    subst hb
    simp

theorem lt_sigma_mul {q t : ℕ} (hq : 1 < q) (ht : 0 < t) : q * σ 1 t < σ 1 (q * t) := by
  rw [sigma_one_apply, sigma_one_apply, Finset.mul_sum]
  have hinj : Set.InjOn (fun d => q * d) ((t.divisors : Set ℕ)) := by
    intro x _ y _ hxy
    exact Nat.eq_of_mul_eq_mul_left (by omega) hxy
  rw [← Finset.sum_image (f := fun x => x) hinj]
  have h1 : 1 ∉ t.divisors.image (fun d => q * d) := by
    simp only [mem_image, Nat.mem_divisors, not_exists, not_and]
    intro d hd h
    have : 0 < d := Nat.pos_of_dvd_of_pos hd.1 ht
    nlinarith
  have hsub : insert 1 (t.divisors.image (fun d => q * d)) ⊆ (q * t).divisors := by
    intro x hx
    rw [mem_insert, mem_image] at hx
    have hqt : q * t ≠ 0 := by positivity
    rcases hx with rfl | ⟨d, hd, rfl⟩
    · exact Nat.mem_divisors.2 ⟨one_dvd _, hqt⟩
    · exact Nat.mem_divisors.2 ⟨Nat.mul_dvd_mul_left q (Nat.dvd_of_mem_divisors hd), hqt⟩
  have := Finset.sum_le_sum_of_subset (f := fun x => x) hsub
  rw [Finset.sum_insert h1] at this
  simp only at this ⊢
  omega

theorem sum_image_le_nat {α : Type*} [DecidableEq α] (s : Finset α) (g : α → ℕ) :
    ∑ y ∈ s.image g, y ≤ ∑ x ∈ s, g x := by
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
    rw [Finset.image_insert, Finset.sum_insert ha]
    by_cases hg : g a ∈ s.image g
    · rw [Finset.insert_eq_of_mem hg]; omega
    · rw [Finset.sum_insert hg]; omega

theorem sigma_mul_le (q t : ℕ) : σ 1 (q * t) ≤ σ 1 q * σ 1 t := by
  rw [sigma_one_apply, sigma_one_apply, sigma_one_apply, Finset.sum_mul_sum, ← Finset.sum_product']
  have hsub : (q * t).divisors ⊆ (q.divisors ×ˢ t.divisors).image (fun p => p.1 * p.2) := by
    rw [Nat.divisors_mul]
    intro x hx
    obtain ⟨a, ha, b, hb, rfl⟩ := Finset.mem_mul.1 hx
    exact Finset.mem_image.2 ⟨(a, b), Finset.mem_product.2 ⟨ha, hb⟩, rfl⟩
  calc ∑ d ∈ (q * t).divisors, d
      ≤ ∑ d ∈ (q.divisors ×ˢ t.divisors).image (fun p => p.1 * p.2), d :=
        Finset.sum_le_sum_of_subset hsub
    _ ≤ ∑ p ∈ q.divisors ×ˢ t.divisors, p.1 * p.2 := sum_image_le_nat _ _

/-- **C01, even `n`, non-abundant Mersenne factor**: if `n = 2^a * m` with `a ≥ 1`, `m` odd,
and `q = 2^(a+1) - 1` satisfies `σ(q) ≤ 2q`, then `σ(σ_odd n) ≠ σ_odd(σ n)`. -/
theorem c01_even_of_not_abundant (a m : ℕ) (ha : 1 ≤ a) (hm : Odd m)
    (hdef : σ 1 (2 ^ (a + 1) - 1) ≤ 2 * (2 ^ (a + 1) - 1)) :
    σ 1 (sigmaOdd (2 ^ a * m)) ≠ sigmaOdd (σ 1 (2 ^ a * m)) := by
  set q := 2 ^ (a + 1) - 1 with hq
  have hq4 : q % 4 = 3 := two_pow_succ_sub_one_mod_four ha
  have hqo : Odd q := Nat.odd_iff.2 (by omega)
  rw [sigmaOdd_two_pow_mul a m hm, sigma_two_pow_mul a m hm, ← hq]
  obtain ⟨b, t, ht, hs⟩ := Nat.exists_eq_two_pow_mul_odd (sigma_pos' hm.pos).ne'
  have hqt : q * σ 1 m = 2 ^ b * (q * t) := by rw [hs]; ring
  rw [hqt, sigmaOdd_two_pow_mul b (q * t) (hqo.mul ht), hs, sigma_two_pow_mul b t ht]
  intro h
  have htpos : 0 < σ 1 t := sigma_pos' ht.pos
  have hlow := lt_sigma_mul (q := q) (t := t) (by omega) ht.pos
  have hup := sigma_mul_le q t
  rw [← h] at hlow hup
  -- q < 2^(b+1) - 1
  have h1 : q < 2 ^ (b + 1) - 1 := lt_of_mul_lt_mul_right hlow (Nat.zero_le _)
  have h2 : a < b := by
    by_contra hab
    push_neg at hab
    have : 2 ^ (b + 1) ≤ 2 ^ (a + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
    omega
  have h3 : 2 ^ (a + 2) ≤ 2 ^ (b + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
  have h4 : 2 ^ (a + 2) = 2 * 2 ^ (a + 1) := by ring
  have h5 : 2 * q + 1 ≤ 2 ^ (b + 1) - 1 := by
    have : 2 ≤ 2 ^ (a + 1) := by
      calc 2 = 2 ^ 1 := by norm_num
        _ ≤ 2 ^ (a + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
    omega
  have h6 : (2 * q + 1) * σ 1 t ≤ σ 1 q * σ 1 t :=
    le_trans (Nat.mul_le_mul_right _ h5) hup
  have h7 : 2 * q + 1 ≤ σ 1 q := Nat.le_of_mul_le_mul_right h6 htpos
  omega

theorem isSquare_of_mul {q t : ℕ} (hq : IsSquare (q * t)) (ht : IsSquare t) (ht0 : t ≠ 0) :
    IsSquare q := by
  obtain ⟨x, hx⟩ := hq
  obtain ⟨y, rfl⟩ := ht
  have hy : 0 < y * y := Nat.pos_of_ne_zero ht0
  have hd : y ^ 2 ∣ x ^ 2 := ⟨q, by rw [sq, sq, ← hx]; ring⟩
  obtain ⟨z, rfl⟩ := (Nat.pow_dvd_pow_iff two_ne_zero).1 hd
  refine ⟨z, Nat.eq_of_mul_eq_mul_right hy ?_⟩
  rw [hx]
  ring

theorem not_isSquare_of_mod_four {q : ℕ} (h : q % 4 = 3) : ¬ IsSquare q := by
  rintro ⟨z, rfl⟩
  have hm : z * z % 4 = (z % 4) * (z % 4) % 4 := Nat.mul_mod _ _ _
  have hz : z % 4 < 4 := Nat.mod_lt _ (by norm_num)
  generalize z % 4 = r at hm hz
  generalize z * z = w at hm h
  interval_cases r <;> omega

/-- **C01, even `n`, square odd part**: if `n = 2^a * m` (`a ≥ 1`, `m` odd) and the odd part
`t` of `σ(m)` is a perfect square, then `σ(σ_odd n) ≠ σ_odd(σ n)` (parity argument). -/
theorem c01_even_of_oddPart_square (a m b t : ℕ) (ha : 1 ≤ a) (hm : Odd m) (ht : Odd t)
    (hs : σ 1 m = 2 ^ b * t) (hsq : IsSquare t) :
    σ 1 (sigmaOdd (2 ^ a * m)) ≠ sigmaOdd (σ 1 (2 ^ a * m)) := by
  set q := 2 ^ (a + 1) - 1 with hq
  have hq4 : q % 4 = 3 := two_pow_succ_sub_one_mod_four ha
  have hqo : Odd q := Nat.odd_iff.2 (by omega)
  rw [sigmaOdd_two_pow_mul a m hm, sigma_two_pow_mul a m hm, ← hq]
  have hqt : q * σ 1 m = 2 ^ b * (q * t) := by rw [hs]; ring
  rw [hqt, sigmaOdd_two_pow_mul b (q * t) (hqo.mul ht), hs, sigma_two_pow_mul b t ht]
  intro h
  have hb : Odd (2 ^ (b + 1) - 1) := by
    have : 2 ^ (b + 1) = 2 * 2 ^ b := by ring
    have : 0 < 2 ^ b := Nat.pos_pow_of_pos b (by norm_num)
    exact Nat.odd_iff.2 (by omega)
  have hl : Odd ((2 ^ (b + 1) - 1) * σ 1 t) :=
    hb.mul ((odd_sigma_iff_isSquare t ht).2 hsq)
  rw [h, odd_sigma_iff_isSquare (q * t) (hqo.mul ht)] at hl
  exact not_isSquare_of_mod_four hq4 (isSquare_of_mul hl hsq ht.pos.ne')

/-- `2^(a+1) - 1` is not abundant for `1 ≤ a ≤ 10` (checked by `decide`). -/
theorem mersenne_not_abundant (a : ℕ) (ha : 1 ≤ a) (ha10 : a ≤ 10) :
    σ 1 (2 ^ (a + 1) - 1) ≤ 2 * (2 ^ (a + 1) - 1) := by
  set_option maxRecDepth 1000000 in
  interval_cases a <;> decide

/-- **C01 for every `n > 0` with `2^11 ∤ n`** (i.e. `v₂(n) ≤ 10`):
`σ(σ_odd n) = σ_odd(σ n) ↔ n` is an odd perfect square. -/
theorem c01_of_not_two_pow_eleven_dvd (n : ℕ) (hn : 0 < n) (h : ¬ 2 ^ 11 ∣ n) :
    σ 1 (sigmaOdd n) = sigmaOdd (σ 1 n) ↔ Odd n ∧ IsSquare n := by
  obtain ⟨a, m, hm, rfl⟩ := Nat.exists_eq_two_pow_mul_odd hn.ne'
  rcases Nat.eq_zero_or_pos a with rfl | ha
  · simp only [pow_zero, one_mul]
    rw [c01_odd m hm]
    exact ⟨fun h => ⟨hm, h⟩, fun h => h.2⟩
  · have ha10 : a ≤ 10 := by
      by_contra hc
      push_neg at hc
      exact h (Dvd.dvd.mul_right (Nat.pow_dvd_pow 2 hc) m)
    have hne := c01_even_of_not_abundant a m ha hm (mersenne_not_abundant a ha ha10)
    have hev : ¬ Odd (2 ^ a * m) := by
      rw [Nat.not_odd_iff_even]
      exact (Nat.even_pow.2 ⟨even_two, ha.ne'⟩).mul_right m
    exact ⟨fun h => absurd h hne, fun h => absurd h.1 hev⟩

end Discovery.SigmaOdd
