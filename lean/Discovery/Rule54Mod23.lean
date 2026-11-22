import Discovery.Rule54Mod4

/-!
# DISC-0011: rule 54 on a ring of width `w ≡ 2` or `3 (mod 4)`, single live cell

Same encoding as `Discovery.Rule54` / `Discovery.Rule54Mod4` (bit `i` = cell `i`, seed `1`,
rule 54 = `c xor (l or r)`).

Idea: the single-seed orbit is mirror-symmetric, so every state is a function of the ring
distance `dist w i = min i (w - i)` to the seed. `fold_step` turns one ring step into one step
on the folded segment `0, 1, …, m` (`m = w / 2`), reflecting at both ends (`lo`, `up`).
For `w ≡ 2, 3 (mod 4)` we have `m = T w + 3` with `T w` even, and on the segment:

* `iter_cone`: for `t ≤ T w`, cell `i` is alive iff `dist w i ≤ t` and `E t (dist w i)`
  (`E` = the period-4 ether of `Rule54Mod4`).
* `iter_defect`: at time `T w + k` cell `i` is alive iff `E (T w + k) (dist w i)`, except that
  the centre (`dist w i = m`, the one or two cells farthest from the seed) is dead when
  `k ≡ 1 (mod 4)`: a stationary one-cell defect where the two ether halves meet.
* `rule54_mod4_two`, `rule54_mod4_three`: transient `T w` ( = `(w - 6) / 2` resp.
  `(w - 7) / 2`) and exact period 4, for every such `w ≥ 6`.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.Rule54Mod23

