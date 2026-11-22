/-!
# DISC-0008 / R3-L01: ECA rule 26 on an odd ring, single live cell

State of a ring of `w` cells = a natural number `x < 2 ^ w` whose bit `i` is cell `i`
(same encoding as `research/r002/impl_b.py`; seed `1` = only cell 0 alive; the left
neighbour of cell `i` is cell `i - 1 mod w`, the right neighbour is cell `i + 1 mod w`).
Rule 26 = `00011010`: the new cell is 1 exactly on the neighbourhoods `100`, `011`, `001`
(left, centre, right). `step w` implements it with the same rotations and the same
"OR over the 1-patterns of an AND of (complemented) words" as `impl_b._step`.

Main results (every odd `w ≥ 3`, no finite range):

* `iter_testBit` (closed form): after `t` steps, cell `i` is alive iff
  `s = (i + t) mod w` is even and `C(t, s/2)` is odd. Here `pas t j` is Pascal's
  triangle mod 2 defined directly by Pascal's rule (it equals `C(t, j) mod 2`, but the
  link to `Nat.choose` is not stated in Lean and is not needed).
* `iter_eq_one_iff`: `x_t = x_0 ↔ w * 2 ^ log₂ w ∣ t`.
* `rule26_odd_period`: with `P = w * 2 ^ ⌊log₂ w⌋`, the orbit is purely periodic
  (transient 0) and its exact period is `P`.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.Rule26

/-! ## The rule and the bit-encoded ring -/

/-- Wolfram rule 26 on a neighbourhood `(l, c, r)`: bit `4l + 2c + r` of `26`. -/
def rule26 (l c r : Bool) : Bool :=
  (26 >>> ((if l then 4 else 0) + (if c then 2 else 0) + (if r then 1 else 0))) % 2 == 1

/-- Bit `i` = cell `i - 1` (left neighbour), cyclically. -/
def rotL (w x : Nat) : Nat := ((x <<< 1) ||| (x >>> (w - 1))) &&& (2 ^ w - 1)

/-- Bit `i` = cell `i + 1` (right neighbour), cyclically. -/
def rotR (w x : Nat) : Nat := ((x >>> 1) ||| ((x &&& 1) <<< (w - 1))) &&& (2 ^ w - 1)

/-- One step of rule 26 on the ring of `w` cells: OR over the patterns
`100`, `011`, `001` (bits 4, 3, 1 of 26) of the AND of the (complemented) words. -/
def step (w x : Nat) : Nat :=
  let m := 2 ^ w - 1
  let l := rotL w x
  let r := rotR w x
  (l &&& (x ^^^ m) &&& (r ^^^ m)) ||| ((l ^^^ m) &&& x &&& r) |||
    ((l ^^^ m) &&& (x ^^^ m) &&& r)

/-- `iter w k x` = state after `k` steps. -/
def iter (w : Nat) : Nat → Nat → Nat
  | 0, x => x
  | k + 1, x => iter w k (step w x)

theorem iter_succ' (w k x : Nat) : iter w (k + 1) x = step w (iter w k x) := by
  induction k generalizing x with
  | zero => rfl
  | succ k ih => exact ih (step w x)

theorem iter_add (w a b x : Nat) : iter w (a + b) x = iter w a (iter w b x) := by
  induction a with
  | zero => simp [iter]
  | succ a ih => rw [Nat.add_right_comm, iter_succ', ih, iter_succ']

/-! ## Bit-level description of `step` -/

theorem tb_high {w x i : Nat} (hx : x < 2 ^ w) (hi : w ≤ i) : x.testBit i = false :=
  Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le hx (Nat.pow_le_pow_right (by decide) hi))

theorem tb_mask (w i : Nat) : (2 ^ w - 1).testBit i = decide (i < w) :=
  Nat.testBit_two_pow_sub_one w i

theorem tb_one (i : Nat) : (1 : Nat).testBit i = decide (i = 0) := by
  by_cases h : i = 0
  · subst h; rfl
  · rw [decide_eq_false h]
    exact Bool.eq_false_iff.mpr fun h' => h (Nat.testBit_one_eq_true_iff_self_eq_zero.mp h')

