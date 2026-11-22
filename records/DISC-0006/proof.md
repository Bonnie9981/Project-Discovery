# DISC-0006 證明紀錄（Proof agent）

對象：DISC-0004 C01、DISC-0004 C02、DISC-0005 R2-C10（repo main `58dbd39`）。

狀態總表：

| 候選 | 紙本證明 | Lean 形式化 |
|---|---|---|
| C01 | **部分**：奇數 n 完整；偶數 n 在 v₂(n) = a 且 2^(a+1) − 1 不是過剩數時完整（含 a ≤ 10 與 12 ≤ a ≤ 22），或 σ(n 的奇部分) 的奇部分是平方數時完整。v₂(n) = 11 紙本已排除（critic 窮舉，審查員獨立重算：f 不全為 0 時比值最大 8156.57 < 8191，全為 0 時是 8736 ≠ 8191），只是 Lean 還沒做；v₂(n) ≥ 23 的一部分仍開放 | 奇數 n 全部；偶數 n 的兩個充分條件；合併成「2¹¹ ∤ n 時 C01 成立」 |
| C02 | **完整**（見下，關鍵一步用 LTE） | **部分**：A065301 ⊆ 解集；無平方因子的解 σ(n) 也無平方因子；任何解至多一個奇質因數。2^a·p^b 的分類未形式化 |
| R2-C10 | **失敗**（沒有一般 w 的證明） | 只有 6 ≤ w ≤ 200 的 kernel 有限驗證（`decide`），加上「有限檢查 ⇒ 暫態／週期」的一般引理 |

## 定理對照

Lean 檔案：`lean/Discovery/SigmaOdd.lean`（C01）、`lean/Discovery/RadSigma.lean`（C02）、`lean/Discovery/Rule54.lean`（R2-C10），皆已加入 `lean/Discovery.lean`。σ 是 Mathlib 的 `ArithmeticFunction.sigma 1`。

### C01（`lean/Discovery/SigmaOdd.lean`）

| Lean 定理 | 數學敘述 |
|---|---|
| `Discovery.SigmaOdd.odd_sigma_iff_isSquare` | m 奇 ⇒（σ(m) 奇 ⇔ m 是平方數） |
| `Discovery.SigmaOdd.sigmaOdd_two_pow_mul` | t 奇 ⇒ σ_odd(2^k·t) = σ(t)（σ_odd 定義為奇因數和） |
| `Discovery.SigmaOdd.sigma_two_pow_mul` | t 奇 ⇒ σ(2^k·t) = (2^(k+1) − 1)·σ(t) |
| `Discovery.SigmaOdd.c01_odd` | **C01 奇數情形**：n 奇 ⇒（σ(σ_odd n) = σ_odd(σ n) ⇔ n 是平方數） |
| `Discovery.SigmaOdd.lt_sigma_mul` | q > 1, t > 0 ⇒ q·σ(t) < σ(q·t) |
| `Discovery.SigmaOdd.sigma_mul_le` | σ(q·t) ≤ σ(q)·σ(t) |
| `Discovery.SigmaOdd.c01_even_of_not_abundant` | n = 2^a·m（a ≥ 1、m 奇）且 σ(2^(a+1) − 1) ≤ 2(2^(a+1) − 1) ⇒ σ(σ_odd n) ≠ σ_odd(σ n) |
| `Discovery.SigmaOdd.c01_even_of_oddPart_square` | n = 2^a·m（a ≥ 1、m 奇），σ(m) = 2^b·t（t 奇）且 t 是平方數 ⇒ σ(σ_odd n) ≠ σ_odd(σ n) |
| `Discovery.SigmaOdd.mersenne_not_abundant` | 1 ≤ a ≤ 10 ⇒ σ(2^(a+1) − 1) ≤ 2(2^(a+1) − 1)（`decide`） |
| `Discovery.SigmaOdd.c01_of_not_two_pow_eleven_dvd` | **C01 在 2¹¹ ∤ n 時成立**：n > 0、2¹¹ ∤ n ⇒（σ(σ_odd n) = σ_odd(σ n) ⇔ n 奇且是平方數） |

