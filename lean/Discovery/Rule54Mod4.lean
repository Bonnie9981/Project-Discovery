import Discovery.Rule26
import Discovery.Rule54

/-!
# DISC-0010: rule 54 on a ring of width `w ≡ 0 (mod 4)`, single live cell

Encoding, `step`, `iter` and `T` are those of `Discovery.Rule54` (bit `i` = cell `i`,
seed `1` = only cell 0 alive, rule 54 = `c xor (l or r)`). The bit lemmas for the two
cyclic rotations are reused from `Discovery.Rule26` (the rotations are literally the same).

Main results (every `w` with `w % 4 = 0` and `w ≥ 4`, no finite range):

* `iter_cone`: for `2t + 4 ≤ w`, after `t` steps cell `i` is alive iff it lies in the
  light cone (`i ≤ t` or `w ≤ i + t`) and the ether pattern `E t i` is `true`.
  `E t i` (period 4 in space and time): `t` even → `i ≡ t (mod 4)`;
  `t` odd → `i ≢ t + 1 (mod 4)`.
* `iter_ether`: from `T w = (w - 4) / 2` on, the ring is exactly the ether: cell `i` at
  time `T w + k` is `E (T w + k) i`.
* `rule54_mod4_zero`: for every such `w`, `x_{μ+4} = x_μ ↔ T w ≤ μ`, and the cycle has
  exact period 4. This is R2-C10 for `w ≡ 0 (mod 4)` with no upper bound on `w`.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.Rule54Mod4