theorem tb_rotL {w x i : Nat} (hw : 1 ≤ w) (hx : x < 2 ^ w) (hi : i < w) :
    (rotL w x).testBit i = x.testBit (if i = 0 then w - 1 else i - 1) := by
  unfold rotL
  rw [Nat.testBit_and, Nat.testBit_or, Nat.testBit_shiftLeft, Nat.testBit_shiftRight, tb_mask]
  rw [decide_eq_true hi, Bool.and_true]
  by_cases h0 : i = 0
  · subst h0; simp
  · rw [tb_high (i := w - 1 + i) hx (by omega), if_neg h0,
      decide_eq_true (show i ≥ 1 by omega), Bool.true_and, Bool.or_false]

theorem tb_rotR {w x i : Nat} (hw : 1 ≤ w) (hx : x < 2 ^ w) (hi : i < w) :
    (rotR w x).testBit i = x.testBit (if i = w - 1 then 0 else i + 1) := by
  unfold rotR
  rw [Nat.testBit_and, Nat.testBit_or, Nat.testBit_shiftLeft, Nat.testBit_shiftRight, tb_mask]
  rw [decide_eq_true hi, Bool.and_true]
  by_cases h0 : i = w - 1
  · have h1 : 1 + i = w := by omega
    rw [h1, tb_high hx (Nat.le_refl w), if_pos h0, decide_eq_true (show i ≥ w - 1 by omega),
      show i - (w - 1) = 0 by omega, Nat.testBit_and, tb_one]
    simp
  · rw [if_neg h0, decide_eq_false (show ¬ (i ≥ w - 1) by omega), Bool.false_and,
      Bool.or_false, Nat.add_comm]

theorem tb_rotL_high {w x i : Nat} (hi : w ≤ i) : (rotL w x).testBit i = false := by
  unfold rotL; rw [Nat.testBit_and, tb_mask]; simp; omega

theorem tb_rotR_high {w x i : Nat} (hi : w ≤ i) : (rotR w x).testBit i = false := by
  unfold rotR; rw [Nat.testBit_and, tb_mask]; simp; omega

theorem rule26_eq (l c r : Bool) :
    rule26 l c r = ((l && !c && !r) || (!l && c && r) || (!l && !c && r)) := by
  cases l <;> cases c <;> cases r <;> rfl

theorem tb_step {w x i : Nat} (hw : 1 ≤ w) (hx : x < 2 ^ w) (hi : i < w) :
    (step w x).testBit i =
      rule26 (x.testBit (if i = 0 then w - 1 else i - 1)) (x.testBit i)
        (x.testBit (if i = w - 1 then 0 else i + 1)) := by
  unfold step
  simp only [Nat.testBit_or, Nat.testBit_and, Nat.testBit_xor, tb_mask, hi, decide_true,
    tb_rotL hw hx hi, tb_rotR hw hx hi, rule26_eq]
  generalize x.testBit (if i = 0 then w - 1 else i - 1) = a
  generalize x.testBit (if i = w - 1 then 0 else i + 1) = b
  generalize x.testBit i = c
  cases a <;> cases b <;> cases c <;> rfl

theorem tb_step_high {w x i : Nat} (hx : x < 2 ^ w) (hi : w ≤ i) :
    (step w x).testBit i = false := by
  unfold step
  simp only [Nat.testBit_or, Nat.testBit_and, Nat.testBit_xor, tb_rotL_high hi,
    tb_rotR_high hi, tb_high hx hi]
  simp

theorem step_lt {w x : Nat} (hx : x < 2 ^ w) : step w x < 2 ^ w :=
  Nat.lt_pow_two_of_testBit _ fun _ hi => tb_step_high hx hi

/-! ## Pascal's triangle mod 2 -/

/-- `pas t j = C(t, j) mod 2`, by Pascal's rule (`true` = odd). -/
def pas : Nat → Nat → Bool
  | 0, 0 => true
  | 0, _ + 1 => false
  | _ + 1, 0 => true
  | t + 1, j + 1 => xor (pas t j) (pas t (j + 1))

