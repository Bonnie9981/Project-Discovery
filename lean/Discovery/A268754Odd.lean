import Discovery.Rule26Even

/-!
# DISC-0013: OEIS A268754, `a(2n+1) = 2 a(n)` unless `n = 2^k - 1`

A268754(n) is the least eventual period of null-boundary rule 90 on a wire of `n` cells
started from one live cell at the left end (the PROG/MATHEMATICA definition of the entry;
`nstep`/`niter` of `Discovery.Rule26Even` are literally its Python update `((h<<1)^(h>>1)) & mask`).
The entry's FORMULA says: for odd indices `a(2n+1) = 2 a(n)`, except when `n = 2^k - 1`,
where the value is `1`. No proof is given in the entry.

Idea (spreading): put the `n`-wire on the even cells `2, 4, …, 2n` of the `(2n+1)`-wire
(bit `i` ↦ bit `2i+1`). Two rule-90 steps on the long wire act on the spread state exactly
like one step on the short wire (`spr_step`), and the seed reaches the spread seed after one
step (`spr_seed`). By the parity lemma `niter_par`, states at odd and even times live on
disjoint cells, so an odd eventual period is impossible unless the wire dies.
The wire dies iff `n + 1` is a power of two (`dies_iff`): even widths have an injective
update (`ker_even`), and `Dies (2r+1) ↔ Dies r`.

Main results: `a268754_odd`, `a268754_odd_exception`, plus `dies_iff`.
Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A268754Odd

open Discovery.Rule26 Discovery.Rule26Even

/-- `z` is `y` spread onto the odd bits: bit `2i+1` of `z` is bit `i` of `y`, even bits `0`. -/
def Spr (y z : Nat) : Prop := ∀ j, z.testBit j = (decide (j % 2 = 1) && y.testBit (j / 2))

theorem spr_step {n y z : Nat} (h : Spr y z) :
    Spr (nstep n y) (nstep (2 * n + 1) (nstep (2 * n + 1) z)) := by
  unfold Spr at h
  intro j
  obtain ⟨i, rfl | rfl⟩ : ∃ i, j = 2 * i ∨ j = 2 * i + 1 := ⟨j / 2, by omega⟩
  · simp only [tb_nstep, h]
    rcases i with _ | i
    · simp
    · have e1 : (2 * (i+1) - 1 - 1) % 2 = 0 := by omega
      have e2 : (2 * (i+1) - 1 + 1) % 2 = 0 := by omega
      have e3 : (2 * (i+1) + 1 - 1) % 2 = 0 := by omega
      have e4 : (2 * (i+1) + 1 + 1) % 2 = 0 := by omega
      have e5 : (2 * (i+1)) % 2 = 0 := by omega
      simp [e1, e2, e3, e4, e5]
  · simp only [tb_nstep, h]
    have e1 : (2 * i + 1 - 1) = 2 * i := by omega
    have e2 : (2 * i + 1 + 1 + 1) = 2 * i + 3 := by omega
    have e3 : (2 * i + 1 + 1 - 1) = 2 * i + 1 := by omega
    have e4 : (2 * i + 1 + 1) = 2 * i + 2 := by omega
    rw [e1, e2, e4] 
    have f1 : (2 * i + 1) % 2 = 1 := by omega
    have f2 : (2 * i + 3) % 2 = 1 := by omega
    have f3 : (2 * i + 1) / 2 = i := by omega
    have f4 : (2 * i + 3) / 2 = i + 1 := by omega
    have f5 : (2 * i + 2 - 1) = 2 * i + 1 := by omega
    rw [f5]
    rcases i with _ | i
    · simp [f1, f2, f3, f4]
      by_cases hn : 0 < n
      · simp [hn, show 2 < 2 * n + 1 by omega]
      · simp [hn]
    · have g1 : (2 * (i+1) - 1) % 2 = 1 := by omega
      have g2 : (2 * (i+1) - 1) / 2 = i := by omega
      simp [f1, f2, f3, f4, g1, g2]
      by_cases hn : i + 1 < n
      · simp [hn, show 2 * (i + 1) < 2 * n + 1 by omega, show 2 * (i + 1) + 2 < 2 * n + 1 by omega,
          show 1 ≤ 2 * (i + 1) by omega]
      · simp [hn]

