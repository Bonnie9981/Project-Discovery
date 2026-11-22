import Discovery.Rule54Mod23

/-!
# DISC-0012: rule 54 on a ring of width `w ≡ 1 (mod 4)`, single live cell

Same encoding as `Discovery.Rule54` (bit `i` = cell `i`, seed `1`, rule 54 =
`c xor (l or r)`), and the same folding as `Discovery.Rule54Mod23`: the orbit is
mirror-symmetric, so we work on the segment `0, 1, …, m` (`m = w / 2`, even here).

Picture (folded segment, time going down):

* up to time `m - 2` the light cone grows (`iter_cone`) and at `m - 2` it is exactly the
  ether `E` everywhere;
* from then on a *phase wall* starts at the centre and walks back to the seed at speed 1:
  cells with `d + t < w` still carry `E`, cells with `d + t ≥ w` carry the shifted ether
  `N t d = E (t + 1) (d + 3)`;
* behind the wall the two ends of the segment are not mirror points of `N`, so each end
  carries a one-cell defect once every 4 steps (`d = 0` when `t ≡ 2`, `d = m` when
  `t ≡ m (mod 4)`).

`G w t d` is this description. `G_step` checks one step of the folded rule on it
(finitely many residue cases, closed by `decide`-style evaluation), `iter_G` is the
induction from time `m - 2`, and `rule54_mod4_one` reads off transient `w - 3` and exact
period 4.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.Rule54Mod1