theorem pas_zero_right (t : Nat) : pas t 0 = true := by cases t <;> rfl

theorem pas_succ_succ (t j : Nat) : pas (t + 1) (j + 1) = xor (pas t j) (pas t (j + 1)) := rfl

theorem pas_two_succ_succ (t k : Nat) : pas (t + 2) (k + 2) = xor (pas t k) (pas t (k + 2)) := by
  rw [pas_succ_succ, pas_succ_succ, pas_succ_succ]
  cases pas t k <;> cases pas t (k + 1) <;> cases pas t (k + 2) <;> rfl

theorem pas_two_one (t : Nat) : pas (t + 2) 1 = pas t 1 := by
  rw [pas_succ_succ, pas_succ_succ, pas_zero_right, pas_zero_right]
  cases pas t 1 <;> rfl

/-- Lucas' theorem for `p = 2`, one digit: `C(2a, 2b) ≡ C(a, b)`, `C(2a, 2b+1) ≡ 0`. -/
theorem pas_double (a : Nat) :
    ∀ b, pas (2 * a) (2 * b) = pas a b ∧ pas (2 * a) (2 * b + 1) = false := by
  induction a with
  | zero => intro b; cases b <;> exact ⟨rfl, rfl⟩
  | succ a ih =>
    intro b
    have e : 2 * (a + 1) = 2 * a + 2 := by omega
    rw [e]
    cases b with
    | zero => exact ⟨by simp [pas_zero_right], by rw [pas_two_one]; exact (ih 0).2⟩
    | succ b =>
      have e1 : 2 * (b + 1) = 2 * b + 2 := by omega
      have e2 : 2 * b + 2 + 1 = (2 * b + 1) + 2 := by omega
      rw [e1, pas_two_succ_succ, e2, pas_two_succ_succ, (ih b).1, (ih b).2]
      have e3 : 2 * b + 2 = 2 * (b + 1) := by omega
      have e4 : 2 * b + 1 + 2 = 2 * (b + 1) + 1 := by omega
      rw [e3, (ih (b + 1)).1, e4, (ih (b + 1)).2, pas_succ_succ]
      exact ⟨rfl, rfl⟩

theorem pas_one (t : Nat) : pas t 1 = (t % 2 == 1) := by
  induction t with
  | zero => rfl
  | succ t ih =>
    rw [pas_succ_succ, pas_zero_right, ih]
    rcases Nat.mod_two_eq_zero_or_one t with h | h
    · have : (t + 1) % 2 = 1 := by omega
      simp [h, this]
    · have : (t + 1) % 2 = 0 := by omega
      simp [h, this]

/-- If `2^m ∣ t` then `C(t, j)` is even for `0 < j < 2^m`. -/
theorem pas_eq_false_of_dvd (m : Nat) :
    ∀ t j, 2 ^ m ∣ t → 0 < j → j < 2 ^ m → pas t j = false := by
  induction m with
  | zero => intro t j _ h0 h1; simp at h1; omega
  | succ m ih =>
    intro t j hd h0 h1
    obtain ⟨q, rfl⟩ := hd
    have ht : 2 ^ (m + 1) * q = 2 * (2 ^ m * q) := by rw [Nat.pow_succ]; rw [Nat.mul_comm (2 ^ m) 2, Nat.mul_assoc]
    rw [ht]
    rcases Nat.mod_two_eq_zero_or_one j with hj | hj
    · have hb : j = 2 * (j / 2) := by omega
      rw [hb, (pas_double _ _).1]
      have : 2 ^ (m + 1) = 2 * 2 ^ m := by rw [Nat.pow_succ, Nat.mul_comm]
      exact ih _ _ ⟨q, rfl⟩ (by omega) (by omega)
    · have hb : j = 2 * (j / 2) + 1 := by omega
      rw [hb, (pas_double _ _).2]

