# DISC-0012 證明：規則 54，w ≡ 1 (mod 4) 時暫態 w − 3、週期 4

## 敘述

記號同 `Discovery.Rule54`；E、`ee`、對折（d(i)、lo、up、`fold_step`）沿用 DISC-0010、DISC-0011。w = 2m + 1，m 偶數。

**定理。** w ≡ 1 (mod 4)、w ≥ 9。則 x_{μ+4} = x_μ ⇔ μ ≥ w − 3，而且 x_{w−3+p} ≠ x_{w−3}（p = 1, 2, 3）。

## 證明

1. **對折光錐延長一步。** DISC-0011 的 `cone_seg` 前提原本寫 t + 4 ≤ m，其實 t + 3 ≤ m 就夠（各情形用到的只是 d ≤ t + 1 < m）；`iter_cone` 因此對 t + 2 ≤ m 成立。本 PR 把這兩個前提放寬（結論不變，舊的呼叫照樣成立；數值上 `cone_seg` 在 t + 2 ≤ m 也成立，t + 3 只是夠用、不是最緊）。所以 t = m − 2 時第 i 格 = [d ≤ m − 2] 且 E(m − 2, d)。
2. **在 m − 2 線段全是 ether。** m − 2 是偶數，E(m − 2, ·) 只在 d ≡ m − 2 活；m − 1、m 不是，所以光錐外兩格本來就是 E 的空白（`cone_eq_G`）。
3. **描述 G。** 對 t ≥ m − 2、0 ≤ d ≤ m 定義：d + t < w 時 G = E(t, d)；否則 G = N(t, d) XOR f，N(t, d) = E(t + 1, d + 3)，f =（d = 0 且 t ≡ 2）或（d = m 且 t ≡ m (mod 4)）。Lean 裡把 G 寫成「區域（牆前／牆後）、t mod 4、d mod 4、缺陷旗標」的函數（`val`、`eN`、`fl`、`G`）。
4. **G 走一步還是 G（`G_step`）。** 要證 G(t + 1, d) = G(t, d) XOR (G(t, lo d) OR G(t, up d))。分四種位置：
   - d = 0（兩鄰都是 1；`G_step_zero`）：再分 t + 1 < w、t + 1 = w、t ≥ w。
   - 0 < d < m − 1（`G_step_inner`）：分 d + t + 1 < w（全在牆前）、= w（自己下一步過牆）、d + t = w（自己剛過牆，下鄰還在牆前）、> w（全在牆後）；d = 1 另外處理（下鄰 0 可能有缺陷）。
   - d = m − 1（上鄰是中心，可能有缺陷；`G_step_near`）：同上四種。
   - d = m（w 奇，上鄰是自己；`G_step_centre`）：牆前只可能 t = m − 2、m − 1；以及剛過牆、牆後。
   每個情形先用 `omega` 把「在牆前還是牆後」「是否為 0 或 m」化成 true／false，剩下只和 t mod 4、d mod 4（以及牆所在處 d + t mod 4 的限制）有關，16 種組合逐一計算（`fin4`／`fint`：不可能的組合用 `omega` 排除，其餘 `decide`）。
5. **歸納。** 從 m − 2 出發，用 `fold_step` 和第 4 步對 k 歸納：時刻 m − 2 + k 的第 i 格 = G(m − 2 + k, d(i))（`iter_G`）。
6. **從 w − 3 起週期 4（`G_period`）。** t ≥ w − 3 時 G(t + 4, d) = G(t, d)：d + t ≥ w 時兩邊都在牆後、餘數相同；否則 d ≤ 2，t + 4 在牆後而 t 在牆前，三個 d 和 t mod 4 ∈ {2, 3, 0} 逐一算（E 和 N 加缺陷在這幾格剛好一致）。
7. **週期恰好 4。** 取第 5 格（p = 1, 2）或第 6 格（p = 3），w ≥ 17 時都在牆後、不是 0 或 m：G(w − 3 + p, ·) 和 G(w − 3, ·) 的值直接算出不同。
8. **暫態恰好 w − 3。** 若 μ < w − 3，則 x_w = x_{w−4}。第 0 格在 w − 4 時在牆前，值 E(w − 4, 0) = ee(1, 0) = 1；在 w 時在牆後，值 N(w, 0) = ee(2, 3) = 0（w ≡ 1，不是缺陷時刻）。矛盾。
9. **小寬度。** w = 9、13 直接用 DISC-0006 的 `rule54_transient_period`（Lean `decide` 核驗 6 ≤ w ≤ 200）。∎

## 定理對照

| 猜想／引理 | Lean 定理 | 檔案 |
|---|---|---|
| H1 對折光錐（第 1 步，前提放寬） | `Discovery.Rule54Mod23.cone_seg`、`Discovery.Rule54Mod23.iter_cone` | `lean/Discovery/Rule54Mod23.lean` |
| 第 2 步 | `Discovery.Rule54Mod1.cone_eq_G` | `lean/Discovery/Rule54Mod1.lean` |
| H2 相位牆單步（第 4 步） | `Discovery.Rule54Mod1.G_step_zero`、`Discovery.Rule54Mod1.G_step_inner`、`Discovery.Rule54Mod1.G_step_near`、`Discovery.Rule54Mod1.G_step_centre`、`Discovery.Rule54Mod1.G_step` | 同上 |
| H2 歸納（第 5 步） | `Discovery.Rule54Mod1.iter_G` | 同上 |
| 第 6 步 | `Discovery.Rule54Mod1.G_period` | 同上 |
| **H3** | `Discovery.Rule54Mod1.rule54_mod4_one` | 同上 |

## 敘述差異

- 主定理的形式和 `rule54_mod4_two/three` 相同（同一個 `step`、`iter`、`T`），前提 `w % 4 = 1 ∧ 9 ≤ w`，沒有上界；並給出 `T w = w - 3`。
- Lean 的一般論證只用在 w ≥ 17；w = 9、13 引用有限核驗定理。兩者合起來涵蓋所有 w ≥ 9。
- 加上 DISC-0010、DISC-0011，R2-C10 的四類（w ≥ 6，以及 w ≡ 0 時 w ≥ 4）全部有 Lean 證明。
- H2 的描述只在 Lean 裡以 `G` 出現；數值上另外逐格核到 w = 1200。

## 編譯結果

本機 Lean 4.15.0（與 `lean/lean-toolchain` 相同），只用 Lean core，`lean -o` 依序編譯 `Rule26`、`Rule54`、`Rule54Mod4`、`Rule54Mod23`（前提放寬後）、`Rule54Mod1`，無錯誤、無警告（`Rule54Mod1` 約 2 分鐘，`G_step_near`、`G_step_centre` 用 `set_option maxHeartbeats 1000000`）。`#print axioms` 對 `rule54_mod4_one`：propext、Classical.choice、Quot.sound。最終以 CI `lean` 工作的公理稽核為準。

## 附註

- DISC-0011 的 proof.md 第 3 步寫「t + 4 ≤ m 時從 t 推到 t + 1」；本 PR 把 Lean 前提放寬為 t + 3 ≤ m，DISC-0011 的紀錄不改，以這裡為準。