open Discovery.Rule54 (step iter T iter_succ' periodic_from rule54_transient_period)
open Discovery.Rule54Mod4 (iter_lt ee E eq_of_bits)
open Discovery.Rule54Mod23 (dist lo up dist_le dist_self fold_step Cf iter_cone E_dead_even)

/-! ## The description -/

/-- The shifted ether behind the wall, in residues. -/
def eN (a b : Nat) : Bool := ee ((a + 1) % 4) ((b + 3) % 4)

/-- A cell value: `r` = behind the wall, `f` = defect flag. -/
def val (r : Bool) (a b : Nat) (f : Bool) : Bool := if r then xor (eN a b) f else ee a b

/-- Defect flag: seed end at `t ≡ 2`, centre at `t ≡ m (mod 4)`. -/
def fl (w t d : Nat) : Bool :=
  (decide (d = 0) && decide (t % 4 = 2)) || (decide (d = w / 2) && decide (t % 4 = w / 2 % 4))

/-- The folded state at time `t` (valid from `t = w / 2 - 2` on). -/
def G (w t d : Nat) : Bool := val (decide (w ≤ d + t)) (t % 4) (d % 4) (fl w t d)

/-! ## One step -/

set_option hygiene false in
/-- Close a residue goal: split `t % 4`, `d % 4` and evaluate. -/
macro "fin4" : tactic => `(tactic| (
  rcases (show t % 4 = 0 ∨ t % 4 = 1 ∨ t % 4 = 2 ∨ t % 4 = 3 by omega) with h1 | h1 | h1 | h1 <;>
  rcases (show d % 4 = 0 ∨ d % 4 = 1 ∨ d % 4 = 2 ∨ d % 4 = 3 by omega) with h2 | h2 | h2 | h2 <;>
  first | (exfalso; omega) | (simp only [h1, h2, Bool.false_and, Bool.or_false, Bool.false_or]; decide)))

set_option hygiene false in
/-- Same with `d` already a numeral. -/
macro "fint" : tactic => `(tactic| (
  rcases (show t % 4 = 0 ∨ t % 4 = 1 ∨ t % 4 = 2 ∨ t % 4 = 3 by omega) with h1 | h1 | h1 | h1 <;>
  first | (exfalso; omega) | (simp only [h1, Bool.false_and, Bool.or_false, Bool.false_or]; decide)))

/-- Step case: seed end: both neighbours are cell 1. -/
theorem G_step_zero {w t d : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (_ht : w / 2 ≤ t + 2)
    (hd : d ≤ w / 2) (h : d = 0) :
    G w (t + 1) d = xor (G w t d) (G w t (lo d) || G w t (up w d)) := by
  have rt : (t + 1) % 4 = (t % 4 + 1) % 4 := by omega
  have hm4 : w / 2 % 4 = 0 ∨ w / 2 % 4 = 2 := by omega
  unfold G fl
  rw [rt]
  subst h
  have e1 : lo 0 = 1 := rfl
  have e2 : up w 0 = 1 := by unfold up; rw [if_neg (by omega)]
  rw [e1, e2, decide_eq_true (rfl : (0 : Nat) = 0), decide_eq_false (show ¬ 0 = w / 2 by omega),
    decide_eq_false (show ¬ 1 = 0 by omega), decide_eq_false (show ¬ 1 = w / 2 by omega)]
  rcases (show t + 1 < w ∨ t + 1 = w ∨ w ≤ t by omega) with r | r | r
  · rw [decide_eq_false (show ¬ w ≤ 0 + (t + 1) by omega),
      decide_eq_false (show ¬ w ≤ 0 + t by omega), decide_eq_false (show ¬ w ≤ 1 + t by omega)]
    fint
  · have : t % 4 = 0 := by omega
    rw [decide_eq_true (show w ≤ 0 + (t + 1) by omega),
      decide_eq_false (show ¬ w ≤ 0 + t by omega), decide_eq_true (show w ≤ 1 + t by omega)]
    fint
  · rw [decide_eq_true (show w ≤ 0 + (t + 1) by omega),
      decide_eq_true (show w ≤ 0 + t by omega), decide_eq_true (show w ≤ 1 + t by omega)]
    fint

/-- Step case: interior, the upper neighbour is not the centre. -/
theorem G_step_inner {w t d : Nat} (hw : w % 4 = 1) (_h9 : 9 ≤ w) (_ht : w / 2 ≤ t + 2)
    (hd : d ≤ w / 2) (h : 0 < d ∧ d + 1 < w / 2) :
    G w (t + 1) d = xor (G w t d) (G w t (lo d) || G w t (up w d)) := by
  have rt : (t + 1) % 4 = (t % 4 + 1) % 4 := by omega
  have hm4 : w / 2 % 4 = 0 ∨ w / 2 % 4 = 2 := by omega
  unfold G fl
  rw [rt]
  have e1 : lo d = d - 1 := by unfold lo; rw [if_neg (by omega)]
  have e2 : up w d = d + 1 := by unfold up; rw [if_neg (by omega)]
  have r1 : (d - 1) % 4 = (d % 4 + 3) % 4 := by omega
  have r2 : (d + 1) % 4 = (d % 4 + 1) % 4 := by omega
  rw [e1, e2, r1, r2, decide_eq_false (show ¬ d = 0 by omega),
    decide_eq_false (show ¬ d = w / 2 by omega), decide_eq_false (show ¬ d + 1 = w / 2 by omega),
    decide_eq_false (show ¬ d + 1 = 0 by omega)]
  by_cases h1 : d = 1
  · subst h1
    rw [show 1 - 1 = 0 by rfl, decide_eq_true (rfl : (0 : Nat) = 0),
      decide_eq_false (show ¬ 0 = w / 2 by omega)]
    rcases (show t + 2 < w ∨ t + 2 = w ∨ t + 1 = w ∨ w ≤ t by omega) with r | r | r | r
    · rw [decide_eq_false (show ¬ w ≤ 1 + (t + 1) by omega),
        decide_eq_false (show ¬ w ≤ 1 + t by omega), decide_eq_false (show ¬ w ≤ 0 + t by omega),
        decide_eq_false (show ¬ w ≤ 1 + 1 + t by omega)]
      fint
    · have : t % 4 = 3 := by omega
      rw [decide_eq_true (show w ≤ 1 + (t + 1) by omega),
        decide_eq_false (show ¬ w ≤ 1 + t by omega), decide_eq_false (show ¬ w ≤ 0 + t by omega),
        decide_eq_true (show w ≤ 1 + 1 + t by omega)]
      fint
    · have : t % 4 = 0 := by omega
      rw [decide_eq_true (show w ≤ 1 + (t + 1) by omega),
        decide_eq_true (show w ≤ 1 + t by omega), decide_eq_false (show ¬ w ≤ 0 + t by omega),
        decide_eq_true (show w ≤ 1 + 1 + t by omega)]
      fint
    · rw [decide_eq_true (show w ≤ 1 + (t + 1) by omega),
        decide_eq_true (show w ≤ 1 + t by omega), decide_eq_true (show w ≤ 0 + t by omega),
        decide_eq_true (show w ≤ 1 + 1 + t by omega)]
      fint
  · rw [decide_eq_false (show ¬ d - 1 = 0 by omega), decide_eq_false (show ¬ d - 1 = w / 2 by omega)]
    rcases (show d + t + 1 < w ∨ d + t + 1 = w ∨ d + t = w ∨ w + 1 ≤ d + t by omega)
      with r | r | r | r
    · rw [decide_eq_false (show ¬ w ≤ d + (t + 1) by omega),
        decide_eq_false (show ¬ w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega),
        decide_eq_false (show ¬ w ≤ d + 1 + t by omega)]
      fin4
    · have : (d + t) % 4 = 0 := by omega
      rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
        decide_eq_false (show ¬ w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega),
        decide_eq_true (show w ≤ d + 1 + t by omega)]
      fin4
    · have : (d + t) % 4 = 1 := by omega
      rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
        decide_eq_true (show w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega),
        decide_eq_true (show w ≤ d + 1 + t by omega)]
      fin4
    · rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
        decide_eq_true (show w ≤ d + t by omega), decide_eq_true (show w ≤ d - 1 + t by omega),
        decide_eq_true (show w ≤ d + 1 + t by omega)]
      fin4

