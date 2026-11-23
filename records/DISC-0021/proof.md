# DISC-0021 證明

## 定理對照（`lean/Discovery/A134559Counter.lean`）

| Lean 定理 | 白話 |
|---|---|
| `Discovery.A134559Counter.sumTo_add`、`Discovery.A134559Counter.sumTo_mul` | 長的和可以切成 a 段、每段 c 項來算（只為了讓 kernel 不會遞迴過深；`b` 的定義本身是逐項相加） |
| `Discovery.A134559Counter.sumTo_eq_zero` | 非負項的和是 0，每一項都是 0 |
| `Discovery.A134559Counter.isPrime_of_blocks` | 若 2 ≤ d < p 的因數個數（分段加總）是 0，p 是質數 |
| `Discovery.A134559Counter.dvd_prodTo`、`Discovery.A134559Counter.dvd_prodTo_two` | 乘積的任一項、任兩個不同項的乘積都整除整個乘積 |
| `Discovery.A134559Counter.prime_4933`、`Discovery.A134559Counter.prime_2467` | 4933、2467 是質數 |
| `Discovery.A134559Counter.b_0`、`Discovery.A134559Counter.b_134` | b_4934(0) = 7404，b_4934(134) = 14802 |
| `Discovery.A134559Counter.dvd_P` | 4934 整除 P(4934)（因為 7404·14802 = 4934·22212，且兩者是乘積中不同的兩項） |
| `Discovery.A134559Counter.a134559_counterexample` | 4933 與 (4933+1)/2 都是質數，但 gcd(P(4934), 4934) = 4934 ≠ 2 |

## 編譯結果

只用 core（沒有 Mathlib、沒有 `native_decide`）。第一版用 `decide` 直接算 4935 項的和，kernel stack overflow；改成分段（47 段 × 105 項）後 CI 通過（lean run 45123339086）。

## 敘述差異

- `b n k` 定義為 Σ_{u=0}^{n} [1 ≤ u ∧ n mod u = k]·u，就是條目「n mod u = k、1 ≤ u ≤ n 的 u 之和」。
- `P n` = ∏_{k < (n+1)/2} b n k，(n+1)/2 = ⌈n/2⌉，與條目的 k = 0..ceiling(n/2)−1 一致。
- 條目寫「Consecutive n satisfying two equations … are consecutive elements of A005383 (… save A005383(1)=3 and A005383(2)=5)」，我們讀成「解集合 = A005383 去掉 3、5」。4933 在 A005383 裡卻不是解，所以在 4933 附近，解集合的相鄰兩項不是 A005383 的相鄰兩項（6 ≤ n ≤ 1.5·10^5 範圍內用程式確認，見 experiment.md）。
- 「另一半成立」（解一定在 A005383 裡）是紙上證明（paper/a134559-counterexample.md），n < 36 靠計算，沒有寫進 Lean。
- 「4933 是最小反例」「1.5·10^5 內共 7 個」是計算結果，沒有寫進 Lean。
