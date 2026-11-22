# DISC-0009 證明：A334504(2n+2) = A268754(n)

## 敘述

記號同 DISC-0008：w 格環，狀態是自然數 x < 2^w，第 i 位元是第 i 格；左鄰 i−1、右鄰 i+1（mod w）；種子 x₀ = 1。規則 26 的 1 鄰域是 100、011、001。
導線（零邊界規則 90）：n 格，狀態 y < 2^n，`nstep n y = ((y <<< 1) ^^^ (y >>> 1)) &&& (2^n − 1)`，種子 y₀ = 1（左端）。這就是 A268754 Python 程式的更新式。

**定理。** w = 2m，m ≥ 2，n = m − 1。對所有 t ≥ 0，x_{t+1} = E(y_t)，其中嵌入 E(y) 的第 0 格、第 m 格為 0，第 i 格（0 < i < m）= y 的第 i−1 位，第 i 格（m < i < 2m）= y 的第 2m−1−i 位。所以 x_{s+1} = x_{t+1} ⇔ y_s = y_t，且 x_{t+1} ≠ x₀；兩條軌道對每個 p「最終以 p 為週期」同時成立或同時不成立，最終週期相同。另外（只有紙上推論，沒有單獨的 Lean 定理）環的暫態 = 導線暫態 + 1。

## 證明

1. **奇偶。** 導線 y_t 的活格都在 j ≡ t (mod 2)：種子在 j = 0；規則 90 的新格 j 是 j−1 和 j+1 的 XOR，兩者同奇偶。（Lean `Discovery.Rule26Even.niter_par`）
2. **一步對一步。** 設 x = E(y)，y 的活格同奇偶。環上沒有相鄰兩個活格：左半相鄰格對應導線相鄰位（奇偶不同），右半同理，第 0、m 格是死的，w 偶所以繞回也沒問題。活的中心格左鄰必死，所以鄰域 110 不出現，規則 26 在這裡等於規則 90：新值 = 左 XOR 右（`Discovery.Rule26Even.rule26_xor`）。逐格核對：
   - 第 0 格：左 = 第 2m−1 格 = y₀，右 = 第 1 格 = y₀，XOR = 0。第 m 格：左右都是 y_{m−2}，得 0。
   - 0 < i < m：左 = 第 i−1 格（i = 1 時是死格 0，否則 y_{i−2}），右 = 第 i+1 格（i = m−1 時是死格 m，此時 y_{m−1} 也因 y < 2^{m−1} 為 0，否則 y_i）。XOR 正是 nstep 的第 i−1 位：左移給 y_{i−2}（i−1 ≥ 1 時），右移給 y_i，遮罩保留 i−1 < m−1。
   - m < i < 2m：鏡像，同理（i = 2m−1 時右鄰是第 0 格）。（Lean `Discovery.Rule26Even.step_Z`）
3. **第一步。** x₁ = 規則 26(e₀) 的活格是 1 和 2m−1（鄰域 100 和 001），正是 E(1)（m ≥ 2 所以 1 < m < 2m−1）。歸納得 x_{t+1} = E(y_t)。（`Discovery.Rule26Even.iter_succ_testBit`）
4. **單射與收尾。** E 是單射（左半就讀回 y），x_{t+1} 第 0 格是 0 而 x₀ 的是 1。所以 x_{s+1} = x_{t+1} ⇔ y_s = y_t（`Discovery.Rule26Even.iter_succ_eq_iff`），x_{t+1} ≠ x₀（`Discovery.Rule26Even.iter_succ_ne_one`）。最終週期：環在 t ≥ T+1 有週期 p ⇔ 導線在 t ≥ T 有週期 p（`Discovery.Rule26Even.rule26_even_eventual_period`）。∎

w = 2（n = 0）不在 A334504 猜想範圍（A268754 offset 1），沒有證；數值上 a(2) = 1。

## 定理對照

| 猜想／引理 | Lean 定理 | 檔案 |
|---|---|---|
| 規則 90 更新式（A268754 程式） | `nstep`、`Discovery.Rule26Even.tb_nstep` | `lean/Discovery/Rule26Even.lean` |
| 步驟 1 奇偶 | `Discovery.Rule26Even.niter_par` | 同上 |
| 步驟 2 一步對一步 | `Discovery.Rule26Even.step_Z`、`Discovery.Rule26Even.rule26_xor` | 同上 |
| H1 結構（步驟 3） | `Discovery.Rule26Even.iter_succ_testBit` | 同上 |
| 步驟 4 | `Discovery.Rule26Even.iter_succ_eq_iff`、`Discovery.Rule26Even.iter_succ_ne_one` | 同上 |
| H2 最終週期相同 | `Discovery.Rule26Even.rule26_even_eventual_period` | 同上 |
| H2 最小最終週期相同（OEIS 的定義） | `Discovery.Rule26Even.rule26_even_least_period` | 同上 |
| 暫態差 1 | （沒有單獨的 Lean 定理；由 `iter_succ_eq_iff` 和 `iter_succ_ne_one` 在紙上推出） | — |
| 小例子（w = 8、10） | `Discovery.Rule26Even.check_small`（`decide`） | 同上 |

## 編譯結果

本機 Lean 4.15.0（與 `lean/lean-toolchain` 相同），只用 Lean core，`lean Discovery/Rule26Even.lean` 無錯誤、無警告。`#print axioms`：主定理只用 propext、Classical.choice、Quot.sound；`Discovery.Rule26Even.check_small` 只用 propext。最終以 CI `lean` 工作的公理稽核為準。

## 敘述差異

- 「最終週期」在 Lean 是 `EvPer f p := ∃ T, ∀ t ≥ T, f (t+p) = f t`；OEIS 的最終週期是使它成立的最小 p ≥ 1。定理對每個 p 給出等價，所以最小值相同；critic 建議後加了 `rule26_even_least_period`，直接說「p 是最小正最終週期」兩邊等價。
- 「環的暫態 = 導線暫態 + 1」**沒有單獨的 Lean 定理**，只在紙上由 `iter_succ_eq_iff`（x_{s+1} = x_{t+1} ⇔ y_s = y_t）和 `iter_succ_ne_one`（x₀ 不再出現）推出；數值上 n ≤ 40 由 l02_check 驗證。
- 環的編碼、`step`、`iter` 直接沿用 DISC-0008 的 `Discovery.Rule26`（已審查過和 impl_b 一致）。
- 導線寬度 n = m − 1，種子 1 = 左端；A268754 程式也是從 1 開始。A268754(n) 的 n 對應 m = n + 1、w = 2n + 2。

## 數值檢查

`python research/r003/l02_check.py 40`：見 experiment.md。
