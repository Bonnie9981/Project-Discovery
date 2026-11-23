/-!
# DISC-0016: OEIS A085588, eventual period of Rule 150 on a ring of `n` cells

A085588(n) is the eventual period of a single ON cell under elementary CA Rule 150,
`new(i) = old(i-1) xor old(i) xor old(i+1)`, on a ring of `n` cells.
A state of the ring is the same thing as an `n`-periodic configuration `Int → Bool`, so we work
with those.

Write `n = 2^D * m` with `m` odd, and let `s` be any number with `m ∣ 2^s - 1` or `m ∣ 2^s + 1`
(the least such `s` is A309786(n)).  Over GF(2), `2^j` steps of Rule 150 are
`new(i) = old(i - 2^j) xor old(i) xor old(i + 2^j)` (`iter_pow_two`, the Frobenius identity
`(x⁻¹+1+x)^(2^j) = x^(-2^j)+1+x^(2^j)`).  Since `2^(D+s) ≡ ±2^D (mod n)`, on an `n`-periodic
configuration the step counts `2^(D+s)` and `2^D` give the same map (`iter_identity`):

  `F^(2^D + 2^D*(2^s-1)) = F^(2^D)`.

So every orbit (not only the single cell) becomes periodic after at most `2^D` steps, and its
eventual period divides `2^D * (2^s - 1)` (`period_dvd`, `a085588_dvd`).

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A085588Period

/-- One Rule 150 step on the bi-infinite line. -/
def step (f : Int → Bool) (i : Int) : Bool := xor (f (i - 1)) (xor (f i) (f (i + 1)))

/-- `k` steps. -/
def iter : Nat → (Int → Bool) → (Int → Bool)
  | 0, f => f
  | k + 1, f => step (iter k f)

/-- The "spread" operator `old(i-a) xor old(i) xor old(i+a)`. -/
def spread (a : Int) (f : Int → Bool) (i : Int) : Bool := xor (f (i - a)) (xor (f i) (f (i + a)))

/-- `f` is `n`-periodic, i.e. a state of the ring with `n` cells. -/
def Periodic (n : Int) (f : Int → Bool) : Prop := ∀ i, f (i + n) = f i

/-- The single ON cell on the ring of `n` cells. -/
def seed (n : Int) (i : Int) : Bool := decide (i % n = 0)

theorem iter_add (a b : Nat) (f : Int → Bool) : iter (a + b) f = iter a (iter b f) := by
  induction a with
  | zero => simp [iter]
  | succ a ih =>
    rw [show a + 1 + b = (a + b) + 1 by omega]
    simp only [iter, ih]

theorem xor_five (a b c d e : Bool) :
    xor (xor a (xor b c)) (xor (xor b (xor c d)) (xor c (xor d e))) = xor a (xor c e) := by
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> rfl

/-- GF(2) Frobenius: spreading twice by `a` is spreading once by `2a`. -/
theorem spread_spread (a : Int) (f : Int → Bool) : spread a (spread a f) = spread (2 * a) f := by
  funext i
  unfold spread
  have h1 : i - a - a = i - 2 * a := by omega
  have h2 : i - a + a = i := by omega
  have h3 : i + a - a = i := by omega
  have h4 : i + a + a = i + 2 * a := by omega
  rw [h1, h2, h3, h4]
  exact xor_five _ _ _ _ _

theorem step_eq_spread (f : Int → Bool) : step f = spread 1 f := rfl

/-- `2^j` Rule 150 steps are one spread by `2^j`. -/
theorem iter_pow_two (j : Nat) (f : Int → Bool) :
    iter (2 ^ j) f = spread ((2 ^ j : Nat) : Int) f := by
  induction j generalizing f with
  | zero => simp [iter, step_eq_spread]
  | succ j ih =>
    have e : iter (2 ^ (j + 1)) f = iter (2 ^ j) (iter (2 ^ j) f) := by
      rw [← iter_add, Nat.pow_succ, Nat.mul_two]
    rw [e, ih, ih, spread_spread]
    have h : (2 : Int) * ((2 ^ j : Nat) : Int) = ((2 ^ (j + 1) : Nat) : Int) := by
      rw [Nat.pow_succ]; push_cast; omega
    rw [h]

