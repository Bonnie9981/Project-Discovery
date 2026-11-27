# Counting locating-dominating sets and identifying codes in paths and cycles

Chi Hsia, November 2026. Prepared with the help of an AI assistant (Claude); every numerical statement below was checked by three independent computer programs (see the end).

Throughout, P_n is the path with vertices 1, 2, ..., n (i adjacent to i+1) and C_n is the cycle with vertices 1, ..., n (also n adjacent to 1). For a set S of vertices write w = w_1 w_2 ... w_n for its 0/1 word (w_i = 1 iff i is in S). N(v) is the set of neighbours of v and N[v] = N(v) ∪ {v}.

* S is a **locating-dominating (LD) set** if every vertex v not in S has N(v) ∩ S nonempty, and N(u) ∩ S ≠ N(v) ∩ S for any two different vertices u, v not in S (Slater).
* S is an **identifying code** if N[v] ∩ S is nonempty for every vertex v, and N[u] ∩ S ≠ N[v] ∩ S for any two different vertices u, v (Karpovsky, Chakrabarty, Levitin).

The minimum sizes of these sets in paths and cycles are classical (for example ⌈2n/5⌉ for LD sets of P_n, ⌈(n+1)/2⌉ for identifying codes of P_n, n ≥ 3). Here we count **all** of them.

## 1. Locating-dominating sets of P_n

Let the ones of w be at positions p_1 < ... < p_k. Call g_0 = p_1 − 1 and g_k = n − p_k the *end gaps* and g_i = p_{i+1} − p_i − 1 (0 < i < k) the *inner gaps* (numbers of zeros). Call a gap **long** if it is an inner gap equal to 2 or an end gap equal to 1.

**Lemma 1.** S is an LD set of P_n if and only if (a) k ≥ 1, the end gaps are at most 1 and the inner gaps at most 2; and (b) no two consecutive gaps g_{i−1}, g_i (1 ≤ i ≤ k) are both long.

*Proof.* (a) is exactly "every vertex not in S has a neighbour in S": a 0 in an inner gap of length ≥ 3 (its middle zero) or the zero at the very end of an end gap of length ≥ 2 has no neighbour in S, and if (a) holds every zero touches a one.
Assume (a). In a path two different vertices have at most one common neighbour (this fails in C_4, which is why n = 4 is excluded in Theorem 2). A vertex has at most two neighbours, so if u ≠ v are not in S and N(u) ∩ S = N(v) ∩ S, this common set contains some p ∈ S adjacent to both, so {u, v} = {p − 1, p + 1}, and N(p − 1) ∩ S = N(p + 1) ∩ S = {p}. That means: p − 1 and p + 1 are zeros, and p − 2 is either not a vertex or a zero, and the same for p + 2. On the left of p this says: the gap before p is an end gap equal to 1 (p − 1 = 1), or an inner gap of length ≥ 2, i.e. = 2 by (a). (An end gap ≥ 2 is excluded by (a).) So the gap before p is long; likewise the gap after p. Conversely two long gaps around the one at p make p − 1 and p + 1 indistinguishable. ∎

**Theorem 1.** Let a(n) be the number of LD sets of P_n. Then

  Sum_{n≥1} a(n) x^n = x (1 + 2x + 2x^3 + x^4) / (1 − x − x^2 − x^4 − x^5),

so a(n) = a(n−1) + a(n−2) + a(n−4) + a(n−5) for n ≥ 6, with a(1..5) = 1, 3, 4, 9, 15.

*Proof.* By Lemma 1, w is determined by the gap sequence g_0, g_1, ..., g_k, read as g_0, 1, g_1, 1, ..., 1, g_k. Count with weight x^(length) and track whether the last gap was long (state L) or not (state N). The first gap gives N with weight 1 (g_0 = 0) or L with weight x (g_0 = 1). Each "1 followed by an inner gap" has weight x · (1 + x) into state N (gap 0 or 1) or x · x^2 into state L (gap 2), the latter not allowed from L. The last "1 followed by the end gap" has weight x·(1 + x) from N and x·1 from L. Hence, with s = (1, x), T = [[1+x, x^2], [1+x, 0]], t = (1+x, 1)^T,

  Sum a(n) x^n = x · s (I − xT)^(−1) t,

and a direct 2 × 2 computation gives the stated rational function. ∎

Example: n = 3. The LD sets are {1,2}, {2,3}, {1,3}, {1,2,3}, so a(3) = 4. The set {2} (word 010) is not one: vertices 1 and 3 both see only vertex 2; in Lemma 1 its only one has a long end gap on each side.

The growth rate is the largest root 1.81240... of x^5 − x^4 − x^3 − x − 1.

