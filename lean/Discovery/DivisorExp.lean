/-!
# DISC-0024: the exponent inequality behind A225004

A225004: a(n) = largest multiple of n with fewer than twice as many divisors as n.
Conjecture (J. Lowell, 2013): a(n) always divides n^2.

Write the multiple as n*m and list every prime p dividing n*m as a pair
(a, x) = (v_p(n), v_p(m)) (a may be 0 for a new prime).  Then
d(n) = prod (a+1) = `P l` and d(n*m) = prod (a+x+1) = `Q l`
(the usual divisor-count formula; that step is not formalized here).

`two_P_le_Q`: if some x >= a+1 then d(n*m) >= 2 d(n).
`exponents_le`: so d(n*m) < 2 d(n) forces x <= a for every prime, i.e. m | n,
hence n*m | n^2 (and a new prime, a = 0, can never appear).

Only core Lean is used.
-/

namespace Discovery.DivisorExp

/-- prod (a+1) over the pairs (a, x). -/
def P : List (Nat × Nat) → Nat
  | [] => 1
  | (a, _) :: t => (a + 1) * P t

/-- prod (a+x+1) over the pairs (a, x). -/
def Q : List (Nat × Nat) → Nat
  | [] => 1
  | (a, x) :: t => (a + x + 1) * Q t

theorem P_le_Q (l : List (Nat × Nat)) : P l ≤ Q l := by
  induction l with
  | nil => simp [P, Q]
  | cons ax t ih =>
    obtain ⟨a, x⟩ := ax
    simp only [P, Q]
    exact Nat.mul_le_mul (by omega) ih

theorem two_P_le_Q (l : List (Nat × Nat)) (h : ∃ ax ∈ l, ax.1 + 1 ≤ ax.2) :
    2 * P l ≤ Q l := by
  induction l with
  | nil =>
    obtain ⟨_, hm, _⟩ := h
    simp at hm
  | cons ax t ih =>
    obtain ⟨a, x⟩ := ax
    obtain ⟨⟨a', x'⟩, hm, hle⟩ := h
    simp only [P, Q]
    rcases List.mem_cons.mp hm with he | ht
    · -- the witness is the head
      simp only [Prod.mk.injEq] at he
      obtain ⟨e1, e2⟩ := he
      simp only at hle
      have h1 := Nat.mul_le_mul (show 2 * (a + 1) ≤ a + x + 1 by omega) (P_le_Q t)
      rw [Nat.mul_assoc] at h1
      exact h1
    · have h1 := Nat.mul_le_mul (show a + 1 ≤ a + x + 1 by omega) (ih ⟨(a', x'), ht, hle⟩)
      rw [Nat.mul_left_comm] at h1
      exact h1

/-- If d(n*m) < 2 d(n) then every exponent of m is at most the exponent in n. -/
theorem exponents_le (l : List (Nat × Nat)) (h : Q l < 2 * P l) :
    ∀ ax ∈ l, ax.2 ≤ ax.1 := by
  intro ax hm
  rcases Nat.lt_or_ge ax.1 ax.2 with hlt | hge
  · have := two_P_le_Q l ⟨ax, hm, hlt⟩
    omega
  · exact hge

/-! Sanity checks: n = 6 = 2*3.  m = 3 gives 18 with d = 6 < 8; m = 9 gives 54 with d = 8. -/
example : Q [(1, 0), (1, 1)] = 6 ∧ P [(1, 0), (1, 1)] = 4 := by decide
example : Q [(1, 0), (1, 2)] = 8 := by decide

end Discovery.DivisorExp