open Discovery.Rule54 (step iter T iter_succ' iter_add periodic_from)
open Discovery.Rule26 (rotL rotR tb_rotL tb_rotR tb_rotL_high tb_rotR_high tb_high tb_one
  iL iR iL_lt iR_lt)

/-! ## Bit-level description of rule 54's `step` -/

theorem step_eq (w x : Nat) : step w x = x ^^^ (rotL w x ||| rotR w x) := rfl

theorem tb_step {w x i : Nat} (hw : 1 ≤ w) (hx : x < 2 ^ w) (hi : i < w) :
    (step w x).testBit i =
      xor (x.testBit i) (x.testBit (iL w i) || x.testBit (iR w i)) := by
  rw [step_eq, Nat.testBit_xor, Nat.testBit_or, tb_rotL hw hx hi, tb_rotR hw hx hi]
  rfl

theorem step_lt {w x : Nat} (hx : x < 2 ^ w) : step w x < 2 ^ w :=
  Nat.lt_pow_two_of_testBit _ fun i hi => by
    rw [step_eq, Nat.testBit_xor, Nat.testBit_or, tb_rotL_high hi, tb_rotR_high hi,
      tb_high hx hi]
    rfl

theorem iter_lt {w : Nat} (hw : 1 ≤ w) (t : Nat) : iter w t 1 < 2 ^ w := by
  induction t with
  | zero => exact Nat.one_lt_two_pow (by omega)
  | succ t ih => rw [iter_succ']; exact step_lt ih

/-! ## The ether (space and time period 4) -/

/-- Ether on residues: `a = t mod 4`, `b = i mod 4`. -/
def ee (a b : Nat) : Bool := if a % 2 = 0 then b == a else !(b == (a + 1) % 4)

/-- Ether pattern: cell `i` at time `t`. -/
def E (t i : Nat) : Bool := ee (t % 4) (i % 4)

theorem E_congr {t i j : Nat} (h : i % 4 = j % 4) : E t i = E t j := by
  unfold E; rw [h]

theorem E_succ (t i : Nat) : E (t + 1) i = ee ((t % 4 + 1) % 4) (i % 4) := by
  unfold E; rw [Nat.add_mod]

theorem E_add_four (t i : Nat) : E (t + 4) i = E t i := by
  unfold E; rw [Nat.add_mod_right]

/-- All residue facts used below, checked by `decide`. -/
theorem ee_table : ∀ a, a < 4 → ∀ b, b < 4 →
    -- interior: one step of rule 54 maps the ether to itself, shifted in time
    ee ((a + 1) % 4) b = xor (ee a b) (ee a ((b + 3) % 4) || ee a ((b + 1) % 4)) ∧
    -- the two cone edges are live
    (b = a → ee a b = true) ∧ ((a + b) % 4 = 0 → ee a b = true) ∧
    -- the cell just inside the right edge / left edge
    (b = a → ee ((a + 1) % 4) b = xor (ee a b) (ee a ((b + 3) % 4))) ∧
    ((a + b) % 4 = 0 → ee ((a + 1) % 4) b = xor (ee a b) (ee a ((b + 1) % 4))) := by
  decide

/-- Exact period 4 of the ether, on residues: for an even phase `a`, each shift `p = 1, 2, 3`
changes some cell `b < 4`. -/
theorem ee_witness' : ∀ a, a < 4 → ∀ p, p < 4 → a % 2 = 0 → 0 < p →
    ee ((a + p) % 4) (if p = 2 then a else (a + 1) % 4) ≠
      ee a (if p = 2 then a else (a + 1) % 4) := by
  decide

theorem ee_witness (a : Nat) (ha : a < 4) (h2 : a % 2 = 0) (p : Nat) (hp0 : 0 < p)
    (hp : p < 4) : ∃ b, b < 4 ∧ ee ((a + p) % 4) b ≠ ee a b :=
  ⟨if p = 2 then a else (a + 1) % 4, by split <;> omega, ee_witness' a ha p hp h2 hp0⟩

/-- At the odd phase `a + 3` the cell `a + 1` is alive (`a` even). -/
theorem ee_odd_live : ∀ a, a < 4 → a % 2 = 0 → ee ((a + 3) % 4) ((a + 1) % 4) = true := by
  decide

/-- Ether one-step identity for all `t`, `i`. -/
theorem E_step (t i : Nat) :
    E (t + 1) i = xor (E t i) (E t (i + 3) || E t (i + 1)) := by
  have h := (ee_table (t % 4) (Nat.mod_lt _ (by decide)) (i % 4) (Nat.mod_lt _ (by decide))).1
  rw [E_succ]; unfold E
  rw [show (i + 3) % 4 = (i % 4 + 3) % 4 by omega, show (i + 1) % 4 = (i % 4 + 1) % 4 by omega]
  exact h

/-! ## Neighbour residues on a ring with `w % 4 = 0` -/

theorem iL_mod {w i : Nat} (hw : w % 4 = 0) (h4 : 4 ≤ w) :
    (iL w i) % 4 = (i + 3) % 4 := by
  unfold iL; split <;> omega

theorem iR_mod {w i : Nat} (hw : w % 4 = 0) (hi : i < w) :
    (iR w i) % 4 = (i + 1) % 4 := by
  unfold iR; split <;> omega

/-! ## The light cone -/

/-- Closed form for `2t + 4 ≤ w`: light cone times ether. -/
def C (w t i : Nat) : Bool := decide (i ≤ t ∨ w ≤ i + t) && E t i

theorem E_edge_right (t i : Nat) (h : i % 4 = t % 4) : E t i = true :=
  ((ee_table (t % 4) (Nat.mod_lt _ (by decide)) (i % 4) (Nat.mod_lt _ (by decide))).2.1 h)

theorem E_edge_left (t i : Nat) (h : (t + i) % 4 = 0) : E t i = true :=
  ((ee_table (t % 4) (Nat.mod_lt _ (by decide)) (i % 4) (Nat.mod_lt _ (by decide))).2.2.1
    (by omega))

theorem E_in_right (t i : Nat) (h : i % 4 = t % 4) :
    E (t + 1) i = xor (E t i) (E t (i + 3)) := by
  have h' := (ee_table (t % 4) (Nat.mod_lt _ (by decide)) (i % 4)
    (Nat.mod_lt _ (by decide))).2.2.2.1 h
  rw [E_succ]; unfold E
  rw [show (i + 3) % 4 = (i % 4 + 3) % 4 by omega]
  exact h'

theorem E_in_left (t i : Nat) (h : (t + i) % 4 = 0) :
    E (t + 1) i = xor (E t i) (E t (i + 1)) := by
  have h' := (ee_table (t % 4) (Nat.mod_lt _ (by decide)) (i % 4)
    (Nat.mod_lt _ (by decide))).2.2.2.2 (by omega)
  rw [E_succ]; unfold E
  rw [show (i + 1) % 4 = (i % 4 + 1) % 4 by omega]
  exact h'

