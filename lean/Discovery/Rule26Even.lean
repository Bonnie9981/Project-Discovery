import Discovery.Rule26

/-!
# DISC-0009 / R3-L02: rule 26 on an even ring = null-boundary rule 90 (A334504 ↔ A268754)

Ring encoding and `step`/`iter` are those of `Discovery.Rule26` (bit `i` = cell `i`,
left neighbour `i - 1 mod w`, right neighbour `i + 1 mod w`, seed `1`).

Null-boundary rule 90 on `n` cells: `nstep n y = ((y <<< 1) ^^^ (y >>> 1)) &&& (2^n - 1)`,
seed `1` (one live cell at the left end). This is literally the update in the Python
program of OEIS A268754 (`hare = ((hare << 1) ^ (hare >> 1)) & wire_mask`, start `1`).

Main results (every `m ≥ 2`, i.e. ring width `w = 2m ≥ 4`, wire width `n = m - 1 ≥ 1`):

* `iter_succ_testBit`: for every `t`, after `t + 1` steps of rule 26 on the ring of `2m`
  cells, cells `0` and `m` are dead, cells `1 … m-1` are the wire after `t` steps of
  null-boundary rule 90, and cells `m+1 … 2m-1` are its mirror image.
* `iter_succ_eq_iff`: `x_{s+1} = x_{t+1} ↔ y_s = y_t`, and `iter_succ_ne_one`: `x_{t+1} ≠ x_0`.
* `rule26_even_eventual_period`: for every `p`, the rule-26 ring orbit is eventually
  `p`-periodic iff the rule-90 wire orbit is. Hence the two eventual (least) periods are
  equal: `A334504(2n+2) = A268754(n)` for all `n ≥ 1`.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.Rule26Even

open Discovery.Rule26

/-! ## Null-boundary rule 90 -/

/-- One step of rule 90 on a wire of `n` cells with dead cells beyond both ends. -/
def nstep (n y : Nat) : Nat := ((y <<< 1) ^^^ (y >>> 1)) &&& (2 ^ n - 1)

/-- `niter n k y` = wire after `k` steps. -/
def niter (n : Nat) : Nat → Nat → Nat
  | 0, y => y
  | k + 1, y => nstep n (niter n k y)

theorem tb_nstep (n y j : Nat) :
    (nstep n y).testBit j =
      (decide (j < n) && xor (decide (1 ≤ j) && y.testBit (j - 1)) (y.testBit (j + 1))) := by
  unfold nstep
  rw [Nat.testBit_and, Nat.testBit_xor, Nat.testBit_shiftLeft, Nat.testBit_shiftRight, tb_mask,
    Nat.add_comm 1 j, Bool.and_comm]

theorem nstep_lt (n y : Nat) : nstep n y < 2 ^ n :=
  Nat.lt_pow_two_of_testBit _ fun j hj => by rw [tb_nstep]; simp; omega

theorem niter_lt {n : Nat} (hn : 1 ≤ n) (t : Nat) : niter n t 1 < 2 ^ n := by
  cases t with
  | zero => exact Nat.one_lt_two_pow (by omega)
  | succ t => exact nstep_lt _ _

/-- Parity: after `t` steps the live wire cells all have index `≡ t (mod 2)`. -/
theorem niter_par (n t j : Nat) : (niter n t 1).testBit j = true → j % 2 = t % 2 := by
  induction t generalizing j with
  | zero => intro h; rw [show niter n 0 1 = 1 from rfl, tb_one] at h; simp at h; omega
  | succ t ih =>
    intro h
    rw [show niter n (t + 1) 1 = nstep n (niter n t 1) from rfl, tb_nstep] at h
    by_cases h1 : (niter n t 1).testBit (j + 1) = true
    · have := ih _ h1; omega
    · have h2 : (niter n t 1).testBit (j - 1) = true ∧ 1 ≤ j := by
        revert h h1
        cases (niter n t 1).testBit (j + 1) <;> cases (niter n t 1).testBit (j - 1) <;>
          simp
      have := ih _ h2.1; omega

/-! ## The mirrored embedding of a wire into the ring -/