## 2. Locating-dominating sets of C_n and A001642

**Theorem 2.** For n ≥ 5 the number of LD sets of C_n equals A001642(n), the sequence with g.f. x(1 + 2x + 4x^3 + 5x^4)/(1 − x − x^2 − x^4 − x^5) (also true for n = 3; for n = 4 the count is 9, not 11).

*Proof.* For n ≥ 5 the vertices p − 2, p − 1, p + 1, p + 2 are distinct, and the argument of Lemma 1 applies cyclically: S is an LD set of C_n iff every cyclic gap (zeros after each one, up to the next one) is at most 2 and no two cyclically consecutive gaps are both 2. (A single one is impossible: its gap n − 1 ≥ 4.) Attach to each one the zeros after it: units 1, 10, 100. A 100 is always followed by a 1 or a 10; glue them together. This is a bijection between LD sets of C_n and tilings of the labelled n-cycle by the four tiles 1, 10, 1001, 10010 of lengths 1, 2, 4, 5. For tiles of lengths in a set L, the number of tilings of the labelled n-cycle is c(n) = Sum_{l in L} l · t(n − l), where t(m) = A079976(m) is the number of tilings of a path of length m (t(0) = 1, t(m) = 0 for m < 0): choose the tile covering vertex 1 and which of its l cells is vertex 1; the rest is a path. In g.f. form Sum c(n) x^n = (x + 2x^2 + 4x^4 + 5x^5)/(1 − x − x^2 − x^4 − x^5), which is the g.f. of A001642. ∎

## 3. Identifying codes of P_n

**Lemma 3.** For n ≥ 3, S is an identifying code of P_n iff
 (a) w_j = 1 or w_{j+3} = 1 for 1 ≤ j ≤ n − 3;
 (b) w_3 = w_{n−2} = 1;
 (c) no three consecutive zeros, w_1 or w_2 is 1, and w_{n−1} or w_n is 1.

*Proof.* (c) says every N[v] meets S. If dist(u, v) ≥ 3, N[u] and N[v] are disjoint, so (c) already separates them. For u = i, v = i + 1 the symmetric difference N[i] Δ N[i+1] is {i − 1, i + 2} ∩ {1..n}; requiring it to meet S gives (a) with j = i − 1 for 2 ≤ i ≤ n − 2, and w_3 = 1 (i = 1), w_{n−2} = 1 (i = n − 1). For u = i, v = i + 2, N[i] Δ N[i+2] = {i − 1, i, i + 2, i + 3} ∩ {1..n} contains {i − 1, i + 2} (i ≥ 2) or 3 (i = 1), so it is met once (a) and (b) hold. ∎

**Theorem 3.** Let b(n) be the number of identifying codes of P_n (b(1) = 1, b(2) = 0). Then

  Sum_{n≥1} b(n) x^n = x (1 − x + x^2 + 2x^3 + x^4 − x^5 − x^6) / (1 − x − x^2 + x^3 − x^4 − x^5 + x^7),

i.e. b(n) = b(n−1) + b(n−2) − b(n−3) + b(n−4) + b(n−5) − b(n−7) for n ≥ 8.

*Proof.* By Lemma 3 the conditions only involve windows of four consecutive letters plus the first and last three letters. Let the state be the last three letters (8 states) and M the 8 × 8 0/1 matrix allowing p → q when they overlap in two letters and the 4-letter word satisfies (a) and "no 000". Then b(n) = s M^(n−3) t (n ≥ 3), where s marks the allowed first three letters (w_1 or w_2, w_3 = 1) and t the allowed last three (w_{n−2} = 1, w_{n−1} or w_n). The characteristic polynomial of M is x · (x^7 − x^6 − x^5 + x^4 − x^3 − x^2 + 1) (exact computation), so by Cayley–Hamilton the recurrence holds for n ≥ 11; together with the values b(1..20) (computed by brute force from the definition) it determines the g.f. above, whose expansion agrees with b(1..20). ∎

The growth rate is 1.58133..., the largest root of x^7 − x^6 − x^5 + x^4 − x^3 − x^2 + 1.

## 4. Computer checks

`results/locating-dominating-path/code/check_paths.py` (standard library only) compares, for n ≤ 20, (A) brute force over all 2^n subsets using the definitions, (B) the word rules of Lemmas 1 and 3 and the transfer matrix of Theorem 3, and (C) the recurrences; and A001642 against brute-force LD counts on C_n. A second implementation in `discovery/newseq/` (vectorised brute force for |V| ≤ 20 and a window-DP over the bitmask conditions, up to n = 70) gives the same numbers.