/-- One step inside the cone regime (`2t + 6 ≤ w`, so the two fronts are ≥ 5 cells apart). -/
theorem cone_step {w t i : Nat} (hw : w % 4 = 0) (ht : 2 * t + 6 ≤ w) (hi : i < w) :
    C w (t + 1) i = xor (C w t i) (C w t (iL w i) || C w t (iR w i)) := by
  have h4 : 4 ≤ w := by omega
  unfold C
  rw [E_congr (iL_mod hw h4), E_congr (iR_mod hw hi)]
  -- positions of the neighbours, as plain arithmetic facts
  have hLv : iL w i = if i = 0 then w - 1 else i - 1 := rfl
  have hRv : iR w i = if i = w - 1 then 0 else i + 1 := rfl
  by_cases hin : i ≤ t ∨ w ≤ i + t
  · -- `i` is in the cone at time `t`, hence also at `t + 1`
    rw [decide_eq_true hin, decide_eq_true (show i ≤ t + 1 ∨ w ≤ i + (t + 1) by omega)]
    by_cases hL : iL w i ≤ t ∨ w ≤ iL w i + t
    · by_cases hR : iR w i ≤ t ∨ w ≤ iR w i + t
      · rw [decide_eq_true hL, decide_eq_true hR]
        simpa using E_step t i
      · -- right edge: `i = t` (or `t = 0`, `i = 0`, both neighbours outside)
        rw [decide_eq_true hL, decide_eq_false hR]
        have hit : i = t := by
          rw [hLv] at hL; rw [hRv] at hR; split at hL <;> split at hR <;> omega
        simpa using E_in_right t i (by rw [hit])
    · by_cases hR : iR w i ≤ t ∨ w ≤ iR w i + t
      · -- left edge: `i + t = w`
        rw [decide_eq_false hL, decide_eq_true hR]
        have hit : i + t = w := by
          rw [hLv] at hL; rw [hRv] at hR; split at hL <;> split at hR <;> omega
        simpa using E_in_left t i (by omega)
      · -- `t = 0`, `i = 0`: both neighbours outside
        rw [decide_eq_false hL, decide_eq_false hR]
        have hit : i = 0 ∧ t = 0 := by
          rw [hLv] at hL; rw [hRv] at hR; split at hL <;> split at hR <;> omega
        obtain ⟨rfl, rfl⟩ := hit
        rfl
  · rw [decide_eq_false hin]
    by_cases hL : iL w i ≤ t ∨ w ≤ iL w i + t
    · -- `i = t + 1`, just outside the right front
      have hit : i = t + 1 := by
        rw [hLv] at hL; split at hL <;> omega
      have hR : ¬ (iR w i ≤ t ∨ w ≤ iR w i + t) := by
        rw [hRv]; split <;> omega
      rw [decide_eq_true hL, decide_eq_false hR,
        decide_eq_true (show i ≤ t + 1 ∨ w ≤ i + (t + 1) by omega)]
      have e1 : E (t + 1) i = true := E_edge_right (t + 1) i (by rw [hit])
      have e2 : E t (i + 3) = true := E_edge_right t (i + 3) (by omega)
      simp [e1, e2]
    · by_cases hR : iR w i ≤ t ∨ w ≤ iR w i + t
      · -- `i + t + 1 = w`, just outside the left front
        have hit : i + t + 1 = w := by
          rw [hRv] at hR; split at hR <;> omega
        rw [decide_eq_false hL, decide_eq_true hR,
          decide_eq_true (show i ≤ t + 1 ∨ w ≤ i + (t + 1) by omega)]
        have e1 : E (t + 1) i = true := E_edge_left (t + 1) i (by omega)
        have e2 : E t (i + 1) = true := E_edge_left t (i + 1) (by omega)
        simp [e1, e2]
      · -- far outside: stays dead
        have hout : ¬ (i ≤ t + 1 ∨ w ≤ i + (t + 1)) := by
          rw [hLv] at hL; rw [hRv] at hR; split at hL <;> split at hR <;> omega
        rw [decide_eq_false hL, decide_eq_false hR, decide_eq_false hout]
        rfl

