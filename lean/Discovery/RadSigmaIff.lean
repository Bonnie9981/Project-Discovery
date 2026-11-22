import Mathlib.NumberTheory.Multiplicity
import Mathlib.Data.Nat.Factorization.Basic
import Discovery.RadSigma
import Discovery.SigmaOdd

/-!
# DISC-0007 / C02: full characterisation of `rad(σ n) = σ(rad n)`

Main theorem `c02_iff`: for `n > 0`,
`rad(σ n) = σ(rad n)` iff
* `n` and `σ n` are both squarefree, or
* `n = 2^a p` with `p` an odd prime, `a ≥ 3` odd, `p + 1` squarefree, `3 ∤ p + 1`,
  and `rad(2^(a+1) - 1) ∣ 3(p+1)`.

The only non-elementary input is lifting-the-exponent (`padicValNat.pow_sub_pow`,
`padicValNat.pow_two_sub_pow`), used in `lte_core` to rule out `n = 2^a p^b` with `b ≥ 3`.
-/

namespace Discovery.RadSigma

open ArithmeticFunction Finset

/-! ## `rad` -/

theorem primeFactors_rad (n : ℕ) : (rad n).primeFactors = n.primeFactors :=
  Nat.primeFactors_prod fun _ hp => Nat.prime_of_mem_primeFactors hp

/-- `rad x = y` iff `y` is squarefree with the same prime factors as `x`. -/
theorem rad_eq_iff {x y : ℕ} :
    rad x = y ↔ Squarefree y ∧ x.primeFactors = y.primeFactors := by
  constructor
  · rintro rfl
    exact ⟨squarefree_rad x, (primeFactors_rad x).symm⟩
  · rintro ⟨hy, hxy⟩
    rw [rad, hxy]
    exact Nat.prod_primeFactors_of_squarefree hy

theorem rad_dvd_of_primeFactors_subset {x y : ℕ}
    (h : x.primeFactors ⊆ y.primeFactors) : rad x ∣ y :=
  Finset.prod_primes_dvd y (fun _ hp => (Nat.prime_of_mem_primeFactors hp).prime)
    fun _ hp => Nat.dvd_of_mem_primeFactors (h hp)

theorem prime_dvd_rad {q x : ℕ} (hq : q.Prime) (hx : x ≠ 0) (h : q ∣ x) : q ∣ rad x :=
  Finset.dvd_prod_of_mem _ (Nat.mem_primeFactors.2 ⟨hq, h, hx⟩)

theorem rad_prime_pow {p k : ℕ} (hp : p.Prime) (hk : k ≠ 0) : rad (p ^ k) = p := by
  rw [rad, Nat.primeFactors_prime_pow hk hp, prod_singleton]

theorem rad_two_pow_mul_prime_pow {a b p : ℕ} (hp : p.Prime) (hp2 : p ≠ 2) (ha : a ≠ 0)
    (hb : b ≠ 0) : rad (2 ^ a * p ^ b) = 2 * p := by
  rw [rad, Nat.primeFactors_mul (pow_ne_zero _ two_ne_zero) (pow_ne_zero _ hp.ne_zero),
    Nat.primeFactors_prime_pow ha Nat.prime_two, Nat.primeFactors_prime_pow hb hp,
    ← Finset.insert_eq, prod_insert (by simpa using hp2.symm), prod_singleton]

/-! ## `σ` and valuations -/

theorem padicValNat_mul' {r x y : ℕ} (hr : r.Prime) (hx : x ≠ 0) (hy : y ≠ 0) :
    padicValNat r (x * y) = padicValNat r x + padicValNat r y := by
  rw [← Nat.factorization_def _ hr, ← Nat.factorization_def _ hr, ← Nat.factorization_def _ hr,
    Nat.factorization_mul hx hy, Finsupp.add_apply]

theorem padicValNat_two_two : padicValNat 2 2 = 1 := by
  rw [← Nat.factorization_def _ Nat.prime_two, Nat.prime_two.factorization_self]

