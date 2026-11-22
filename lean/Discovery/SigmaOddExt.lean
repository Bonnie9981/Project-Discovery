import Discovery.SigmaOdd
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Tactic.NormNum.Prime

/-!
# DISC-0006 / C01 extension: `v₂(n) ≤ 22`

Extends `Discovery.SigmaOdd.c01_of_not_two_pow_eleven_dvd`.

* `mersenne_not_abundant_ext`: `2^(a+1) - 1` is not abundant for `12 ≤ a ≤ 22`
  (explicit factorizations, `σ` multiplicativity, `norm_num`; no large `decide`).
* `c01_even_v2_eq_eleven`: no even solution with `v₂(n) = 11`, although `4095 = 2^12 - 1`
  is abundant. With `σ(m) = 2^b t` (`t` odd) the equation becomes
  `(2^(b+1) - 1) σ(t) = σ(4095 t)`, with `b ≥ 12`. Splitting off the `3, 5, 7, 13` parts of `t`,
  the ratio `σ(4095 t)/σ(t)` equals `8736` (even, impossible) when `gcd(t, 4095) = 1`, and is
  `< 8191` otherwise.
* `c01_of_not_two_pow_twentythree_dvd`: C01 for every `n > 0` with `2^23 ∤ n`.
-/

namespace Discovery.SigmaOdd

open ArithmeticFunction Finset

/-! ### Helpers on `σ` of prime powers -/

theorem sigma_pp_mul {p k r : ℕ} (hp : p.Prime) (hr : ¬ p ∣ r) :
    σ 1 (p ^ k * r) = σ 1 (p ^ k) * σ 1 r :=
  isMultiplicative_sigma.map_mul_of_coprime
    (Nat.Coprime.pow_left k ((Nat.Prime.coprime_iff_not_dvd hp).2 hr))

theorem not_dvd_pp_mul {p q k r : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q)
    (hr : ¬ p ∣ r) : ¬ p ∣ q ^ k * r := by
  intro h
  rcases (Nat.Prime.dvd_mul hp).1 h with h | h
  · exact hpq ((Nat.prime_dvd_prime_iff_eq hp hq).1 (hp.dvd_of_dvd_pow h))
  · exact hr h

/-- `σ(p^(e+f)) = (1 + p + ⋯ + p^(e-1)) + p^e σ(p^f)`. -/
theorem sigma_pp_split {p : ℕ} (hp : p.Prime) (e f : ℕ) :
    σ 1 (p ^ (e + f)) = (∑ i ∈ range e, p ^ i) + p ^ e * σ 1 (p ^ f) := by
  rw [sigma_one_apply_prime_pow hp, sigma_one_apply_prime_pow hp,
    show e + f + 1 = e + (f + 1) by ring, Finset.sum_range_add, Finset.mul_sum]
  simp [pow_add]

theorem sigma_pp_ge {p f : ℕ} (hp : p.Prime) (hf : 1 ≤ f) : p + 1 ≤ σ 1 (p ^ f) := by
  rw [sigma_one_apply_prime_pow hp]
  have hs : range 2 ⊆ range (f + 1) := range_subset.2 (by omega)
  have := Finset.sum_le_sum_of_subset (f := fun i => p ^ i) hs
  rw [show (∑ i ∈ range 2, p ^ i) = p + 1 by
    rw [Finset.sum_range_succ, Finset.sum_range_one]; ring] at this
  exact this

theorem sigma_pp_le {p : ℕ} (e f : ℕ) :
    σ 1 (p ^ (e + f)) ≤ σ 1 (p ^ e) * σ 1 (p ^ f) := by
  rw [pow_add]; exact sigma_mul_le _ _

