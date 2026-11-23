/-!
# DISC-0021: a counterexample to Ratajczak's 2019 conjecture in OEIS A134559

`b n k` is the sum of all `u` with `1 ≤ u ≤ n` and `n mod u = k`, and
`P n = ∏_{k=0}^{⌈n/2⌉-1} b n k` (the `n`-th antidiagonal product of A134559).
The conjecture says the `n` with `gcd(P n, n) = 1` and `gcd(P (n+1), n+1) = 2`
are exactly the primes `p > 5` with `(p+1)/2` prime (A005383 without 3, 5).

`p = 4933` is such a prime (`2467` is prime too), but `4934 ∣ P 4934`, so
`gcd(P 4934, 4934) = 4934 ≠ 2` and `4933` is not a solution. The reason is
`b 4934 134 = 14802 = 6 * 2467`.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A134559Counter

/-- `sumTo g K = g 0 + g 1 + ⋯ + g (K-1)`. -/
def sumTo (g : Nat → Nat) : Nat → Nat
  | 0 => 0
  | K + 1 => sumTo g K + g K

/-- `b n k = Σ { u : 1 ≤ u ≤ n, n % u = k }` (terms `u = 0..n`, `u = 0` contributes 0). -/
def b (n k : Nat) : Nat :=
  sumTo (fun u => if 1 ≤ u ∧ n % u = k then u else 0) (n + 1)

/-- `prodTo f K = f 0 * f 1 * ⋯ * f (K-1)`. -/
def prodTo (f : Nat → Nat) : Nat → Nat
  | 0 => 1
  | K + 1 => prodTo f K * f K

/-- `P n = ∏_{k < ⌈n/2⌉} b n k`; note `⌈n/2⌉ = (n+1)/2`. -/
def P (n : Nat) : Nat := prodTo (b n) ((n + 1) / 2)

def IsPrime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d < p → 2 ≤ d → p % d ≠ 0

/-! Kernel evaluation of a recursion of depth ~5000 overflows the stack, so long sums
are evaluated as `a` blocks of length `c` (`sumTo_mul`); the definitions above stay literal. -/

theorem sumTo_add (g : Nat → Nat) (m c : Nat) :
    sumTo g (m + c) = sumTo g m + sumTo (fun j => g (m + j)) c := by
  induction c with
  | zero => rfl
  | succ c ih =>
    show sumTo g (m + c) + g (m + c) = sumTo g m + (sumTo (fun j => g (m + j)) c + g (m + c))
    rw [ih, Nat.add_assoc]

theorem sumTo_mul (g : Nat → Nat) (a c : Nat) :
    sumTo g (a * c) = sumTo (fun i => sumTo (fun j => g (c * i + j)) c) a := by
  induction a with
  | zero => simp [sumTo]
  | succ a ih =>
    show sumTo g ((a + 1) * c) = sumTo (fun i => sumTo (fun j => g (c * i + j)) c) a +
      sumTo (fun j => g (c * a + j)) c
    rw [Nat.add_mul, Nat.one_mul, sumTo_add, ih, Nat.mul_comm a c]

theorem sumTo_eq_zero {g : Nat → Nat} {K : Nat} (h : sumTo g K = 0) : ∀ i, i < K → g i = 0 := by
  induction K with
  | zero => intro i hi; exact absurd hi (Nat.not_lt_zero i)
  | succ K ih =>
    intro i hi
    have h' : sumTo g K + g K = 0 := h
    rcases Nat.lt_succ_iff_lt_or_eq.mp hi with hlt | heq
    · exact ih (Nat.eq_zero_of_add_eq_zero_right h') i hlt
    · subst heq; exact Nat.eq_zero_of_add_eq_zero_left h'

/-- Number of divisors `d` of `p` with `2 ≤ d < p`, as an indicator sum over `d < a*c`. -/
def ndiv (p : Nat) (d : Nat) : Nat := if 2 ≤ d ∧ d < p ∧ p % d = 0 then 1 else 0

theorem isPrime_of_blocks (p a c : Nat) (hp : 2 ≤ p) (hac : p ≤ a * c)
    (h : sumTo (fun i => sumTo (fun j => ndiv p (c * i + j)) c) a = 0) : IsPrime p := by
  refine ⟨hp, fun d hd h2 hmod => ?_⟩
  rw [← sumTo_mul] at h
  have := sumTo_eq_zero h d (Nat.lt_of_lt_of_le hd hac)
  simp [ndiv, h2, hd, hmod] at this

theorem dvd_prodTo (f : Nat → Nat) {i K : Nat} (h : i < K) : f i ∣ prodTo f K := by
  induction K with
  | zero => exact absurd h (Nat.not_lt_zero i)
  | succ K ih =>
    simp only [prodTo]
    rcases Nat.lt_succ_iff_lt_or_eq.mp h with hlt | heq
    · exact Nat.dvd_trans (ih hlt) (Nat.dvd_mul_right _ _)
    · subst heq; exact Nat.dvd_mul_left _ _

theorem dvd_prodTo_two (f : Nat → Nat) {i j K : Nat} (hij : i < j) (hj : j < K) :
    f i * f j ∣ prodTo f K := by
  induction K with
  | zero => exact absurd hj (Nat.not_lt_zero j)
  | succ K ih =>
    simp only [prodTo]
    rcases Nat.lt_succ_iff_lt_or_eq.mp hj with hlt | heq
    · exact Nat.dvd_trans (ih hlt) (Nat.dvd_mul_right _ _)
    · subst heq; exact Nat.mul_dvd_mul (dvd_prodTo f hij) (Nat.dvd_refl _)

set_option maxRecDepth 100000 in
theorem prime_4933 : IsPrime 4933 := isPrime_of_blocks 4933 47 105 (by decide) (by decide) (by decide)

set_option maxRecDepth 100000 in
theorem prime_2467 : IsPrime 2467 := isPrime_of_blocks 2467 50 50 (by decide) (by decide) (by decide)

set_option maxRecDepth 100000 in
theorem b_0 : b 4934 0 = 7404 := by
  unfold b; rw [show 4934 + 1 = 47 * 105 from rfl, sumTo_mul]; decide

set_option maxRecDepth 100000 in
theorem b_134 : b 4934 134 = 14802 := by
  unfold b; rw [show 4934 + 1 = 47 * 105 from rfl, sumTo_mul]; decide

theorem dvd_P : 4934 ∣ P 4934 := by
  have h : b 4934 0 * b 4934 134 ∣ P 4934 :=
    dvd_prodTo_two (b 4934) (by decide) (by decide)
  rw [b_0, b_134] at h
  exact Nat.dvd_trans ⟨22212, by decide⟩ h

/-- Counterexample to the A134559 conjecture: `4933` and `(4933+1)/2 = 2467` are prime,
yet `gcd(P 4934, 4934) = 4934`, not `2`. -/
theorem a134559_counterexample :
    IsPrime 4933 ∧ IsPrime ((4933 + 1) / 2) ∧ Nat.gcd (P 4934) 4934 = 4934 :=
  ⟨prime_4933, prime_2467, Nat.gcd_eq_right dvd_P⟩

end Discovery.A134559Counter
