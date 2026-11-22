# DISC-0014 證明：A071052 的 a(2n) = a(n) + 2n

## 敘述

規則 150 在整數格上，`step f i = f(i−1) xor f(i) xor f(i+1)`，種子 = 位置 0 為 1。`row n` = 走 n 步。`ones n`、`zeros n` = `row n` 在 −n..n（共 2n+1 格）的 1、0 個數。對所有 n ≥ 0：zeros(2n) = zeros(n) + 2n。

## 證明

1. **兩步。** 展開兩次 xor，f(i±1) 各出現兩次、f(i) 出現三次，抵銷後 step(step f)(i) = f(i−2) xor f(i) xor f(i+2)（`step_step`；就是 GF(2) 上 (x⁻¹+1+x)² = x⁻²+1+x²）。
2. **放大。** dil g：g 放到偶數格、奇數格補 0。由第 1 步，偶數格 2m 得 g(m−1) xor g(m) xor g(m+1)，奇數格三項都是 0，所以 step(step(dil g)) = dil(step g)（`step_step_dil`）。種子放大後不變（`seed_dil`），歸納得 row(2n) = dil(row n)（`row_double`）。
3. **計數。** 視窗 −2n..2n 補上奇數格 2n+1（值 0）變成 4n+2 格，兩兩一組（偶數格 = g 的一格、奇數格 = 0），1 的個數 = g 在 −n..n 的 1 個數（`cnt_dil`），所以 ones(2n) = ones(n)（`ones_double`）。
4. **合起來。** ones + zeros = 視窗長（`ones_add_zeros`）：zeros(2n) = 4n+1 − ones(n) = (2n+1 − ones(n)) + 2n（`a071052_double`）。
5. **附帶。** 光錐：|i| > n 時 row n i = 0（`row_support`），所以視窗 −n..n 就是整個 ON 區，和 A071053「第 n 代 ON 細胞數」同義。

## 定理對照

| 敘述 | Lean 定理 | 檔案 |
|---|---|---|
| 兩步 = 隔兩格的一步 | `Discovery.A071052Even.step_step` | `lean/Discovery/A071052Even.lean` |
| 放大後兩步 = 一步再放大 | `Discovery.A071052Even.step_step_dil` | 同上 |
| row(2n) = dil(row n) | `Discovery.A071052Even.row_double` | 同上 |
| A071053(2n) = A071053(n) | `Discovery.A071052Even.ones_double` | 同上 |
| A071052(2n) = A071052(n) + 2n | `Discovery.A071052Even.a071052_double` | 同上 |
| 光錐 | `Discovery.A071052Even.row_support` | 同上 |

## 編譯結果

Lean 4.15.0，只用 core（無 Mathlib、無 `native_decide`），本機 `lean` 編譯 0 錯誤約 1 秒；`#print axioms a071052_double` = [propext, Quot.sound]。CI（lean.yml）另做全庫公理檢查。

## 敘述差異

- OEIS 用 A071036 三角形第 n 列（2n+1 項）；Lean 用整數格上的函數，取視窗 −n..n，`row_support` 保證視窗外全是 0。
- A071036 的列是否真的是 −n..n 的 2n+1 格：條目 DATA 第 0、1 項 0、0 與 1、3 格的列吻合，實驗比對 67 項 DATA 一致。
- Lean 的 `step` 是條目名稱說的規則 150（xor 三鄰居），與 A071053 COMMENTS「(1+x+x²)^n 的奇數係數」等價；實驗兩種算法都比對過。
