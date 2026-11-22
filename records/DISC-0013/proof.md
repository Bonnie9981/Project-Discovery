# DISC-0013 證明：A268754 的 a(2n+1) = 2a(n)（n ≠ 2^k − 1）

## 敘述

導線同 DISC-0009：n 格，狀態 y < 2^n，`nstep n y = ((y <<< 1) ^^^ (y >>> 1)) &&& (2^n − 1)`，種子 1。對所有 n ≥ 1：
- n + 1 不是 2 的次方：若 p 是 n 格導線的最小正最終週期，則 2p 是 2n+1 格導線的最小正最終週期，即 a(2n+1) = 2a(n)。
- n + 1 = 2^k：兩條導線都死光，a(n) = a(2n+1) = 1。
- 附帶：導線死光 ⇔ n + 1 是 2 的次方（條目 COMMENTS 的敘述）。

## 證明

1. **奇偶。** y_t 的活格都在位元 ≡ t (mod 2)（`Rule26Even.niter_par`，DISC-0009）。
2. **間隔展開。** S(y)：y 的第 i 位搬到第 2i+1 位。長導線（2n+1 格）走兩步：第一步奇數位都變 0，偶數位 2i 變 y_{i−1} xor y_i；第二步偶數位都變 0，奇數位 2i+1 變 (y_{i−1} xor y_i) xor (y_i xor y_{i+1}) = y_{i−1} xor y_{i+1}，正好是短導線一步。右端：2i+1 < 2n+1 ⇔ i < n，位置 2n 讀到的 y_n 在兩邊都出現，不用額外處理。所以「長兩步 = 短一步」（`spr_step`）。種子 1 走一步變第 1 位 = S(1)（`spr_seed`），歸納得 y^(2n+1)_{2t+1} = S(y^(n)_t)（`spr_iter`）。S 是單射（`spr_eq_iff`）。
3. **週期加倍。** 設短導線永不死。若長導線有奇數最終週期 p，取夠大的奇數時刻 s：x_{s+p}（偶數時刻，活格在偶數位）= x_s（奇數時刻，活格在奇數位），兩者只能都是 0，但 x_s = S(y) ≠ 0，矛盾（`evper_odd_width_even`）。所以週期是偶數 2q，而「長導線最終以 2q 為週期 ⇔ 短導線最終以 q 為週期」：奇數時刻由第 2 步，偶數時刻是奇數時刻再走一步（`evper_double_iff`）。最小值因此加倍（`leastPer_double`）。
4. **死亡條件。** n 偶數：`nstep` 的核只有 0（由 nstep y = 0 推出奇數位從低往高全 0、偶數位從 y_n = 0 往下全 0），種子非 0 所以永不死（`ker_even`、`not_dies_even`）。n = 1：一步就死。n = 2r+1、r ≥ 1：由第 2 步，長導線死 ⇔ 短導線死（`dies_odd_iff`）。對 n 強歸納：死 ⇔ n+1 = 2^k（`dies_iff`）。
5. **合起來。** 非例外時用 3＋4（`a268754_odd`）；例外時兩條都死，最終週期 1（`a268754_odd_exception`）。

## 定理對照

| 敘述 | Lean 定理 | 檔案 |
|---|---|---|
| 間隔展開，一步對兩步 | `Discovery.A268754Odd.spr_step` | `lean/Discovery/A268754Odd.lean` |
| 第一步 = 展開的種子 | `Discovery.A268754Odd.spr_seed` | 同上 |
| y^(2n+1)_{2t+1} = S(y^(n)_t) | `Discovery.A268754Odd.spr_iter` | 同上 |
| 偶數寬度不會死 | `Discovery.A268754Odd.ker_even`、`Discovery.A268754Odd.not_dies_even` | 同上 |
| 死亡 ⇔ n+1 = 2^k | `Discovery.A268754Odd.dies_iff` | 同上 |
| 長導線最終週期是偶數 | `Discovery.A268754Odd.evper_odd_width_even` | 同上 |
| 2q ⇔ q | `Discovery.A268754Odd.evper_double_iff` | 同上 |
| a(2n+1) = 2a(n)（非例外） | `Discovery.A268754Odd.a268754_odd` | 同上 |
| a(n) = a(2n+1) = 1（例外） | `Discovery.A268754Odd.a268754_odd_exception` | 同上 |
| 反向：2p = a(2n+1) ⇒ p = a(n)；兩邊最小週期同時存在 | `Discovery.A268754Odd.a268754_odd_iff`、`Discovery.A268754Odd.exists_leastPer_iff` | 同上 |
| 最小週期唯一 | `Discovery.A268754Odd.leastPer_unique` | 同上 |

## 編譯結果

本機 Lean 4.15.0（與 `lean/lean-toolchain` 相同），只用 Lean core：`lean Discovery/A268754Odd.lean`（依賴 Rule26、Rule26Even 的 .olean）無錯誤、無警告，約數秒。CI 的 `AxiomCheck.lean` 會檢查所有定理只用 propext、Classical.choice、Quot.sound。

## 敘述差異

- OEIS 的 a(n) 是最小正最終週期。Lean 用 `LeastPer f p := 0 < p ∧ EvPer f p ∧ ∀ q, 0 < q → q < p → ¬ EvPer f q`，`EvPer` 同 DISC-0009；最小值唯一（`leastPer_unique`），所以「p 是 a(n) ⇒ 2p 是 a(2n+1)」就是 a(2n+1) = 2a(n)。最小週期存在（有限狀態、鴿籠原理）沒有在 Lean 證，OEIS 的定義本身預設了它；critic 建議補。為了不讓主定理只是單向條件句，加了 `a268754_odd_iff`（p 是 a(n) ⇔ 2p 是 a(2n+1)）和 `exists_leastPer_iff`（兩邊的最小週期同時存在或同時不存在），所以只差一般性的鴿籠引理。
- 例外句條目寫「a(n) = 1」，我們證的是 a(n) = a(2n+1) = 1，建議 OEIS 改寫法。
- n = 0 不在範圍（offset 1）。
- 更新式照條目 Python 程式（DISC-0009 已核對）；條目名稱「B1/S 規則中 n×1 長方形振盪子」與這個定義等價沒有另外論證（同 DISC-0009 review 的非阻擋項），數值上 54 項一致。

## 數值檢查

`python research/r003/l06_a268754_odd.py 40 2000`：見 experiment.md。