輔助引理（同檔）：`sum_range_pow_mod_two`、`isSquare_prime_pow_iff`、`isSquare_mul_of_coprime`、`sigma_two_pow`、`sigma_pos'`、`sigma_odd_eq`、`two_pow_succ_sub_one_mod_four`、`sum_image_le_nat`、`isSquare_of_mul`、`not_isSquare_of_mod_four`。

### C02（`lean/Discovery/RadSigma.lean`）

| Lean 定理 | 數學敘述 |
|---|---|
| `Discovery.RadSigma.c02b` | n、σ(n) 都無平方因子 ⇒ rad(σ n) = σ(rad n)（A065301 ⊆ 解集） |
| `Discovery.RadSigma.c02_of_squarefree` | n 無平方因子且 rad(σ n) = σ(rad n) ⇒ σ(n) 無平方因子 |
| `Discovery.RadSigma.squarefree_sigma_rad` | rad(σ n) = σ(rad n) ⇒ σ(rad n) 無平方因子 |
| `Discovery.RadSigma.odd_prime_factor_unique` | σ(rad n) 無平方因子 ⇒ n 至多一個奇質因數 |

輔助引理：`squarefree_prod_primes`、`squarefree_rad`、`rad_of_squarefree`。

### R2-C10（`lean/Discovery/Rule54.lean`）

| Lean 定理 | 數學敘述 |
|---|---|
| `Discovery.Rule54.check_range` | 6 ≤ w ≤ 200：x_{T+4} = x_T、（T = 0 或 x_{T+3} ≠ x_{T−1}）、x_{T+p} ≠ x_T（p = 1, 2, 3），T = T(w) 為猜想公式（kernel `decide`） |
| `Discovery.Rule54.periodic_from` | x_{t+4} = x_t ⇒ 對所有 μ ≥ t，x_{μ+4} = x_μ |
| `Discovery.Rule54.rule54_transient_period` | **R2-C10 在 6 ≤ w ≤ 200**：x_{μ+4} = x_μ ⇔ μ ≥ T(w)，且 x_{T+p} ≠ x_T（0 < p < 4），即暫態 T(w)、週期恰為 4 |

輔助引理：`iter_succ'`、`iter_add`。

## 編譯結果

**GitHub CI（lean 工作）：通過**，commit 58fb4c9，包含 `lean/Discovery.lean` 匯入三個新模組與 AxiomCheck 全環境公理檢查：https://github.com/Bonnie9981/Project-Discovery/actions/runs/45011976606


**本機已編譯（非 CI）。** 本機原本沒有 `lake`；Mathlib cache 主機（lakecache.blob.core.windows.net）被代理擋下，因此改為：

- 下載官方 Lean 4.15.0 工具鏈（`lean-4.15.0-linux.zip`）。
- `git clone --branch v4.15.0` Mathlib（與 `lean/lakefile.toml` 的 `rev = "v4.15.0"` 相同），從原始碼 `lake build` 本檔需要的模組（`Mathlib.NumberTheory.ArithmeticFunction`、`Mathlib.Algebra.GeomSum`、`Mathlib.Algebra.GCDMonoid.Nat`、`Mathlib.Data.Finset.NatDivisors`、`Mathlib.Tactic.{Ring,Positivity,Linarith,IntervalCases}`、`Mathlib.Data.Nat.Squarefree`），結果 `Build completed successfully.`
- 在該 Mathlib 環境下逐檔 `lake env lean lean/Discovery/<檔>.lean`：`SigmaOdd.lean`、`RadSigma.lean`、`Rule54.lean` 三檔皆 0 錯誤（`Rule54.lean` 只用 core，約 8 秒；`SigmaOdd.lean` 約 8 秒）。
- 將 `AxiomCheck.lean` 的 `#check_discovery_axioms` 附在各檔後執行：`THEOREM_COUNT` 分別為 21、7、7，全部只用 `propext`、`Classical.choice`、`Quot.sound`，沒有 `sorryAx`，沒有 `native_decide`（`Lean.ofReduceBool`）。
- `python -m discovery.lean_decls` 的原始碼解析列出同樣的 35 個新定理。
- `grep -nE '\b(sorry|admit)\b|^\s*axiom '` 對新檔無輸出。