theorem periodic_nat {n : Int} {f : Int → Bool} (hf : Periodic n f) (k : Nat) (i : Int) :
    f (i + k * n) = f i := by
  induction k generalizing i with
  | zero => simp
  | succ k ih =>
    rw [show i + ((k + 1 : Nat) : Int) * n = (i + k * n) + n by push_cast; rw [Int.add_mul]; omega,
      hf, ih]

theorem periodic_int {n : Int} {f : Int → Bool} (hf : Periodic n f) (k : Int) (i : Int) :
    f (i + k * n) = f i := by
  cases k with
  | ofNat k => exact periodic_nat hf k i
  | negSucc k =>
    have h := periodic_nat hf (k + 1) (i + Int.negSucc k * n)
    rw [← h]
    congr 1
    rw [Int.negSucc_eq]
    rw [show ((k + 1 : Nat) : Int) = (k : Int) + 1 by push_cast; rfl]
    rw [Int.neg_mul]
    omega

/-- On an `n`-periodic configuration a spread only depends on `±a` modulo `n`. -/
theorem spread_congr {n a b : Int} {f : Int → Bool} (hf : Periodic n f)
    (h : (∃ k, a = b + k * n) ∨ (∃ k, a = -b + k * n)) : spread a f = spread b f := by
  funext i
  unfold spread
  rcases h with ⟨k, hk⟩ | ⟨k, hk⟩
  · have e1 : i - a = (i - b) + (-k) * n := by rw [hk, Int.neg_mul]; omega
    have e2 : i + a = (i + b) + k * n := by rw [hk]; omega
    rw [e1, e2, periodic_int hf, periodic_int hf]
  · have e1 : i - a = (i + b) + (-k) * n := by rw [hk, Int.neg_mul]; omega
    have e2 : i + a = (i - b) + k * n := by rw [hk]; omega
    rw [e1, e2, periodic_int hf, periodic_int hf]
    cases f (i - b) <;> cases f i <;> cases f (i + b) <;> rfl

/-- The key identity: `F^(2^D + 2^D(2^s-1)) = F^(2^D)` on the ring of `n = 2^D m` cells,
whenever `m ∣ 2^s - 1` or `m ∣ 2^s + 1`. -/
theorem iter_identity (D m s : Nat) (f : Int → Bool)
    (hf : Periodic ((2 ^ D * m : Nat) : Int) f)
    (hs : m ∣ 2 ^ s - 1 ∨ m ∣ 2 ^ s + 1) :
    iter (2 ^ D + 2 ^ D * (2 ^ s - 1)) f = iter (2 ^ D) f := by
  have hpos : 1 ≤ 2 ^ s := Nat.one_le_two_pow
  obtain ⟨Y, hY⟩ : ∃ Y, 2 ^ s = Y + 1 := ⟨2 ^ s - 1, by omega⟩
  have e : 2 ^ D + 2 ^ D * (2 ^ s - 1) = 2 ^ D * 2 ^ s := by
    rw [hY, Nat.add_sub_cancel, Nat.mul_succ]; omega
  rw [e, ← Nat.pow_add, iter_pow_two, iter_pow_two]
  apply spread_congr hf
  rw [Nat.pow_add]
  generalize 2 ^ D = X
  rcases hs with ⟨c, hc⟩ | ⟨c, hc⟩
  · left
    refine ⟨c, ?_⟩
    have h2 : 2 ^ s = m * c + 1 := by omega
    rw [h2]
    have : X * (m * c + 1) = X + c * (X * m) := by
      rw [Nat.mul_add, Nat.mul_one, Nat.add_comm, Nat.mul_comm c, Nat.mul_assoc]
    rw [this]; push_cast; rfl
  · right
    refine ⟨c, ?_⟩
    have : X * 2 ^ s + X = c * (X * m) := by
      rw [← Nat.mul_succ, Nat.succ_eq_add_one, hc, Nat.mul_comm c, Nat.mul_assoc]
    have h3 : ((X * 2 ^ s : Nat) : Int) + (X : Int) = (c : Int) * ((X * m : Nat) : Int) := by
      rw [← Int.ofNat_add, this]; push_cast; rfl
    omega

