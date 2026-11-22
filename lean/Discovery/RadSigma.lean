import Mathlib.NumberTheory.ArithmeticFunction
import Mathlib.Data.Nat.Squarefree

/-!
# DISC-0006 / C02: `rad(σ n) = σ(rad n)` (partial)

C02: if `rad(σ n) = σ(rad n)` then `n` and `σ n` are both squarefree, or `n = 2^a p` with
`p` an odd prime and `a ≥ 3` odd. Only the following pieces are formalised:
* `c02b`: A065301 (`n`, `σ n` squarefree) solves the equation.
* `c02_of_squarefree`: a squarefree solution `n` has `σ n` squarefree.
* `squarefree_sigma_rad`, `odd_prime_factor_unique`: every solution has `σ(rad n)` squarefree,
  hence at most one odd prime factor.
The remaining case analysis (`n = 2^a p^b`, which needs lifting-the-exponent) and the full
"if and only if" characterisation `c02_iff` are in `Discovery/RadSigmaIff.lean` (DISC-0007).
-/

namespace Discovery.RadSigma

open ArithmeticFunction Finset

/-- Radical: product of the distinct prime factors (`rad 0 = rad 1 = 1`). -/
def rad (n : ℕ) : ℕ := ∏ p ∈ n.primeFactors, p

theorem squarefree_prod_primes (s : Finset ℕ) (hs : ∀ p ∈ s, p.Prime) :
    Squarefree (∏ p ∈ s, p) := by
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
    rw [Finset.prod_insert ha, Nat.squarefree_mul_iff]
    have hpa : a.Prime := hs a (mem_insert_self a s)
    have hs' : ∀ p ∈ s, p.Prime := fun p hp => hs p (mem_insert_of_mem hp)
    refine ⟨Nat.Coprime.prod_right fun p hp => ?_, hpa.prime.squarefree, ih hs'⟩
    exact (Nat.coprime_primes hpa (hs' p hp)).2 (fun h => ha (h ▸ hp))

theorem squarefree_rad (n : ℕ) : Squarefree (rad n) :=
  squarefree_prod_primes _ fun _ hp => Nat.prime_of_mem_primeFactors hp

theorem rad_of_squarefree {n : ℕ} (h : Squarefree n) : rad n = n :=
  Nat.prod_primeFactors_of_squarefree h

/-- C02b: if `n` and `σ n` are both squarefree (A065301), then `rad(σ n) = σ(rad n)`. -/
theorem c02b (n : ℕ) (hn : Squarefree n) (hs : Squarefree (σ 1 n)) :
    rad (σ 1 n) = σ 1 (rad n) := by
  rw [rad_of_squarefree hn, rad_of_squarefree hs]

/-- C02, squarefree `n`: if `n` is squarefree and `rad(σ n) = σ(rad n)`, then `σ n` is
squarefree, i.e. `n` is in the first alternative of C02. -/
theorem c02_of_squarefree (n : ℕ) (hn : Squarefree n) (h : rad (σ 1 n) = σ 1 (rad n)) :
    Squarefree (σ 1 n) := by
  rw [rad_of_squarefree hn] at h
  rw [← h]
  exact squarefree_rad _

/-- Necessary condition: any solution has `σ(rad n)` squarefree. -/
theorem squarefree_sigma_rad (n : ℕ) (h : rad (σ 1 n) = σ 1 (rad n)) :
    Squarefree (σ 1 (rad n)) := h ▸ squarefree_rad _

/-- From `σ(rad n)` squarefree: `n` has at most one odd prime factor
(two odd primes `p ≠ q` would give `4 ∣ (p+1)(q+1) ∣ σ(rad n)`). -/
theorem odd_prime_factor_unique (n : ℕ) (h : Squarefree (σ 1 (rad n))) :
    ∀ p ∈ n.primeFactors, ∀ q ∈ n.primeFactors, Odd p → Odd q → p = q := by
  intro p hp q hq hpo hqo
  by_contra hne
  have hpr : p.Prime := Nat.prime_of_mem_primeFactors hp
  have hqr : q.Prime := Nat.prime_of_mem_primeFactors hq
  have hσ : σ 1 (rad n) = ∏ r ∈ n.primeFactors, σ 1 r :=
    isMultiplicative_sigma.map_prod_of_subset_primeFactors n _ subset_rfl
  have hsub : ({p, q} : Finset ℕ) ⊆ n.primeFactors := by
    intro x hx
    rw [mem_insert, mem_singleton] at hx
    rcases hx with rfl | rfl
    · exact hp
    · exact hq
  have hdvd : σ 1 p * σ 1 q ∣ σ 1 (rad n) := by
    rw [hσ, ← prod_pair (f := fun r => σ 1 r) hne]
    exact prod_dvd_prod_of_subset _ _ _ hsub
  have hsp : σ 1 p = p + 1 := by
    have := sigma_one_apply_prime_pow (i := 1) hpr
    simpa [Finset.sum_range_succ, add_comm] using this
  have hsq : σ 1 q = q + 1 := by
    have := sigma_one_apply_prime_pow (i := 1) hqr
    simpa [Finset.sum_range_succ, add_comm] using this
  rw [hsp, hsq] at hdvd
  have h2p : 2 ∣ p + 1 := (hpo.add_one).two_dvd
  have h2q : 2 ∣ q + 1 := (hqo.add_one).two_dvd
  have h4 : 2 * 2 ∣ σ 1 (rad n) := (mul_dvd_mul h2p h2q).trans hdvd
  have := h 2 h4
  exact absurd (Nat.isUnit_iff.1 this) (by norm_num)

end Discovery.RadSigma
