# 規格審計：A334504 兩個猜想的 Lean 敘述 ↔ OEIS 定義

用途：逐項確認 `lean/Discovery/Rule26.lean`（奇數寬度，DISC-0008）和 `lean/Discovery/Rule26Even.lean`（偶數寬度，DISC-0009）證的東西，就是 OEIS A334504、A268754 說的東西。對外使用（教授審閱、arXiv、OEIS）前必須全部是「✓」或寫明理由的「說明」。

狀態記號：✓ 已核對（寫出依據）；說明 = 不完全一致但不影響結論，理由寫在旁邊；**待辦** = 還沒做。

OEIS 原文依據：`records/DISC-0008/search_evidence.jsonl` 的 S002（A334504 全文）、S003（A268754 全文），2026-11-22 用瀏覽器讀取。

## A. 規則 26 的定義

| 項目 | 結果 | 依據 |
|---|---|---|
| 26 的二進位 | ✓ | 26 = 00011010₂，1 位元在第 1、3、4 位 |
| 鄰域順序（左、中、右），位元 4l+2c+r | ✓ | `rule26 l c r` 直接取 26 的第 4l+2c+r 位（Wolfram 標準編碼） |
| 1 鄰域恰為 100、011、001 | ✓ | 由上兩項；`tb_step` 證明 `step` 第 i 位 = `rule26 左 中 右` |
| 環狀鄰居 mod w | ✓ | `tb_rotL`、`tb_rotR`：第 i 位分別是第 i−1、i+1 格（mod w） |
| 同步更新 | ✓ | `step` 一次用整個舊字計算新字 |
| 左右方向 | 說明 | OEIS 沒規定方向。左右反過來，規則 26 變成鏡像規則 82，單點軌道一一對應，週期不變，所以方向不影響 a(w)。論文 Remark 已寫 |

## B. 初始條件與狀態編碼

| 項目 | 結果 | 依據 |
|---|---|---|
| 第 i 格 = 整數第 i 位 | ✓ | 兩個 Lean 檔的檔頭註解與 `tb_*` 引理 |
| 種子只有第 0 格活 | ✓ | `iter w t 1`；OEIS「a single cell」。單點放在哪一格不影響週期（環有平移對稱） |
| Lean `step` ↔ Python `impl_b` | 說明 | 靠閱讀程式碼＋`check_small` 抽查（DISC-0008 proof.md「敘述差異」）。Lean 定理本身不依賴 impl_b |
| 小寬度 w = 1、2 | 說明 | 兩個定理都不含：奇數要求 w ≥ 3，偶數要求 m ≥ 2（w ≥ 4）。這和 OEIS 猜想的 n ≥ 1 一致。w = 1 時暫態是 1（x₁ = 0），論文 Remark 已寫 |

## C. 週期的定義

| 項目 | 結果 | 依據 |
|---|---|---|
| OEIS 用的是「最終週期」（允許暫態） | ✓ | A334504 標題「Eventual period」 |
| 奇數：證到最小週期，不是某個週期 | ✓ | `rule26_odd_period` 第三個合取：0 < p < P 時 x_p ≠ x₀；x₀ 在循環上，所以最小回返時間就是循環週期 |
| 奇數：暫態 0 | ✓ | `rule26_odd_period` 第二個合取：對所有 μ，x_{μ+P} = x_μ |
| 偶數：`EvPer` 和 OEIS 最終週期的關係 | ✓ | `EvPer f p := ∃ T, ∀ t ≥ T, f (t+p) = f t`。`rule26_even_eventual_period` 對每個 p 給出等價；PR 17 另加 `rule26_even_least_period`，直接證明「p 是最小正最終週期」兩邊等價，這正是 OEIS 的定義 |
| 回到初始 vs 進入任意循環 | ✓ | 奇數證的是回到 x₀（更強）；偶數證的是整條軌道的最終週期等價，x₀ 不在循環上（`iter_succ_ne_one`） |

## D. 奇數寬度的對照

| 項目 | 結果 | 依據 |
|---|---|---|
| 範圍 w 奇且 ≥ 3 | ✓ | `hw : w % 2 = 1`、`h3 : 3 ≤ w`；對應 OEIS 的 w = 2n+1、n ≥ 1 |
| ⌊log₂ w⌋ | ✓ | Lean core 的 `Nat.log2`，對 w ≥ 1 就是 ⌊log₂ w⌋ |
| A070939 換算 | ✓ | A070939(n) = n 的二進位位數 = ⌊log₂ n⌋ + 1（n ≥ 1）= ⌊log₂(2n+1)⌋。例：n = 1，A070939 = 1，⌊log₂ 3⌋ = 1 |
| 和 OEIS 資料對照 | ✓ | 獨立小程式算出 w = 1..13 的週期 1, 1, 6, 1, 20, 2, 28, 1, 72, 6, 88, 4, 104，和 A334504 資料一致（2026-11-22） |

## E. 偶數寬度的對照