theorem sigma_prime' {p : ℕ} (hp : p.Prime) : σ 1 p = p + 1 := by
  have := sigma_one_apply_prime_pow (i := 1) hp
  simpa [Finset.sum_range_succ, add_comm] using this

theorem sigma_two_mul_prime {p : ℕ} (hp : p.Prime) (hp2 : p ≠ 2) :
    σ 1 (2 * p) = 3 * (p + 1) := by
  have hc : Nat.Coprime 2 p := (Nat.coprime_primes Nat.prime_two hp).2 hp2.symm
  rw [isMultiplicative_sigma.map_mul_of_coprime hc, sigma_prime' Nat.prime_two,
    sigma_prime' hp]

theorem sum_range_two_mul (p m : ℕ) :
    ∑ i ∈ range (2 * m), p ^ i = (p + 1) * ∑ i ∈ range m, (p ^ 2) ^ i := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [show 2 * (m + 1) = 2 * m + 1 + 1 by ring, sum_range_succ, sum_range_succ, ih,
      sum_range_succ, ← pow_mul]
    ring

/-! ## Elementary congruences -/

theorem pow_three_mod_eight (k : ℕ) : 3 ^ k % 8 = 1 ∨ 3 ^ k % 8 = 3 := by
  induction k with
  | zero => left; rfl
  | succ k ih =>
    rw [pow_succ, Nat.mul_mod]
    rcases ih with h | h <;> rw [h] <;> norm_num

theorem three_dvd_four_pow_sub_one (j : ℕ) : 3 ∣ 4 ^ j - 1 := by
  simpa using nat_sub_dvd_pow_sub_pow 4 1 j

/-- `3 ∣ 2^(a+1) - 1` iff `a` is odd. -/
theorem three_dvd_mersenne_iff (a : ℕ) : 3 ∣ 2 ^ (a + 1) - 1 ↔ Odd a := by
  have h4 : ∀ j, (2 : ℕ) ^ (2 * j) = 4 ^ j := fun j => by
    rw [pow_mul]; norm_num
  have h1 : ∀ j, 1 ≤ (4 : ℕ) ^ j := fun j => Nat.one_le_pow _ _ (by norm_num)
  rcases Nat.even_or_odd' a with ⟨j, rfl | rfl⟩
  · have e : 2 ^ (2 * j + 1) = 2 * 4 ^ j := by rw [pow_succ, h4, mul_comm]
    rw [e]
    have := three_dvd_four_pow_sub_one j
    have := h1 j
    constructor
    · intro h; omega
    · intro h
      exact absurd h (by rw [Nat.not_odd_iff_even]; exact ⟨j, by ring⟩)
  · have e : 2 ^ (2 * j + 1 + 1) = 4 ^ (j + 1) := by
      rw [show 2 * j + 1 + 1 = 2 * (j + 1) by ring, h4]
    rw [e]
    exact ⟨fun _ => ⟨j, rfl⟩, fun _ => three_dvd_four_pow_sub_one _⟩

/-- If `2^(a+1) - 1` has `3` as its only prime factor then `a ≤ 1`. -/
theorem mersenne_primeFactors_three {a : ℕ} (h : (2 ^ (a + 1) - 1).primeFactors = {3}) :
    a ≤ 1 := by
  by_contra ha
  push_neg at ha
  have hpos : 1 < 2 ^ (a + 1) := Nat.one_lt_two_pow (by omega)
  have hM : 2 ^ (a + 1) - 1 ≠ 0 := by omega
  have huniq : ∀ {d}, Nat.Prime d → d ∣ 2 ^ (a + 1) - 1 → d = 3 := by
    intro d hd hdvd
    have : d ∈ (2 ^ (a + 1) - 1).primeFactors := Nat.mem_primeFactors.2 ⟨hd, hdvd, hM⟩
    rw [h] at this
    simpa using this
  have hpow := Nat.eq_prime_pow_of_unique_prime_dvd hM huniq
  have h8 : 2 ^ (a + 1) = 8 * 2 ^ (a - 2) := by
    rw [show a + 1 = (a - 2) + 3 by omega, pow_add]; ring
  have hmod : (2 ^ (a + 1) - 1) % 8 = 7 := by
    have : 0 < 2 ^ (a - 2) := Nat.pos_pow_of_pos _ (by norm_num)
    omega
  rw [hpow] at hmod
  rcases pow_three_mod_eight (2 ^ (a + 1) - 1).primeFactorsList.length with h' | h' <;> omega

/-! ## Lifting the exponent: `σ(p^b)` with `b ≥ 3` -/

theorem lt_geom_sum {q : ℕ} (hq : 2 ≤ q) {m : ℕ} (hm : 2 ≤ m) :
    m < ∑ i ∈ range m, q ^ i := by
  induction m, hm using Nat.le_induction with
  | base => simp [sum_range_succ]; omega
  | succ k _ ih =>
    rw [sum_range_succ]
    have := Nat.one_le_pow k q (by omega)
    omega

/-- Core LTE step. For an odd prime `p` and `m ≥ 2`, the number
`C = 1 + p^2 + ⋯ + p^(2(m-1))` has a prime factor not dividing `3(p+1)`. -/
theorem lte_core {p m : ℕ} (hp : p.Prime) (hpo : Odd p) (hm : 2 ≤ m)
    (h : ∀ r, r.Prime → r ∣ ∑ i ∈ range m, (p ^ 2) ^ i → r ∣ 3 * (p + 1)) : False := by
  set q := p ^ 2 with hq
  set C := ∑ i ∈ range m, q ^ i with hC
  have hp3 : 3 ≤ p := by
    rcases hp.eq_two_or_odd' with h2 | _
    · subst h2; exact absurd hpo (by decide)
    · have := hp.two_le
      rcases Nat.lt_or_ge p 3 with h | h
      · interval_cases p; exact absurd hpo (by decide)
      · exact h
  have hq9 : 9 ≤ q := by rw [hq]; nlinarith
  have hqC : (q - 1) * C + 1 = q ^ m := by
    have := geom_sum_mul_add (q - 1) m
    rw [Nat.sub_add_cancel (by omega : 1 ≤ q)] at this
    rw [mul_comm]; exact this
  have hCm : m < C := lt_geom_sum (by omega) hm
  have hC0 : C ≠ 0 := by omega
  have hm0 : m ≠ 0 := by omega
  have hqm : q ^ m - 1 = (q - 1) * C := by omega
  have hpm1 : (p + 1) * (p - 1) = q - 1 := by
    obtain ⟨k, rfl⟩ : ∃ k, p = k + 1 := ⟨p - 1, by omega⟩
    rw [hq]
    simp only [Nat.add_sub_cancel]
    apply (Nat.sub_eq_of_eq_add _).symm
    ring
  have key : ∀ r, r.Prime → C.factorization r ≤ m.factorization r := by
    intro r hr
    by_cases hrC : r ∣ C
    swap
    · rw [Nat.factorization_eq_zero_of_not_dvd hrC]; exact Nat.zero_le _
    -- `r ∤ p`, since `C ≡ 1 (mod p)`
    have hrp : ¬ r ∣ p := by
      intro hrp
      have hsplit : C = (∑ i ∈ range (m - 1), q ^ (i + 1)) + 1 := by
        rw [hC, show m = (m - 1) + 1 by omega, sum_range_succ']
        simp
      have hrs : r ∣ ∑ i ∈ range (m - 1), q ^ (i + 1) :=
        Finset.dvd_sum fun i _ =>
          (dvd_pow hrp two_ne_zero).trans (dvd_pow_self q (Nat.succ_ne_zero i))
      rw [hsplit] at hrC
      have := (Nat.dvd_add_right hrs).1 hrC
      exact hr.one_lt.ne' (Nat.dvd_one.1 this)
    have hrq : ¬ r ∣ q := fun h => hrp (hr.dvd_of_dvd_pow h)
    -- `r ∣ q - 1`
    have hrq1 : r ∣ q - 1 := by
      rw [← hpm1]
      rcases (Nat.Prime.dvd_mul hr).1 (h r hr hrC) with h3 | h3
      · have : r = 3 := (Nat.prime_dvd_prime_iff_eq hr Nat.prime_three).1 h3
        subst this
        have : 3 ∣ p + 1 ∨ 3 ∣ p - 1 := by omega
        rcases this with h' | h'
        · exact Dvd.dvd.mul_right h' _
        · exact Dvd.dvd.mul_left h' _
      · exact Dvd.dvd.mul_right h3 _
    haveI := Fact.mk hr
    rw [Nat.factorization_def C hr, Nat.factorization_def m hr]
    have hmul : padicValNat r (q ^ m - 1) = padicValNat r (q - 1) + padicValNat r C := by
      rw [hqm]; exact padicValNat_mul' hr (by omega) hC0
    by_cases hr2 : r = 2
    · subst hr2
      have hlte := padicValNat.pow_two_sub_pow (x := p) (y := 1) (by omega)
        (by rw [← even_iff_two_dvd]; exact Nat.Odd.sub_odd hpo odd_one)
        (by rw [← even_iff_two_dvd]; exact Nat.not_even_iff_odd.2 hpo)
        (n := 2 * m) (by omega) (even_two_mul m)
      rw [one_pow, pow_mul, ← hq] at hlte
      have h2m : padicValNat 2 (2 * m) = 1 + padicValNat 2 m := by
        rw [padicValNat_mul' Nat.prime_two two_ne_zero hm0, padicValNat_two_two]
      have hq1 : padicValNat 2 (q - 1) = padicValNat 2 (p + 1) + padicValNat 2 (p - 1) := by
        rw [← hpm1]; exact padicValNat_mul' Nat.prime_two (by omega) (by omega)
      omega
    · have hro : Odd r := hr.odd_of_ne_two hr2
      have hlte := padicValNat.pow_sub_pow (p := r) (x := q) (y := 1) hro (by omega)
        (by simpa using hrq1) (by exact hrq) hm0
      rw [one_pow] at hlte
      omega
  have hdvd : C ∣ m := (Nat.factorization_prime_le_iff_dvd hC0 hm0).1 key
  have := Nat.le_of_dvd (by omega) hdvd
  omega

/-! ## Forward direction for `n = 2^a p^b` -/

theorem sigma_pos'' {n : ℕ} (hn : 0 < n) : σ 1 n ≠ 0 :=
  (Discovery.SigmaOdd.sigma_pos' hn).ne'

/-- Forward direction when `n = 2^a p^b`, `p` an odd prime, `b ≥ 1`. -/
theorem c02_forward_prime_pow {a b p : ℕ} (hp : p.Prime) (hpo : Odd p) (hb : b ≠ 0)
    (h : rad (σ 1 (2 ^ a * p ^ b)) = σ 1 (rad (2 ^ a * p ^ b))) :
    (Squarefree (2 ^ a * p ^ b) ∧ Squarefree (σ 1 (2 ^ a * p ^ b))) ∨
      ∃ a' p', 2 ^ a * p ^ b = 2 ^ a' * p' ∧ p'.Prime ∧ Odd p' ∧ Odd a' ∧ 3 ≤ a' ∧
        Squarefree (p' + 1) ∧ ¬ 3 ∣ (p' + 1) ∧ rad (2 ^ (a' + 1) - 1) ∣ 3 * (p' + 1) := by
  have hp2 : p ≠ 2 := by rintro rfl; exact absurd hpo (by decide)
  have hn0 : 0 < 2 ^ a * p ^ b := Nat.pos_of_ne_zero
    (mul_ne_zero (pow_ne_zero _ two_ne_zero) (pow_ne_zero _ hp.ne_zero))
  have hσn : σ 1 (2 ^ a * p ^ b) = (2 ^ (a + 1) - 1) * σ 1 (p ^ b) :=
    Discovery.SigmaOdd.sigma_two_pow_mul a (p ^ b) (hpo.pow)
  have hσn0 := sigma_pos'' hn0
  -- `σ(rad n)` divides `3(p+1)` and is divisible by `p + 1`
  have hrad : σ 1 (rad (2 ^ a * p ^ b)) ∣ 3 * (p + 1) ∧
      (p + 1) ∣ σ 1 (rad (2 ^ a * p ^ b)) := by
    rcases Nat.eq_zero_or_pos a with rfl | ha
    · rw [pow_zero, one_mul, rad_prime_pow hp hb, sigma_prime' hp]
      exact ⟨dvd_mul_left _ _, dvd_rfl⟩
    · rw [rad_two_pow_mul_prime_pow hp hp2 ha.ne' hb, sigma_two_mul_prime hp hp2]
      exact ⟨dvd_rfl, dvd_mul_left _ _⟩
  obtain ⟨hsq, hpf⟩ := rad_eq_iff.1 h
  have hsr0 : σ 1 (rad (2 ^ a * p ^ b)) ≠ 0 := hsq.ne_zero
  -- every prime factor of `σ n` divides `3(p+1)`
  have hpfσ : ∀ r, r.Prime → r ∣ σ 1 (2 ^ a * p ^ b) → r ∣ 3 * (p + 1) := by
    intro r hr hrd
    have : r ∈ (σ 1 (2 ^ a * p ^ b)).primeFactors := Nat.mem_primeFactors.2 ⟨hr, hrd, hσn0⟩
    rw [hpf] at this
    exact (Nat.dvd_of_mem_primeFactors this).trans hrad.1
  have hMo : (2 ^ (a + 1) - 1) % 2 = 1 := by
    have : 2 ^ (a + 1) = 2 * 2 ^ a := by rw [pow_succ, mul_comm]
    have : 0 < 2 ^ a := Nat.pos_pow_of_pos _ (by norm_num)
    omega
  -- `b` is odd
  have hbo : Odd b := by
    have h2 : 2 ∣ σ 1 (rad (2 ^ a * p ^ b)) :=
      (even_iff_two_dvd.1 hpo.add_one).trans hrad.2
    have h2' : 2 ∈ (σ 1 (2 ^ a * p ^ b)).primeFactors := by
      rw [hpf]; exact Nat.mem_primeFactors.2 ⟨Nat.prime_two, h2, hsr0⟩
    have h2'' := Nat.dvd_of_mem_primeFactors h2'
    rw [hσn] at h2''
    rcases (Nat.Prime.dvd_mul Nat.prime_two).1 h2'' with h | h
    · omega
    · rw [sigma_one_apply_prime_pow hp] at h
      have := Discovery.SigmaOdd.sum_range_pow_mod_two p hpo (b + 1)
      rw [Nat.odd_iff]; omega
  -- `b = 1` (LTE)
  have hb1 : b = 1 := by
    by_contra hb1
    obtain ⟨k, hk⟩ := hbo
    have hm : 2 ≤ k + 1 := by omega
    apply lte_core hp hpo hm
    intro r hr hrC
    apply hpfσ r hr
    rw [hσn, sigma_one_apply_prime_pow hp, show b + 1 = 2 * (k + 1) by omega,
      sum_range_two_mul]
    exact Dvd.dvd.mul_left (Dvd.dvd.mul_left hrC _) _
  subst hb1
  rw [pow_one] at hσn hsq hpf h hrad hpfσ hn0 hσn0 ⊢
  rw [sigma_prime' hp] at hσn
  rcases Nat.eq_zero_or_pos a with rfl | ha
  · -- `n = p`
    left
    rw [pow_zero, one_mul] at h ⊢
    exact ⟨hp.prime.squarefree, c02_of_squarefree p hp.prime.squarefree h⟩
  -- `n = 2^a p`, `a ≥ 1`
  have hrn : rad (2 ^ a * p) = 2 * p := by
    simpa using rad_two_pow_mul_prime_pow (b := 1) hp hp2 ha.ne' one_ne_zero
  rw [hrn, sigma_two_mul_prime hp hp2] at hsq hpf
  obtain ⟨hcop, -, hsqp⟩ := Nat.squarefree_mul_iff.1 hsq
  have h3 : ¬ 3 ∣ p + 1 := (Nat.Prime.coprime_iff_not_dvd Nat.prime_three).1 hcop
  have hao : Odd a := by
    rw [← three_dvd_mersenne_iff]
    have h3' : 3 ∈ (σ 1 (2 ^ a * p)).primeFactors := by
      rw [hpf]; exact Nat.mem_primeFactors.2 ⟨Nat.prime_three, dvd_mul_right _ _, by omega⟩
    have := Nat.dvd_of_mem_primeFactors h3'
    rw [hσn] at this
    rcases (Nat.Prime.dvd_mul Nat.prime_three).1 this with h' | h'
    · exact h'
    · exact absurd h' h3
  rcases Nat.lt_or_ge a 3 with ha3 | ha3
  · -- `a = 1`, `n = 2p`
    have : a = 1 := by
      rcases hao with ⟨j, rfl⟩; omega
    subst this
    left
    rw [pow_one] at h ⊢
    have hsq2 : Squarefree (2 * p) := Nat.squarefree_mul_iff.2
      ⟨(Nat.coprime_primes Nat.prime_two hp).2 hp2.symm, Nat.prime_two.prime.squarefree,
        hp.prime.squarefree⟩
    exact ⟨hsq2, c02_of_squarefree _ hsq2 h⟩
  · right
    refine ⟨a, p, rfl, hp, hpo, hao, ha3, hsqp, h3, ?_⟩
    apply rad_dvd_of_primeFactors_subset
    rw [← hpf, hσn]
    exact Nat.primeFactors_mono (dvd_mul_right _ _) (by rw [← hσn]; exact hσn0)

/-! ## Main theorem -/

/-- **C02 (H2′), full characterisation.** For `n > 0`, `rad(σ n) = σ(rad n)` iff either
`n` and `σ n` are both squarefree, or `n = 2^a p` with `p` an odd prime, `a ≥ 3` odd,
`p + 1` squarefree, `3 ∤ p + 1` and `rad(2^(a+1) - 1) ∣ 3(p+1)`. -/
theorem c02_iff (n : ℕ) (hn : 0 < n) :
    rad (σ 1 n) = σ 1 (rad n) ↔
      (Squarefree n ∧ Squarefree (σ 1 n)) ∨
        ∃ a p, n = 2 ^ a * p ∧ p.Prime ∧ Odd p ∧ Odd a ∧ 3 ≤ a ∧ Squarefree (p + 1) ∧
          ¬ 3 ∣ (p + 1) ∧ rad (2 ^ (a + 1) - 1) ∣ 3 * (p + 1) := by
  constructor
  · intro h
    obtain ⟨a, m, hmo, rfl⟩ := Nat.exists_eq_two_pow_mul_odd hn.ne'
    by_cases hm1 : m = 1
    · subst hm1
      rw [mul_one] at h ⊢
      rcases Nat.eq_zero_or_pos a with rfl | ha
      · left
        simp [isMultiplicative_sigma.map_one]
      -- `n = 2^a`, `a ≥ 1`: only `a = 1`
      have hra : rad (2 ^ a) = 2 := rad_prime_pow Nat.prime_two ha.ne'
      rw [hra, sigma_prime' Nat.prime_two, Discovery.SigmaOdd.sigma_two_pow] at h
      obtain ⟨-, hpf⟩ := rad_eq_iff.1 h
      rw [Nat.Prime.primeFactors Nat.prime_three] at hpf
      have : a = 1 := by have := mersenne_primeFactors_three hpf; omega
      subst this
      left
      rw [pow_one]
      rw [sigma_prime' Nat.prime_two]
      exact ⟨Nat.prime_two.prime.squarefree, Nat.prime_three.prime.squarefree⟩
    · -- `m > 1` odd: `m = p^b`
      have hm0 : m ≠ 0 := by rintro rfl; exact absurd hmo (by decide)
      set p := m.minFac with hpdef
      have hp : p.Prime := Nat.minFac_prime hm1
      have hpm : p ∣ m := Nat.minFac_dvd m
      have hpo : Odd p := hmo.of_dvd_nat hpm
      have hn0 : 2 ^ a * m ≠ 0 := hn.ne'
      have huniq := odd_prime_factor_unique (2 ^ a * m) (squarefree_sigma_rad _ h)
      have hd : ∀ {d}, Nat.Prime d → d ∣ m → d = p := by
        intro d hd hdm
        exact huniq d (Nat.mem_primeFactors.2 ⟨hd, hdm.mul_left _, hn0⟩) p
          (Nat.mem_primeFactors.2 ⟨hp, hpm.mul_left _, hn0⟩) (hmo.of_dvd_nat hdm) hpo
      have hmp := Nat.eq_prime_pow_of_unique_prime_dvd hm0 hd
      set b := m.primeFactorsList.length
      have hb : b ≠ 0 := by
        intro hb0
        rw [hb0, pow_zero] at hmp
        exact hm1 hmp
      rw [hmp] at h ⊢
      exact c02_forward_prime_pow hp hpo hb h
  · rintro (⟨hsq, hsσ⟩ | ⟨a, p, rfl, hp, hpo, hao, -, hsqp, h3, hrad⟩)
    · exact c02b n hsq hsσ
    · have hp2 : p ≠ 2 := by rintro rfl; exact absurd hpo (by decide)
      have ha : a ≠ 0 := by rintro rfl; exact absurd hao (by decide)
      have hrn : rad (2 ^ a * p) = 2 * p := by
        simpa using rad_two_pow_mul_prime_pow (b := 1) hp hp2 ha one_ne_zero
      rw [hrn, sigma_two_mul_prime hp hp2,
        Discovery.SigmaOdd.sigma_two_pow_mul a p hpo, sigma_prime' hp]
      have hcop : Nat.Coprime 3 (p + 1) :=
        (Nat.Prime.coprime_iff_not_dvd Nat.prime_three).2 h3
      have hM0 : 2 ^ (a + 1) - 1 ≠ 0 := by
        have := Nat.one_lt_two_pow (n := a + 1) (by omega); omega
      have h3M : 3 ∣ 2 ^ (a + 1) - 1 := (three_dvd_mersenne_iff a).2 hao
      apply rad_eq_iff.2
      refine ⟨Nat.squarefree_mul_iff.2 ⟨hcop, Nat.prime_three.prime.squarefree, hsqp⟩, ?_⟩
      ext q
      simp only [Nat.mem_primeFactors, ne_eq, mul_eq_zero, hM0, Nat.add_one_ne_zero,
        OfNat.ofNat_ne_zero, or_self, not_false_eq_true, and_true]
      constructor
      · rintro ⟨hq, hqd⟩
        refine ⟨hq, ?_⟩
        rcases (Nat.Prime.dvd_mul hq).1 hqd with h' | h'
        · exact (prime_dvd_rad hq hM0 h').trans hrad
        · exact Dvd.dvd.mul_left h' _
      · rintro ⟨hq, hqd⟩
        refine ⟨hq, ?_⟩
        rcases (Nat.Prime.dvd_mul hq).1 hqd with h' | h'
        · exact (h'.trans h3M).mul_right _
        · exact Dvd.dvd.mul_left h' _

end Discovery.RadSigma
