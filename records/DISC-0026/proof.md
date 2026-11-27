# DISC-0026 證明（反例驗證）

## 反例

k = 2^87 + 2^49 = 2^49 · (2^38 + 1) = 154742504911235484315811840。
- 二進位：只有第 49、87 位（從 0 算）是 1，所以二進位指標是 {50, 88}。
- 2^38 + 1 = 274877906945 = 5 · 229 · 457 · 525313，所以 229 | k、457 | k。
- 229 是第 50 個質數，457 是第 88 個質數。
因此 k 的二進位指標 {50, 88} 都是質數指標，k ≠ 4100，A372430 的猜想不成立。

最小性：`experiment.md` 的 DFS 窮舉所有 k < 2^120，只有 4100 和 k；k < 2^88，所以 k 是第二小的這種數。最小性只靠電腦窮舉，沒有形式化。

## 定理對照（`lean/Discovery/A372430Counter.lean`）

| Lean 定理 | 內容 |
|---|---|
| `Discovery.A372430Counter.isPrimeB_iff` | 試除法 `isPrimeB` 等價於一般的質數定義 |
| `Discovery.A372430Counter.k_value` | k = 154742504911235484315811840 |
| `Discovery.A372430Counter.prime_229` | 229 是質數 |
| `Discovery.A372430Counter.prime_457` | 457 是質數 |
| `Discovery.A372430Counter.count_229` | 229 以下有 49 個質數（229 是第 50 個） |
| `Discovery.A372430Counter.count_457` | 457 以下有 87 個質數（457 是第 88 個） |
| `Discovery.A372430Counter.k_bits` | 第 i 位（i < 88）是 1 ⇔ i = 49 或 87 |
| `Discovery.A372430Counter.k_lt` | k < 2^88 |
| `Discovery.A372430Counter.dvd_229` | 229 \| k |
| `Discovery.A372430Counter.dvd_457` | 457 \| k |
| `Discovery.A372430Counter.a372430_counterexample` | 以上合起來：k ≠ 4100 且每個二進位指標都是質數指標 |

## 編譯結果

本機沒有 Lean 工具鏈，靠 GitHub Actions 的 lean CI：編譯通過，公理只有 propext、Quot.sound（kernel 直接算，沒有 native_decide）。

## 敘述差異

- 「第 j 個質數」用「j−1 個質數比它小、它本身是質數」表示（`primesBelow`、`isPrimeB`，已證與一般定義等價）。
- 位元用 core 的 `Nat.testBit`（第 i 位對應二進位指標 i+1）。
- 最小性（2^120 以內只有兩個）與 A219433 的延伸驗證都只有電腦搜尋，沒有形式化。
