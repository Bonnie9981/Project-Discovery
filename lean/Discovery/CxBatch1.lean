/-!
# DISC-0019: three OEIS conjecture checks (A215944, A058128, A218483)

1. `a215944_counterexample`: `n = 3048841 = 61 * 151 * 331` is a base-2 Fermat pseudoprime,
   divisible by the smaller base-2 pseudoprime `49981 = 151 * 331`, not of the form
   `p * ((m+1)p - m) * ((k+1)p - k)` with `m, k ≥ 1`, and not a multiple of 5461.
   This contradicts Coman's conjecture in A215944.
2. `a058128_weak_psp`: for every even `n ≥ 2`, `a = (n^n - n)/(n-1)^2` is an exact quotient
   and `n^a ≡ n (mod a)`; so `a` is prime or a weak Fermat pseudoprime to base `n`
   (Rotondo's conjecture in A058128).
3. `a218483_no_psp`: no `n ≡ 15 (mod 40)` satisfies `2^(n-1) ≡ 1 (mod n)` (A218483).

Big modular powers use the binary exponentiation `powModAux` (copied from
`A294646Counter`), proved equal to `b ^ e % m` by `powModAux_eq`.
Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.CxBatch1

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

/-! ## 1. A215944 -/

/-- Simple decidable primality: `p ≥ 2` and no divisor `d` with `2 ≤ d < p`. -/
def IsPrime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d < p → 2 ≤ d → p % d ≠ 0

instance : DecidablePred IsPrime := fun p =>
  inferInstanceAs (Decidable (2 ≤ p ∧ ∀ d, d < p → 2 ≤ d → p % d ≠ 0))

set_option maxRecDepth 100000 in
theorem prime_61 : IsPrime 61 := by decide
set_option maxRecDepth 100000 in
theorem prime_151 : IsPrime 151 := by decide
set_option maxRecDepth 100000 in
theorem prime_331 : IsPrime 331 := by decide

/-- The witness `N = 3048841` and its pseudoprime divisor `Q = 49981`. -/
def N : Nat := 3048841
def Q : Nat := 49981

theorem psp_N : 2 ^ (N - 1) % N = 1 := by
  rw [← powModAux_eq 64]; decide

theorem psp_Q : 2 ^ (Q - 1) % Q = 1 := by
  rw [← powModAux_eq 64]; decide

theorem factor_ge (p m : Nat) (hp : 1 ≤ p) : p ≤ (m + 1) * p - m := by
  have h1 : (m + 1) * p = m * p + p := Nat.succ_mul m p
  have h2 : m ≤ m * p := Nat.le_mul_of_pos_right m hp
  omega

set_option maxRecDepth 100000 in
theorem small_div : ∀ p, p < 146 → 3048841 % p = 0 → p = 1 ∨ p = 61 := by decide

set_option maxRecDepth 100000 in
theorem small_div2 : ∀ a, a < 414 → 121 ≤ a → 49981 % a = 0 → a % 60 = 1 → False := by
  decide

/-- 3048841 is not `p * ((m+1)p - m) * ((k+1)p - k)` for any naturals `p` and `m, k ≥ 1`. -/
theorem not_coman_form : ∀ p m k, 1 ≤ m → 1 ≤ k →
    p * ((m + 1) * p - m) * ((k + 1) * p - k) ≠ 3048841 := by
  intro p m k _ _ h
  rcases Nat.lt_or_ge p 1 with h0 | hp
  · have : p = 0 := by omega
    subst this; simp at h
  have hA := factor_ge p m hp
  have hB := factor_ge p k hp
  generalize hAdef : (m + 1) * p - m = A at h hA
  generalize hBdef : (k + 1) * p - k = B at h hB
  have hcube : p * p * p ≤ 3048841 :=
    h ▸ Nat.mul_le_mul (Nat.mul_le_mul (Nat.le_refl p) hA) hB
  have hp146 : p < 146 := by
    refine Nat.lt_of_not_le fun hge => ?_
    have := Nat.mul_le_mul (Nat.mul_le_mul hge hge) hge
    omega
  have hdiv : 3048841 % p = 0 := by
    rw [← h, Nat.mul_assoc]; exact Nat.mul_mod_right _ _
  rcases small_div p hp146 hdiv with h1 | h61
  · subst h1
    rw [Nat.mul_one] at hAdef hBdef
    have hA1 : A = 1 := by omega
    have hB1 : B = 1 := by omega
    subst hA1 hB1
    simp at h
  · subst h61
    have hA' : A = 60 * m + 61 := by omega
    have hB' : B = 60 * k + 61 := by omega
    have hAB : A * B = 49981 := by rw [Nat.mul_assoc] at h; omega
    have hAle : A < 414 := by
      have : A * 121 ≤ A * B := Nat.mul_le_mul_left A (by omega)
      omega
    exact small_div2 A hAle (by omega)
      (by rw [← hAB]; exact Nat.mul_mod_right _ _) (by omega)

/-- Counterexample to Coman's conjecture in A215944. -/
theorem a215944_counterexample :
    N = 3048841 ∧ N = 61 * 151 * 331 ∧ IsPrime 61 ∧ IsPrime 151 ∧ IsPrime 331 ∧
    2 ^ (N - 1) % N = 1 ∧
    Q = 151 * 331 ∧ 2 ^ (Q - 1) % Q = 1 ∧ N % Q = 0 ∧ Q < N ∧
    (∀ p m k, 1 ≤ m → 1 ≤ k → p * ((m + 1) * p - m) * ((k + 1) * p - k) ≠ N) ∧
    N % 5461 ≠ 0 :=
  ⟨rfl, by decide, prime_61, prime_151, prime_331, psp_N, by decide, psp_Q,
    by decide, by decide, not_coman_form, by decide⟩

/-! ## 2. A058128 -/

/-- Triangular numbers `tri j = j(j-1)/2`. -/
def tri : Nat → Nat
  | 0 => 0
  | j + 1 => tri j + j

theorem tri_two (j : Nat) : tri j * 2 + j = j * j := by
  induction j with
  | zero => rfl
  | succ j ih =>
    simp only [tri, Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul]
    omega

/-- Second-order binomial expansion: `(1+m)^j = 1 + j m + C(j,2) m^2 + m^3 c`. -/
theorem expand (m j : Nat) : ∃ c, (1 + m) ^ j = 1 + j * m + tri j * (m * m) + m * m * m * c := by
  induction j with
  | zero => exact ⟨0, by simp [tri]⟩
  | succ j ih =>
    obtain ⟨c, hc⟩ := ih
    refine ⟨c + tri j + m * c, ?_⟩
    rw [Nat.pow_succ, hc]
    simp only [tri, Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul, Nat.mul_assoc,
      Nat.mul_comm, Nat.mul_left_comm]
    omega

theorem geo_pow (S x t : Nat) : ∃ w, (1 + S * x) ^ t = 1 + S * w := by
  induction t with
  | zero => exact ⟨0, by simp⟩
  | succ t ih =>
    obtain ⟨w, hw⟩ := ih
    refine ⟨w + x + S * w * x, ?_⟩
    rw [Nat.pow_succ, hw]
    simp only [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul, Nat.mul_assoc,
      Nat.mul_comm, Nat.mul_left_comm]
    omega

/-- Rotondo's conjecture (A058128): for even `n ≥ 2`, `a = (n^n - n)/(n-1)^2` is an exact
quotient and `n^a ≡ n (mod a)`. -/
theorem a058128_weak_psp (n : Nat) (h2 : 2 ≤ n) (heven : n % 2 = 0) :
    (n - 1) ^ 2 * ((n ^ n - n) / (n - 1) ^ 2) = n ^ n - n ∧
    n ^ ((n ^ n - n) / (n - 1) ^ 2) % ((n ^ n - n) / (n - 1) ^ 2) =
      n % ((n ^ n - n) / (n - 1) ^ 2) := by
  obtain ⟨r, hr⟩ : ∃ r, n = 1 + (2 * r + 1) := ⟨n / 2 - 1, by omega⟩
  generalize hm : 2 * r + 1 = m at hr
  subst hr
  obtain ⟨c, hc⟩ := expand m m
  have htri : tri m = m * r := by
    have h1 := tri_two m
    have h' : m * m = m * r * 2 + m := by
      rw [← hm]
      simp only [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul, Nat.mul_assoc,
        Nat.mul_comm, Nat.mul_left_comm]
    omega
  have hpow : (1 + m) ^ m = 1 + m * m * (1 + m * (r + c)) := by
    rw [hc, htri]
    simp only [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul, Nat.mul_assoc,
      Nat.mul_comm, Nat.mul_left_comm]
    omega
  have ha1 : (1 + m) * (1 + m * (r + c)) = 1 + m * (1 + (r + c) + m * (r + c)) := by
    simp only [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul, Nat.mul_assoc,
      Nat.mul_comm, Nat.mul_left_comm]
    omega
  generalize hS : 1 + m * (r + c) = S at hpow ha1
  generalize ht : 1 + (r + c) + m * (r + c) = t at ha1
  have hsub : 1 + m - 1 = m := by omega
  have hX : (1 + m) ^ (1 + m) - (1 + m) = m ^ 2 * ((1 + m) * S) := by
    rw [Nat.pow_add, Nat.pow_one, hpow, Nat.mul_add, Nat.mul_one, Nat.add_sub_cancel_left,
      Nat.pow_two]
    simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  have hm2 : 0 < m ^ 2 := by rw [Nat.pow_two]; exact Nat.mul_pos (by omega) (by omega)
  rw [hsub, hX, Nat.mul_div_cancel_left _ hm2]
  refine ⟨rfl, ?_⟩
  obtain ⟨w, hw⟩ := geo_pow S (m * m) t
  have hpa : (1 + m) ^ ((1 + m) * S) = (1 + m) + (1 + m) * S * w := by
    conv => lhs; rw [ha1]
    rw [Nat.pow_add, Nat.pow_one, Nat.pow_mul, hpow, Nat.mul_comm (m * m) S, hw,
      Nat.mul_add, Nat.mul_one, Nat.mul_assoc]
  rw [hpa, Nat.add_mul_mod_self_left]

/-- Sanity check `n = 4`: `a = 28` and `4^28 ≡ 4 (mod 28)`. -/
theorem a058128_n4 : (4 ^ 4 - 4) / (4 - 1) ^ 2 = 28 ∧ 4 ^ 28 % 28 = 4 := by decide

/-! ## 3. A218483 -/

/-- No `n ≡ 15 (mod 40)` is a base-2 Fermat pseudoprime (indeed none satisfies
`2^(n-1) ≡ 1 (mod n)`): `5 ∣ n` but `n - 1 ≡ 2 (mod 4)`, so `2^(n-1) ≡ 4 (mod 5)`. -/
theorem a218483_no_psp (n : Nat) (h : n % 40 = 15) : 2 ^ (n - 1) % n ≠ 1 := by
  intro h1
  obtain ⟨q, hq⟩ : ∃ q, n - 1 = 4 * q + 2 := ⟨(n - 1) / 4, by omega⟩
  have h5 : 5 ∣ n := ⟨n / 5, by omega⟩
  have hm5 : 2 ^ (n - 1) % 5 = 1 := by
    rw [← Nat.mod_mod_of_dvd _ h5, h1]
  rw [hq, Nat.pow_add, Nat.pow_mul, Nat.mul_mod, ← pow_mod' (2 ^ 4) q 5] at hm5
  simp at hm5

end Discovery.CxBatch1
