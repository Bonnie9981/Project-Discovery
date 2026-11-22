# DISC-0011 證明：規則 54，w ≡ 2, 3 (mod 4) 時暫態 T、週期 4

## 敘述

記號同 `Discovery.Rule54`：w 格環，狀態是自然數 x < 2^w，第 i 位元是第 i 格；左鄰 i − 1、右鄰 i + 1（mod w）；x₀ = 1；規則 54 是 新 = 中 XOR（左 OR 右）。E、`ee_table` 沿用 DISC-0010（`Discovery.Rule54Mod4`）。d(i) = min(i, w − i)，m = ⌊w/2⌋。

**定理。** w ≡ 2 (mod 4)、w ≥ 6，T = (w − 6)/2；或 w ≡ 3 (mod 4)、w ≥ 7，T = (w − 7)/2。則 x_{μ+4} = x_μ ⇔ μ ≥ T，而且 x_{T+p} ≠ x_T（p = 1, 2, 3）。

兩種情形共同的只有：m = T + 3，T 是偶數，w ≥ 6。主證明 `rule54_core` 只用這三個前提。

## 證明

1. **對折。** 定義線段 0..m 上的鄰居：lo(d) = 1（d = 0）否則 d − 1；up(d) = d + 1（d < m），d = m 時 w 偶取 m − 1、w 奇取 m（另一個中心格）。對每個 i < w，第 i 格的兩個環上鄰居的 d 值恰好是 {lo(d(i)), up(d(i))}（`fold`，展開 if 後 `omega`）。所以只要狀態是 d 的函數 f，走一步後就是 g(d) = f(d) XOR (f(lo d) OR f(up d))（`fold_step`）。以下全部在線段上算。
2. **ether 在線段上自己走一步。** E(t+1, d) = E(t, d) XOR (E(t, lo d) OR E(t, d+1))。d ≥ 1 是 DISC-0010 的 `E_step`；d = 0 時要 E(t, 1) = E(t, 3)，也就是 ether 對 0 左右對稱，四種 t mod 4 用 `decide`（`ee_sym`、`E_step_lo`）。
3. **對折光錐（H1）。** t + 3 ≤ m 時第 i 格 = [d(i) ≤ t] 且 E(t, d(i))。對 t 歸納，t + 4 ≤ m 時從 t 推到 t + 1（此時 d ≤ t + 1 的格子都碰不到中心）。分四類：d < t（第 2 步）；d = t（右緣，DISC-0010 的 `E_in_right`；t = 0 直接算）；d = t + 1（只有下鄰活，`E_edge_right`）；更遠（全死）。（`cone_seg`、`iter_cone`）因為 m = T + 3，t = T 在範圍內。
4. **在 T 接成 ether（k = 0）。** d ≤ T 時兩邊一樣；T < d ≤ m = T + 3 時光錐外是死的，而 T 是偶數，E(T, d) 只在 d ≡ T 活，T + 1, T + 2, T + 3 都不是。（`E_dead_even`、`cone_eq_defect`）
5. **之後是 ether 加中心缺陷（H2）。** 定義 D_k(d) = E(T + k, d) 且非（d = m 且 k ≡ 1 mod 4）。證明 D_{k+1} = D_k 走一步（`defect_seg`）：
   - d + 1 < m：三格都不是中心，就是第 2 步。
   - d = m − 1 = T + 2：上鄰是中心。
   - d = m：w 偶時兩鄰都是 m − 1；w 奇時鄰居是 m − 1 和另一個中心格 m。
   後兩類的值只和 a = T mod 4（0 或 2）、r = k mod 4 有關，a ∈ {0, 2}、r < 4 的 8 種情形各 3 條等式，`defect_table` 用 `decide`。（`iter_defect`）