/-- If `f ≥ 1`: `(p+1) σ(p^(e+f)) ≤ ((1 + ⋯ + p^(e-1)) + (p+1) p^e) σ(p^f)`. -/
theorem sigma_pp_le' {p : ℕ} (hp : p.Prime) (e : ℕ) {f : ℕ} (hf : 1 ≤ f) :
    (p + 1) * σ 1 (p ^ (e + f)) ≤ ((∑ i ∈ range e, p ^ i) + (p + 1) * p ^ e) * σ 1 (p ^ f) := by
  rw [sigma_pp_split hp]
  set c := ∑ i ∈ range e, p ^ i
  set B := σ 1 (p ^ f)
  have hB : p + 1 ≤ B := sigma_pp_ge hp hf
  have h1 : (p + 1) * c ≤ B * c := Nat.mul_le_mul_right c hB
  calc (p + 1) * (c + p ^ e * B) = (p + 1) * c + (p + 1) * p ^ e * B := by ring
    _ ≤ B * c + (p + 1) * p ^ e * B := Nat.add_le_add_right h1 _
    _ = (c + (p + 1) * p ^ e) * B := by ring

theorem prod4_bound {A1 A2 A3 A4 B1 B2 B3 B4 m1 m2 m3 m4 k1 k2 k3 k4 : ℕ}
    (h1 : m1 * A1 ≤ k1 * B1) (h2 : m2 * A2 ≤ k2 * B2) (h3 : m3 * A3 ≤ k3 * B3)
    (h4 : m4 * A4 ≤ k4 * B4) :
    (m1 * m2 * m3 * m4) * (A1 * (A2 * (A3 * A4))) ≤
      (k1 * k2 * k3 * k4) * (B1 * (B2 * (B3 * B4))) :=
  calc (m1 * m2 * m3 * m4) * (A1 * (A2 * (A3 * A4)))
      = (m1 * A1) * (m2 * A2) * (m3 * A3) * (m4 * A4) := by ring
    _ ≤ (k1 * B1) * (k2 * B2) * (k3 * B3) * (k4 * B4) :=
        Nat.mul_le_mul (Nat.mul_le_mul (Nat.mul_le_mul h1 h2) h3) h4
    _ = (k1 * k2 * k3 * k4) * (B1 * (B2 * (B3 * B4))) := by ring

/-! ### Part 1: `2^(a+1) - 1` is not abundant for `12 ≤ a ≤ 22` -/

theorem sigma_prime_eq {p : ℕ} (hp : p.Prime) : σ 1 p = p + 1 := by
  have := sigma_one_apply_prime_pow (i := 1) hp
  simp [Finset.sum_range_succ] at this
  rw [this, add_comm]

theorem sigma_pp_eval {p : ℕ} (hp : p.Prime) (k : ℕ) :
    σ 1 (p ^ k) = ∑ i ∈ range (k + 1), p ^ i := sigma_one_apply_prime_pow hp

-- a = 12: 8191 is prime
theorem mersenne13 : σ 1 (2 ^ 13 - 1) ≤ 2 * (2 ^ 13 - 1) := by
  rw [show (2 ^ 13 - 1 : ℕ) = 8191 by norm_num, sigma_prime_eq (by norm_num)]
  norm_num

