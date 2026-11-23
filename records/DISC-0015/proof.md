# DISC-0015 證明：規則 54 單細胞的每一列（A118109、A265225）

英文版：`paper/rule54-rows.md`。

## 證明大意

1. 規則 54 = 新(x) = 舊(x) xor (舊(x−1) or 舊(x+1))（八種情況直接核對，`rule_eq`）。
2. H1 用歸納：新一列每格只看 x mod 4 和是不是邊界，`C_step` 用 omega 一次證完，`row_eq` 得到每一列。
3. 第 t+2 列 = 第 t 列往左移 2 格，右邊多 4 格 `0001`（t 偶）或 `0111`（t 奇）（`shift`、`tail`）。所以 a118109(t+2) = 10000·a(t) + 1 或 111，ones(t+2) = ones(t) + 1 或 3。
4. 由此推出所有公式：遞迴、下取整、Barker 封閉式、Hurt、Veselovac、5 階遞迴。生成函數由遞迴加初值推出（紙上）。
5. H6：n 元子集的和取遍 [n(n+1)/2, n(3n+1)/2] 的每個整數；n 奇時最小和 n(n+1)/2，n 偶時 n(n+2)/2，都等於 a265225(n−1)（紙上證明 + 窮舉 n ≤ 11）。

## 定理對照

| 敘述 | Lean 定理（`lean/Discovery/Rule54Rows.lean`） |
|---|---|
| 規則 54 = c xor (l or r) | `Discovery.Rule54Rows.rule_eq` |
| H1 單步 | `Discovery.Rule54Rows.C_step` |
| H1 | `Discovery.Rule54Rows.row_eq` |
| 位移、尾端 4 格 | `Discovery.Rule54Rows.shift`、`Discovery.Rule54Rows.tail` |
| a(n+2) = 10000a(n) + e | `Discovery.Rule54Rows.a118109_step` |
| H2 遞迴 | `Discovery.Rule54Rows.a118109_rec` |
| H3（乘 9999） | `Discovery.Rule54Rows.a118109_mul` |
| H3 | `Discovery.Rule54Rows.a118109_floor` |
| ones 公式 | `Discovery.Rule54Rows.ones_formula` |
| a265225 偶數項 | `Discovery.Rule54Rows.a265225_even` |
| a265225 奇數項 | `Discovery.Rule54Rows.a265225_odd` |
| H4 封閉式 | `Discovery.Rule54Rows.a265225_barker` |
| H4 遞迴 | `Discovery.Rule54Rows.a265225_rec` |
| H5（Hurt） | `Discovery.Rule54Rows.a265225_hurt` |
| H5（Veselovac） | `Discovery.Rule54Rows.a265225_veselovac` |

## 編譯結果

Lean 4.15.0，只用 core（無 Mathlib、無 `native_decide`），本機 0 錯誤約 25 秒；`#print axioms` 對 `a118109_floor`、`a265225_barker`、`a265225_rec` = [propext, Classical.choice, Quot.sound]（`Classical.choice` 來自 omega/simp，CI 允許）。

## 沒形式化的部分

- 兩個生成函數（core 沒有形式冪級數）：由已證遞迴 + 初值推出，數值上也核對過。
- H6（Ianakiev 註解）：紙上證明 + 窮舉 n ≤ 11。

## 敘述差異

Ianakiev 註解寫「equals a(n)」，實際是 a(n−1)。其他公式和條目原句完全一致（offset 0）。

## 對 critic 的回應

1. Ianakiev 原文已逐字存進 S002 和 literature.md：「Take the first 2n positive integers and choose n of them … It seems their sum equals a(n).」字面就是「1..2n 選 n 個」，n = 1 時最小和 1 = a(0) ≠ a(1)，所以「差一個索引」成立。critic 指出的等價讀法（1..2n+2 選 n+1 個 = a(n)）已寫進論文和 OEIS 草稿，讓編輯自己選怎麼改。
2. A093353 的名稱就是 a(n) = (n + (n mod 2))*(n + 1)/2（S003 逐字），是定義不是猜想，所以 `a265225_veselovac` 就是原公式。
3. 論文 AI 聲明裡「reviewed」「CI」：比照 DISC-0014，條件是合併前 review.md 存在且 CI 全綠。
4. OEIS 草稿已在 `results/A118109/`、`results/A265225/`（critic 讀檔時還沒寫好）。
5. 公式數改成 8 個、6 個 Lean 定理；論文邊界情況補一句。