set_option maxHeartbeats 1000000 in
/-- Step case: next to the centre: the upper neighbour is the centre. -/
theorem G_step_near {w t d : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (ht : w / 2 ≤ t + 2)
    (_hd : d ≤ w / 2) (h : d + 1 = w / 2) :
    G w (t + 1) d = xor (G w t d) (G w t (lo d) || G w t (up w d)) := by
  have rt : (t + 1) % 4 = (t % 4 + 1) % 4 := by omega
  have hm4 : w / 2 % 4 = 0 ∨ w / 2 % 4 = 2 := by omega
  unfold G fl
  rw [rt]
  have e1 : lo d = d - 1 := by unfold lo; rw [if_neg (by omega)]
  have e2 : up w d = d + 1 := by unfold up; rw [if_neg (by omega)]
  have r1 : (d - 1) % 4 = (d % 4 + 3) % 4 := by omega
  have r2 : (d + 1) % 4 = (d % 4 + 1) % 4 := by omega
  have hc : w / 2 % 4 = (d % 4 + 1) % 4 := by omega
  have hdo : d % 2 = 1 := by omega
  rw [e1, e2, r1, r2, hc, decide_eq_false (show ¬ d = 0 by omega),
    decide_eq_false (show ¬ d = w / 2 by omega), decide_eq_true (show d + 1 = w / 2 by omega),
    decide_eq_false (show ¬ d + 1 = 0 by omega), decide_eq_false (show ¬ d - 1 = 0 by omega),
    decide_eq_false (show ¬ d - 1 = w / 2 by omega)]
  rcases (show d + t + 1 < w ∨ d + t + 1 = w ∨ d + t = w ∨ w + 1 ≤ d + t by omega)
    with r | r | r | r
  · rw [decide_eq_false (show ¬ w ≤ d + (t + 1) by omega),
      decide_eq_false (show ¬ w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega),
      decide_eq_false (show ¬ w ≤ d + 1 + t by omega)]
    fin4
  · have : (d + t) % 4 = 0 := by omega
    rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
      decide_eq_false (show ¬ w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega),
      decide_eq_true (show w ≤ d + 1 + t by omega)]
    fin4
  · have : (d + t) % 4 = 1 := by omega
    rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
      decide_eq_true (show w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega),
      decide_eq_true (show w ≤ d + 1 + t by omega)]
    fin4
  · rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
      decide_eq_true (show w ≤ d + t by omega), decide_eq_true (show w ≤ d - 1 + t by omega),
      decide_eq_true (show w ≤ d + 1 + t by omega)]
    fin4

