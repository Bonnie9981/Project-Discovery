/-!
# DISC-0015: Rule 54 from a single ON cell — rows, A118109 and A265225

Rule 54 maps neighbourhoods 111..000 to 0,0,1,1,0,1,1,0, i.e. `new = c xor (l or r)`.
`row_eq` gives every row in closed form; the OEIS formulas follow.
Only core Lean is used (no Mathlib, no `native_decide`).
-/
namespace Discovery.Rule54Rows

/-- Wolfram rule 54 as a lookup in the bits of 54. -/
def rule (l c r : Bool) : Bool := Nat.testBit 54 (4 * l.toNat + 2 * c.toNat + r.toNat)

theorem rule_eq (l c r : Bool) : rule l c r = xor c (l || r) := by
  cases l <;> cases c <;> cases r <;> decide

/-- One Rule 54 step on the bi-infinite line. -/
def step (f : Int → Bool) (x : Int) : Bool := rule (f (x - 1)) (f x) (f (x + 1))

/-- Generation `n` from a single ON cell at `0`. -/
def row : Nat → Int → Bool
  | 0 => fun x => decide (x = 0)
  | n + 1 => step (row n)

/-- Closed form: inside the light cone, even rows are ON at `x ≡ t (mod 4)`,
odd rows are ON except at `x ≡ t+1 (mod 4)`. -/
def C (t : Nat) (x : Int) : Prop :=
  -(t:Int) ≤ x ∧ x ≤ t ∧ ((t % 2 = 0 ∧ (x - t) % 4 = 0) ∨ (t % 2 = 1 ∧ (x - t - 1) % 4 ≠ 0))

instance (t : Nat) (x : Int) : Decidable (C t x) := by unfold C; infer_instance

theorem C_step (t : Nat) (x : Int) :
    C (t+1) x ↔ (C t x ↔ ¬ (C t (x-1) ∨ C t (x+1))) := by
  unfold C; push_cast; omega

theorem row_eq (t : Nat) (x : Int) : row t x = decide (C t x) := by
  induction t generalizing x with
  | zero =>
    show decide (x = 0) = decide (C 0 x)
    apply decide_eq_decide.mpr; unfold C; simp; omega
  | succ t ih =>
    simp only [row, step, rule_eq, ih]
    have h := C_step t x
    by_cases a : C t x <;> by_cases b : C t (x-1) <;> by_cases c : C t (x+1) <;>
      simp_all

/-! ## Reading a window of cells -/

/-- Cells `lo, …, lo+k-1` read as a decimal numeral of 0/1 digits (A118109). -/
def val (f : Int → Bool) (lo : Int) : Nat → Nat
  | 0 => 0
  | k + 1 => val f lo k * 10 + (if f (lo + k) then 1 else 0)

/-- Number of ON cells among `lo, …, lo+k-1`. -/
def cnt (f : Int → Bool) (lo : Int) : Nat → Nat
  | 0 => 0
  | k + 1 => cnt f lo k + (if f (lo + k) then 1 else 0)

theorem val_append (f : Int → Bool) (lo : Int) (m k : Nat) :
    val f lo (m + k) = val f lo m * 10 ^ k + val f (lo + m) k := by
  induction k with
  | zero => simp [val]
  | succ k ih =>
    rw [← Nat.add_assoc, val, ih, val, Nat.pow_succ, Int.natCast_add, Int.add_assoc]
    simp only [Nat.add_mul, Nat.mul_assoc, Nat.add_assoc]

theorem cnt_append (f : Int → Bool) (lo : Int) (m k : Nat) :
    cnt f lo (m + k) = cnt f lo m + cnt f (lo + m) k := by
  induction k with
  | zero => simp [cnt]
  | succ k ih =>
    rw [← Nat.add_assoc, cnt, ih, cnt, Int.natCast_add, Int.add_assoc, Nat.add_assoc]