/-- Lemma 1 (light cone): for `2t + 4 ≤ w`, cell `i` after `t` steps is `C w t i`. -/
theorem iter_cone {w : Nat} (hw : w % 4 = 0) (h4 : 4 ≤ w) :
    ∀ t, 2 * t + 4 ≤ w → ∀ i, i < w → (iter w t 1).testBit i = C w t i := by
  have hw1 : 1 ≤ w := by omega
  intro t
  induction t with
  | zero =>
    intro _ i hi
    show (1 : Nat).testBit i = _
    rw [tb_one]
    unfold C E ee
    by_cases h : i = 0
    · subst h; rfl
    · rw [decide_eq_false h, decide_eq_false (show ¬ (i ≤ 0 ∨ w ≤ i + 0) by omega)]
      rfl
  | succ t ih =>
    intro ht i hi
    have hb := ih (by omega)
    rw [iter_succ', tb_step hw1 (iter_lt hw1 t) hi, hb i hi, hb _ (iL_lt hw1 hi),
      hb _ (iR_lt hw1 hi), cone_step hw (by omega) hi]

/-! ## From `T w` on: pure ether -/

theorem T_eq {w : Nat} (hw : w % 4 = 0) : T w = (w - 4) / 2 := by
  unfold T
  rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]

/-- At `T w` the cone has closed up: three dead cells remain, and they are exactly the
dead cells of the ether, so the ring state is the ether. -/
theorem iter_T_ether {w : Nat} (hw : w % 4 = 0) (h4 : 4 ≤ w) :
    ∀ i, i < w → (iter w (T w) 1).testBit i = E (T w) i := by
  intro i hi
  rw [iter_cone hw h4 (T w) (by rw [T_eq hw]; omega) i hi]
  unfold C
  by_cases hin : i ≤ T w ∨ w ≤ i + T w
  · rw [decide_eq_true hin]; rfl
  · rw [decide_eq_false hin, Bool.false_and]
    -- `i ∈ {T+1, T+2, T+3}` and `T` is even: the ether is dead there
    rw [T_eq hw] at hin ⊢
    unfold E ee
    have h1 : ((w - 4) / 2 % 4) % 2 = 0 := by omega
    rw [if_pos h1]
    have h2 : i % 4 ≠ (w - 4) / 2 % 4 := by omega
    simp [h2]

theorem ether_step {w x t : Nat} (hw : w % 4 = 0) (h4 : 4 ≤ w) (hx : x < 2 ^ w)
    (hb : ∀ i, i < w → x.testBit i = E t i) :
    ∀ i, i < w → (step w x).testBit i = E (t + 1) i := by
  intro i hi
  have hw1 : 1 ≤ w := by omega
  rw [tb_step hw1 hx hi, hb i hi, hb _ (iL_lt hw1 hi), hb _ (iR_lt hw1 hi),
    E_congr (iL_mod hw h4), E_congr (iR_mod hw hi), E_step]

