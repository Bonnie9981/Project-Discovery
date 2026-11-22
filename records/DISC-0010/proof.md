# DISC-0010 證明：規則 54，w ≡ 0 (mod 4) 時暫態 (w − 4)/2、週期 4

## 敘述

記號同 DISC-0006 的 `Discovery.Rule54`：w 格環，狀態是自然數 x < 2^w，第 i 位元是第 i 格；左鄰 i − 1、右鄰 i + 1（mod w）；種子 x₀ = 1；規則 54 是 新 = 中 XOR（左 OR 右）。

ether：E(t, i) = 「i ≡ t (mod 4)」（t 偶數），「i ≢ t + 1 (mod 4)」（t 奇數）。只和 t mod 4、i mod 4 有關；在 w ≡ 0 (mod 4) 的環上，i 和 i ± w 的餘數相同，所以 E 在環上定義得好。

**定理。** w ≡ 0 (mod 4)、w ≥ 4，T = (w − 4)/2。則 x_{μ+4} = x_μ ⇔ μ ≥ T，而且 x_{T+p} ≠ x_T（p = 1, 2, 3）。也就是暫態 T、週期恰好 4。

## 證明

1. **ether 自己走一步。** 對所有 t、i：E(t+1, i) = E(t, i) XOR（E(t, i−1) OR E(t, i+1)）。只和 (t mod 4, i mod 4) 有關，16 種情形逐一代值（Lean `ee_table` 用 `decide`）。
2. **光錐（引理 1）。** 2t + 4 ≤ w 時，x_t 的第 i 格 = [i ≤ t 或 i + t ≥ w] 且 E(t, i)。對 t 歸納（2t + 6 ≤ w 時從 t 推到 t + 1，此時錐外至少 5 格死格，兩側前緣不會碰到）。第 i 格分五類：
   - 錐內、兩鄰也在錐內：就是第 1 步。
   - 右緣 i = t（右鄰在錐外）：要 E(t+1, t) = E(t, t) XOR E(t, t−1)；左緣 i + t = w 對稱。t = 0 時 i = 0 兩鄰都在錐外，直接算 E(1, 0) = 1。
   - 錐外緊鄰：i = t + 1（只有左鄰活）或 i + t + 1 = w（只有右鄰活）。前緣格 E(t, t)、E(t, w − t) 都是 1，新格 E(t+1, t+1)、E(t+1, w−t−1) 也是 1。
   - 更遠：三格都死，新格也死，而且仍在 t + 1 的錐外。
   這些餘數等式都在 `ee_table` 裡一次 `decide`。（`Discovery.Rule54Mod4.cone_step`、`Discovery.Rule54Mod4.iter_cone`）
3. **在 T 合攏成 ether。** t = T = 2m − 2（w = 4m）時錐外剩第 2m − 1、2m、2m + 1 三格，T 是偶數，E(T, i) 只在 i ≡ T 活；這三格的餘數是 T + 1、T + 2、T + 3，本來就是 ether 的死格。所以 x_T 的每一格 = E(T, i)。（`Discovery.Rule54Mod4.iter_T_ether`）
4. **之後一直是 ether。** 由第 1 步和 w ≡ 0（鄰格餘數是 i ± 1），x_{T+k} 的第 i 格 = E(T + k, i)。E 對 t 週期 4，所以 x_{T+4} = x_T。（`Discovery.Rule54Mod4.iter_ether`）
5. **週期恰好 4。** p = 1、3：取第 T + 1 格（T mod 4 + 1），x_T 死、奇數時刻活；p = 2：取第 T mod 4 格，x_T 活、x_{T+2} 死。（`Discovery.Rule54Mod4.ee_witness`）
6. **暫態恰好 T。** 若某 μ < T 有 x_{μ+4} = x_μ，則從 μ 起週期 4，特別是 x_{T+3} = x_{T−1}。但 x_{T−1} 由光錐引理在第 T + 1 = 2m − 1 格是死的（在錐外），x_{T+3} 是奇數時刻的 ether，第 T + 1 格活（`Discovery.Rule54Mod4.ee_odd_live`）。矛盾。w = 4 時 T = 0，不用這步。∎

## 定理對照

| 猜想／引理 | Lean 定理 | 檔案 |
|---|---|---|
| 規則 54 的位元更新式 | `Discovery.Rule54Mod4.step_eq`、`Discovery.Rule54Mod4.tb_step`、`Discovery.Rule54Mod4.step_lt`、`Discovery.Rule54Mod4.iter_lt` | `lean/Discovery/Rule54Mod4.lean` |
| 第 1 步 ether（餘數表） | `Discovery.Rule54Mod4.ee_table`、`Discovery.Rule54Mod4.E_step` | 同上 |
| H1 光錐（第 2 步） | `Discovery.Rule54Mod4.cone_step`、`Discovery.Rule54Mod4.iter_cone` | 同上 |
| 第 3 步 | `Discovery.Rule54Mod4.iter_T_ether`、`Discovery.Rule54Mod4.T_eq` | 同上 |
| H2 ether（第 4 步） | `Discovery.Rule54Mod4.ether_step`、`Discovery.Rule54Mod4.iter_ether` | 同上 |
| 第 5、6 步的餘數事實 | `Discovery.Rule54Mod4.ee_witness`、`Discovery.Rule54Mod4.ee_odd_live` | 同上 |
| **H3 主定理** | `Discovery.Rule54Mod4.rule54_mod4_zero` | 同上 |

## 編譯結果

本機 Lean 4.15.0（與 `lean/lean-toolchain` 相同），只用 Lean core，`lean Discovery/Rule54Mod4.lean`（先編譯 `Rule26`、`Rule54`）無錯誤、無警告。`#print axioms Discovery.Rule54Mod4.rule54_mod4_zero`：propext、Classical.choice、Quot.sound。最終以 CI `lean` 工作的公理稽核為準。

## 敘述差異

- 主定理的形式和 DISC-0006 的 `rule54_transient_period` 完全相同（同一個 `step`、`iter`、`T`），差別是前提從 `6 ≤ w ≤ 200` 換成 `w % 4 = 0 ∧ 4 ≤ w`，沒有上界。
- 「x_μ 在循環上 ⇔ x_{μ+4} = x_μ」這個標準等價和 DISC-0006 一樣沒有另外形式化（週期 4 的循環上這是定義）。
- 只證了 w ≡ 0 (mod 4)。w ≡ 2, 3（靜止缺陷）和 w ≡ 1（兩道相位牆碰撞）仍然只有 6 ≤ w ≤ 200 的有限核驗。
- `step` 的位元引理借用 `Discovery.Rule26` 的旋轉引理（`rotL`、`rotR` 和 `Rule54.step` 裡的兩個旋轉逐字相同，`step_eq` 用 `rfl` 證明）。

## 數值檢查

`python research/r003/l03_rule54_mod4.py 1200`：見 experiment.md。