/-- Ring of `2m` cells built from a wire `y` of `m - 1` cells: cells `0` and `m` dead,
cell `i` (`0 < i < m`) = wire cell `i - 1`, cell `i` (`m < i`) = wire cell `2m - 1 - i`. -/
def Z (m y i : Nat) : Bool :=
  if i = 0 then false else if i < m then y.testBit (i - 1) else if i = m then false
  else y.testBit (2 * m - 1 - i)

theorem Z_zero (m y : Nat) : Z m y 0 = false := rfl

theorem Z_left {m y i : Nat} (h0 : 0 < i) (h : i < m) : Z m y i = y.testBit (i - 1) := by
  unfold Z; rw [if_neg (by omega), if_pos h]

theorem Z_mid {m y : Nat} (h : 0 < m) : Z m y m = false := by
  unfold Z; rw [if_neg (by omega), if_neg (by omega), if_pos rfl]

theorem Z_right {m y i : Nat} (h : m < i) : Z m y i = y.testBit (2 * m - 1 - i) := by
  unfold Z; rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]

/-- On a neighbourhood with no `11` around a live centre, rule 26 is rule 90. -/
theorem rule26_xor {l c r : Bool} (h : c = true → l = false) : rule26 l c r = xor l r := by
  cases l <;> cases c <;> cases r <;> simp_all [rule26_eq]

/-- One rule-26 step on the mirrored ring = one null-boundary rule-90 step on the wire,
provided the wire is supported on one parity class. -/
theorem step_Z {m y x p : Nat} (hm : 2 ≤ m) (hy : y < 2 ^ (m - 1))
    (hpar : ∀ j, y.testBit j = true → j % 2 = p) (hx : x < 2 ^ (2 * m))
    (hb : ∀ i, i < 2 * m → x.testBit i = Z m y i) :
    ∀ i, i < 2 * m → (step (2 * m) x).testBit i = Z m (nstep (m - 1) y) i := by
  intro i hi
  have hw1 : 1 ≤ 2 * m := by omega
  have hyh : ∀ j, m - 1 ≤ j → y.testBit j = false := fun j hj => tb_high hy hj
  have hadj : ∀ j, y.testBit j = true → y.testBit (j + 1) = true → False := fun j a b => by
    have := hpar _ a; have := hpar _ b; omega
  rw [tb_step hw1 hx hi]
  have a := hb _ (iL_lt hw1 hi)
  have b := hb _ (iR_lt hw1 hi)
  unfold iL at a; unfold iR at b
  rw [a, b, hb i hi]
  by_cases h0 : i = 0
  · subst h0
    rw [if_pos rfl, if_neg (by omega), Z_zero, Z_zero, Z_right (by omega), Z_left (by omega) hm,
      rule26_xor (by simp)]
    simp
  by_cases hl : i < m
  · rw [if_neg h0, if_neg (by omega), Z_left (by omega) hl, Z_left (by omega) hl, tb_nstep,
      decide_eq_true (show i - 1 < m - 1 by omega), Bool.true_and,
      show i - 1 + 1 = i by omega]
    have hR : Z m y (i + 1) = y.testBit i := by
      by_cases he : i + 1 = m
      · rw [he, Z_mid (by omega), hyh _ (by omega)]
      · rw [Z_left (by omega) (by omega), Nat.add_sub_cancel]
    have hL : Z m y (i - 1) = (decide (1 ≤ i - 1) && y.testBit (i - 1 - 1)) := by
      by_cases he : i = 1
      · subst he; rfl
      · rw [Z_left (by omega) (by omega), decide_eq_true (show 1 ≤ i - 1 by omega),
          Bool.true_and]
    rw [hR, hL]
    apply rule26_xor
    intro hc
    cases hz : y.testBit (i - 1 - 1)
    · simp
    · by_cases h2 : 2 ≤ i
      · exact (hadj (i - 1 - 1) hz (by rw [show i - 1 - 1 + 1 = i - 1 by omega]; exact hc)).elim
      · rw [decide_eq_false (by omega)]; rfl
  by_cases hmid : i = m
  · subst hmid
    rw [if_neg h0, if_neg (by omega), Z_mid (by omega), Z_mid (by omega), Z_left (by omega) (by omega),
      Z_right (by omega), show 2 * i - 1 - (i + 1) = i - 1 - 1 by omega,
      rule26_xor (by simp)]
    simp
  · have hr : m < i := by omega
    rw [if_neg h0, Z_right (y := y) hr, Z_right (y := nstep (m - 1) y) hr, tb_nstep,
      decide_eq_true (show 2 * m - 1 - i < m - 1 by omega), Bool.true_and,
      show 2 * m - 1 - i + 1 = 2 * m - 1 - (i - 1) by omega]
    have hL : Z m y (i - 1) = y.testBit (2 * m - 1 - (i - 1)) := by
      by_cases he : i - 1 = m
      · rw [he, Z_mid (by omega), hyh _ (by omega)]
      · rw [Z_right (by omega)]
    have hR : Z m y (if i = 2 * m - 1 then 0 else i + 1) =
        (decide (1 ≤ 2 * m - 1 - i) && y.testBit (2 * m - 1 - i - 1)) := by
      by_cases he : i = 2 * m - 1
      · rw [if_pos he, Z_zero, decide_eq_false (by omega)]; rfl
      · rw [if_neg he, Z_right (by omega), decide_eq_true (by omega), Bool.true_and,
          show 2 * m - 1 - (i + 1) = 2 * m - 1 - i - 1 by omega]
    rw [hL, hR, Bool.xor_comm]
    apply rule26_xor
    intro hc
    cases hz : y.testBit (2 * m - 1 - (i - 1))
    · rfl
    · exact (hadj (2 * m - 1 - i) hc
        (by rw [show 2 * m - 1 - i + 1 = 2 * m - 1 - (i - 1) by omega]; exact hz)).elim