/-- If `2^m ∤ t` then `C(t, 2^v)` is odd for some `v < m` (namely `v = v₂(t)`). -/
theorem exists_pas_of_not_dvd (m : Nat) :
    ∀ t, ¬ 2 ^ m ∣ t → ∃ v, v < m ∧ pas t (2 ^ v) = true := by
  induction m with
  | zero => intro t h; exact absurd (by simp : 2 ^ 0 ∣ t) h
  | succ m ih =>
    intro t h
    rcases Nat.mod_two_eq_zero_or_one t with ht | ht
    · have e : t = 2 * (t / 2) := by omega
      have h' : ¬ 2 ^ m ∣ t / 2 := by
        intro ⟨q, hq⟩
        apply h
        refine ⟨q, ?_⟩
        rw [e, hq, Nat.pow_succ, Nat.mul_comm (2 ^ m) 2, Nat.mul_assoc]
      obtain ⟨v, hv, hp⟩ := ih _ h'
      refine ⟨v + 1, by omega, ?_⟩
      rw [e, Nat.pow_succ, Nat.mul_comm (2 ^ v) 2, (pas_double _ _).1, hp]
    · exact ⟨0, by omega, by rw [Nat.pow_zero, pas_one]; simp [ht]⟩

/-! ## Closed form of the orbit -/

/-- Rule-90 (Pascal) row `t`, read in the window coordinate `s`. -/
def Y (t s : Nat) : Bool := s % 2 == 0 && pas t (s / 2)

/-- Conjectured closed form: cell `i` at time `t`. -/
def X (w t i : Nat) : Bool := Y t ((i + t) % w)

theorem Y_odd {t s : Nat} (h : s % 2 = 1) : Y t s = false := by
  unfold Y; simp [h]

theorem Y_even (t j : Nat) : Y t (2 * j) = pas t j := by
  unfold Y
  have h1 : 2 * j % 2 = 0 := by omega
  have h2 : 2 * j / 2 = j := by omega
  simp [h1, h2]

/-- Cyclic successor on `{0, …, w-1}`. -/
def sucw (w a : Nat) : Nat := if a + 1 = w then 0 else a + 1

theorem mod_succ_eq (w n : Nat) (hw : 0 < w) : (n + 1) % w = sucw w (n % w) := by
  have hlt := Nat.mod_lt n hw
  have e : n + 1 = (n % w + 1) + w * (n / w) := by have := Nat.mod_add_div n w; omega
  rw [e, Nat.add_mul_mod_self_left]
  unfold sucw
  by_cases h : n % w + 1 = w
  · rw [if_pos h, h, Nat.mod_self]
  · rw [if_neg h]; exact Nat.mod_eq_of_lt (by omega)

theorem Y_zero_right (t : Nat) : Y t 0 = true := by
  have := Y_even t 0; simp only [Nat.mul_zero] at this; rw [this, pas_zero_right]