set_option maxHeartbeats 1000000 in
/-- Step case: the centre: odd width, so the upper neighbour is the centre itself. -/
theorem G_step_centre {w t d : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (ht : w / 2 ≤ t + 2)
    (_hd : d ≤ w / 2) (h : d = w / 2) :
    G w (t + 1) d = xor (G w t d) (G w t (lo d) || G w t (up w d)) := by
  have rt : (t + 1) % 4 = (t % 4 + 1) % 4 := by omega
  have hm4 : w / 2 % 4 = 0 ∨ w / 2 % 4 = 2 := by omega
  unfold G fl
  rw [rt]
  have e1 : lo d = d - 1 := by unfold lo; rw [if_neg (by omega)]
  have e2 : up w d = d := by unfold up; rw [if_pos h, if_neg (by omega)]
  have r1 : (d - 1) % 4 = (d % 4 + 3) % 4 := by omega
  have hc : w / 2 % 4 = d % 4 := by omega
  have hde : d % 2 = 0 := by omega
  rw [e1, e2, r1, hc, decide_eq_false (show ¬ d = 0 by omega),
    decide_eq_true (show d = w / 2 by omega), decide_eq_false (show ¬ d - 1 = 0 by omega),
    decide_eq_false (show ¬ d - 1 = w / 2 by omega)]
  rcases (show d + t + 1 < w ∨ d + t + 1 = w ∨ w ≤ d + t by omega) with r | r | r
  · -- only the last two cone steps reach here: `t = m - 2` or `m - 1`
    have : t + 2 = d ∨ t + 1 = d := by omega
    have : (d + 4 - t) % 4 = 2 ∨ (d + 4 - t) % 4 = 1 := by omega
    rw [decide_eq_false (show ¬ w ≤ d + (t + 1) by omega),
      decide_eq_false (show ¬ w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega)]
    fin4
  · have : (d + t) % 4 = 0 := by omega
    rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
      decide_eq_false (show ¬ w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega)]
    fin4
  · rcases (show d + t = w ∨ w + 1 ≤ d + t by omega) with r' | r'
    · have : (d + t) % 4 = 1 := by omega
      rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
        decide_eq_true (show w ≤ d + t by omega), decide_eq_false (show ¬ w ≤ d - 1 + t by omega)]
      fin4
    · rw [decide_eq_true (show w ≤ d + (t + 1) by omega),
        decide_eq_true (show w ≤ d + t by omega), decide_eq_true (show w ≤ d - 1 + t by omega)]
      fin4