| 項目 | 結果 | 依據 |
|---|---|---|
| w = 2n+2，n = m−1 | ✓ | `rule26_even_eventual_period` 用 w = 2m、導線長 m−1 |
| A268754 offset 1（n ≥ 1） | ✓ | m ≥ 2 ⇔ n ≥ 1 |
| 導線兩端是死格（零邊界） | ✓ | `nstep n y = ((y <<< 1) ^^^ (y >>> 1)) &&& (2^n − 1)`：左移後遮罩砍掉第 n 位、右移丟掉第 −1 位，等於兩端補 0 |
| 種子在左端 | ✓ | 導線種子 1 = 第 0 位；和 A268754 Python 程式從 h = 1 開始一致 |
| A268754 的原始定義 | 說明 | OEIS 的標題是「B1/S 規則下 n×1 振盪器的週期」，程式用的是上面的 Rule 90 更新式。我們證明的是規則 26 ↔ 這個更新式；B1/S ↔ Rule 90 是 OEIS 條目本身的程式內容，不是我們證的。論文已照這個說法寫 |
| 環和導線差一步 | ✓ | `iter_succ_testBit`：x_{t+1} = E(y_t) |
| 環的暫態 = 導線暫態 + 1 | 說明 | 不是 OEIS 猜想的一部分。沒有單獨的 Lean 定理，由 `iter_succ_eq_iff` 和 `iter_succ_ne_one` 在紙上推出；n ≤ 40 數值驗證（l02_check），w = 4 時環的暫態是 2。論文 Discussion 已寫明 |
| 最小最終週期相同 | ✓ | `rule26_even_least_period` |
| A268754 的 Mathematica 程式也一致 | ✓ | 2026-11-22 讀 OEIS 文字版：矩陣 `Boole[Abs[i-j]==1]`（n×n 三對角，即零邊界 Rule 90）、向量 `Boole[i==1]`（左端單點）、在 GF(2) 上求最終週期，和 Python 程式、Lean `nstep` 同一個系統 |

## F. Lean ↔ 論文 ↔ 版本

| 項目 | 結果 | 依據 |
|---|---|---|
| `pas` 和 C(t, j) mod 2 | 說明 | Lean 的 `pas` 用 Pascal 遞迴定義，沒有證明它等於 `Nat.choose t j % 2`（core 沒有 `Nat.choose`）。主定理不提 `pas`，不受影響；論文 Discussion 已明寫 |
| `iter` 方向 | ✓ | `iter w (k+1) x = iter w k (step w x)`，`iter_succ'` 證明也等於 `step w (iter w k x)` |
| 偶數證明的 Lean 檔已合併、CI 通過 | ✓ | PR 17 合併為 main 的 b481f0f；CI 在 PR head e9ef507 上通過：Lean build（含公理稽核）run 45021537194、測試 run 45021533388（審查者另行核對 run 45021537194 = success、commit e9ef507）。獨立審查判定 PROVEN_KNOWN（records/DISC-0009/review.md） |
| 奇數證明的 CI | ✓ | run 45017724157（commit af98758），含公理稽核 |
| 論文、Lean、CI 對應同一 commit | ✓ | 兩個 Lean 檔自 005a335 起沒改；含公理稽核的 CI 在 e9ef507 通過（run 45021537194）。論文 Formal verification 段已寫這兩個 hash |

## G. 文獻定位（對外前要補）

| 項目 | 結果 |
|---|---|
| Martin–Odlyzko–Wolfram 1984 中規則 18 的奇偶化約（ChatGPT 指出） | 說明：可取得的版本（scispace）只讀到第 1～4D 節，第 4F 節（其他邊界）和第 5 節（非加法規則）缺頁；Project Euclid 被機器人防護擋住。讀到的部分沒有規則 18 化約或規則 26。論文只引用它的循環邊界 Rule 90 理論，並明寫 4F、5 節沒讀到、不對其內容下結論 |
| OEIS A160657 的 2019 評論（矩形振盪器 → Rule 90 導線） | ✓ 已讀原文：C. Neder 2019 證明 B36/S125 規則的 2×4n 振盪器角落像寬 n 的 Rule 90 帶子，所以 A160657(n) = A268754(2n)；A268754 也記「偶數項恰為 A160657」。這是偶數證明的直接先例（不同機制），論文 Discussion 已引用 |
| 反射技巧（對稱環 ↔ 零邊界導線）的可引用出處 | 說明：查了 Tadaki 1993（arXiv:cond-mat/9305012，零邊界 Rule 90 的軌道）和 MOW 可讀部分，都沒找到這個對應。論文寫「沒找到可引用出處，自行證明」，Tadaki 只當零邊界 Rule 90 的背景文獻 |
| 規則 26 單點圖樣在直線上和規則 90 相同 | ✓ 論文改成一行自證（規則 90 單點各列沒有相鄰活格，110 不出現），不再引用 NKS |
| 猜想提出者姓名拼法 | ✓ 照紀錄 DISC-0008 S002 寫 Zabolotskii |
| MathSciNet、zbMATH、Google Scholar、math-fun 郵件列表 | 說明：zbMATH（"rule 26" & cellular：1 筆無關；A334504：0 筆）、Google Scholar（兩個查詢，只看第一頁標題和摘要）、OpenAlex（再一次全文查詢）都沒找到證明。MathSciNet 需要訂閱，無法查。math-fun 郵件列表存檔沒有去找，只用 OEIS 的 %D 紀錄（Klee 2020-04-26）。詳見 `results/A334504/literature_check.md` |
