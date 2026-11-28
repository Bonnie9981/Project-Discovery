# Compositions: left-to-right maxima, largest parts and longest runs

Chi Hsia, 2026-11-28. (Prepared with the help of an AI assistant (Claude); to be checked by the author before any OEIS submission.)

A composition of n is an ordered list of positive integers with sum n; there are 2^(n-1) of them for n >= 1. A left-to-right maximum (record) is a part larger than every part before it; the first part is always one.

- A102712(n): sum of the largest parts of all compositions of n (n >= 1; we put A102712(0) = 0).
- A336482(n): total number of left-to-right maxima in all compositions of n.
- A119706(n): total length of the longest runs of 1's in all binary words of length n.

## Theorem 1. A336482(n) = A102712(n) - A102712(n-1) for n >= 1.

Fix j >= 1. A composition has a record equal to j exactly when its first part that is >= j equals j. So

  A336482(n) = sum_{j>=1} B_j(n),  B_j(n) = #{c |= n : the first part >= j equals j},
  A102712(n) = sum_{j>=1} A_j(n),  A_j(n) = #{c |= n : max(c) >= j},

the second because max(c) = #{j >= 1 : max(c) >= j}. It suffices to show B_j(n) = A_j(n) - A_j(n-1) for every j and n >= 1.

Let N_j(x) = sum_n #{c |= n : all parts < j} x^n (the empty composition counts for n = 0), so N_j(x) = 1/(1 - x - x^2 - ... - x^(j-1)) and hence (1 - 2x + x^j) N_j(x) = 1 - x. The g.f. of all compositions, with the empty one, is K(x) = (1-x)/(1-2x).

- A composition counted by B_j(n) is u, j, v with u having all parts < j (possibly empty) and v any composition (possibly empty). So sum_n B_j(n) x^n = N_j(x) x^j K(x).
- sum_n A_j(n) x^n = K(x) - N_j(x), and multiplying by (1 - x) gives the g.f. of A_j(n) - A_j(n-1).

Now (1-x)(K - N_j) = (1-x)^2/(1-2x) - (1-x) N_j, and (1-x)^2/(1-2x) = (1-x) K = (1 - 2x + x^j) N_j K = (1-2x) N_j K + x^j N_j K = (1-x) N_j + x^j N_j K, using (1-2x)K = 1-x. Hence (1-x)(K - N_j) = x^j N_j K, which is the claim. QED

(Equivalently, the g.f. of A336482 is (1-x) times Vladeta Jovovic's g.f. of A102712, (1-x)/(1-2x) * Sum_{i>=1} x^i/(1-2x+x^i); summing x^j N_j K over j gives the same expression, since N_j = (1-x)/(1-2x+x^j).)

## Theorem 2 (R. J. Mathar's conjecture in A119706). A119706(n) = A102712(n+1) - 2^n for n >= 1.

Write a binary word w = w_1...w_n and read the composition of n+1 obtained from 1+1+...+1 (n+1 ones) by joining the i-th and (i+1)-th ones when w_i = 1. This is a bijection between binary words of length n and compositions of n+1, and a maximal run of k consecutive 1's in w becomes a part k+1; every part arises this way (a part 1 from a run of length 0). So max part = (longest run of 1's) + 1, and summing over the 2^n words gives A102712(n+1) = A119706(n) + 2^n. QED

(The identity also follows in one step by subtracting the g.f. of A119706 given by Félix Balado (2025) in that entry from the g.f. of A102712; the bijection above is the classical one between binary words and compositions.)

## Checks

`results/A336482/code/check_a336482.py`: brute force over all compositions and binary words for n <= 18 (Theorems 1, 2 and the refinement B_j = A_j(n) - A_j(n-1) for every j), a dynamic program from the decomposition above (not independent of the proof) for n < 80, and all terms stored in the three OEIS entries.
