/-!
# DISC-0014: OEIS A071052, `a(2n) = a(n) + 2n`

A071052(n) is the number of 0's in row `n` of the Rule 150 triangle A071036, i.e. among the
`2n+1` cells `-n..n` at generation `n` of elementary CA Rule 150 started from one ON cell.
The entry's FORMULA states `a(2n) = a(n) + 2n` as "(conjectured)" (Ralf Stephan, 2004).

Rule 150 is `new(i) = old(i-1) xor old(i) xor old(i+1)`.  Over GF(2) two steps give
`new(i) = old(i-2) xor old(i) xor old(i+2)` (`step_step`), so two steps on a configuration
"dilated" onto the even cells equal one step before dilation (`step_step_dil`).
Hence generation `2n` is generation `n` dilated (`row_double`): the ON count is unchanged
(`ones_double`, the known A071053(2n) = A071053(n)), and the row is `2n` cells longer, all new
cells 0 (`a071052_double`).

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A071052Even

/-- One Rule 150 step on the bi-infinite line. -/
def step (f : Int → Bool) (i : Int) : Bool := xor (f (i - 1)) (xor (f i) (f (i + 1)))

/-- The single ON seed at cell `0`. -/
def seed (i : Int) : Bool := decide (i = 0)

/-- Generation `n` of Rule 150 from the single seed. -/
def row : Nat → Int → Bool
  | 0 => seed
  | n + 1 => step (row n)

/-- Dilation: put `g` on the even cells, odd cells 0. -/
def dil (g : Int → Bool) (i : Int) : Bool := if i % 2 = 0 then g (i / 2) else false

/-- Number of `j < len` with `g (a + j)` true. -/
def cnt (g : Int → Bool) (a : Int) : Nat → Nat
  | 0 => 0
  | len + 1 => cnt g a len + (if g (a + len) then 1 else 0)

/-- Number of ON cells in row `n` (cells `-n..n`): A071053(n). -/
def ones (n : Nat) : Nat := cnt (row n) (-(n : Int)) (2 * n + 1)

/-- Number of 0 cells in row `n` (cells `-n..n`): A071052(n). -/
def zeros (n : Nat) : Nat := cnt (fun i => !row n i) (-(n : Int)) (2 * n + 1)

theorem xor_five (a b c d e : Bool) :
    xor (xor a (xor b c)) (xor (xor b (xor c d)) (xor c (xor d e))) = xor a (xor c e) := by
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> rfl

/-- Two Rule 150 steps: the GF(2) "Frobenius" identity `(x⁻¹+1+x)² = x⁻²+1+x²`. -/
theorem step_step (f : Int → Bool) (i : Int) :
    step (step f) i = xor (f (i - 2)) (xor (f i) (f (i + 2))) := by
  unfold step
  have h1 : i - 1 - 1 = i - 2 := by omega
  have h2 : i - 1 + 1 = i := by omega
  have h3 : i + 1 - 1 = i := by omega
  have h4 : i + 1 + 1 = i + 2 := by omega
  rw [h1, h2, h3, h4]
  exact xor_five _ _ _ _ _

theorem dil_even (g : Int → Bool) (m : Int) : dil g (2 * m) = g m := by
  unfold dil
  have h1 : (2 * m) % 2 = 0 := by omega
  have h2 : (2 * m) / 2 = m := by omega
  rw [if_pos h1, h2]

theorem dil_odd (g : Int → Bool) (m : Int) : dil g (2 * m + 1) = false := by
  unfold dil
  have h1 : ¬ (2 * m + 1) % 2 = 0 := by omega
  rw [if_neg h1]

/-- Two steps on a dilated configuration = dilation of one step. -/
theorem step_step_dil (g : Int → Bool) : step (step (dil g)) = dil (step g) := by
  funext i
  rw [step_step]
  rcases (show ∃ m, i = 2 * m ∨ i = 2 * m + 1 from ⟨i / 2, by omega⟩) with ⟨m, h | h⟩
  · subst h
    have e1 : 2 * m - 2 = 2 * (m - 1) := by omega
    have e2 : 2 * m + 2 = 2 * (m + 1) := by omega
    rw [e1, e2, dil_even, dil_even, dil_even, dil_even]
    rfl
  · subst h
    have e1 : 2 * m + 1 - 2 = 2 * (m - 1) + 1 := by omega
    have e2 : 2 * m + 1 + 2 = 2 * (m + 1) + 1 := by omega
    rw [e1, e2, dil_odd, dil_odd, dil_odd, dil_odd]
    rfl