open Discovery.Rule54 (step iter T iter_succ' periodic_from)
open Discovery.Rule26 (iL iR iL_lt iR_lt tb_one)
open Discovery.Rule54Mod4 (tb_step iter_lt ee E E_congr E_add_four E_step E_edge_right
  E_in_right ee_witness' ee_odd_live eq_of_bits)

/-! ## Folding the ring onto the segment `0..w/2` -/

/-- Ring distance from cell `i` to the seed cell `0`. -/
def dist (w i : Nat) : Nat := min i (w - i)

/-- Lower neighbour on the folded segment (reflect at `0`). -/
def lo (d : Nat) : Nat := if d = 0 then 1 else d - 1

/-- Upper neighbour on the folded segment (reflect at the centre `w / 2`). -/
def up (w d : Nat) : Nat := if d = w / 2 then (if w % 2 = 0 then d - 1 else d) else d + 1

theorem dist_le (w i : Nat) : dist w i ≤ w / 2 := by unfold dist; omega

theorem dist_self {w d : Nat} (h : d ≤ w / 2) : dist w d = d := by unfold dist; omega

/-- The two ring neighbours of `i` sit at folded positions `lo` and `up` (in some order). -/
theorem fold {w i : Nat} (hw : 3 ≤ w) (hi : i < w) :
    (dist w (iL w i) = lo (dist w i) ∧ dist w (iR w i) = up w (dist w i)) ∨
    (dist w (iL w i) = up w (dist w i) ∧ dist w (iR w i) = lo (dist w i)) := by
  have hL : iL w i = if i = 0 then w - 1 else i - 1 := rfl
  have hR : iR w i = if i = w - 1 then 0 else i + 1 := rfl
  rw [hL, hR]
  unfold dist lo up
  repeat' split
  all_goals omega

/-- One ring step on a mirror-symmetric state is one step on the folded segment. -/
theorem fold_step {w x : Nat} {f g : Nat → Bool} (hw : 3 ≤ w) (hx : x < 2 ^ w)
    (hf : ∀ i, i < w → x.testBit i = f (dist w i))
    (hg : ∀ d, d ≤ w / 2 → g d = xor (f d) (f (lo d) || f (up w d))) :
    ∀ i, i < w → (step w x).testBit i = g (dist w i) := by
  intro i hi
  have hw1 : 1 ≤ w := by omega
  rw [tb_step hw1 hx hi, hf i hi, hf _ (iL_lt hw1 hi), hf _ (iR_lt hw1 hi),
    hg _ (dist_le w i)]
  rcases fold hw hi with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · rw [h1, h2]
  · rw [h1, h2, Bool.or_comm]

/-! ## Ether facts on the segment -/

/-- The ether is mirror-symmetric around cell `0`: cells `1` and `3` agree. -/
theorem ee_sym : ∀ a, a < 4 → ee a 1 = ee a 3 := by decide

/-- Ether step at a folded position (both neighbours present, reflection at `0` allowed). -/
theorem E_step_lo (t d : Nat) : E (t + 1) d = xor (E t d) (E t (lo d) || E t (d + 1)) := by
  rw [E_step]
  unfold lo
  split
  · subst d
    have h3 : E t (0 + 3) = E t 1 := by
      show ee (t % 4) ((0 + 3) % 4) = ee (t % 4) (1 % 4)
      exact (ee_sym (t % 4) (Nat.mod_lt _ (by decide))).symm
    rw [h3]
  · rw [E_congr (show (d + 3) % 4 = (d - 1) % 4 by omega)]

/-- At an even time the ether is dead off its residue class. -/
theorem E_dead_even {t d : Nat} (ht : t % 2 = 0) (hd : d % 4 ≠ t % 4) : E t d = false := by
  unfold E ee
  rw [if_pos (by omega)]
  simp [hd]

/-! ## Lemma 1: the folded light cone, `t ≤ T w` -/

/-- Folded cone: alive iff within distance `t` and on the ether. -/
def Cf (t d : Nat) : Bool := decide (d ≤ t) && E t d

theorem cone_seg {w t d : Nat} (hc : t + 3 ≤ w / 2) (hd : d ≤ w / 2) :
    Cf (t + 1) d = xor (Cf t d) (Cf t (lo d) || Cf t (up w d)) := by
  have hhi : up w d = d + 1 ∨ d = w / 2 := by unfold up; split <;> omega
  unfold Cf
  by_cases h1 : d < t
  · -- deep inside: both neighbours inside
    have hlo : lo d ≤ t := by unfold lo; split <;> omega
    have hh : up w d = d + 1 := by omega
    rw [hh, decide_eq_true (show d ≤ t + 1 by omega), decide_eq_true (show d ≤ t by omega),
      decide_eq_true hlo, decide_eq_true (show d + 1 ≤ t by omega)]
    simpa using E_step_lo t d
  · by_cases h2 : d = t
    · subst d
      have hh : up w t = t + 1 := by omega
      rw [hh, decide_eq_true (show t ≤ t + 1 by omega), decide_eq_true (Nat.le_refl t),
        decide_eq_false (show ¬ t + 1 ≤ t by omega)]
      by_cases ht : t = 0
      · subst ht; decide
      · have hlo : lo t = t - 1 := by unfold lo; split <;> omega
        rw [hlo, decide_eq_true (show t - 1 ≤ t by omega), E_in_right t t rfl,
          E_congr (show (t + 3) % 4 = (t - 1) % 4 by omega)]
        simp
    · by_cases h3 : d = t + 1
      · subst d
        have hh : up w (t + 1) = t + 2 := by omega
        have hlo : lo (t + 1) = t := by unfold lo; split <;> omega
        rw [hh, hlo, decide_eq_true (Nat.le_refl (t + 1)),
          decide_eq_false (show ¬ t + 1 ≤ t by omega), decide_eq_true (Nat.le_refl t),
          decide_eq_false (show ¬ t + 2 ≤ t by omega),
          E_edge_right (t + 1) (t + 1) rfl, E_edge_right t t rfl]
        rfl
      · -- far outside: everything dead
        have hlo : lo d = d - 1 := by unfold lo; split <;> omega
        have hout : ¬ up w d ≤ t := by
          unfold up; split
          · split <;> omega
          · omega
        rw [hlo, decide_eq_false (show ¬ d ≤ t + 1 by omega),
          decide_eq_false (show ¬ d ≤ t by omega), decide_eq_false (show ¬ d - 1 ≤ t by omega),
          decide_eq_false hout]
        rfl

/-- Lemma 1: for `t + 2 ≤ w / 2`, cell `i` after `t` steps is `Cf t (dist w i)`. -/
theorem iter_cone {w : Nat} (hw : 6 ≤ w) :
    ∀ t, t + 2 ≤ w / 2 → ∀ i, i < w → (iter w t 1).testBit i = Cf t (dist w i) := by
  have hw1 : 1 ≤ w := by omega
  intro t
  induction t with
  | zero =>
    intro _ i hi
    show (1 : Nat).testBit i = _
    rw [tb_one]
    unfold Cf dist
    by_cases h : i = 0
    · subst h
      rw [show min 0 (w - 0) = 0 by omega]; rfl
    · rw [decide_eq_false h, decide_eq_false (show ¬ min i (w - i) ≤ 0 by omega)]
      rfl
  | succ t ih =>
    intro ht
    rw [iter_succ']
    exact fold_step (by omega) (iter_lt hw1 t) (ih (by omega))
      (fun d hd => cone_seg (by omega) hd)

/-! ## Lemma 2: from `T w` on, ether with a stationary centre defect -/

/-- State at time `T + k` on the segment with centre `m`. -/
def Df (T m k d : Nat) : Bool := E (T + k) d && !(decide (d = m) && decide (k % 4 = 1))

/-- The residue facts at the centre (`a = T mod 4` even, `r = k mod 4`), by `decide`. -/
theorem defect_table : ∀ a, a < 4 → a % 2 = 0 → ∀ r, r < 4 →
    -- the cell next to the centre (`d = m - 1 = T + 2`)
    ee ((a + r + 1) % 4) ((a + 2) % 4) = xor (ee ((a + r) % 4) ((a + 2) % 4))
      (ee ((a + r) % 4) ((a + 1) % 4) ||
        (ee ((a + r) % 4) ((a + 3) % 4) && !decide (r = 1))) ∧
    -- the centre, even width (both neighbours are `m - 1`)
    (ee ((a + r + 1) % 4) ((a + 3) % 4) && !decide ((r + 1) % 4 = 1)) =
      xor (ee ((a + r) % 4) ((a + 3) % 4) && !decide (r = 1))
        (ee ((a + r) % 4) ((a + 2) % 4) || ee ((a + r) % 4) ((a + 2) % 4)) ∧
    -- the centre, odd width (neighbours `m - 1` and the other centre cell `m`)
    (ee ((a + r + 1) % 4) ((a + 3) % 4) && !decide ((r + 1) % 4 = 1)) =
      xor (ee ((a + r) % 4) ((a + 3) % 4) && !decide (r = 1))
        (ee ((a + r) % 4) ((a + 2) % 4) ||
          (ee ((a + r) % 4) ((a + 3) % 4) && !decide (r = 1))) := by
  decide

theorem defect_seg {w T k d : Nat} (hm : w / 2 = T + 3) (hT : T % 2 = 0) (hd : d ≤ w / 2) :
    Df T (w / 2) (k + 1) d =
      xor (Df T (w / 2) k d) (Df T (w / 2) k (lo d) || Df T (w / 2) k (up w d)) := by
  have tab := defect_table (T % 4) (Nat.mod_lt _ (by decide)) (by omega) (k % 4)
    (Nat.mod_lt _ (by decide))
  -- residues of the times and positions involved
  have e1 : (T + (k + 1)) % 4 = (T % 4 + k % 4 + 1) % 4 := by omega
  have e0 : (T + k) % 4 = (T % 4 + k % 4) % 4 := by omega
  have ek : (k + 1) % 4 = (k % 4 + 1) % 4 := by omega
  unfold Df
  by_cases h1 : d + 1 < w / 2
  · -- away from the centre: plain ether step
    have hlo : lo d ≠ w / 2 := by unfold lo; split <;> omega
    have hh : up w d = d + 1 := by unfold up; split <;> omega
    rw [hh, decide_eq_false (show ¬ d = w / 2 by omega), decide_eq_false hlo,
      decide_eq_false (show ¬ d + 1 = w / 2 by omega), ← Nat.add_assoc]
    simpa using E_step_lo (T + k) d
  · by_cases h2 : d + 1 = w / 2
    · -- next to the centre
      have hlo : lo d = T + 1 := by unfold lo; split <;> omega
      have hh : up w d = T + 3 := by unfold up; split <;> omega
      have hdT : d = T + 2 := by omega
      rw [hlo, hh, hm, hdT, decide_eq_false (show ¬ T + 2 = T + 3 by omega),
        decide_eq_false (show ¬ T + 1 = T + 3 by omega), decide_eq_true rfl]
      unfold E
      rw [e1, e0, show (T + 2) % 4 = (T % 4 + 2) % 4 by omega,
        show (T + 1) % 4 = (T % 4 + 1) % 4 by omega, show (T + 3) % 4 = (T % 4 + 3) % 4 by omega]
      simpa using tab.1
    · -- the centre
      have hdm : d = w / 2 := by omega
      have hlo : lo d = T + 2 := by unfold lo; split <;> omega
      rw [hlo, hdm, hm, decide_eq_true rfl, decide_eq_false (show ¬ T + 2 = T + 3 by omega),
        ek]
      have r3 : (T + 3) % 4 = (T % 4 + 3) % 4 := by omega
      have r2 : (T + 2) % 4 = (T % 4 + 2) % 4 := by omega
      by_cases hpar : w % 2 = 0
      · have hh : up w (w / 2) = T + 2 := by unfold up; rw [if_pos rfl, if_pos hpar]; omega
        rw [hm] at hh
        rw [hh, decide_eq_false (show ¬ T + 2 = T + 3 by omega)]
        unfold E
        rw [e1, e0, r3, r2]
        simpa using tab.2.1
      · have hh : up w (w / 2) = T + 3 := by unfold up; rw [if_pos rfl, if_neg hpar]; omega
        rw [hm] at hh
        rw [hh, decide_eq_true rfl]
        unfold E
        rw [e1, e0, r3]
        simpa using tab.2.2

/-- At `T w` the folded cone is already the defect ether (phase `k = 0`, no defect). -/
theorem cone_eq_defect {w T d : Nat} (hm : w / 2 = T + 3) (hT : T % 2 = 0) (hd : d ≤ w / 2) :
    Cf T d = Df T (w / 2) 0 d := by
  unfold Cf Df
  rw [Nat.add_zero, decide_eq_false (show ¬ (0 % 4 = 1) by decide)]
  by_cases h : d ≤ T
  · rw [decide_eq_true h]; simp
  · rw [decide_eq_false h, E_dead_even hT (by omega)]; rfl

/-- Lemma 2: at time `T + k` cell `i` is `Df T m k (dist w i)`. -/
theorem iter_defect {w T : Nat} (hw : 6 ≤ w) (hm : w / 2 = T + 3) (hT : T % 2 = 0) (k : Nat) :
    ∀ i, i < w → (iter w (T + k) 1).testBit i = Df T (w / 2) k (dist w i) := by
  have hw1 : 1 ≤ w := by omega
  induction k with
  | zero =>
    intro i hi
    rw [Nat.add_zero, iter_cone hw T (by omega) i hi, cone_eq_defect hm hT (dist_le w i)]
  | succ k ih =>
    rw [← Nat.add_assoc, iter_succ']
    exact fold_step (by omega) (iter_lt hw1 _) ih (fun d hd => defect_seg hm hT hd)

/-! ## Main theorem -/

/-- Transient `T` and exact period 4, for any `w ≥ 6` whose half-width is `T + 3`, `T` even. -/
theorem rule54_core {w T : Nat} (hw : 6 ≤ w) (hm : w / 2 = T + 3) (hT : T % 2 = 0) :
    (∀ μ, iter w (μ + 4) 1 = iter w μ 1 ↔ T ≤ μ) ∧
    (∀ p, 0 < p → p < 4 → iter w (T + p) 1 ≠ iter w T 1) := by
  have hw1 : 1 ≤ w := by omega
  have h0 : ∀ i, i < w → (iter w T 1).testBit i = Df T (w / 2) 0 (dist w i) := by
    intro i hi; have := iter_defect hw hm hT 0 i hi; rwa [Nat.add_zero] at this
  -- periodicity from `T`
  have hper : iter w (T + 4) 1 = iter w T 1 := by
    apply eq_of_bits (iter_lt hw1 _) (iter_lt hw1 _)
    intro i hi
    rw [iter_defect hw hm hT 4 i hi, h0 i hi]
    unfold Df
    rw [show T + 4 = T + 0 + 4 by rfl, E_add_four]
    rfl
  -- exact period 4: witness cell `b < 4`, away from the centre
  have hne : ∀ p, 0 < p → p < 4 → iter w (T + p) 1 ≠ iter w T 1 := by
    intro p hp0 hp4 heq
    have hwit := ee_witness' (T % 4) (Nat.mod_lt _ (by decide)) p hp4 (by omega) hp0
    generalize hb : (if p = 2 then T % 4 else (T % 4 + 1) % 4) = b at hwit
    have hb4 : b < 4 := by rw [← hb]; split <;> omega
    have hbm : b ≠ w / 2 := by rw [← hb]; split <;> omega
    have hbw : b < w := by omega
    have e := iter_defect hw hm hT p b hbw
    rw [heq, h0 b hbw, dist_self (by omega)] at e
    unfold Df at e
    rw [decide_eq_false hbm] at e
    simp only [Bool.false_and, Bool.not_false, Bool.and_true, Nat.add_zero] at e
    unfold E at e
    rw [Nat.mod_eq_of_lt hb4, show (T + p) % 4 = (T % 4 + p) % 4 by omega] at e
    exact hwit e.symm
  refine ⟨fun μ => ⟨fun hμ => ?_, fun hμ => periodic_from w 1 T hper μ hμ⟩, hne⟩
  -- minimality: if `μ < T`, then `x_{T-1}` is on the cycle; but cell `T + 1` is dead at
  -- `T - 1` (outside the cone) and alive at `T + 3` (odd phase, not the centre)
  refine Nat.le_of_not_lt fun hlt => ?_
  have h1 : iter w (T - 1 + 4) 1 = iter w (T - 1) 1 :=
    periodic_from w 1 μ hμ (T - 1) (by omega)
  have hi : T + 1 < w := by omega
  have hd : dist w (T + 1) = T + 1 := dist_self (by omega)
  have a := iter_cone hw (T - 1) (by omega) (T + 1) hi
  have b := iter_defect hw hm hT 3 (T + 1) hi
  rw [show T - 1 + 4 = T + 3 by omega] at h1
  rw [h1, a, hd] at b
  unfold Cf Df at b
  rw [decide_eq_false (show ¬ T + 1 ≤ T - 1 by omega), Bool.false_and,
    decide_eq_false (show ¬ T + 1 = w / 2 by omega), Bool.false_and, Bool.not_false,
    Bool.and_true] at b
  unfold E at b
  rw [show (T + 3) % 4 = (T % 4 + 3) % 4 by omega,
    show (T + 1) % 4 = (T % 4 + 1) % 4 by omega,
    ee_odd_live (T % 4) (Nat.mod_lt _ (by decide)) (by omega)] at b
  exact Bool.false_ne_true b

/-- **R2-C10 for `w ≡ 2 (mod 4)`**, every `w ≥ 6`: transient `T w = (w - 6) / 2`, exact
period 4. -/
theorem rule54_mod4_two (w : Nat) (hw : w % 4 = 2) (h6 : 6 ≤ w) :
    T w = (w - 6) / 2 ∧
    (∀ μ, iter w (μ + 4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧
    (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1) := by
  have hT : T w = (w - 6) / 2 := by
    unfold T; rw [if_neg (by omega), if_pos hw]
  exact ⟨hT, rule54_core h6 (by omega) (by omega)⟩

/-- **R2-C10 for `w ≡ 3 (mod 4)`**, every `w ≥ 7`: transient `T w = (w - 7) / 2`, exact
period 4. -/
theorem rule54_mod4_three (w : Nat) (hw : w % 4 = 3) (h7 : 7 ≤ w) :
    T w = (w - 7) / 2 ∧
    (∀ μ, iter w (μ + 4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧
    (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1) := by
  have hT : T w = (w - 7) / 2 := by
    unfold T; rw [if_neg (by omega), if_neg (by omega), if_pos hw]
  exact ⟨hT, rule54_core (by omega) (by omega) (by omega)⟩

end Discovery.Rule54Mod23