theorem spr_seed {n : Nat} (hn : 1 ≤ n) : Spr 1 (nstep (2 * n + 1) 1) := by
  intro j
  rw [tb_nstep, tb_one, tb_one, tb_one]
  rcases j with _ | _ | j
  · simp
  · simp; omega
  · simp
    intro _ h
    omega

/-- Wire of width `2n+1` after `2t+1` steps is the spread of the width-`n` wire after `t`. -/
theorem spr_iter {n : Nat} (hn : 1 ≤ n) (t : Nat) :
    Spr (niter n t 1) (niter (2 * n + 1) (2 * t + 1) 1) := by
  induction t with
  | zero => exact spr_seed hn
  | succ t ih =>
    show Spr (nstep n (niter n t 1)) (nstep (2 * n + 1) (nstep (2 * n + 1) (niter (2 * n + 1) (2 * t + 1) 1)))
    exact spr_step ih

theorem spr_eq_iff {y y' z z' : Nat} (h : Spr y z) (h' : Spr y' z') : z = z' ↔ y = y' := by
  constructor
  · intro e; subst e
    apply Nat.eq_of_testBit_eq; intro i
    have a := h (2 * i + 1); have b := h' (2 * i + 1)
    rw [show (2 * i + 1) % 2 = 1 by omega, show (2 * i + 1) / 2 = i by omega] at a b
    simp at a b; rw [← a, ← b]
  · intro e; subst e
    apply Nat.eq_of_testBit_eq; intro i; rw [h i, h' i]

theorem spr_zero_iff {y z : Nat} (h : Spr y z) : z = 0 ↔ y = 0 :=
  spr_eq_iff h (fun j => by simp [Nat.zero_testBit])

theorem nstep_zero (n : Nat) : nstep n 0 = 0 :=
  Nat.eq_of_testBit_eq fun j => by simp [tb_nstep, Nat.zero_testBit]

theorem niter_zero_of {n t : Nat} (h : niter n t 1 = 0) (k : Nat) : niter n (t + k) 1 = 0 := by
  induction k with
  | zero => exact h
  | succ k ih => show nstep n (niter n (t + k) 1) = 0; rw [ih, nstep_zero]

/-- States at times of different parity can only agree when both are `0`. -/
theorem niter_par_eq {n s t : Nat} (hst : s % 2 ≠ t % 2) (h : niter n s 1 = niter n t 1) :
    niter n s 1 = 0 :=
  Nat.eq_of_testBit_eq fun j => by
    rw [Nat.zero_testBit]
    cases hb : (niter n s 1).testBit j
    · rfl
    · have a := niter_par n s j hb
      rw [h] at hb
      have b := niter_par n t j hb
      omega

/-- The rule-90 wire map is injective on even widths: its kernel is `0`. -/
theorem ker_even {n y : Nat} (hev : n % 2 = 0) (hy : y < 2 ^ n) (h : nstep n y = 0) : y = 0 := by
  have key : ∀ i, i < n → (decide (1 ≤ i) && y.testBit (i - 1)) = y.testBit (i + 1) := by
    intro i hi
    have := congrArg (fun x => Nat.testBit x i) h
    simp only [tb_nstep, Nat.zero_testBit, show decide (i < n) = true by simp [hi],
      Bool.true_and] at this
    revert this
    cases (decide (1 ≤ i) && y.testBit (i - 1)) <;> cases y.testBit (i + 1) <;> simp
  have odd : ∀ k, 2 * k + 1 < n → y.testBit (2 * k + 1) = false := by
    intro k
    induction k with
    | zero => intro hk; have := key 0 (by omega); simp at this; exact this ▸ rfl
    | succ k ih =>
      intro hk
      have := key (2 * k + 2) (by omega)
      rw [show 2 * k + 2 - 1 = 2 * k + 1 by omega, ih (by omega)] at this
      simp at this
      rw [show 2 * (k + 1) + 1 = 2 * k + 2 + 1 by omega]; exact this ▸ rfl
  have even : ∀ k, 2 * k ≤ n → y.testBit (n - 2 * k) = false := by
    intro k
    induction k with
    | zero => intro _; exact tb_high hy (by omega)
    | succ k ih =>
      intro hk
      have := key (n - 2 * k - 1) (by omega)
      rw [show n - 2 * k - 1 + 1 = n - 2 * k by omega, ih (by omega),
        show n - 2 * k - 1 - 1 = n - 2 * (k + 1) by omega,
        show decide (1 ≤ n - 2 * k - 1) = true by simp; omega] at this
      simpa using this
  apply Nat.eq_of_testBit_eq; intro j
  rw [Nat.zero_testBit]
  by_cases hj : n ≤ j
  · exact tb_high hy hj
  · by_cases hp : j % 2 = 1
    · have := odd (j / 2) (by omega)
      rwa [show 2 * (j / 2) + 1 = j by omega] at this
    · have := even ((n - j) / 2) (by omega)
      rwa [show n - 2 * ((n - j) / 2) = j by omega] at this

/-- The wire of `n` cells eventually dies (reaches the empty state). -/
def Dies (n : Nat) : Prop := ∃ t, niter n t 1 = 0

theorem not_dies_even {n : Nat} (hn : 1 ≤ n) (hev : n % 2 = 0) : ¬ Dies n := by
  intro ⟨t, ht⟩
  induction t with
  | zero => exact absurd ht (by show (1 : Nat) ≠ 0; decide)
  | succ t ih => exact ih (ker_even hev (niter_lt hn t) ht)

theorem dies_odd_iff {r : Nat} (hr : 1 ≤ r) : Dies (2 * r + 1) ↔ Dies r := by
  constructor
  · intro ⟨s, hs⟩
    refine ⟨s, ?_⟩
    have h0 := niter_zero_of hs (s + 1)
    rw [show s + (s + 1) = 2 * s + 1 by omega] at h0
    exact (spr_zero_iff (spr_iter hr s)).1 h0
  · intro ⟨t, ht⟩
    exact ⟨2 * t + 1, (spr_zero_iff (spr_iter hr t)).2 ht⟩

/-- **The wire dies iff `n + 1` is a power of two** (the comment of OEIS A268754). -/
theorem dies_iff (n : Nat) (hn : 1 ≤ n) : Dies n ↔ ∃ k, n + 1 = 2 ^ k := by
  by_cases hev : n % 2 = 0
  · refine iff_of_false (not_dies_even hn hev) ?_
    intro ⟨k, hk⟩
    cases k with
    | zero => simp at hk; omega
    | succ k => rw [Nat.pow_succ] at hk; omega
  · by_cases h1 : n = 1
    · subst h1; exact iff_of_true ⟨1, by decide⟩ ⟨1, rfl⟩
    · obtain ⟨r, rfl⟩ : ∃ r, n = 2 * r + 1 := ⟨n / 2, by omega⟩
      have hr : 1 ≤ r := by omega
      rw [dies_odd_iff hr, dies_iff r hr]
      constructor
      · intro ⟨k, hk⟩; exact ⟨k + 1, by rw [Nat.pow_succ]; omega⟩
      · intro ⟨k, hk⟩
        cases k with
        | zero => simp at hk
        | succ k => exact ⟨k, by rw [Nat.pow_succ] at hk; omega⟩
termination_by n
decreasing_by omega

/-- `p` is the least eventual period of `f` (the OEIS definition of A268754). -/
def LeastPer (f : Nat → Nat) (p : Nat) : Prop :=
  0 < p ∧ EvPer f p ∧ ∀ q, 0 < q → q < p → ¬ EvPer f q

theorem leastPer_unique {f : Nat → Nat} {p q : Nat} (hp : LeastPer f p) (hq : LeastPer f q) :
    p = q := by
  rcases Nat.lt_trichotomy p q with h | h | h
  · exact absurd hp.2.1 (hq.2.2 p hp.1 h)
  · exact h
  · exact absurd hq.2.1 (hp.2.2 q hq.1 h)

theorem evper_double_iff {n : Nat} (hn : 1 ≤ n) (q : Nat) :
    EvPer (fun s => niter (2 * n + 1) s 1) (2 * q) ↔ EvPer (fun t => niter n t 1) q := by
  constructor
  · intro ⟨T, hT⟩
    refine ⟨T, fun t ht => ?_⟩
    have e := hT (2 * t + 1) (by omega)
    simp only [show 2 * t + 1 + 2 * q = 2 * (t + q) + 1 by omega] at e
    exact (spr_eq_iff (spr_iter hn (t + q)) (spr_iter hn t)).1 e
  · intro ⟨T, hT⟩
    have odd : ∀ t, T ≤ t →
        niter (2 * n + 1) (2 * t + 1 + 2 * q) 1 = niter (2 * n + 1) (2 * t + 1) 1 := by
      intro t ht
      rw [show 2 * t + 1 + 2 * q = 2 * (t + q) + 1 by omega]
      exact (spr_eq_iff (spr_iter hn (t + q)) (spr_iter hn t)).2 (hT t ht)
    refine ⟨2 * T + 1, fun s hs => ?_⟩
    obtain ⟨t, rfl | rfl⟩ : ∃ t, s = 2 * t + 1 ∨ s = 2 * t + 2 := ⟨(s - 1) / 2, by omega⟩
    · exact odd t (by omega)
    · show niter (2 * n + 1) (2 * t + 2 + 2 * q) 1 = niter (2 * n + 1) (2 * t + 2) 1
      rw [show 2 * t + 2 + 2 * q = 2 * t + 1 + 2 * q + 1 by omega]
      show nstep _ (niter (2 * n + 1) (2 * t + 1 + 2 * q) 1) = nstep _ (niter (2 * n + 1) (2 * t + 1) 1)
      rw [odd t (by omega)]

section alive
variable {n : Nat} (hn : 1 ≤ n) (alive : ∀ t, niter n t 1 ≠ 0)
include hn alive

theorem evper_odd_width_even {p : Nat} (h : EvPer (fun s => niter (2 * n + 1) s 1) p) :
    p % 2 = 0 := by
  obtain ⟨T, hT⟩ := h
  have e : niter (2 * n + 1) (2 * T + 1 + p) 1 = niter (2 * n + 1) (2 * T + 1) 1 :=
    hT (2 * T + 1) (by omega)
  refine Classical.byContradiction fun hp => ?_
  have z := niter_par_eq (show (2 * T + 1 + p) % 2 ≠ (2 * T + 1) % 2 by omega) e
  rw [e] at z
  exact alive T ((spr_zero_iff (spr_iter hn T)).1 z)

/-- Least eventual period doubles: if the `n`-wire never dies and has least eventual
period `p`, the `(2n+1)`-wire has least eventual period `2p`. -/
theorem leastPer_double {p : Nat} (hp : LeastPer (fun t => niter n t 1) p) :
    LeastPer (fun s => niter (2 * n + 1) s 1) (2 * p) := by
  refine ⟨by have := hp.1; omega, (evper_double_iff hn p).2 hp.2.1, fun q hq hlt hq' => ?_⟩
  obtain ⟨r, rfl⟩ : ∃ r, q = 2 * r := ⟨q / 2, by have := evper_odd_width_even hn alive hq'; omega⟩
  exact hp.2.2 r (by omega) (by omega) ((evper_double_iff hn r).1 hq')

omit alive in
/-- Converse of `leastPer_double`: if the `(2n+1)`-wire has least eventual period `2p`,
the `n`-wire has least eventual period `p`. -/
theorem leastPer_half {p : Nat} (hp : LeastPer (fun s => niter (2 * n + 1) s 1) (2 * p)) :
    LeastPer (fun t => niter n t 1) p := by
  refine ⟨by have := hp.1; omega, (evper_double_iff hn p).1 hp.2.1, fun q hq hlt hq' => ?_⟩
  exact hp.2.2 (2 * q) (by omega) (by omega) ((evper_double_iff hn q).2 hq')

/-- Least eventual periods exist for both wires or for neither (no `p` is lost). -/
theorem exists_leastPer_iff :
    (∃ p, LeastPer (fun t => niter n t 1) p) ↔
      ∃ p, LeastPer (fun s => niter (2 * n + 1) s 1) p := by
  constructor
  · intro ⟨p, hp⟩; exact ⟨2 * p, leastPer_double hn alive hp⟩
  · intro ⟨p, hp⟩
    obtain ⟨r, rfl⟩ : ∃ r, p = 2 * r :=
      ⟨p / 2, by have := evper_odd_width_even hn alive hp.2.1; omega⟩
    exact ⟨r, leastPer_half hn hp⟩

end alive

theorem leastPer_one_of_dies {n : Nat} (h : Dies n) : LeastPer (fun t => niter n t 1) 1 := by
  obtain ⟨t, ht⟩ := h
  refine ⟨by decide, ⟨t, fun s hs => ?_⟩, fun q h0 h1 => by omega⟩
  obtain ⟨k, rfl⟩ : ∃ k, s = t + k := ⟨s - t, by omega⟩
  show niter n (t + k + 1) 1 = niter n (t + k) 1
  rw [niter_zero_of ht k, show t + k + 1 = t + (k + 1) by omega, niter_zero_of ht]

/-- **OEIS A268754 FORMULA, generic case.** For `n ≥ 1` with `n + 1` not a power of two,
`a(2n+1) = 2 a(n)`: whenever `p` is the least eventual period of the left-seeded
null-boundary rule-90 wire of `n` cells, `2p` is that of the wire of `2n+1` cells. -/
theorem a268754_odd {n p : Nat} (hn : 1 ≤ n) (hk : ¬ ∃ k, n + 1 = 2 ^ k)
    (hp : LeastPer (fun t => niter n t 1) p) :
    LeastPer (fun s => niter (2 * n + 1) s 1) (2 * p) :=
  leastPer_double hn (fun t ht => hk ((dies_iff n hn).1 ⟨t, ht⟩)) hp

/-- Generic case as an equivalence: `p = a(n)` iff `2p = a(2n+1)`. -/
theorem a268754_odd_iff {n p : Nat} (hn : 1 ≤ n) (hk : ¬ ∃ k, n + 1 = 2 ^ k) :
    LeastPer (fun t => niter n t 1) p ↔ LeastPer (fun s => niter (2 * n + 1) s 1) (2 * p) :=
  ⟨a268754_odd hn hk, leastPer_half hn⟩

/-- **OEIS A268754 FORMULA, exceptional case.** If `n + 1 = 2^k` (`n ≥ 1`), both wires die,
so `a(n) = a(2n+1) = 1`. -/
theorem a268754_odd_exception {n k : Nat} (hn : 1 ≤ n) (hk : n + 1 = 2 ^ k) :
    LeastPer (fun t => niter n t 1) 1 ∧ LeastPer (fun s => niter (2 * n + 1) s 1) 1 := by
  have d := (dies_iff n hn).2 ⟨k, hk⟩
  exact ⟨leastPer_one_of_dies d, leastPer_one_of_dies ((dies_odd_iff hn).2 d)⟩

set_option maxRecDepth 100000 in
/-- Kernel spot checks: `a(4) = 6` and the long wire of `9` cells repeats with `12`. -/
theorem check_small : niter 4 6 1 = niter 4 0 1 ∧ niter 9 13 1 = niter 9 1 1 ∧
    niter 9 7 1 ≠ niter 9 1 1 ∧ niter 3 3 1 = 0 ∧ niter 7 7 1 = 0 := by decide

end Discovery.A268754Odd