theorem seed_dil : dil seed = seed := by
  funext i
  unfold dil seed
  by_cases h : i % 2 = 0
  · rw [if_pos h]
    by_cases h0 : i = 0
    · have : i / 2 = 0 := by omega
      simp [h0]
    · have : ¬ i / 2 = 0 := by omega
      simp [h0, this]
  · rw [if_neg h]
    have : ¬ i = 0 := by omega
    simp [this]

/-- Generation `2n` is generation `n` dilated. -/
theorem row_double (n : Nat) : row (2 * n) = dil (row n) := by
  induction n with
  | zero => exact seed_dil.symm
  | succ n ih =>
    have : 2 * (n + 1) = 2 * n + 1 + 1 := by omega
    rw [this]
    show step (step (row (2 * n))) = dil (step (row n))
    rw [ih, step_step_dil]

/-- The Rule 150 light cone: row `n` is 0 outside `-n..n`. -/
theorem row_support (n : Nat) (i : Int) (h : (n : Int) < i ∨ i < -(n : Int)) :
    row n i = false := by
  induction n generalizing i with
  | zero => unfold row seed; simp; omega
  | succ n ih =>
    show step (row n) i = false
    unfold step
    rw [ih (i - 1) (by omega), ih i (by omega), ih (i + 1) (by omega)]
    rfl

theorem cnt_le (g : Int → Bool) (a : Int) (len : Nat) : cnt g a len ≤ len := by
  induction len with
  | zero => exact Nat.le_refl 0
  | succ len ih => unfold cnt; split <;> omega

theorem cnt_compl (g : Int → Bool) (a : Int) (len : Nat) :
    cnt g a len + cnt (fun i => !g i) a len = len := by
  induction len with
  | zero => rfl
  | succ len ih =>
    unfold cnt
    cases hg : g (a + len) <;> simp [hg] <;> omega

/-- Counting a dilated configuration over a window of even length `2L`. -/
theorem cnt_dil (g : Int → Bool) (a : Int) (L : Nat) :
    cnt (dil g) (2 * a) (2 * L) = cnt g a L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    have : 2 * (L + 1) = 2 * L + 1 + 1 := by omega
    rw [this]
    simp only [cnt]
    rw [ih]
    have e1 : 2 * a + ((2 * L + 1 : Nat) : Int) = 2 * (a + L) + 1 := by omega
    have e2 : 2 * a + ((2 * L : Nat) : Int) = 2 * (a + L) := by omega
    rw [e1, e2, dil_odd, dil_even]
    simp

/-- A071053(2n) = A071053(n) (known; Peter J. Taylor 2020 in the entry). -/
theorem ones_double (n : Nat) : ones (2 * n) = ones n := by
  unfold ones
  rw [row_double]
  -- extend the window `-2n..2n` by the odd cell `2n+1`, which is 0
  have hext : cnt (dil (row n)) (-((2 * n : Nat) : Int)) (2 * (2 * n) + 1 + 1)
      = cnt (dil (row n)) (-((2 * n : Nat) : Int)) (2 * (2 * n) + 1) := by
    show cnt _ _ (2 * (2 * n) + 1) + _ = _
    have e : -((2 * n : Nat) : Int) + ((2 * (2 * n) + 1 : Nat) : Int) = 2 * (n : Int) + 1 := by
      omega
    rw [e, dil_odd]
    simp
  rw [← hext]
  have e2 : 2 * (2 * n) + 1 + 1 = 2 * (2 * n + 1) := by omega
  have e3 : -((2 * n : Nat) : Int) = 2 * (-(n : Int)) := by omega
  rw [e2, e3, cnt_dil]

theorem ones_add_zeros (n : Nat) : ones n + zeros n = 2 * n + 1 :=
  cnt_compl (row n) (-(n : Int)) (2 * n + 1)

/-- **OEIS A071052 conjecture**: `a(2n) = a(n) + 2n` for every `n ≥ 0`. -/
theorem a071052_double (n : Nat) : zeros (2 * n) = zeros n + 2 * n := by
  have h1 := ones_add_zeros n
  have h2 := ones_add_zeros (2 * n)
  have h3 := ones_double n
  omega

end Discovery.A071052Even