-- a = 13: 16383 = 3 · 43 · 127
theorem mersenne14 : σ 1 (2 ^ 14 - 1) ≤ 2 * (2 ^ 14 - 1) := by
  rw [show (2 ^ 14 - 1 : ℕ) = 3 ^ 1 * (43 ^ 1 * 127 ^ 1) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 14: 32767 = 7 · 31 · 151
theorem mersenne15 : σ 1 (2 ^ 15 - 1) ≤ 2 * (2 ^ 15 - 1) := by
  rw [show (2 ^ 15 - 1 : ℕ) = 7 ^ 1 * (31 ^ 1 * 151 ^ 1) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 15: 65535 = 3 · 5 · 17 · 257
theorem mersenne16 : σ 1 (2 ^ 16 - 1) ≤ 2 * (2 ^ 16 - 1) := by
  rw [show (2 ^ 16 - 1 : ℕ) = 3 ^ 1 * (5 ^ 1 * (17 ^ 1 * 257 ^ 1)) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num),
    sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 16: 131071 is prime
theorem mersenne17 : σ 1 (2 ^ 17 - 1) ≤ 2 * (2 ^ 17 - 1) := by
  rw [show (2 ^ 17 - 1 : ℕ) = 131071 by norm_num, sigma_prime_eq (by norm_num)]
  norm_num

-- a = 17: 262143 = 3^3 · 7 · 19 · 73
theorem mersenne18 : σ 1 (2 ^ 18 - 1) ≤ 2 * (2 ^ 18 - 1) := by
  rw [show (2 ^ 18 - 1 : ℕ) = 3 ^ 3 * (7 ^ 1 * (19 ^ 1 * 73 ^ 1)) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num),
    sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 18: 524287 is prime
theorem mersenne19 : σ 1 (2 ^ 19 - 1) ≤ 2 * (2 ^ 19 - 1) := by
  rw [show (2 ^ 19 - 1 : ℕ) = 524287 by norm_num, sigma_prime_eq (by norm_num)]
  norm_num

-- a = 19: 1048575 = 3 · 5^2 · 11 · 31 · 41
theorem mersenne20 : σ 1 (2 ^ 20 - 1) ≤ 2 * (2 ^ 20 - 1) := by
  rw [show (2 ^ 20 - 1 : ℕ) = 3 ^ 1 * (5 ^ 2 * (11 ^ 1 * (31 ^ 1 * 41 ^ 1))) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 20: 2097151 = 7^2 · 127 · 337
theorem mersenne21 : σ 1 (2 ^ 21 - 1) ≤ 2 * (2 ^ 21 - 1) := by
  rw [show (2 ^ 21 - 1 : ℕ) = 7 ^ 2 * (127 ^ 1 * 337 ^ 1) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 21: 4194303 = 3 · 23 · 89 · 683
theorem mersenne22 : σ 1 (2 ^ 22 - 1) ≤ 2 * (2 ^ 22 - 1) := by
  rw [show (2 ^ 22 - 1 : ℕ) = 3 ^ 1 * (23 ^ 1 * (89 ^ 1 * 683 ^ 1)) by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num), sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num),
    sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

-- a = 22: 8388607 = 47 · 178481
theorem mersenne23 : σ 1 (2 ^ 23 - 1) ≤ 2 * (2 ^ 23 - 1) := by
  rw [show (2 ^ 23 - 1 : ℕ) = 47 ^ 1 * 178481 ^ 1 by norm_num,
    sigma_pp_mul (by norm_num) (by norm_num),
    sigma_pp_eval (by norm_num), sigma_pp_eval (by norm_num)]
  norm_num [Finset.sum_range_succ]

/-- `2^(a+1) - 1` is not abundant for `12 ≤ a ≤ 22`. -/
theorem mersenne_not_abundant_ext (a : ℕ) (ha : 12 ≤ a) (ha22 : a ≤ 22) :
    σ 1 (2 ^ (a + 1) - 1) ≤ 2 * (2 ^ (a + 1) - 1) := by
  interval_cases a
  · exact mersenne13
  · exact mersenne14
  · exact mersenne15
  · exact mersenne16
  · exact mersenne17
  · exact mersenne18
  · exact mersenne19
  · exact mersenne20
  · exact mersenne21
  · exact mersenne22
  · exact mersenne23

/-! ### Part 2: `v₂(n) = 11` -/

/-- Key inequality for `q = 4095 = 3^2 · 5 · 7 · 13`: for `t > 0` and odd `N ≥ 8191`,
`σ(4095 t) ≠ N σ(t)`. -/
theorem sigma_4095_mul_ne (t N : ℕ) (ht : 0 < t) (hN : 8191 ≤ N) (hNo : Odd N) :
    σ 1 (4095 * t) ≠ N * σ 1 t := by
  have p3 : Nat.Prime 3 := by norm_num
  have p5 : Nat.Prime 5 := by norm_num
  have p7 : Nat.Prime 7 := by norm_num
  have p13 : Nat.Prime 13 := by norm_num
  obtain ⟨f3, t1, h3, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd ht.ne' 3 (by norm_num)
  have ht1 : t1 ≠ 0 := by rintro rfl; simp at ht
  obtain ⟨f5, t2, h5, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd ht1 5 (by norm_num)
  have ht2 : t2 ≠ 0 := by rintro rfl; simp at ht1
  obtain ⟨f7, t3, h7, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd ht2 7 (by norm_num)
  have ht3 : t3 ≠ 0 := by rintro rfl; simp at ht2
  obtain ⟨f13, u, h13, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd ht3 13 (by norm_num)
  have hu : u ≠ 0 := by rintro rfl; simp at ht3
  -- divisibility facts about `u`
  have h3u : ¬ 3 ∣ u := fun h => h3 (h.trans ⟨5 ^ f5 * (7 ^ f7 * 13 ^ f13), by ring⟩)
  have h5u : ¬ 5 ∣ u := fun h => h5 (h.trans ⟨7 ^ f7 * 13 ^ f13, by ring⟩)
  have h7u : ¬ 7 ∣ u := fun h => h7 (h.trans ⟨13 ^ f13, by ring⟩)
  have hqt : 4095 * (3 ^ f3 * (5 ^ f5 * (7 ^ f7 * (13 ^ f13 * u)))) =
      3 ^ (2 + f3) * (5 ^ (1 + f5) * (7 ^ (1 + f7) * (13 ^ (1 + f13) * u))) := by ring
  have n35 : ¬ 3 ∣ 5 ^ (1 + f5) * (7 ^ (1 + f7) * (13 ^ (1 + f13) * u)) :=
    not_dvd_pp_mul p3 p5 (by norm_num) (not_dvd_pp_mul p3 p7 (by norm_num)
      (not_dvd_pp_mul p3 p13 (by norm_num) h3u))
  have n57 : ¬ 5 ∣ 7 ^ (1 + f7) * (13 ^ (1 + f13) * u) :=
    not_dvd_pp_mul p5 p7 (by norm_num) (not_dvd_pp_mul p5 p13 (by norm_num) h5u)
  have n713 : ¬ 7 ∣ 13 ^ (1 + f13) * u := not_dvd_pp_mul p7 p13 (by norm_num) h7u
  rw [hqt, sigma_pp_mul p3 n35, sigma_pp_mul p5 n57, sigma_pp_mul p7 n713,
    sigma_pp_mul p13 h13, sigma_pp_mul p3 h3, sigma_pp_mul p5 h5, sigma_pp_mul p7 h7,
    sigma_pp_mul p13 h13]
  -- the `0`-exponent bounds `A ≤ σ(p^e) B`
  have b3 := sigma_pp_le (p := 3) 2 f3
  have b5 := sigma_pp_le (p := 5) 1 f5
  have b7 := sigma_pp_le (p := 7) 1 f7
  have b13 := sigma_pp_le (p := 13) 1 f13
  have e3 : σ 1 (3 ^ 2) = 13 := by rw [sigma_pp_eval p3]; norm_num [Finset.sum_range_succ]
  have e5 : σ 1 (5 ^ 1) = 6 := by rw [sigma_pp_eval p5]; norm_num [Finset.sum_range_succ]
  have e7 : σ 1 (7 ^ 1) = 8 := by rw [sigma_pp_eval p7]; norm_num [Finset.sum_range_succ]
  have e13 : σ 1 (13 ^ 1) = 14 := by rw [sigma_pp_eval p13]; norm_num [Finset.sum_range_succ]
  rw [e3] at b3
  rw [e5] at b5
  rw [e7] at b7
  rw [e13] at b13
  have hS : 0 < σ 1 u := sigma_pos' (Nat.pos_of_ne_zero hu)
  have hB : 0 < σ 1 (3 ^ f3) * (σ 1 (5 ^ f5) * (σ 1 (7 ^ f7) * σ 1 (13 ^ f13))) := by
    have := sigma_pos' (n := 3 ^ f3) (by positivity)
    have := sigma_pos' (n := 5 ^ f5) (by positivity)
    have := sigma_pos' (n := 7 ^ f7) (by positivity)
    have := sigma_pos' (n := 13 ^ f13) (by positivity)
    positivity
  set A3 := σ 1 (3 ^ (2 + f3))
  set A5 := σ 1 (5 ^ (1 + f5))
  set A7 := σ 1 (7 ^ (1 + f7))
  set A13 := σ 1 (13 ^ (1 + f13))
  set B3 := σ 1 (3 ^ f3)
  set B5 := σ 1 (5 ^ f5)
  set B7 := σ 1 (7 ^ f7)
  set B13 := σ 1 (13 ^ f13)
  set S := σ 1 u
  intro h
  have hAB : A3 * (A5 * (A7 * A13)) = N * (B3 * (B5 * (B7 * B13))) := by
    apply Nat.eq_of_mul_eq_mul_right hS
    calc A3 * (A5 * (A7 * A13)) * S = A3 * (A5 * (A7 * (A13 * S))) := by ring
      _ = N * (B3 * (B5 * (B7 * (B13 * S)))) := h
      _ = N * (B3 * (B5 * (B7 * B13))) * S := by ring
  set B := B3 * (B5 * (B7 * B13))
  -- if some exponent `f ≥ 1`, the product is too small
  have key : ∀ m k : ℕ, m * (A3 * (A5 * (A7 * A13))) ≤ k * B → k < m * 8191 → False := by
    intro m k hle hlt
    rw [hAB] at hle
    have : (m * N) * B ≤ k * B := by rw [mul_assoc]; exact hle
    have := Nat.le_of_mul_le_mul_right this hB
    have : m * 8191 ≤ m * N := Nat.mul_le_mul_left m hN
    omega
  have o3 : 1 * A3 ≤ 13 * B3 := by omega
  have o5 : 1 * A5 ≤ 6 * B5 := by omega
  have o7 : 1 * A7 ≤ 8 * B7 := by omega
  have o13 : 1 * A13 ≤ 14 * B13 := by omega
  by_cases g3 : 1 ≤ f3
  · have := sigma_pp_le' p3 2 g3
    norm_num [Finset.sum_range_succ] at this
    exact key _ _ (prod4_bound this o5 o7 o13) (by norm_num)
  by_cases g5 : 1 ≤ f5
  · have := sigma_pp_le' p5 1 g5
    norm_num [Finset.sum_range_succ] at this
    exact key _ _ (prod4_bound o3 this o7 o13) (by norm_num)
  by_cases g7 : 1 ≤ f7
  · have := sigma_pp_le' p7 1 g7
    norm_num [Finset.sum_range_succ] at this
    exact key _ _ (prod4_bound o3 o5 this o13) (by norm_num)
  by_cases g13 : 1 ≤ f13
  · have := sigma_pp_le' p13 1 g13
    norm_num [Finset.sum_range_succ] at this
    exact key _ _ (prod4_bound o3 o5 o7 this) (by norm_num)
  -- all exponents zero: the ratio is `σ(4095) = 8736`, which is even
  have z3 : f3 = 0 := by omega
  have z5 : f5 = 0 := by omega
  have z7 : f7 = 0 := by omega
  have z13 : f13 = 0 := by omega
  subst z3 z5 z7 z13
  simp only [A3, A5, A7, A13, B, B3, B5, B7, B13, add_zero, pow_zero,
    isMultiplicative_sigma.map_one, e3, e5, e7, e13] at hAB
  obtain ⟨r, hr⟩ := hNo
  omega

/-- **C01, `v₂(n) = 11`**: for odd `m`, `σ(σ_odd(2^11 m)) ≠ σ_odd(σ(2^11 m))`. -/
theorem c01_even_v2_eq_eleven (m : ℕ) (hm : Odd m) :
    σ 1 (sigmaOdd (2 ^ 11 * m)) ≠ sigmaOdd (σ 1 (2 ^ 11 * m)) := by
  rw [sigmaOdd_two_pow_mul 11 m hm, sigma_two_pow_mul 11 m hm]
  obtain ⟨b, t, ht, hs⟩ := Nat.exists_eq_two_pow_mul_odd (sigma_pos' hm.pos).ne'
  rw [show (2 ^ (11 + 1) - 1 : ℕ) = 4095 by norm_num]
  have hqo : Odd 4095 := ⟨2047, by norm_num⟩
  have hqt : 4095 * σ 1 m = 2 ^ b * (4095 * t) := by rw [hs]; ring
  rw [hqt, sigmaOdd_two_pow_mul b (4095 * t) (hqo.mul ht), hs, sigma_two_pow_mul b t ht]
  intro h
  have hlow := lt_sigma_mul (q := 4095) (t := t) (by norm_num) ht.pos
  rw [← h] at hlow
  have h1 : 4095 < 2 ^ (b + 1) - 1 := lt_of_mul_lt_mul_right hlow (Nat.zero_le _)
  have hb : 12 ≤ b := by
    by_contra hc
    push_neg at hc
    have : 2 ^ (b + 1) ≤ 2 ^ 12 := Nat.pow_le_pow_right (by norm_num) (by omega)
    norm_num at this
    omega
  have hN : 8191 ≤ 2 ^ (b + 1) - 1 := by
    have : 2 ^ 13 ≤ 2 ^ (b + 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
    norm_num at this
    omega
  have hNo : Odd (2 ^ (b + 1) - 1) := by
    have : 2 ^ (b + 1) = 2 * 2 ^ b := by ring
    have : 0 < 2 ^ b := Nat.pos_pow_of_pos b (by norm_num)
    exact Nat.odd_iff.2 (by omega)
  exact sigma_4095_mul_ne t _ ht.pos hN hNo h.symm

/-! ### Part 3: combined -/

/-- **C01 for every `n > 0` with `2^23 ∤ n`** (i.e. `v₂(n) ≤ 22`):
`σ(σ_odd n) = σ_odd(σ n) ↔ n` is an odd perfect square. -/
theorem c01_of_not_two_pow_twentythree_dvd (n : ℕ) (hn : 0 < n) (h : ¬ 2 ^ 23 ∣ n) :
    σ 1 (sigmaOdd n) = sigmaOdd (σ 1 n) ↔ Odd n ∧ IsSquare n := by
  obtain ⟨a, m, hm, rfl⟩ := Nat.exists_eq_two_pow_mul_odd hn.ne'
  rcases Nat.eq_zero_or_pos a with rfl | ha
  · simp only [pow_zero, one_mul]
    rw [c01_odd m hm]
    exact ⟨fun h => ⟨hm, h⟩, fun h => h.2⟩
  · have ha22 : a ≤ 22 := by
      by_contra hc
      push_neg at hc
      exact h (Dvd.dvd.mul_right (Nat.pow_dvd_pow 2 hc) m)
    have hne : σ 1 (sigmaOdd (2 ^ a * m)) ≠ sigmaOdd (σ 1 (2 ^ a * m)) := by
      rcases lt_trichotomy a 11 with hlt | rfl | hgt
      · exact c01_even_of_not_abundant a m ha hm (mersenne_not_abundant a ha (by omega))
      · exact c01_even_v2_eq_eleven m hm
      · exact c01_even_of_not_abundant a m ha hm (mersenne_not_abundant_ext a hgt ha22)
    have hev : ¬ Odd (2 ^ a * m) := by
      rw [Nat.not_odd_iff_even]
      exact (Nat.even_pow.2 ⟨even_two, ha.ne'⟩).mul_right m
    exact ⟨fun h => absurd h hne, fun h => absurd h.1 hev⟩

end Discovery.SigmaOdd