/-- **Structure lemma.** For `m ≥ 2` and every `t`, the ring state after `t + 1` steps of
rule 26 is the mirrored embedding of the wire after `t` steps of null-boundary rule 90. -/
theorem iter_succ_testBit {m : Nat} (hm : 2 ≤ m) (t : Nat) :
    iter (2 * m) (t + 1) 1 < 2 ^ (2 * m) ∧
      ∀ i, i < 2 * m → (iter (2 * m) (t + 1) 1).testBit i = Z m (niter (m - 1) t 1) i := by
  have hw1 : 1 ≤ 2 * m := by omega
  have h1 : (1 : Nat) < 2 ^ (2 * m) := Nat.one_lt_two_pow (by omega)
  induction t with
  | zero =>
    refine ⟨step_lt h1, fun i hi => ?_⟩
    show (step (2 * m) 1).testBit i = Z m 1 i
    rw [tb_step hw1 h1 hi, tb_one, tb_one, tb_one]
    by_cases h0 : i = 0
    · subst h0
      rw [if_pos rfl, if_neg (show ¬ 0 = 2 * m - 1 by omega),
        decide_eq_false (show ¬ 2 * m - 1 = 0 by omega), decide_eq_true rfl,
        decide_eq_false (show ¬ 0 + 1 = 0 by omega), Z_zero]; rfl
    by_cases hl : i < m
    · rw [if_neg h0, if_neg (show ¬ i = 2 * m - 1 by omega), decide_eq_false h0,
        decide_eq_false (show ¬ i + 1 = 0 by omega), Z_left (by omega) hl, tb_one]
      cases decide (i - 1 = 0) <;> rfl
    by_cases hmid : i = m
    · rw [if_neg h0, if_neg (show ¬ i = 2 * m - 1 by omega),
        decide_eq_false (show ¬ i - 1 = 0 by omega), decide_eq_false h0,
        decide_eq_false (show ¬ i + 1 = 0 by omega), hmid, Z_mid (by omega)]; rfl
    · have hr : m < i := by omega
      rw [if_neg h0, decide_eq_false (show ¬ i - 1 = 0 by omega), decide_eq_false h0,
        Z_right (y := 1) hr, tb_one]
      by_cases he : i = 2 * m - 1
      · rw [if_pos he, decide_eq_true rfl, decide_eq_true (show 2 * m - 1 - i = 0 by omega)]; rfl
      · rw [if_neg he, decide_eq_false (show ¬ i + 1 = 0 by omega),
          decide_eq_false (show ¬ 2 * m - 1 - i = 0 by omega)]; rfl
  | succ t ih =>
    obtain ⟨hlt, hb⟩ := ih
    rw [iter_succ']
    exact ⟨step_lt hlt, step_Z hm (niter_lt (by omega) t) (niter_par (m - 1) t) hlt hb⟩

/-- After the first step, the seed never comes back (cell 0 stays dead). -/
theorem iter_succ_ne_one {m : Nat} (hm : 2 ≤ m) (t : Nat) : iter (2 * m) (t + 1) 1 ≠ 1 := by
  intro h
  have := (iter_succ_testBit hm t).2 0 (by omega)
  rw [h, Z_zero] at this
  exact absurd this (by decide)

/-- Equality of ring states after the first step is equality of wire states. -/
theorem iter_succ_eq_iff {m : Nat} (hm : 2 ≤ m) (s t : Nat) :
    iter (2 * m) (s + 1) 1 = iter (2 * m) (t + 1) 1 ↔ niter (m - 1) s 1 = niter (m - 1) t 1 := by
  obtain ⟨hs, bs⟩ := iter_succ_testBit hm s
  obtain ⟨ht, bt⟩ := iter_succ_testBit hm t
  constructor
  · intro h
    apply Nat.eq_of_testBit_eq
    intro j
    by_cases hj : j < m - 1
    · have e1 := bs (j + 1) (by omega)
      have e2 := bt (j + 1) (by omega)
      rw [Z_left (by omega) (by omega), Nat.add_sub_cancel] at e1 e2
      rw [← e1, ← e2, h]
    · rw [tb_high (niter_lt (by omega) s) (by omega), tb_high (niter_lt (by omega) t) (by omega)]
  · intro h
    apply Nat.eq_of_testBit_eq
    intro i
    by_cases hi : i < 2 * m
    · rw [bs i hi, bt i hi, h]
    · rw [tb_high hs (by omega), tb_high ht (by omega)]

/-- A sequence is eventually `p`-periodic. -/
def EvPer (f : Nat → Nat) (p : Nat) : Prop := ∃ T, ∀ t, T ≤ t → f (t + p) = f t

/-- **R3-L02 (A334504(2n+2) = A268754(n)).** For `m ≥ 2` and every `p`, the single-seed
rule-26 orbit on the ring of `2m` cells is eventually `p`-periodic iff the left-end-seed
null-boundary rule-90 orbit on the wire of `m - 1` cells is. So the least `p ≥ 1` is the
same for both: the eventual periods agree. (By `iter_succ_eq_iff` and `iter_succ_ne_one`
the ring's transient is also exactly one more than the wire's.) -/
theorem rule26_even_eventual_period {m : Nat} (hm : 2 ≤ m) (p : Nat) :
    EvPer (fun t => iter (2 * m) t 1) p ↔ EvPer (fun t => niter (m - 1) t 1) p := by
  constructor
  · intro ⟨T, hT⟩
    refine ⟨T, fun t ht => ?_⟩
    have := hT (t + 1) (by omega)
    simp only [show t + 1 + p = t + p + 1 by omega] at this
    exact (iter_succ_eq_iff hm _ _).1 this
  · intro ⟨T, hT⟩
    refine ⟨T + 1, fun t ht => ?_⟩
    obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
    simp only [show s + 1 + p = s + p + 1 by omega]
    exact (iter_succ_eq_iff hm _ _).2 (hT s (by omega))

set_option maxRecDepth 100000 in
/-- Kernel-evaluated spot checks: `w = 10` (`n = 4`): transient 1, period 6 = A268754(4);
`w = 8` (`n = 3`): the wire dies, period 1 = A268754(3). -/
theorem check_small : niter 4 6 1 = 1 ∧ niter 4 3 1 ≠ 1 ∧ iter 10 7 1 = iter 10 1 1 ∧
    iter 10 4 1 ≠ iter 10 1 1 ∧ niter 3 3 1 = 0 ∧ iter 8 5 1 = iter 8 4 1 := by decide

end Discovery.Rule26Even
