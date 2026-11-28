# Quadrant marked mesh patterns in 132-avoiding permutations: the coefficient of x

Chi Hsia, 2026-11-28. (Prepared with the help of an AI assistant (Claude); to be checked by the author before any OEIS submission.)

Notation of Kitaev, Remmel and Tiefenbruck (KRT, arXiv:1201.6243). For a permutation sigma = sigma_1...sigma_n, the entry sigma_i matches MMP(0,0,k,0) if at least k entries sigma_j with j < i satisfy sigma_j < sigma_i (at least k points in the third quadrant, south-west of (i, sigma_i)). mmp^(0,0,k,0)(sigma) is the number of such i, and

  Q_{n,132}^(0,0,k,0)(x) = sum over sigma in S_n(132) of x^mmp^(0,0,k,0)(sigma),  Q^(0,0,k,0)(t,x) = sum_{n>=0} Q_{n,132}^(0,0,k,0)(x) t^n.

C_m = binomial(2m,m)/(m+1) and P_k(t) = C_0 + C_1 t + ... + C_{k-1} t^(k-1).

## Theorem. For every k >= 1,

  sum_{n>=0} ( [x^1] Q_{n,132}^(0,0,k,0)(x) ) t^n = t (1 - P_k + t P_k^2) / (1 - t P_k)^3.

For k = 2, 3, 4 this is A212338, A212339, A212341:

- k = 2: t^3 (2 + t) / (1 - t - t^2)^3 (already in A212338).
- k = 3: t^4 (5 + 4t + 4t^2) / ((1 - 2t)^3 (1 + t + t^2)^3), because 1 - t - t^2 - 2t^3 = (1 - 2t)(1 + t + t^2). This is Colin Barker's empirical g.f. in A212339. Expanding (1 - t - t^2 - 2t^3)^3 = 1 - 3t - t^3 + 12t^4 + 3t^5 - t^6 - 18t^7 - 12t^8 - 8t^9 gives Harvey P. Dale's conjectured signature (3, 0, 1, -12, -3, 1, 18, 12, 8); the numerator has degree 6, so with a(n) = 0 for n < 4 the recurrence holds for n >= 7; using only terms with index >= 4 it holds for n >= 13.
- k = 4: t^5 (14 + 14t + 20t^2 + 25t^3) / (1 - t - t^2 - 2t^3 - 5t^4)^3. This is Colin Barker's empirical g.f. in A212341.

## Proof

Decomposition. Let sigma in S_n(132), n >= 1, and let n be at position a+1, so sigma = alpha n beta with |alpha| = a, |beta| = b = n-1-a. Every entry of alpha is larger than every entry of beta: if x in alpha and y in beta had x < y, then x, n, y would form a 132. So alpha is a 132-avoiding permutation of {b+1, ..., n-1} and beta one of {1, ..., b}. Conversely, for any such alpha and beta, alpha n beta avoids 132: n can only play the role of the 3, and then the 1 would lie in alpha and the 2 in beta, which is impossible; an occurrence without n cannot lie in a single block, and if its 1 is in alpha then the 2 (which must exceed the 1) cannot lie in beta, while if its 1 is in beta all later entries are in beta too. Hence sigma <-> (alpha, beta) is a bijection S_n(132) <-> S_a(132) x S_b(132) for each a. (This is the standard decomposition used by KRT.)

Counting south-west points.
- For an entry of alpha, the earlier entries are earlier entries of alpha; the count is the same as inside alpha.
- For n, all a earlier entries are smaller, so n matches iff a >= k.
- For an entry of beta, the entries of alpha and n are earlier but larger; only earlier entries of beta count.

Hence mmp(sigma) = mmp(alpha) + [a >= k] + mmp(beta), and

  Q_n(x) = sum_{a+b=n-1} x^[a>=k] Q_a(x) Q_b(x)   (n >= 1),  Q_0 = 1.

An entry needs at least k earlier entries to match, so Q_a(x) = C_a for a <= k; in particular sum_{a<k} Q_a(x) t^a = P_k(t). With Q = Q^(0,0,k,0)(t,x),

  Q = 1 + t (P_k + x (Q - P_k)) Q.    (*)

(KRT derive their generating function for Q^(0,0,k,0)(t,x) from the same decomposition.) Write Q = F + x G + O(x^2).

- x^0 in (*): F = 1 + t P_k F, so F = 1/(1 - t P_k).
- x^1 in (*): G = t P_k G + t (F - P_k) F, so G = t F (F - P_k)/(1 - t P_k) = t F^2 (F - P_k).

Finally F - P_k = (1 - P_k (1 - t P_k))/(1 - t P_k) = (1 - P_k + t P_k^2)/(1 - t P_k), which gives the theorem. The k = 2, 3, 4 forms follow by multiplying out (they are exact polynomial identities, checked by the script below). QED

Remark. KRT (Section 4) list the x-coefficients for k = 3 as 5, 19, 61, 188, 532, 1387, ...; the fifth term should be 523, as in their own expansion of Q^(0,0,3,0)(t,x) and in A212339. They also write that there does not seem to be a simple way to extract a formula for Q^(0,0,k,0)(t,x)|_x from their closed form; the theorem above does this directly from (*).

## Related known results (for A212344, A212345)

KRT, Theorem 13: the highest power of x in Q_{n,132}^(0,k,0,0)(x) is x^(n-k), with coefficient C_k C_{n-k}; the coefficient of x^(n-k-1) is a_k C_{n-k} with a_1 = 1, a_k = C_k + sum_{i=1}^{k-1} C_{i-1} a_{k-i}. For k = 3: C_3 = 5 and a_3 = 9, so A212344(n) = 5 C_{n-3} (this settles Bala's comment and Mathar's conjectured recurrence in A212344, and the closed form 5*(1-sqrt(1-4*x))/(2*x) up to the offset; Gladkovskii's continued fractions are not checked here) and A212345(n) = 9 C_{n-3}. These are results of KRT, not new.

## Checks

`results/A212339/code/check_a212339.py`: brute force over S_n(132) for n <= 11 (k = 2, 3, 4, and the A212344/A212345 values); the polynomial recursion above for n < 60; exact polynomial cross-multiplication with the three g.f.s and Dale's signature; all terms stored in A212338, A212339, A212341, A212344, A212345.
