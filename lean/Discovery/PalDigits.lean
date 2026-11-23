/-!
# DISC-0024: Jason Earls' 2003 digit conjectures A084189 and A084352 are true

* A084189: minimum digit of the two prime factors of the palindromes in A046376
  (palindromes that are a product of two palindromic primes).
  Conjecture (2003): a(n) is never greater than 3.
* A084352: the same for palindromic brilliant numbers (palindromes p*q, p and q
  primes with the same number of digits).  Same conjecture.

Proof idea.  If every digit of p and q is at least 4, then p and q have leading
digit >= 4, so p*q >= 16 * 10^(a+b-2) and p*q has exactly a + b digits
(a, b = numbers of digits).  When a + b is even, the palindrome p*q has even
length, hence is divisible by 11 (alternating digit sum is 0), so p or q is 11,
whose digits are 1.  For A084352, a = b.  For A084189, p and q are palindromic
primes with digits >= 4; an even-length palindrome is divisible by 11, so a and
b are odd and a + b is even again.

Numbers are given by their little-endian digit lists; `val` reads a list.
A standard representation has most significant (last) digit >= 1.
Only core Lean is used (no Mathlib, no `native_decide`).
-/

namespace Discovery.PalDigits

/-- Value of a little-endian decimal digit list. -/
def val : List Nat → Nat
  | [] => 0
  | d :: ds => d + 10 * val ds

/-- Alternating digit sum d0 - d1 + d2 - ... -/
def alt : List Nat → Int
  | [] => 0
  | d :: ds => (d : Int) - alt ds

def IsPrime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d ∣ p → d = 1 ∨ d = p

theorem val_sub_alt (l : List Nat) : ∃ k : Int, (val l : Int) - alt l = 11 * k := by
  induction l with
  | nil => exact ⟨0, by simp [val, alt]⟩
  | cons d ds ih =>
    obtain ⟨k, hk⟩ := ih
    refine ⟨(val ds : Int) - k, ?_⟩
    simp only [val, alt]
    omega

