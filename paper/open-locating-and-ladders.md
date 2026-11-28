# Counting open-locating-dominating sets in paths and cycles, and locating sets in ladders

Chi Hsia, November 2026. Prepared with the help of an AI assistant (Claude); every numerical statement below was checked by independent computer programs (Section 4).

Notation as in the companion note *Counting locating-dominating sets and identifying codes in paths and cycles* (paper/locating-dominating-paths.md): P_n has vertices 1..n, C_n has vertices 0..n−1 (indices mod n), N(v) is the set of neighbours of v, N[v] = N(v) ∪ {v}.

* S is an **open-locating-dominating (OLD) set** if the sets N(v) ∩ S, over all vertices v, are nonempty and pairwise distinct (Seo and Slater).

A000930 (Narayana's cows: 1, 1, 1, 2, 3, 4, 6, 9, ...; a(n) = a(n−1) + a(n−3), offset 0) and A001609 (1, 1, 4, 5, 6, 10, 15, ...; same recurrence, offset 1) appear below.

## 1. Words with sparse zeros

**Lemma A.** (i) The number of 0/1 words of length m in which any two zeros are at distance at least 3 is A000930(m + 2). (ii) For m ≥ 3, the number of such *cyclic* words (positions 0..m−1, distance measured around the cycle) is A001609(m). (Only m ≥ 3 is used below.)

*Proof.* (i) Let g(m) be the count, g(0) = 1. If the last letter is 1, the rest is any valid word of length m − 1. If it is 0, the two letters before it (those that exist) must be 1 and the rest is any valid word of length m − 3; for m = 1, 2 this gives only "0" and "10". So g(1) = 2, g(2) = 3 and g(m) = g(m−1) + g(m−3) for m ≥ 3. Since A000930(2), A000930(3), A000930(4) = 1, 2, 3 and A000930 has the same recurrence, g(m) = A000930(m + 2).
(ii) For m ≥ 3, glue each zero to the two ones before it (cyclically): such words are exactly the tilings of the labelled m-cycle by tiles 1 and 110. As in the companion note, the number of tilings of a labelled m-cycle with tile lengths L is Sum_{l in L} l · t(m − l), t = path tilings, giving the g.f. (x + 3x^3)/(1 − x − x^3), which is the g.f. of A001609. ∎

## 2. OLD sets of cycles

**Theorem 1.** OLD(C_n) = A001609(n) for odd n ≥ 3, OLD(C_n) = A001609(n/2)^2 for even n ≥ 6, and OLD(C_4) = 0.

*Proof.* For n ≥ 5, two vertices u ≠ v have a common neighbour only if v = u ± 2, and N(u) ∩ N(v) = ∅ otherwise; so S is OLD iff (T) every N(v) = {v − 1, v + 1} meets S, and (D) for every v, S meets N(v) Δ N(v + 2) = {v − 1, v + 3}. (Pairs with disjoint neighbourhoods are separated by (T).)
*Odd n ≥ 5.* Re-index the vertices along steps of 2: u_j = 2j mod n, j = 0..n−1 (a single cycle since n is odd), and let y_j = 1 iff u_j ∈ S. For v = u_j + 1 we have v − 1 = u_j, v + 1 = u_{j+1}, v + 3 = u_{j+2}. So (T) says y_j or y_{j+1} is 1 and (D) says y_j or y_{j+2} is 1, for every j: a cyclic word of length n with zeros at cyclic distance ≥ 3. Lemma A(ii) gives A001609(n). (n = 3: direct check, 4 sets = A001609(3).)
*Even n = 2m ≥ 6.* N(v) lies in the parity class opposite to v. Conditions (T) and (D) for the odd vertices involve only S ∩ (even class) and vice versa. Each class, stepped by 2, is a cycle of length m, and the conditions on it are exactly those of the odd case with n replaced by m. So OLD(C_2m) = A001609(m)^2 = A218439(m). (For m = 3 the conditions "y_j or y_{j+1}" and "y_j or y_{j+2}" coincide and Lemma A(ii) still applies.)
*n = 4.* N(v) = N(v + 2), so no OLD set exists. ∎

## 3. OLD sets of paths

**Theorem 2.** OLD(P_2k) = A000930(k)^2 for k ≥ 1, and OLD(P_{2k+1}) = A000930(k + 3) · A000930(k − 2) for k ≥ 2 (OLD(P_1) = OLD(P_3) = 0). The cases n = 2, 4, 5, 6, 7, where a class has at most 3 vertices and the two forced ends overlap or the forcing argument degenerates, are checked directly (the values 1, 1, 4, 4, 6 agree with the formula); the argument below is for n ≥ 8.

*Proof.* As before, S is OLD iff every N(v) meets S and, for v, v + 2 both in 1..n, S meets N(v) Δ N(v + 2) = {v − 1, v + 3} ∩ {1..n}. Again N(v) lies in the other parity class, so the conditions split into one problem for each class X = {x_1 < x_2 < ... < x_m} (consecutive vertices of one parity), with word y_1..y_m, whose constraints come from the vertices of the other class Y:
- a vertex of Y between x_i and x_{i+1} gives: y_i or y_{i+1} is 1;
- two vertices of Y on both sides of x_i (at x_i − 1 and x_i + 1) give: y_{i−1} or y_{i+1} is 1, where a y outside 1..m counts as 0.
Inside the class this says exactly that any two zeros of y are at distance ≥ 3. At an end of the path the two cases differ. If the extreme vertex (1 or n) belongs to X, nothing more is required there. If it belongs to Y, that vertex has the single neighbour x_1 (or x_m), so y_1 = 1, and the pair formed by it and the next vertex of Y is separated only by x_2 (or x_{m−1}), so y_2 = 1: the two letters nearest that end are forced to be 1, and the rest is free subject to the distance rule (a zero right after the forced "11" is allowed). With one forced end this gives A000930((m − 2) + 2) = A000930(m) words, with two forced ends A000930(m − 2), with none A000930(m + 2), by Lemma A(i).
For n = 2k each class has k vertices and exactly one forced end (vertex 1 is odd, vertex 2k is even), giving A000930(k)^2. For n = 2k + 1 the odd class (k + 1 vertices, both ends of the path) has no forced end, A000930(k + 3); the even class (k vertices) has both ends forced, A000930(k − 2). ∎

## 4. Locating-dominating sets and identifying codes of ladders

The ladder L_n = P_2 × P_n has columns 1..n with two vertices each. Write LD(L_n) and ID(L_n) for the numbers of locating-dominating sets and identifying codes.

**Theorem 3.** Sum_{n≥1} LD(L_n) x^n = x·P(x)/Q(x) with
 P = 3 + 7x^2 + 3x^3 − 5x^4 − 6x^5 + 2x^6 − x^7 + x^8 + 2x^9 − 3x^10 + x^12,
 Q = 1 − 3x − 4x^3 − 7x^4 + 2x^5 + 2x^6 − 3x^7 + x^8 + x^9 − 2x^10 + 3x^11 + x^12 − x^13,
so LD(L_n) = 3, 9, 34, 117, 403, 1396, 4872, 16969, ... satisfies an order-13 linear recurrence for n ≥ 14.

**Theorem 4.** Sum_{n≥1} ID(L_n) x^n = x^2·P(x)/Q(x) with
 P = 5 + 19x + 12x^2 + 3x^3 − 5x^4 − 22x^5 − 10x^6 + 6x^7 + 8x^8,
 Q = 1 − 2x − 2x^2 − 6x^3 − 10x^4 + 4x^5 + x^6 + 6x^7 + 8x^8 + 2x^9 − 8x^10,
so ID(L_n) = 0, 5, 29, 80, 251, 881, 2992, ... satisfies an order-10 recurrence for n ≥ 11.

*Proof (computer-assisted).* Both properties say "S meets every set of a list" (LD: N[v] for every v and (N[u] Δ N[v]) ∪ {u, v} for every pair; ID: N[v] and N[u] Δ N[v]). Pairs at distance ≥ 3 need nothing beyond domination, so every needed set lies within K consecutive columns (K = 5 for LD, 4 for ID). Away from the two ends the sets are translates of a fixed finite list. Process columns left to right keeping, as state, the bits of the last K columns; let V_t be the vector of numbers of partial sets in each state after column t. For t ≥ t_0 (past the left end) V_{t+1} = M V_t for one fixed matrix M, and the count for L_n is a fixed linear function of V_{n−c} for a fixed c (the right-end sets are checked in the last c columns). The program `discovery/newseq/strip.py` computes V_t exactly and verifies the *vector* identity V_{t+r} = Σ c_i V_{t+r−i} for one t ≥ t_0, with the coefficients c_i of Q. Applying M shows the identity for all later t, so the counts satisfy the recurrence for all n beyond a fixed bound (n ≥ 29 for LD, n ≥ 24 for ID). All smaller n were computed exactly (brute force over all 2^(2n) subsets for n ≤ 9, the window DP of discovery/newseq/transfer.py for n ≤ 15, the column DP for 15 ≤ n ≤ 28), and they agree with the g.f., which therefore holds for all n. ∎

## 5. Computer checks

`results/open-locating-cycle/code/check_old.py` (standard library) compares Theorems 1 and 2 with brute force over all subsets for n ≤ 20. `results/ladder-locating/code/check_ladder.py` compares Theorems 3 and 4 with brute force (n ≤ 9), with a second DP (`discovery/newseq/transfer.py`, n ≤ 15) and reruns the certificate of Section 4.
