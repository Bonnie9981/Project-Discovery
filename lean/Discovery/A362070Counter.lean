/-!
# DISC-0020: a counterexample to the A362070 conjecture "a(n) = a(n+1) has no solutions"

OEIS A362070 (Ratajczak 2023): `m_min(n, k)` is the smallest `m ≥ 1` such that
`n` divides `∏_{t=1..m} RisingFactorial(t, k)`, and
`a(n) = Σ_{r=1..K(n)} m_min(n, r)` where `K(n)` is the Kempner number
(smallest `K` with `n ∣ K!`).

We encode the definition literally (`rf`, `P`, `IsMMin`, `IsKempner`, `AValue`),
prove that `AValue n s` determines `s` (so it really is a function of `n`), and
check by kernel computation that `a(1715) = a(1716) = 91`.

Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.A362070Counter

/-- Rising factorial `t (t+1) ⋯ (t+k-1)`. -/
def rf (t : Nat) : Nat → Nat
  | 0 => 1
  | k + 1 => rf t k * (t + k)

/-- `P k m = ∏_{t=1..m} rf t k`. -/
def P (k : Nat) : Nat → Nat
  | 0 => 1
  | m + 1 => P k m * rf (m + 1) k

def fact : Nat → Nat
  | 0 => 1
  | n + 1 => fact n * (n + 1)

/-- `m` is the smallest `m ≥ 1` with `n ∣ P k m`. -/
def IsMMin (n k m : Nat) : Prop :=
  1 ≤ m ∧ P k m % n = 0 ∧ ∀ j, j < m → 1 ≤ j → P k j % n ≠ 0

instance (n k m : Nat) : Decidable (IsMMin n k m) :=
  inferInstanceAs (Decidable (1 ≤ m ∧ _ ∧ ∀ j, j < m → 1 ≤ j → P k j % n ≠ 0))

/-- `K` is the Kempner number of `n`: the smallest `K ≥ 1` with `n ∣ K!`. -/
def IsKempner (n K : Nat) : Prop :=
  1 ≤ K ∧ fact K % n = 0 ∧ ∀ j, j < K → 1 ≤ j → fact j % n ≠ 0

instance (n K : Nat) : Decidable (IsKempner n K) :=
  inferInstanceAs (Decidable (1 ≤ K ∧ _ ∧ ∀ j, j < K → 1 ≤ j → fact j % n ≠ 0))

/-- `sumTo f K = f 0 + ⋯ + f (K-1)`. -/
def sumTo (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | K + 1 => sumTo f K + f K

/-- `a(n) = s` in the sense of A362070 (with `f i = m_min(n, i+1)`). -/
def AValue (n s : Nat) : Prop :=
  ∃ K f, IsKempner n K ∧ (∀ i, i < K → IsMMin n (i + 1) (f i)) ∧ sumTo f K = s

theorem mmin_unique {n k m m' : Nat} (h : IsMMin n k m) (h' : IsMMin n k m') : m = m' := by
  obtain ⟨h1, h2, h3⟩ := h
  obtain ⟨h1', h2', h3'⟩ := h'
  rcases Nat.lt_trichotomy m m' with hlt | heq | hgt
  · exact absurd h2 (h3' m hlt h1)
  · exact heq
  · exact absurd h2' (h3 m' hgt h1')

theorem kempner_unique {n K K' : Nat} (h : IsKempner n K) (h' : IsKempner n K') : K = K' := by
  obtain ⟨h1, h2, h3⟩ := h
  obtain ⟨h1', h2', h3'⟩ := h'
  rcases Nat.lt_trichotomy K K' with hlt | heq | hgt
  · exact absurd h2 (h3' K hlt h1)
  · exact heq
  · exact absurd h2' (h3 K' hgt h1')

theorem sumTo_congr (f g : Nat → Nat) (K : Nat) (h : ∀ i, i < K → f i = g i) :
    sumTo f K = sumTo g K := by
  induction K with
  | zero => rfl
  | succ K ih =>
    simp only [sumTo]
    rw [ih (fun i hi => h i (Nat.lt_succ_of_lt hi)), h K (Nat.lt_succ_self K)]

/-- `AValue n ·` is single-valued, so it defines `a(n)`. -/
theorem avalue_unique {n s s' : Nat} (h : AValue n s) (h' : AValue n s') : s = s' := by
  obtain ⟨K, f, hK, hf, hs⟩ := h
  obtain ⟨K', g, hK', hg, hs'⟩ := h'
  have hKK := kempner_unique hK hK'
  subst hKK
  rw [← hs, ← hs']
  exact sumTo_congr f g K (fun i hi => mmin_unique (hf i hi) (hg i hi))

/-- `m_min(1715, r)` for `r = 1..21`. -/
def L1715 : List Nat := [21, 13, 7, 6, 5, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1]

/-- `m_min(1716, r)` for `r = 1..13`. -/
def L1716 : List Nat := [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

set_option maxRecDepth 100000 in
theorem kempner_1715 : IsKempner 1715 21 := by decide

set_option maxRecDepth 100000 in
theorem kempner_1716 : IsKempner 1716 13 := by decide

set_option maxRecDepth 100000 in
theorem mmin_1715 : ∀ i, i < 21 → IsMMin 1715 (i + 1) (L1715.getD i 0) := by decide

set_option maxRecDepth 100000 in
theorem mmin_1716 : ∀ i, i < 13 → IsMMin 1716 (i + 1) (L1716.getD i 0) := by decide

theorem a_1715 : AValue 1715 91 :=
  ⟨21, fun i => L1715.getD i 0, kempner_1715, mmin_1715, by decide⟩

theorem a_1716 : AValue 1716 91 :=
  ⟨13, fun i => L1716.getD i 0, kempner_1716, mmin_1716, by decide⟩

/-- Counterexample to the A362070 conjecture: `a(1715) = a(1716)` (both are 91). -/
theorem a362070_counterexample :
    AValue 1715 91 ∧ AValue 1716 91 ∧
    ∀ s s', AValue 1715 s → AValue 1716 s' → s = s' :=
  ⟨a_1715, a_1716, fun s s' h h' => by
    rw [avalue_unique h a_1715, avalue_unique h' a_1716]⟩

end Discovery.A362070Counter