theorem alt_append_single (l : List Nat) (d : Nat) :
    alt (l ++ [d]) = alt l + (if l.length % 2 = 0 then (d : Int) else -(d : Int)) := by
  induction l with
  | nil => simp [alt]
  | cons x l ih =>
    simp only [List.cons_append, alt, List.length_cons, ih]
    by_cases h : l.length % 2 = 0
    · have h' : ¬ (l.length + 1) % 2 = 0 := by omega
      simp only [h, h', if_true, if_false]
      omega
    · have h' : (l.length + 1) % 2 = 0 := by omega
      simp only [h, h', if_true, if_false]
      omega

theorem alt_reverse (l : List Nat) :
    alt l.reverse = (if l.length % 2 = 1 then alt l else - alt l) := by
  induction l with
  | nil => simp [alt]
  | cons x l ih =>
    rw [List.reverse_cons, alt_append_single, ih, List.length_reverse]
    simp only [alt, List.length_cons]
    by_cases h : l.length % 2 = 0
    · have h1 : ¬ l.length % 2 = 1 := by omega
      have h2 : (l.length + 1) % 2 = 1 := by omega
      simp only [h, h1, h2, if_true, if_false]
      omega
    · have h1 : l.length % 2 = 1 := by omega
      have h2 : ¬ (l.length + 1) % 2 = 1 := by omega
      simp only [h, h1, h2, if_true, if_false]
      omega

/-- An even-length palindrome is divisible by 11. -/
theorem pal_even_dvd11 (l : List Nat) (hp : l.reverse = l) (he : l.length % 2 = 0) :
    11 ∣ val l := by
  have h1 := alt_reverse l
  have h2 : ¬ l.length % 2 = 1 := by omega
  rw [hp] at h1
  simp only [h2, if_false] at h1
  obtain ⟨k, hk⟩ := val_sub_alt l
  have h0 : alt l = 0 := by omega
  rw [h0] at hk
  have hm : val l % 11 = 0 := by omega
  exact Nat.dvd_of_mod_eq_zero hm

/-! ## Size bounds -/

theorem val_lt (l : List Nat) (h : ∀ d ∈ l, d < 10) : val l < 10 ^ l.length := by
  induction l with
  | nil => simp [val]
  | cons d ds ih =>
    have hd : d < 10 := h d (List.mem_cons_self d ds)
    have ih' := ih (fun e he => h e (List.mem_cons_of_mem d he))
    simp only [val, List.length_cons, Nat.pow_succ]
    omega

theorem val_ge_aux (l : List Nat) (h : ∀ d ∈ l, 4 ≤ d) : 4 * 10 ^ l.length ≤ 10 * val l + 4 := by
  induction l with
  | nil => simp [val]
  | cons d ds ih =>
    have hd : 4 ≤ d := h d (List.mem_cons_self d ds)
    have ih' := ih (fun e he => h e (List.mem_cons_of_mem d he))
    simp only [val, List.length_cons, Nat.pow_succ]
    omega

/-- A nonempty list with all digits >= 4 has value >= 4 * 10^(length - 1). -/
theorem val_ge (d : Nat) (t : List Nat) (h : ∀ e ∈ d :: t, 4 ≤ e) :
    4 * 10 ^ t.length ≤ val (d :: t) := by
  have hd : 4 ≤ d := h d (List.mem_cons_self d t)
  have ht := val_ge_aux t (fun e he => h e (List.mem_cons_of_mem d he))
  simp only [val]
  omega

theorem val_append_single (l : List Nat) (d : Nat) :
    val (l ++ [d]) = val l + d * 10 ^ l.length := by
  induction l with
  | nil => simp [val]
  | cons x l ih =>
    simp only [List.cons_append, val, ih, List.length_cons, Nat.pow_succ]
    rw [← Nat.mul_assoc d]
    omega

/-- A list whose most significant digit is >= 1 has value >= 10^(length - 1). -/
theorem val_ge_lead (t : List Nat) (d : Nat) (hd : 1 ≤ d) :
    10 ^ t.length ≤ val (t ++ [d]) := by
  rw [val_append_single]
  have := Nat.mul_le_mul_right (10 ^ t.length) hd
  rw [Nat.one_mul] at this
  omega

theorem pow10_pos (n : Nat) : 1 ≤ 10 ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [Nat.pow_succ]; omega

/-- 11 is not the value of a nonempty list whose digits are all >= 4 and < 10. -/
theorem val_ne_11 (d : Nat) (t : List Nat) (h4 : ∀ e ∈ d :: t, 4 ≤ e)
    (h10 : ∀ e ∈ d :: t, e < 10) : val (d :: t) ≠ 11 := by
  intro h
  have hge := val_ge d t h4
  have hlt := val_lt (d :: t) h10
  cases t with
  | nil =>
    have hd := h10 d (List.mem_cons_self d [])
    simp only [val] at h
    omega
  | cons e t' =>
    simp only [List.length_cons, Nat.pow_succ] at hge
    have := pow10_pos t'.length
    omega

theorem prime_of_dvd11 (p : Nat) (hp : IsPrime p) (h : 11 ∣ p) : p = 11 := by
  rcases hp.2 11 h with h1 | h1
  · omega
  · exact h1.symm

theorem dvd11_mul (p q : Nat) (h : 11 ∣ p * q) : 11 ∣ p ∨ 11 ∣ q := by
  have hm : (p % 11) * (q % 11) % 11 = 0 := by
    rw [← Nat.mul_mod]
    obtain ⟨c, hc⟩ := h
    rw [hc]
    exact Nat.mul_mod_right 11 c
  have key : ∀ a, a < 11 → ∀ b, b < 11 → a * b % 11 = 0 → a = 0 ∨ b = 0 := by decide
  rcases key (p % 11) (Nat.mod_lt _ (by omega)) (q % 11) (Nat.mod_lt _ (by omega)) hm with h1 | h1
  · exact Or.inl (Nat.dvd_of_mod_eq_zero h1)
  · exact Or.inr (Nat.dvd_of_mod_eq_zero h1)

/-! ## Main theorem -/

/-- If p and q are primes all of whose digits are >= 4 and p*q is a palindrome
(written without leading zeros), then p and q together have an odd number of digits. -/
theorem main (ds es fs : List Nat) (hds : ds ≠ []) (hes : es ≠ [])
    (hd4 : ∀ e ∈ ds, 4 ≤ e) (hd10 : ∀ e ∈ ds, e < 10)
    (he4 : ∀ e ∈ es, 4 ≤ e) (he10 : ∀ e ∈ es, e < 10)
    (hp : IsPrime (val ds)) (hq : IsPrime (val es))
    (hf10 : ∀ e ∈ fs, e < 10) (hlead : ∃ t d, fs = t ++ [d] ∧ 1 ≤ d)
    (hpal : fs.reverse = fs) (hN : val fs = val ds * val es) :
    (ds.length + es.length) % 2 = 1 := by
  obtain ⟨d0, A, rfl⟩ : ∃ d0 A, ds = d0 :: A := by
    cases ds with
    | nil => exact absurd rfl hds
    | cons x xs => exact ⟨x, xs, rfl⟩
  obtain ⟨e0, B, rfl⟩ : ∃ e0 B, es = e0 :: B := by
    cases es with
    | nil => exact absurd rfl hes
    | cons x xs => exact ⟨x, xs, rfl⟩
  obtain ⟨t, d, rfl, hd⟩ := hlead
  -- bounds on p and q
  have pge := val_ge d0 A hd4
  have qge := val_ge e0 B he4
  have plt := val_lt _ hd10
  have qlt := val_lt _ he10
  simp only [List.length_cons] at plt qlt ⊢
  -- bounds on N
  have Nge := val_ge_lead t d hd
  have Nlt := val_lt _ hf10
  simp only [List.length_append, List.length_cons, List.length_nil, Nat.zero_add] at Nlt
  -- p*q between 10^(|A|+|B|+1) and 10^(|A|+|B|+2)
  have lo : 10 ^ (A.length + B.length + 1) ≤ val (d0 :: A) * val (e0 :: B) := by
    have h := Nat.mul_le_mul pge qge
    have e1 : 4 * 10 ^ A.length * (4 * 10 ^ B.length)
        = 16 * 10 ^ (A.length + B.length) := by
      rw [Nat.pow_add, Nat.mul_mul_mul_comm]
    rw [Nat.pow_succ]
    omega
  have hi : val (d0 :: A) * val (e0 :: B) < 10 ^ (A.length + 1 + (B.length + 1)) := by
    have h := Nat.mul_le_mul (Nat.succ_le_of_lt plt) (Nat.succ_le_of_lt qlt)
    rw [← Nat.pow_add] at h
    have e2 : (val (d0 :: A) + 1) * (val (e0 :: B) + 1)
        = val (d0 :: A) * val (e0 :: B) + val (d0 :: A) + val (e0 :: B) + 1 := by
      rw [Nat.add_mul, Nat.mul_add, Nat.one_mul, Nat.mul_one]; omega
    omega
  -- so fs has exactly |A| + |B| + 2 digits
  have hlen : t.length + 1 = A.length + 1 + (B.length + 1) := by
    rcases Nat.lt_or_ge (t.length + 1) (A.length + 1 + (B.length + 1)) with h | h
    · exfalso
      have : 10 ^ (t.length + 1) ≤ 10 ^ (A.length + B.length + 1) :=
        Nat.pow_le_pow_right (by omega) (by omega)
      omega
    · rcases Nat.lt_or_ge (A.length + 1 + (B.length + 1)) (t.length + 1) with h' | h'
      · exfalso
        have : 10 ^ (A.length + 1 + (B.length + 1)) ≤ 10 ^ t.length :=
          Nat.pow_le_pow_right (by omega) (by omega)
        omega
      · omega
  -- if the total length were even, 11 | p*q
  refine (Nat.mod_two_eq_zero_or_one _).resolve_left ?_
  intro hev
  have heven : (t ++ [d]).length % 2 = 0 := by
    simp only [List.length_append, List.length_cons, List.length_nil, Nat.zero_add]; omega
  have h11 := pal_even_dvd11 _ hpal heven
  rw [hN] at h11
  rcases dvd11_mul _ _ h11 with h | h
  · exact val_ne_11 d0 A hd4 hd10 (prime_of_dvd11 _ hp h)
  · exact val_ne_11 e0 B he4 he10 (prime_of_dvd11 _ hq h)

/-- A palindromic prime all of whose digits are >= 4 has an odd number of digits. -/
theorem palprime_odd (ds : List Nat) (hds : ds ≠ []) (h4 : ∀ e ∈ ds, 4 ≤ e)
    (h10 : ∀ e ∈ ds, e < 10) (hpal : ds.reverse = ds) (hp : IsPrime (val ds)) :
    ds.length % 2 = 1 := by
  obtain ⟨d0, A, rfl⟩ : ∃ d0 A, ds = d0 :: A := by
    cases ds with
    | nil => exact absurd rfl hds
    | cons x xs => exact ⟨x, xs, rfl⟩
  refine (Nat.mod_two_eq_zero_or_one _).resolve_left ?_
  intro h
  have h11 := pal_even_dvd11 _ hpal h
  exact val_ne_11 d0 A h4 h10 (prime_of_dvd11 _ hp h11)

/-- A084189 conjecture: a palindrome p*q with p, q palindromic primes always has
a digit <= 3 in p or q.  Stated as: digits all >= 4 is impossible. -/
theorem a084189 (ds es fs : List Nat) (hds : ds ≠ []) (hes : es ≠ [])
    (hd4 : ∀ e ∈ ds, 4 ≤ e) (hd10 : ∀ e ∈ ds, e < 10)
    (he4 : ∀ e ∈ es, 4 ≤ e) (he10 : ∀ e ∈ es, e < 10)
    (hdp : ds.reverse = ds) (hep : es.reverse = es)
    (hp : IsPrime (val ds)) (hq : IsPrime (val es))
    (hf10 : ∀ e ∈ fs, e < 10) (hlead : ∃ t d, fs = t ++ [d] ∧ 1 ≤ d)
    (hpal : fs.reverse = fs) (hN : val fs = val ds * val es) : False := by
  have h1 := palprime_odd ds hds hd4 hd10 hdp hp
  have h2 := palprime_odd es hes he4 he10 hep hq
  have h3 := main ds es fs hds hes hd4 hd10 he4 he10 hp hq hf10 hlead hpal hN
  omega

/-- A084352 conjecture: a palindromic brilliant number p*q (p, q primes with the
same number of digits) always has a digit <= 3 in p or q. -/
theorem a084352 (ds es fs : List Nat) (hds : ds ≠ []) (hes : es ≠ [])
    (hlen : ds.length = es.length)
    (hd4 : ∀ e ∈ ds, 4 ≤ e) (hd10 : ∀ e ∈ ds, e < 10)
    (he4 : ∀ e ∈ es, 4 ≤ e) (he10 : ∀ e ∈ es, e < 10)
    (hp : IsPrime (val ds)) (hq : IsPrime (val es))
    (hf10 : ∀ e ∈ fs, e < 10) (hlead : ∃ t d, fs = t ++ [d] ∧ 1 ≤ d)
    (hpal : fs.reverse = fs) (hN : val fs = val ds * val es) : False := by
  have h3 := main ds es fs hds hes hd4 hd10 he4 he10 hp hq hf10 hlead hpal hN
  omega

/-! Sanity checks on the definitions. -/
example : val [1, 3, 1] = 131 := by decide
example : val [3, 4, 4, 3] = 3443 ∧ 3443 % 11 = 0 := by decide

end Discovery.PalDigits