**未做的事：** 沒有在 repo 的 `lean/` 專案內跑完整的 `lake build`（需要整個 Mathlib，本機無 cache）；`lean/Discovery.lean` 匯入三個新模組的那一步沒有本機編譯。新檔只 import Mathlib 模組、命名空間各自獨立（`Discovery.SigmaOdd`、`Discovery.RadSigma`、`Discovery.Rule54`），預期不衝突，但「已證明」須以 CI `lean` 工作通過為準。CI 連結：https://github.com/Bonnie9981/Project-Discovery/actions/runs/45011976606（lean 工作通過，見下方「GitHub CI」一行）。

## 敘述差異

### C01

- **定義**：Lean 的 `sigmaOdd n` 是「n 的奇因數和」（A000593）；repo 的 `sigma_odd` 是 σ(n 的奇部分)。兩者相同，Lean 中由 `sigmaOdd_two_pow_mul` 證明（n = 2^k·t、t 奇 ⇒ sigmaOdd n = σ t）。
- **範圍**：原文對所有 n ≥ 1。Lean 的完整敘述 `c01_of_not_two_pow_eleven_dvd` 多了假設 `¬ 2^11 ∣ n`（即 v₂(n) ≤ 10），並要求 `0 < n`（n = 0 時兩邊都是 0，原文不含 n = 0）。v₂(n) ≥ 11 只有兩個充分條件版本（`c01_even_of_not_abundant`、`c01_even_of_oddPart_square`），**C01 沒有完整證明**。
- 「奇平方數」寫成 `Odd n ∧ IsSquare n`。

紙本證明。記 n = 2^a·m（m 奇），s = σ_odd(n) = σ(m)，s = 2^b·t（t 奇）。

1. 奇數 n（a = 0）：σ_odd(n) = σ(n) = s，σ_odd(σ n) = σ(t)，σ(s) = (2^(b+1) − 1)σ(t)。等式 ⇔ b = 0 ⇔ σ(n) 奇 ⇔ n 是平方數（m 奇時 σ(m) ≡ Π(e_p + 1) mod 2）。
2. 偶數 n（a ≥ 1），q = 2^(a+1) − 1 ≡ 3 (mod 4)：σ(n) = q·s = 2^b·(qt)，RHS = σ(qt)，LHS = (2^(b+1) − 1)σ(t)。
   - 由 σ(qt) > q·σ(t) 與 σ(qt) ≤ σ(q)σ(t)：等式 ⇒ q < 2^(b+1) − 1 ⇒ b ≥ a + 1 ⇒ 2^(b+1) − 1 ≥ 2q + 1 ⇒ σ(q) ≥ 2q + 1，即 q 是過剩數。所以 q 不過剩時無偶數解。σ(2^k − 1) 數值：k = a + 1 ≤ 23 內只有 k = 12（a = 11，4095）過剩，所以紙本上 v₂(n) ∈ {1..10, 12..22} 都成立；Lean 只用 `decide` 驗證了 a ≤ 10。下一個過剩的 k 是 24（critic 另列 36、40、48、60）。
   - 若 t 是平方數：LHS 奇；RHS = σ(qt) 奇 ⇔ qt 是平方數 ⇔ q 是平方數，但 q ≡ 3 (mod 4)，矛盾。
   - **卡住的地方**：q 過剩且 t 不是平方數。此時需要證明 σ(qt)/σ(t) 不會是 2^j − 1（j ≥ a + 2）。比值只依賴 t 中 q 的質因數的指數，是一個有限多質數的指數方程；我沒有找到一般論證（需要例如 σ(p^e) 的 2-adic 或模小質數的控制，對每個過剩的 2^k − 1 個別處理）。critic.md 宣稱 a = 11 已用窮舉排除，那是計算，不在 Lean 內。

### C02

- rad 定義為 `∏ p ∈ n.primeFactors, p`（rad 0 = rad 1 = 1），與 repo 的 `rad` 在 n ≥ 1 相同。
- Lean 只形式化了「A065301 ⊆ 解集」、「無平方因子的解在第一種情形」、「任何解至多一個奇質因數」。**C02 的主要分類（n = 2^a·p^b 的分析）沒有形式化**，下面的紙本證明是完整的，但不算「已證明」。

紙本證明（n ≥ 1，假設 rad(σ n) = σ(rad n)）。