/-- The local rule in window coordinates: one step of rule 26 maps Pascal row `t` to
row `t + 1` (this is where `w` odd and `w ≥ 3` are used). -/
theorem local_step {w t a : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (ha : a < w) :
    rule26 (Y t a) (Y t (sucw w a)) (Y t (sucw w (sucw w a))) =
      Y (t + 1) (sucw w (sucw w a)) := by
  by_cases h1 : a + 1 = w
  · -- a = w - 1 (even), b = 0, c = 1
    have h1' : ¬ (0 + 1 = w) := by omega
    simp only [sucw, if_pos h1, if_neg h1']
    rw [Y_zero_right, Y_odd (t := t) (s := 1) rfl, Y_odd (t := t + 1) (s := 1) rfl]
    cases Y t a <;> rfl
  · by_cases h2 : a + 1 + 1 = w
    · -- a = w - 2 (odd), b = w - 1, c = 0
      simp only [sucw, if_neg h1, if_pos h2]
      rw [Y_odd (show a % 2 = 1 by omega), Y_zero_right, Y_zero_right]
      cases Y t (a + 1) <;> rfl
    · simp only [sucw, if_neg h1, if_neg h2]
      rcases Nat.mod_two_eq_zero_or_one a with ha2 | ha2
      · obtain ⟨j, rfl⟩ : ∃ j, a = 2 * j := ⟨a / 2, by omega⟩
        have e : 2 * j + 1 + 1 = 2 * (j + 1) := by omega
        rw [Y_odd (show (2 * j + 1) % 2 = 1 by omega), e, Y_even, Y_even, Y_even,
          pas_succ_succ]
        cases pas t j <;> cases pas t (j + 1) <;> rfl
      · rw [Y_odd ha2, Y_odd (show (a + 1 + 1) % 2 = 1 by omega),
          Y_odd (show (a + 1 + 1) % 2 = 1 by omega)]
        cases Y t (a + 1) <;> rfl

/-- Left / right neighbour index on the ring. -/
def iL (w i : Nat) : Nat := if i = 0 then w - 1 else i - 1
def iR (w i : Nat) : Nat := if i = w - 1 then 0 else i + 1

theorem step_X {w t i : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (hi : i < w) :
    rule26 (X w t (iL w i)) (X w t i) (X w t (iR w i)) = X w (t + 1) i := by
  have hw0 : 0 < w := by omega
  have eC : sucw w ((iL w i + t) % w) = (i + t) % w := by
    rw [← mod_succ_eq _ _ hw0]
    unfold iL
    by_cases h : i = 0
    · subst h; rw [if_pos rfl, show w - 1 + t + 1 = t + w by omega, Nat.add_mod_right,
        Nat.zero_add]
    · rw [if_neg h, show i - 1 + t + 1 = i + t by omega]
  have eR : sucw w ((i + t) % w) = (iR w i + t) % w := by
    rw [← mod_succ_eq _ _ hw0]
    unfold iR
    by_cases h : i = w - 1
    · rw [if_pos h, show i + t + 1 = t + w by omega, Nat.add_mod_right, Nat.zero_add]
    · rw [if_neg h, show i + 1 + t = i + t + 1 by omega]
  have eN : (i + (t + 1)) % w = (iR w i + t) % w := by
    rw [← eR, ← mod_succ_eq _ _ hw0, Nat.add_assoc]
  unfold X
  rw [eN, ← eR, ← eC]
  exact local_step hw h3 (Nat.mod_lt _ hw0)

theorem iL_lt {w i : Nat} (hw : 1 ≤ w) (hi : i < w) : iL w i < w := by
  unfold iL; split <;> omega

theorem iR_lt {w i : Nat} (hw : 1 ≤ w) (hi : i < w) : iR w i < w := by
  unfold iR; split <;> omega

theorem pas_zero_left (j : Nat) : pas 0 j = (j == 0) := by cases j <;> rfl

theorem X_zero {w i : Nat} (hi : i < w) : X w 0 i = decide (i = 0) := by
  unfold X Y
  rw [Nat.add_zero, Nat.mod_eq_of_lt hi, pas_zero_left]
  by_cases h : i = 0
  · subst h; rfl
  · rw [decide_eq_false h]
    rcases Nat.mod_two_eq_zero_or_one i with h2 | h2
    · have : i / 2 ≠ 0 := by omega
      simp [h2, this]
    · simp [h2]

/-- Closed form of the single-seed orbit of rule 26 on an odd ring (Lemma 1). -/
theorem iter_testBit {w : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (t : Nat) :
    iter w t 1 < 2 ^ w ∧ ∀ i, i < w → (iter w t 1).testBit i = X w t i := by
  have hw1 : 1 ≤ w := by omega
  induction t with
  | zero =>
    refine ⟨Nat.one_lt_two_pow (by omega), fun i hi => ?_⟩
    show (1 : Nat).testBit i = _
    rw [tb_one, X_zero hi]
  | succ t ih =>
    obtain ⟨hlt, hb⟩ := ih
    rw [iter_succ']
    refine ⟨step_lt hlt, fun i hi => ?_⟩
    rw [tb_step hw1 hlt hi]
    have a := hb _ (iL_lt hw1 hi)
    have b := hb _ (iR_lt hw1 hi)
    unfold iL at a; unfold iR at b
    rw [a, b, hb i hi]
    exact step_X hw h3 hi

theorem iter_eq_one_iff_X {w : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (t : Nat) :
    iter w t 1 = 1 ↔ ∀ i, i < w → X w t i = decide (i = 0) := by
  obtain ⟨hlt, hb⟩ := iter_testBit hw h3 t
  constructor
  · intro h i hi; rw [← hb i hi, h, tb_one]
  · intro h
    apply Nat.eq_of_testBit_eq
    intro i
    by_cases hi : i < w
    · rw [hb i hi, h i hi, tb_one]
    · rw [tb_high (i := i) hlt (by omega), tb_high (w := w) (i := i) (Nat.one_lt_two_pow (by omega)) (by omega)]

/-! ## Exact period -/

/-- `2^k ≤ w < 2^(k+1)` with `k = ⌊log₂ w⌋`; for odd `w ≥ 3`, `2^k < w` and `k ≥ 1`. -/
theorem log2_facts {w : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) :
    ∃ M, 2 ^ Nat.log2 w = 2 * M ∧ 2 * M < w ∧ w < 4 * M := by
  have hle := Nat.log2_self_le (show w ≠ 0 by omega)
  have hlt := @Nat.lt_log2_self w
  cases hk : Nat.log2 w with
  | zero => rw [hk] at hlt; simp at hlt; omega
  | succ k =>
    rw [hk] at hle hlt
    refine ⟨2 ^ k, by rw [Nat.pow_succ, Nat.mul_comm], ?_, ?_⟩
    · rw [Nat.pow_succ] at hle; omega
    · rw [Nat.pow_succ, Nat.pow_succ] at hlt; omega

theorem mod_eq_self_of_dvd {w t i : Nat} (hd : w ∣ t) (hi : i < w) : (i + t) % w = i := by
  obtain ⟨q, rfl⟩ := hd
  rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hi]

/-- `x_t = x_0` iff `w ∣ t` and `2^⌊log₂ w⌋ ∣ t`. -/
theorem iter_eq_one_iff' {w : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (t : Nat) :
    iter w t 1 = 1 ↔ w ∣ t ∧ 2 ^ Nat.log2 w ∣ t := by
  obtain ⟨M, hM, hMw, hwM⟩ := log2_facts hw h3
  rw [iter_eq_one_iff_X hw h3]
  constructor
  · intro H
    have hmod : t % w = 0 := by
      apply Classical.byContradiction
      intro hr
      have hrw := Nat.mod_lt t (show 0 < w by omega)
      have hdm := Nat.mod_add_div t w
      have e : (w - t % w + t) % w = 0 := by
        rw [show w - t % w + t = w * (t / w + 1) by rw [Nat.mul_add]; omega, Nat.mul_mod_right]
      have := H (w - t % w) (by omega)
      unfold X at this
      rw [e, Y_zero_right] at this
      simp at this; omega
    have hd : w ∣ t := Nat.dvd_of_mod_eq_zero hmod
    refine ⟨hd, Classical.byContradiction fun hn => ?_⟩
    obtain ⟨v, hv, hp⟩ := exists_pas_of_not_dvd _ t hn
    have hpow : 2 ^ (v + 1) ≤ 2 ^ Nat.log2 w := Nat.pow_le_pow_right (by decide) hv
    rw [Nat.pow_succ, hM] at hpow
    have hpos : 0 < 2 ^ v := Nat.two_pow_pos v
    have := H (2 * 2 ^ v) (by omega)
    unfold X at this
    rw [mod_eq_self_of_dvd hd (by omega), Y_even, hp] at this
    simp at this; omega
  · intro ⟨hd, hk⟩ i hi
    unfold X
    rw [mod_eq_self_of_dvd hd hi]
    by_cases h0 : i = 0
    · subst h0; rw [Y_zero_right]; rfl
    · rw [decide_eq_false h0]
      rcases Nat.mod_two_eq_zero_or_one i with h2 | h2
      · obtain ⟨j, rfl⟩ : ∃ j, i = 2 * j := ⟨i / 2, by omega⟩
        rw [Y_even]
        exact pas_eq_false_of_dvd _ t j hk (by omega) (by rw [hM]; omega)
      · exact Y_odd h2

theorem odd_mul_two_pow_dvd {w : Nat} (hw : w % 2 = 1) (m : Nat) :
    ∀ t, w ∣ t → 2 ^ m ∣ t → w * 2 ^ m ∣ t := by
  induction m with
  | zero => intro t h _; simp at h ⊢; exact h
  | succ m ih =>
    intro t hwt h2
    have h2t : 2 ∣ t := Nat.dvd_trans ⟨2 ^ m, by rw [Nat.pow_succ, Nat.mul_comm]⟩ h2
    obtain ⟨u, rfl⟩ := h2t
    obtain ⟨c, hc⟩ := hwt
    have hc2 : c % 2 = 0 := by
      have e1 : (w * c) % 2 = c % 2 := by rw [Nat.mul_mod, hw, Nat.one_mul, Nat.mod_mod]
      have e2 : (2 * u) % 2 = 0 := by omega
      rw [hc] at e2; omega
    obtain ⟨d, rfl⟩ : ∃ d, c = 2 * d := ⟨c / 2, by omega⟩
    have hu : u = w * d := by
      apply Nat.eq_of_mul_eq_mul_left (show 0 < 2 by decide)
      rw [hc, Nat.mul_left_comm]
    have h2u : 2 ^ m ∣ u := by
      rw [Nat.pow_succ, Nat.mul_comm] at h2
      exact Nat.dvd_of_mul_dvd_mul_left (by decide) h2
    have := ih u ⟨d, hu⟩ h2u
    rw [Nat.pow_succ, Nat.mul_comm (2 ^ m) 2, ← Nat.mul_assoc, Nat.mul_comm w 2, Nat.mul_assoc]
    exact Nat.mul_dvd_mul_left 2 this

/-- Conjectured period `P26(w) = w · 2^⌊log₂ w⌋` (R3-L01). -/
def P (w : Nat) : Nat := w * 2 ^ Nat.log2 w

/-- `x_t = x_0` exactly when `P26(w) ∣ t`. -/
theorem iter_eq_one_iff {w : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (t : Nat) :
    iter w t 1 = 1 ↔ P w ∣ t := by
  rw [iter_eq_one_iff' hw h3]
  constructor
  · intro ⟨a, b⟩; exact odd_mul_two_pow_dvd hw _ t a b
  · intro h
    exact ⟨Nat.dvd_trans (Nat.dvd_mul_right _ _) h, Nat.dvd_trans (Nat.dvd_mul_left _ _) h⟩

/-- **R3-L01.** For odd `w ≥ 3`, the single-seed orbit of rule 26 on the ring of `w` cells
has transient 0 (every state recurs: `x_{μ+P} = x_μ` for all `μ ≥ 0`) and exact period
`P26(w) = w · 2^⌊log₂ w⌋` (`x_p ≠ x_0` for `0 < p < P`). -/
theorem rule26_odd_period (w : Nat) (hw : w % 2 = 1) (h3 : 3 ≤ w) :
    iter w (P w) 1 = 1 ∧
    (∀ μ, iter w (μ + P w) 1 = iter w μ 1) ∧
    (∀ p, 0 < p → p < P w → iter w p 1 ≠ iter w 0 1) := by
  have hP : iter w (P w) 1 = 1 := (iter_eq_one_iff hw h3 _).2 (Nat.dvd_refl _)
  refine ⟨hP, fun μ => by rw [iter_add, hP], fun p hp0 hpP h => ?_⟩
  have := Nat.le_of_dvd hp0 ((iter_eq_one_iff hw h3 p).1 h)
  omega

set_option maxRecDepth 100000 in
/-- Kernel-evaluated spot checks matching the simulations (`w = 3, 11, 21`; `x_1`, `x_8` for `w = 11` as in the space-time diagram). -/
theorem check_small : iter 11 1 1 = 2 + 2 ^ 10 ∧ iter 11 8 1 = 2 ^ 3 ∧ iter 3 6 1 = 1 ∧
    iter 11 88 1 = 1 ∧ iter 11 44 1 ≠ 1 ∧ iter 21 336 1 = 1 := by decide

end Discovery.Rule26