/-- Lemma 2: from time `T w` on the ring is exactly the ether. -/
theorem iter_ether {w : Nat} (hw : w % 4 = 0) (h4 : 4 ≤ w) (k : Nat) :
    ∀ i, i < w → (iter w (T w + k) 1).testBit i = E (T w + k) i := by
  have hw1 : 1 ≤ w := by omega
  induction k with
  | zero => exact iter_T_ether hw h4
  | succ k ih =>
    rw [← Nat.add_assoc, iter_succ']
    exact ether_step hw h4 (iter_lt hw1 _) ih

theorem eq_of_bits {w x y : Nat} (hx : x < 2 ^ w) (hy : y < 2 ^ w)
    (h : ∀ i, i < w → x.testBit i = y.testBit i) : x = y :=
  Nat.eq_of_testBit_eq fun i => by
    by_cases hi : i < w
    · exact h i hi
    · rw [tb_high hx (by omega), tb_high hy (by omega)]

/-! ## Main theorem -/

/-- **R2-C10 for `w ≡ 0 (mod 4)`**, every `w ≥ 4`: the single-seed orbit of rule 54 on the
ring of `w` cells has transient `T w = (w - 4) / 2` and exact period 4. -/
theorem rule54_mod4_zero (w : Nat) (hw : w % 4 = 0) (h4 : 4 ≤ w) :
    (∀ μ, iter w (μ + 4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧
    (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1) := by
  have hw1 : 1 ≤ w := by omega
  -- periodicity from `T w`
  have hper : iter w (T w + 4) 1 = iter w (T w) 1 := by
    apply eq_of_bits (iter_lt hw1 _) (iter_lt hw1 _)
    intro i hi
    have h0 := iter_ether hw h4 0 i hi
    rw [Nat.add_zero] at h0
    rw [iter_ether hw h4 4 i hi, h0, E_add_four]
  -- exact period 4: a witness cell for each `p`
  have hT : T w % 2 = 0 := by rw [T_eq hw]; omega
  have hne : ∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1 := by
    intro p hp0 hp4 heq
    -- witness cell (`ee_witness`): for `p = 2` cell `T w mod 4` (alive at `T w`, dead at
    -- `T w + 2`); for `p = 1, 3` cell `T w mod 4 + 1` (dead at `T w`, alive at odd times)
    have hcell : ∀ j, j < w → E (T w + p) j = E (T w) j := by
      intro j hj
      have h0 := iter_ether hw h4 0 j hj
      rw [Nat.add_zero] at h0
      rw [← iter_ether hw h4 p j hj, heq, h0]
    obtain ⟨b, hb4, hbne⟩ := ee_witness (T w % 4) (Nat.mod_lt _ (by decide)) (by omega) p hp0 hp4
    have := hcell b (by omega)
    unfold E at this
    rw [Nat.mod_eq_of_lt hb4, show (T w + p) % 4 = (T w % 4 + p) % 4 by omega] at this
    exact hbne this
  refine ⟨fun μ => ⟨fun hμ => ?_, fun hμ => periodic_from w 1 (T w) hper μ hμ⟩, hne⟩
  -- minimality: if `μ < T w`, then `x_{T-1}` would be on the cycle, but it has a dead
  -- cell `T w + 1 = 2m - 1` (`w = 4m`) outside the cone, alive in the odd phase `T w + 3`
  refine Nat.le_of_not_lt fun hlt => ?_
  have h1 : iter w (T w - 1 + 4) 1 = iter w (T w - 1) 1 :=
    periodic_from w 1 μ hμ (T w - 1) (by omega)
  have hT' := T_eq hw
  have hi : T w + 1 < w := by omega
  have a := iter_cone hw h4 (T w - 1) (by omega) (T w + 1) hi
  have b := iter_ether hw h4 3 (T w + 1) hi
  rw [show T w - 1 + 4 = T w + 3 by omega] at h1
  rw [h1, a] at b
  unfold C at b
  rw [decide_eq_false (show ¬ (T w + 1 ≤ T w - 1 ∨ w ≤ T w + 1 + (T w - 1)) by omega),
    Bool.false_and] at b
  unfold E at b
  rw [show (T w + 3) % 4 = (T w % 4 + 3) % 4 by omega,
    show (T w + 1) % 4 = (T w % 4 + 1) % 4 by omega,
    ee_odd_live (T w % 4) (Nat.mod_lt _ (by decide)) (by omega)] at b
  exact Bool.false_ne_true b

end Discovery.Rule54Mod4