1. rad(·) 無平方因子，所以 σ(rad n) = Π_{p | n}(p + 1) 無平方因子。兩個相異奇質因數會給出 4 | (p+1)(q+1)，所以 rad n ∈ {1, 2, p, 2p}（p 奇質數）。若 2 | n 且 p | n，則 3(p+1) 無平方因子，所以 p ≠ 3、3 ∤ p + 1。等式等價於 σ(n) 與 σ(rad n) 的質因數集合相同（兩邊都是 rad）。
2. n = 1：成立，n、σ(n) = 1 都無平方因子。
3. n = 2^a，a ≥ 1：2^(a+1) − 1 的質因數只有 3，所以 2^(a+1) − 1 = 3^k；a ≥ 2 時左邊 ≡ 7 (mod 8)，3^k ≡ 1, 3 (mod 8)，矛盾。所以 n = 2，σ = 3，第一種情形。
4. n = 2^a·p^b（a ≥ 0、b ≥ 1）：σ(rad n) 是偶數，σ(n) = (2^(a+1) − 1)σ(p^b) 必須是偶數 ⇒ b 奇。若 b ≥ 3，令 b + 1 = 2m（m ≥ 2），σ(p^b) = (p+1)·C，C = Σ_{i<m} p^(2i)。C 的每個質因數 r 必須整除 3(p+1)（a ≥ 1）或 p + 1（a = 0）：
   - r | p + 1（含 r = 2）：r | p² − 1，由 LTE，v_r(p^(2m) − 1) = v_r(p² − 1) + v_r(m)，所以 v_r(C) = v_r(m)（r = 2 時用 p² ≡ 1 mod 8 的 LTE 形式）。
   - r = 3 ∤ p + 1（只在 a ≥ 1 時需要）：p ≠ 3 且 p ≡ 1 (mod 3)，同樣 v₃(C) = v₃(m)。
   所以 C | m，但 C ≥ 1 + 9(m − 1) > m，矛盾。故 b = 1。
5. n = p：σ(n) = p + 1 = rad(p + 1)，所以 σ(n) 無平方因子，第一種情形。
6. n = 2^a·p，a ≥ 1：3 必須整除 σ(n) = (2^(a+1) − 1)(p + 1)，而 3 ∤ p + 1，所以 3 | 2^(a+1) − 1 ⇒ a 奇。a = 1 時 n = 2p 無平方因子，σ(n) = 3(p+1) 無平方因子（第一種情形）；a ≥ 3 時就是第二種情形 n = 2^a·p、a 奇 ≥ 3。∎

（附註：此證明同時給出 C02 敘述本身不要求的資訊；它不宣稱每個 2^a·p 都是解。）

### R2-C10

- **範圍**：原文是所有 w ≥ 6；Lean 只有 **6 ≤ w ≤ 200**（`h200 : w ≤ 200`）。這是有限驗證，不是一般證明；**R2-C10 的證明狀態是失敗**（critic.md 對 w ≡ 0, 2, 3 (mod 4) 有「光錐 + ether 接縫」的草稿，w ≡ 1 (mod 4) 的牆碰撞沒有論證，我也沒有補上）。
- **編碼**：狀態是自然數 x < 2^w，第 i 位是第 i 格（與 `research/r002/impl_b.py` 相同，種子 `1` = 只有第 0 格活）。`step w x = x xor (左旋 or 右旋)`，即規則 54 的 c ⊕ (l ∨ r)（54 = 0b00110110，8 種鄰域逐一核對過）。我用 `#eval` 確認 w = 13 前 12 步與 `impl_b.evolve(54, 13, 1, k)` 完全相同；Lean 中沒有證明 `step` 與逐格規則表等價。
- **暫態／週期的定義**：Lean 敘述是「x_{μ+4} = x_μ ⇔ μ ≥ T(w)」加上「x_{T+p} ≠ x_T，p = 1, 2, 3」。這等價於 Brent/Floyd 意義下的 (μ, λ) = (T(w), 4)：λ 是 x_T 回到自己的最小步數（4，且 1、2、3 都不行），μ 是最小的使 x_μ 位於循環上的指標（x_μ 在週期 4 的循環上 ⇔ x_{μ+4} = x_μ）。後一個等價是標準事實，沒有在 Lean 中另外形式化。
- T(w) 的 Lean 定義以 `w % 4` 分支，自然數減法與除法（`w - 3`、`(w - 6) / 2` 等）在 w ≥ 6 時與原文一致（w ≡ 2, 3, 0 時分子是偶數）。