/-- `p` is the eventual period of the orbit of `f`: the least `p > 0` with
`F^(k+p) f = F^k f` for some `k`. -/
def EventualPeriod (f : Int → Bool) (p : Nat) : Prop :=
  0 < p ∧ (∃ k, iter (k + p) f = iter k f) ∧
    ∀ q, 0 < q → q < p → ¬ ∃ k, iter (k + q) f = iter k f

theorem shift_of_eq {f : Int → Bool} {k p : Nat} (h : iter (k + p) f = iter k f) (j : Nat) :
    iter (j + k + p) f = iter (j + k) f := by
  rw [Nat.add_assoc, iter_add, h, ← iter_add]

theorem mul_of_eq {f : Int → Bool} {K p : Nat} (h : iter (K + p) f = iter K f) (c : Nat) :
    iter (K + c * p) f = iter K f := by
  induction c with
  | zero => simp
  | succ c ih =>
    rw [show K + (c + 1) * p = (K + p) + c * p by rw [Nat.succ_mul]; omega,
      show K + p + c * p = c * p + (K + p) by omega, iter_add, h, ← iter_add,
      show c * p + K = K + c * p by omega, ih]

/-- The eventual period divides every `P` with `F^(k0+P) f = F^(k0) f`. -/
theorem period_dvd {f : Int → Bool} {p P k0 : Nat} (hp : EventualPeriod f p)
    (hP : iter (k0 + P) f = iter k0 f) : p ∣ P := by
  obtain ⟨hp0, ⟨k1, hk1⟩, hmin⟩ := hp
  let K := k0 + k1
  have hKp : iter (K + p) f = iter K f := by
    have := shift_of_eq hk1 k0
    simpa [K, Nat.add_assoc] using this
  have hKP : iter (K + P) f = iter K f := by
    have := shift_of_eq hP k1
    rw [show k1 + k0 + P = K + P by omega, show k1 + k0 = K by omega] at this
    exact this
  -- r = P % p satisfies F^(K+r) = F^K
  have hr : iter (K + P % p) f = iter K f := by
    have hdiv : P = P % p + p * (P / p) := (Nat.mod_add_div P p).symm
    have hm := mul_of_eq hKp (P / p)
    have : iter (K + P) f = iter (K + P % p) f := by
      conv => lhs; rw [hdiv]
      rw [show K + (P % p + p * (P / p)) = P % p + (K + P / p * p) by
            rw [Nat.mul_comm]; omega,
        iter_add, hm, ← iter_add, show P % p + K = K + P % p by omega]
    rw [← this, hKP]
  apply Nat.dvd_of_mod_eq_zero
  rcases Nat.eq_zero_or_pos (P % p) with h0 | h0
  · exact h0
  · exact absurd ⟨K, hr⟩ (hmin (P % p) h0 (Nat.mod_lt _ hp0))

theorem seed_periodic (n : Int) : Periodic n (seed n) := by
  intro i
  unfold seed
  rw [Int.add_emod_self]

/-- **A085588.**  On the ring of `n = 2^D * m` cells, with `m ∣ 2^s ∓ 1`, the eventual period
of one ON cell divides `2^D * (2^s - 1)`.  (With `m` odd and `s` = A309786(n) this is
`a(n) ∣ 2^A007814(n) * (2^A309786(n) - 1)`.) -/
theorem a085588_dvd (D m s p : Nat)
    (hs : m ∣ 2 ^ s - 1 ∨ m ∣ 2 ^ s + 1)
    (hp : EventualPeriod (seed ((2 ^ D * m : Nat) : Int)) p) :
    p ∣ 2 ^ D * (2 ^ s - 1) :=
  period_dvd hp (iter_identity D m s _ (seed_periodic _) hs)

/-- Same identity for every ring state: the eventual period of any orbit divides
`2^D * (2^s - 1)`, and the pre-period is at most `2^D`. -/
theorem any_state_dvd (D m s p : Nat) (f : Int → Bool)
    (hf : Periodic ((2 ^ D * m : Nat) : Int) f)
    (hs : m ∣ 2 ^ s - 1 ∨ m ∣ 2 ^ s + 1)
    (hp : EventualPeriod f p) :
    p ∣ 2 ^ D * (2 ^ s - 1) :=
  period_dvd hp (iter_identity D m s f hf hs)


end Discovery.A085588Period