theorem G_step {w t d : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (ht : w / 2 ≤ t + 2)
    (hd : d ≤ w / 2) :
    G w (t + 1) d = xor (G w t d) (G w t (lo d) || G w t (up w d)) := by
  rcases (show d = 0 ∨ (0 < d ∧ d + 1 < w / 2) ∨ d + 1 = w / 2 ∨ d = w / 2 by omega)
    with h | h | h | h
  · exact G_step_zero hw h9 ht hd h
  · exact G_step_inner hw h9 ht hd h
  · exact G_step_near hw h9 ht hd h
  · exact G_step_centre hw h9 ht hd h

/-! ## Induction from time `m - 2` -/

/-- At `m - 2` the folded cone has filled the segment and equals `G`. -/
theorem cone_eq_G {w d : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (hd : d ≤ w / 2) :
    Cf (w / 2 - 2) d = G w (w / 2 - 2) d := by
  unfold Cf G val
  rw [decide_eq_false (show ¬ w ≤ d + (w / 2 - 2) by omega), if_neg (by decide)]
  by_cases h : d ≤ w / 2 - 2
  · rw [decide_eq_true h]; rfl
  · rw [decide_eq_false h, Bool.false_and]
    exact (E_dead_even (show (w / 2 - 2) % 2 = 0 by omega) (show d % 4 ≠ (w / 2 - 2) % 4 by omega)).symm

/-- Cell `i` at time `m - 2 + k` is `G` at its folded position. -/
theorem iter_G {w : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (k : Nat) :
    ∀ i, i < w → (iter w (w / 2 - 2 + k) 1).testBit i = G w (w / 2 - 2 + k) (dist w i) := by
  have hw1 : 1 ≤ w := by omega
  induction k with
  | zero =>
    intro i hi
    rw [Nat.add_zero, iter_cone (by omega) (w / 2 - 2) (by omega) i hi,
      cone_eq_G hw h9 (dist_le w i)]
  | succ k ih =>
    rw [← Nat.add_assoc, iter_succ']
    exact fold_step (by omega) (iter_lt hw1 _) ih (fun d hd => G_step hw h9 (by omega) hd)

/-- Behind the wall everywhere (from `w - 3` on), `G` has period 4. -/
theorem G_period {w t d : Nat} (hw : w % 4 = 1) (h9 : 9 ≤ w) (ht : w ≤ t + 3)
    (hd : d ≤ w / 2) : G w (t + 4) d = G w t d := by
  have r4 : (t + 4) % 4 = t % 4 := by omega
  unfold G fl
  rw [r4]
  by_cases hr : w ≤ d + t
  · rw [decide_eq_true hr, decide_eq_true (show w ≤ d + (t + 4) by omega)]
  · rw [decide_eq_false hr, decide_eq_true (show w ≤ d + (t + 4) by omega)]
    rcases (show d = 0 ∨ d = 1 ∨ d = 2 by omega) with h | h | h <;> subst h <;>
      rw [decide_eq_false (show ¬ _ = w / 2 by omega)] <;> fint

/-! ## Main theorem -/

/-- **R2-C10 for `w ≡ 1 (mod 4)`**, every `w ≥ 9`: transient `T w = w - 3`, exact period 4.
(`w ≤ 200` is the kernel-checked range of `Discovery.Rule54`; the argument above covers
`w ≥ 17`.) -/
theorem rule54_mod4_one (w : Nat) (hw : w % 4 = 1) (h9 : 9 ≤ w) :
    T w = w - 3 ∧
    (∀ μ, iter w (μ + 4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧
    (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1) := by
  have hT : T w = w - 3 := by unfold T; rw [if_pos hw]
  refine ⟨hT, ?_⟩
  by_cases hsmall : w < 17
  · exact rule54_transient_period w (by omega) (by omega)
  have h17 : 17 ≤ w := by omega
  rw [hT]
  have hw1 : 1 ≤ w := by omega
  -- times written as `m - 2 + k`
  have tT : ∀ j, w - 3 + j = w / 2 - 2 + (w - 3 - (w / 2 - 2) + j) := by intro j; omega
  have bits : ∀ j, ∀ i, i < w → (iter w (w - 3 + j) 1).testBit i = G w (w - 3 + j) (dist w i) := by
    intro j i hi
    rw [tT j]
    exact iter_G hw h9 _ i hi
  -- periodicity from `w - 3`
  have hper : iter w (w - 3 + 4) 1 = iter w (w - 3) 1 := by
    apply eq_of_bits (iter_lt hw1 _) (iter_lt hw1 _)
    intro i hi
    have b0 := bits 0 i hi
    rw [Nat.add_zero] at b0
    rw [bits 4 i hi, b0, G_period hw h9 (by omega) (dist_le w i)]
  -- exact period 4: witness cells `5` (p = 1, 2) and `6` (p = 3), behind the wall
  have hne : ∀ p, 0 < p → p < 4 → iter w (w - 3 + p) 1 ≠ iter w (w - 3) 1 := by
    intro p hp0 hp4 heq
    have hT4 : (w - 3) % 4 = 2 := by omega
    have b0 := bits 0
    simp only [Nat.add_zero] at b0
    rcases (show p = 1 ∨ p = 2 ∨ p = 3 by omega) with rfl | rfl | rfl
    · have e := bits 1 5 (by omega)
      rw [heq, b0 5 (by omega), dist_self (by omega)] at e
      unfold G fl val at e
      rw [decide_eq_true (show w ≤ 5 + (w - 3 + 1) by omega), decide_eq_true (show w ≤ 5 + (w - 3) by omega),
        decide_eq_false (show ¬ 5 = w / 2 by omega), show (w - 3 + 1) % 4 = 3 by omega, hT4] at e
      simp only [Bool.false_and, Bool.or_false] at e
      exact absurd e (by decide)
    · have e := bits 2 5 (by omega)
      rw [heq, b0 5 (by omega), dist_self (by omega)] at e
      unfold G fl val at e
      rw [decide_eq_true (show w ≤ 5 + (w - 3 + 2) by omega), decide_eq_true (show w ≤ 5 + (w - 3) by omega),
        decide_eq_false (show ¬ 5 = w / 2 by omega), show (w - 3 + 2) % 4 = 0 by omega, hT4] at e
      simp only [Bool.false_and, Bool.or_false] at e
      exact absurd e (by decide)
    · have e := bits 3 6 (by omega)
      rw [heq, b0 6 (by omega), dist_self (by omega)] at e
      unfold G fl val at e
      rw [decide_eq_true (show w ≤ 6 + (w - 3 + 3) by omega), decide_eq_true (show w ≤ 6 + (w - 3) by omega),
        decide_eq_false (show ¬ 6 = w / 2 by omega), show (w - 3 + 3) % 4 = 1 by omega, hT4] at e
      simp only [Bool.false_and, Bool.or_false] at e
      exact absurd e (by decide)
  refine ⟨fun μ => ⟨fun hμ => ?_, fun hμ => periodic_from w 1 (w - 3) hper μ hμ⟩, hne⟩
  -- minimality: cell `0` differs between times `w - 4` and `w`
  refine Nat.le_of_not_lt fun hlt => ?_
  have h1 : iter w (w - 4 + 4) 1 = iter w (w - 4) 1 :=
    periodic_from w 1 μ hμ (w - 4) (by omega)
  have a := iter_G hw h9 (w - 4 - (w / 2 - 2)) 0 (by omega)
  have b := iter_G hw h9 (w - (w / 2 - 2)) 0 (by omega)
  rw [show w / 2 - 2 + (w - 4 - (w / 2 - 2)) = w - 4 by omega] at a
  have h1' : iter w w 1 = iter w (w - 4) 1 := by
    have := h1; rwa [show w - 4 + 4 = w by omega] at this
  rw [show w / 2 - 2 + (w - (w / 2 - 2)) = w by omega, h1', a] at b
  rw [show dist w 0 = 0 by unfold dist; omega] at b
  unfold G fl val at b
  rw [decide_eq_false (show ¬ w ≤ 0 + (w - 4) by omega), decide_eq_true (show w ≤ 0 + w by omega),
    decide_eq_false (show ¬ 0 = w / 2 by omega), show (w - 4) % 4 = 1 by omega,
    hw] at b
  simp only [Bool.false_and, Bool.or_false] at b
  exact absurd b (by decide)

end Discovery.Rule54Mod1