6. **週期。** D_4 = D_0（E 對時間週期 4，4 ≡ 0）。週期恰好 4：見證格 b < 4 和 DISC-0010 相同（p = 2 取 b = T mod 4，p = 1, 3 取 b = T mod 4 + 1），而且 b ≠ m（T = 0 時 b ≤ 1 < 3 = m；T ≥ 2 時 m ≥ 5），所以不受缺陷影響，`ee_witness'` 給出矛盾。週期 1 或 2 的軌道也會在 p = 1 或 2 時回到原狀，所以排除 p = 1, 2, 3 就足以說最小週期是 4。
7. **暫態恰好 T。** 若 μ < T（則 T ≥ 2），x_{T+3} = x_{T−1}。第 T + 1 格（d = T + 1 < m）在 T − 1 時位於光錐外，是死的；在 T + 3（k = 3，不是缺陷時刻，也不是中心）是奇數時刻的 ether，活（`ee_odd_live`）。矛盾。∎

## 定理對照

| 猜想／引理 | Lean 定理 | 檔案 |
|---|---|---|
| 第 1 步對折 | `Discovery.Rule54Mod23.fold`、`Discovery.Rule54Mod23.fold_step`、`Discovery.Rule54Mod23.dist_le`、`Discovery.Rule54Mod23.dist_self` | `lean/Discovery/Rule54Mod23.lean` |
| 第 2 步 | `Discovery.Rule54Mod23.ee_sym`、`Discovery.Rule54Mod23.E_step_lo` | 同上 |
| H1 對折光錐（第 3 步） | `Discovery.Rule54Mod23.cone_seg`、`Discovery.Rule54Mod23.iter_cone` | 同上 |
| 第 4 步 | `Discovery.Rule54Mod23.E_dead_even`、`Discovery.Rule54Mod23.cone_eq_defect` | 同上 |
| H2 中心缺陷（第 5 步） | `Discovery.Rule54Mod23.defect_table`、`Discovery.Rule54Mod23.defect_seg`、`Discovery.Rule54Mod23.iter_defect` | 同上 |
| 第 6、7 步與共同主定理 | `Discovery.Rule54Mod23.rule54_core` | 同上 |
| **H3，w ≡ 2** | `Discovery.Rule54Mod23.rule54_mod4_two` | 同上 |
| **H3，w ≡ 3** | `Discovery.Rule54Mod23.rule54_mod4_three` | 同上 |

## 敘述差異

- 主定理的形式和 DISC-0006 的 `rule54_transient_period`、DISC-0010 的 `rule54_mod4_zero` 相同（同一個 `step`、`iter`、`T`），前提換成 `w % 4 = 2 ∧ 6 ≤ w` 或 `w % 4 = 3 ∧ 7 ≤ w`，沒有上界；另外多給出 `T w` 的明確值。
- 「(μ, λ) = (T, 4)」由「x_{μ+4} = x_μ ⇔ μ ≥ T」加上「x_{T+p} ≠ x_T（p = 1, 2, 3）」決定，這個標準等價沒有另外形式化（同 DISC-0010）。
- w = 2, 3, 5 不在範圍內（週期 1，見 experiment.md）。w ≡ 1 (mod 4) 仍然只有 6 ≤ w ≤ 200 的有限核驗。

## 編譯結果

本機 Lean 4.15.0（與 `lean/lean-toolchain` 相同），只用 Lean core，`lean -o` 依序編譯 `Rule26`、`Rule54`、`Rule54Mod4`、`Rule54Mod23`，無錯誤、無警告。`#print axioms` 對 `rule54_mod4_two`、`rule54_mod4_three`：propext、Classical.choice、Quot.sound。最終以 CI `lean` 工作的公理稽核為準。

## 附註

- 這個對折做法其實也涵蓋 w ≡ 0（那時 m = T + 2，缺陷位置不同），但 DISC-0010 已有證明，沒有重做。
- w ≡ 1 (mod 4)（T = w − 3，比其他三類長一倍）不是靜止缺陷，留待下一段。
