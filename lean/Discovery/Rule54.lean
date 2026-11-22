/-!
# DISC-0006 / R2-C10: ECA rule 54 on a ring, single live cell

State of a ring of `w` cells = a natural number `x < 2 ^ w` whose bit `i` is cell `i`
(same encoding as `research/r002/impl_b.py`, seed `1` = only cell 0 alive). Rule 54 is
`new_i = x_i xor (x_{i-1} or x_{i+1})`; `step w` implements it with a cyclic rotation.

* `check_range`: kernel-checked (`decide`) facts for every `6 ≤ w ≤ 200`.
* `rule54_transient_period`: for `6 ≤ w ≤ 200`, the least `μ` with `x_{μ+4} = x_μ` is
  `T w` (`w-3, (w-6)/2, (w-7)/2, (w-4)/2` for `w ≡ 1, 2, 3, 0 mod 4`), and the cycle
  reached at `T w` has exact period 4 (`x_{T+p} ≠ x_T` for `p = 1, 2, 3`).

Not proved: the statement for `w > 200` (no general argument is formalised).
-/

namespace Discovery.Rule54

/-- Rule 54 on a ring of `w` cells (bit `i` = cell `i`). -/
def step (w x : Nat) : Nat :=
  let mask := 2 ^ w - 1
  let left := Nat.land (Nat.lor (Nat.shiftLeft x 1) (Nat.shiftRight x (w - 1))) mask
  let right := Nat.land (Nat.lor (Nat.shiftRight x 1) (Nat.shiftLeft (Nat.land x 1) (w - 1))) mask
  Nat.xor x (Nat.lor left right)

/-- `iter w k x` = state after `k` steps. -/
def iter (w : Nat) : Nat → Nat → Nat
  | 0, x => x
  | k + 1, x => iter w k (step w x)

/-- Conjectured transient length (R2-C10). -/
def T (w : Nat) : Nat :=
  if w % 4 = 1 then w - 3 else if w % 4 = 2 then (w - 6) / 2
  else if w % 4 = 3 then (w - 7) / 2 else (w - 4) / 2

/-- Finite certificate: period-4 return at `T w`, no return at `T w - 1`, exact period 4. -/
def Check (w : Nat) : Prop :=
  iter w (T w + 4) 1 = iter w (T w) 1 ∧
  (T w = 0 ∨ iter w (T w - 1 + 4) 1 ≠ iter w (T w - 1) 1) ∧
  iter w (T w + 1) 1 ≠ iter w (T w) 1 ∧
  iter w (T w + 2) 1 ≠ iter w (T w) 1 ∧
  iter w (T w + 3) 1 ≠ iter w (T w) 1

instance (w : Nat) : Decidable (Check w) := by unfold Check; infer_instance

set_option maxRecDepth 100000 in
theorem check_range : ∀ w, w < 201 → 6 ≤ w → Check w := by decide

theorem iter_succ' (w k x : Nat) : iter w (k + 1) x = step w (iter w k x) := by
  induction k generalizing x with
  | zero => rfl
  | succ k ih => exact ih (step w x)

theorem iter_add (w a b x : Nat) : iter w (a + b) x = iter w a (iter w b x) := by
  induction a with
  | zero => simp [iter]
  | succ a ih => rw [Nat.add_right_comm, iter_succ', ih, iter_succ']

theorem periodic_from (w x t : Nat) (h : iter w (t + 4) x = iter w t x) :
    ∀ μ, t ≤ μ → iter w (μ + 4) x = iter w μ x := by
  intro μ hμ
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hμ
  rw [Nat.add_comm t d, Nat.add_assoc, iter_add, h, ← iter_add]

theorem rule54_transient_period (w : Nat) (h6 : 6 ≤ w) (h200 : w ≤ 200) :
    (∀ μ, iter w (μ + 4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧
    (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1) := by
  obtain ⟨h4, hmin, h1, h2, h3⟩ := check_range w (by omega) h6
  refine ⟨fun μ => ⟨fun hμ => ?_, fun hμ => periodic_from w 1 (T w) h4 μ hμ⟩, ?_⟩
  · refine Nat.le_of_not_lt fun hlt => ?_
    rcases hmin with h0 | hne
    · omega
    · exact hne (periodic_from w 1 μ hμ (T w - 1) (by omega))
  · intro p hp0 hp4
    rcases (show p = 1 ∨ p = 2 ∨ p = 3 by omega) with rfl | rfl | rfl
    · exact h1
    · exact h2
    · exact h3

end Discovery.Rule54