theorem val_congr (f g : Int → Bool) (lo lo' : Int) (k : Nat)
    (h : ∀ j : Nat, j < k → f (lo + j) = g (lo' + j)) : val f lo k = val g lo' k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [val]; rw [ih (fun j hj => h j (by omega)), h k (by omega)]

theorem cnt_congr (f g : Int → Bool) (lo lo' : Int) (k : Nat)
    (h : ∀ j : Nat, j < k → f (lo + j) = g (lo' + j)) : cnt f lo k = cnt g lo' k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [cnt]; rw [ih (fun j hj => h j (by omega)), h k (by omega)]

/-- A118109(n): row `n`, cells `-n..n`, as a numeral. -/
def a118109 (n : Nat) : Nat := val (row n) (-(n:Int)) (2 * n + 1)

/-- Number of ON cells in row `n`. -/
def ones (n : Nat) : Nat := cnt (row n) (-(n:Int)) (2 * n + 1)

/-- A265225(n): ON cells in rows `0..n`. -/
def a265225 : Nat → Nat
  | 0 => ones 0
  | n + 1 => a265225 n + ones (n + 1)

/-- Row `n+2` = row `n` shifted left by 2, then 4 new cells on the right. -/
theorem shift (n : Nat) (j : Nat) (hj : j < 2 * n + 1) :
    row (n + 2) (-((n + 2 : Nat) : Int) + j) = row n (-(n : Int) + j) := by
  rw [row_eq, row_eq]; apply decide_eq_decide.mpr; unfold C; push_cast; omega

/-- The 4 new cells `n-1..n+2` of row `n+2`: `0001` (n even) or `0111` (n odd). -/
theorem tail (n : Nat) (j : Nat) :
    row (n + 2) (-((n + 2 : Nat) : Int) + ((2 * n + 1 : Nat) : Int) + j) =
      decide ((n % 2 = 0 ∧ j = 3) ∨ (n % 2 = 1 ∧ 1 ≤ j ∧ j ≤ 3)) := by
  rw [row_eq]; apply decide_eq_decide.mpr; unfold C; push_cast; omega

theorem two_mul_add (n : Nat) : 2 * (n + 2) + 1 = (2 * n + 1) + 4 := by omega

theorem a118109_step (n : Nat) :
    a118109 (n + 2) = a118109 n * 10000 + (if n % 2 = 0 then 1 else 111) := by
  unfold a118109
  rw [two_mul_add, val_append, val_congr _ _ _ _ _ (shift n)]
  congr 1
  simp only [val, tail]
  rcases Nat.mod_two_eq_zero_or_one n with h | h <;> simp [h]

theorem ones_step (n : Nat) :
    ones (n + 2) = ones n + (if n % 2 = 0 then 1 else 3) := by
  unfold ones
  rw [two_mul_add, cnt_append, cnt_congr _ _ _ _ _ (shift n)]
  congr 1
  simp only [cnt, tail]
  rcases Nat.mod_two_eq_zero_or_one n with h | h <;> simp [h]

theorem a118109_zero : a118109 0 = 1 := by decide
theorem a118109_one : a118109 1 = 111 := by decide
theorem ones_zero : ones 0 = 1 := by decide
theorem ones_one : ones 1 = 3 := by decide

/-! ## A118109 -/

/-- Barker's conjectured recurrence `a(n) = 10001*a(n-2) - 10000*a(n-4)`, `n > 3`. -/
theorem a118109_rec (n : Nat) :
    a118109 (n + 4) + 10000 * a118109 n = 10001 * a118109 (n + 2) := by
  have : (n + 2) % 2 = n % 2 := by omega
  rw [a118109_step (n + 2), this, a118109_step n]
  rcases Nat.mod_two_eq_zero_or_one n with hp | hp <;> simp only [hp] <;> simp <;> omega

/-- `9999*a(n) + e(n) = (10000 + 1100*(n mod 2))*100^n` with `e = 1` or `111`. -/
theorem a118109_mul (n : Nat) :
    9999 * a118109 n + (if n % 2 = 0 then 1 else 111) = (10000 + 1100 * (n % 2)) * 100 ^ n := by
  induction n using Nat.strongRecOn with
  | _ n ih =>
    match n, ih with
    | 0, _ => decide
    | 1, _ => decide
    | n + 2, ih =>
      have h := ih n (by omega)
      have hp : (n + 2) % 2 = n % 2 := by omega
      rw [a118109_step, hp, Nat.pow_succ, Nat.pow_succ]
      generalize hB : (10000 + 1100 * (n % 2)) * 100 ^ n = B at h
      rw [← Nat.mul_assoc, ← Nat.mul_assoc, hB]
      rcases Nat.mod_two_eq_zero_or_one n with h2 | h2 <;> simp [h2] at h ⊢ <;> omega

/-- Keller's conjecture `a(n) = floor((10000 + 1100*(n mod 2))*100^n / 9999)`. -/
theorem a118109_floor (n : Nat) :
    a118109 n = (10000 + 1100 * (n % 2)) * 100 ^ n / 9999 := by
  rw [← a118109_mul, Nat.mul_add_div (by decide)]
  split <;> simp

/-! ## Row counts and A265225 -/

theorem ones_formula (n : Nat) :
    2 * ones n = (if n % 2 = 0 then n + 2 else 3 * (n + 1)) := by
  induction n using Nat.strongRecOn with
  | _ n ih =>
    match n, ih with
    | 0, _ => decide
    | 1, _ => decide
    | n + 2, ih =>
      have h := ih n (by omega)
      have hp : (n + 2) % 2 = n % 2 := by omega
      rw [ones_step, hp]
      rcases Nat.mod_two_eq_zero_or_one n with h2 | h2 <;> simp [h2] at h ⊢ <;> omega

theorem ones_even (k : Nat) : ones (2 * k) = k + 1 := by
  have h := ones_formula (2 * k)
  have : 2 * k % 2 = 0 := by omega
  rw [this] at h; simp at h; omega

theorem ones_odd (k : Nat) : ones (2 * k + 1) = 3 * k + 3 := by
  have h := ones_formula (2 * k + 1)
  have : (2 * k + 1) % 2 = 1 := by omega
  rw [this] at h; simp at h; omega

/-- The only nonlinear identity used below (instantiated with numerals). -/
theorem lin (a b c d k : Nat) :
    (a * k + b) * (c * k + d) = a * c * (k * k) + (a * d + b * c) * k + b * d := by
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add, Nat.mul_mul_mul_comm, Nat.mul_right_comm a k d,
    ← Nat.mul_assoc b c k, Nat.add_mul]
  omega

theorem sq_add (k c : Nat) : (k + c) * (k + c) = k * k + (c + c) * k + c * c := by
  have := lin 1 c 1 c k; simp only [Nat.one_mul, Nat.mul_one] at this; rw [this]

/-- `a(2k) = 2k^2 + 3k + 1 = (2k+1)(k+1)`. -/
theorem a265225_even (k : Nat) : a265225 (2 * k) = 2 * (k * k) + 3 * k + 1 := by
  induction k with
  | zero => decide
  | succ k ih =>
    have e : 2 * (k + 1) = 2 * k + 1 + 1 := by omega
    rw [e, a265225, a265225, ih, ones_odd, ← e, ones_even, sq_add]; omega

/-- `a(2k+1) = 2k^2 + 6k + 4 = (2k+2)(k+2)`. -/
theorem a265225_odd (k : Nat) : a265225 (2 * k + 1) = 2 * (k * k) + 6 * k + 4 := by
  rw [a265225, a265225_even, ones_odd]; omega

theorem neg_one_pow (n : Nat) : (-1 : Int) ^ n = if n % 2 = 0 then 1 else -1 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Int.pow_succ, ih]
    rcases Nat.mod_two_eq_zero_or_one n with h | h
    · have : (n + 1) % 2 = 1 := by omega
      simp [h, this]
    · have : (n + 1) % 2 = 0 := by omega
      simp [h, this]

/-- Barker's conjecture `a(n) = (n+1)*(2*n - (-1)^n + 5)/4`, stated as `4*a(n) = …`. -/
theorem a265225_barker (n : Nat) :
    4 * (a265225 n : Int) = ((n : Int) + 1) * (2 * n - (-1) ^ n + 5) := by
  rcases Nat.mod_two_eq_zero_or_one n with hp | hp
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k := ⟨n / 2, by omega⟩
    have hN : 4 * a265225 (2 * k) = (2 * k + 1) * (4 * k + 4) := by
      rw [a265225_even, lin]; omega
    have hI : ((2 * k : Nat) : Int) + 1 = ((2 * k + 1 : Nat) : Int) := by push_cast; rfl
    have hJ : 2 * ((2 * k : Nat) : Int) - 1 + 5 = ((4 * k + 4 : Nat) : Int) := by push_cast; omega
    rw [neg_one_pow, if_pos hp, hI, hJ, ← Int.natCast_mul, ← hN]; push_cast; rfl
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
    have hN : 4 * a265225 (2 * k + 1) = (2 * k + 2) * (4 * k + 8) := by
      rw [a265225_odd, lin]; omega
    have hI : ((2 * k + 1 : Nat) : Int) + 1 = ((2 * k + 2 : Nat) : Int) := by push_cast; omega
    have hJ : 2 * ((2 * k + 1 : Nat) : Int) - -1 + 5 = ((4 * k + 8 : Nat) : Int) := by
      push_cast; omega
    rw [neg_one_pow, if_neg (by omega), hI, hJ, ← Int.natCast_mul, ← hN]; push_cast; rfl

/-- Hurt's conjecture `a(n) = n + 1 + (n+1)*floor((n+1)/2)`. -/
theorem a265225_hurt (n : Nat) : a265225 n = n + 1 + (n + 1) * ((n + 1) / 2) := by
  rcases Nat.mod_two_eq_zero_or_one n with hp | hp
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k := ⟨n / 2, by omega⟩
    have : (2 * k + 1) / 2 = k := by omega
    have l := lin 2 1 1 0 k
    simp only [Nat.one_mul, Nat.add_zero] at l
    rw [this, a265225_even, l]; omega
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
    have : (2 * k + 1 + 1) / 2 = k + 1 := by omega
    have l := lin 2 2 1 1 k
    simp only [Nat.one_mul] at l
    have e : 2 * k + 1 + 1 = 2 * k + 2 := rfl
    rw [this, a265225_odd, e, l]; omega

/-- Veselovac's conjecture `a(n) = A093353(n) + n + 1`, `A093353(n) = (n + (n mod 2))*(n+1)/2`. -/
theorem a265225_veselovac (n : Nat) :
    a265225 n = (n + n % 2) * (n + 1) / 2 + n + 1 := by
  rcases Nat.mod_two_eq_zero_or_one n with hp | hp
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k := ⟨n / 2, by omega⟩
    have l := lin 2 0 2 1 k
    simp only [Nat.add_zero, Nat.zero_mul, Nat.mul_zero] at l
    rw [hp, Nat.add_zero (2 * k), l, a265225_even]; omega
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
    have l := lin 2 2 2 2 k
    have e : 2 * k + 1 + 1 = 2 * k + 2 := rfl
    rw [hp, e, l, a265225_odd]; omega

/-- Barker's conjectured recurrence
`a(n) = a(n-1) + 2a(n-2) - 2a(n-3) - a(n-4) + a(n-5)`, `n > 4`. -/
theorem a265225_rec (n : Nat) :
    a265225 (n + 5) + 2 * a265225 (n + 2) + a265225 (n + 1) =
      a265225 (n + 4) + 2 * a265225 (n + 3) + a265225 n := by
  rcases Nat.mod_two_eq_zero_or_one n with hp | hp
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k := ⟨n / 2, by omega⟩
    have e5 : 2 * k + 5 = 2 * (k + 2) + 1 := by omega
    have e4 : 2 * k + 4 = 2 * (k + 2) := by omega
    have e3 : 2 * k + 3 = 2 * (k + 1) + 1 := by omega
    have e2 : 2 * k + 2 = 2 * (k + 1) := by omega
    rw [e5, e4, e3, e2, a265225_odd, a265225_odd, a265225_odd, a265225_even, a265225_even,
      a265225_even]
    have s1 := sq_add k 1
    have s2 := sq_add k 2
    omega
  · obtain ⟨k, rfl⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
    have e5 : 2 * k + 1 + 5 = 2 * (k + 3) := by omega
    have e4 : 2 * k + 1 + 4 = 2 * (k + 2) + 1 := by omega
    have e3 : 2 * k + 1 + 3 = 2 * (k + 2) := by omega
    have e2 : 2 * k + 1 + 2 = 2 * (k + 1) + 1 := by omega
    have e1 : 2 * k + 1 + 1 = 2 * (k + 1) := by omega
    rw [e5, e4, e3, e2, e1, a265225_odd, a265225_odd, a265225_odd, a265225_even, a265225_even,
      a265225_even]
    have s1 := sq_add k 1
    have s2 := sq_add k 2
    have s3 := sq_add k 3
    omega

end Discovery.Rule54Rows
