# DISC-0012 Critic

Critic：獨立 subagent（opus）。只讀 repo、新增 `research/r003/critic_c_mod1.py` 與本檔；沒有改其他檔案、沒有 commit。讀到的紀錄、程式、Lean 檔裡沒有出現要 agent 做事的文字。

## 攻擊項目

1. **第三套模擬，H1／H2 逐格、H3 直接比對（不找循環）。**
   做法：`research/r003/critic_c_mod1.py`，numpy uint8 整環陣列，一步 = `x ^ (roll(x,1) | roll(x,-1))`；G 依 hypotheses.md 的文字重寫（沒看 Lean 的 `val/eN/fl`，也沒用 l05 的 `wall`）。每個 w ≡ 1 (mod 4)、9 ≤ w ≤ 1201（299 個寬度），t = 0..w + 12 每一格：t ≤ m − 2 比 H1，t ≥ m − 2 比 G；另外直接比整個狀態：x_{w−4+4} ≠ x_{w−4}、x_{w−3+4} = x_{w−3}、x_{w−3+p} ≠ x_{w−3}（p = 1, 2, 3）。
   結果：0 個不符。w ≤ 401 另以 bytes 雜湊找第一次重複（第四種方法），99 個寬度全部 (w − 3, 4)。約 12 秒。

2. **缺陷規則是否非做不可（替代描述）。** 把中心缺陷改成「t ≡ 2 (mod 4)」重跑。
   結果：w = 9, 17, 25, 33, 41, 49 … 失敗（m ≡ 0 (mod 4) 的寬度），m ≡ 2 的寬度通過。所以 `t ≡ m (mod 4)` 是必要的。**小錯：** experiment.md 寫「w = 17 反駁」，實際上最小反例是 w = 9（m = 4）。不影響結論。

3. **小寬度與邊界。** w = 9、13：G 描述與 H3 都成立（Lean 一般論證不涵蓋它們，因為第 6 格在 w = 13 時是中心 m = 6，`¬ 6 = w / 2` 不成立，所以 Lean 用 `w < 17` 分界是對的）。w = 5：(暫態, 週期) = (5, 1)，確實要排除，定理前提 9 ≤ w 正確。

4. **Lean 主定理敘述（實際編譯）。** 我自己用 Lean 4.15.0 在 scratchpad 重新編譯 `Rule54Mod23.lean`（放寬後）與 `Rule54Mod1.lean`（約 1 分 55 秒），兩者 exit 0、無錯誤。`#check` 得到：
   `∀ w, w % 4 = 1 → 9 ≤ w → T w = w - 3 ∧ (∀ μ, iter w (μ+4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧ ∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1`。
   這正是 H3：「μ+4 回到 μ ⇔ μ ≥ w − 3」給出最小暫態（任何週期 P | 4 的回歸都蘊含 4 步回歸），p = 1, 2, 3 不回歸給出週期恰好 4。量詞沒有上界。`T` 是 `Rule54.T` 的 `if w % 4 = 1 then w - 3`，`hT` 只用 `if_pos`，沒有循環論證。小寬度分支 `rule54_transient_period w (by omega) (by omega)` 的前提是 6 ≤ w ≤ 200，`w < 17` 時成立，結論形式與目標逐字相同。`#print axioms`：`rule54_mod4_one`、`rule54_mod4_two`、`rule54_mod4_three` 都只有 propext、Classical.choice、Quot.sound（無 sorryAx、無 native_decide）。

5. **Lean `step` 真的是規則 54 嗎。** 把 `Rule54.step` 的位元公式逐字翻成 Python，和 numpy 環模擬比較 w = 3..59、每個 w 走 3w 步，0 個不符。

6. **G 有沒有漏的情形。** `G_step` 的分案 d = 0 ／ 0 < d ∧ d + 1 < m ／ d + 1 = m ／ d = m 涵蓋 d ≤ m 全部（m ≥ 4）；`fold_step` 只要求 d ≤ w / 2，相符。`G_step_centre` 牆前分支只剩 t ∈ {m − 2, m − 1}（d = m，t + m + 1 < 2m + 1），和 proof.md 第 4 步一致。`iter_G` 的 k 歸納在 t = m − 2 + k 上用 `G_step`，前提 w / 2 ≤ t + 2 恆成立。`G_period` 牆前分支 d ∈ {0, 1, 2} 正確（t ≥ w − 3 且 d + t < w ⇒ d ≤ 2，也 ≠ m）。全部已由 kernel 檢查。

7. **`cone_seg`／`iter_cone` 前提放寬是否影響舊定理。** 前提變弱（t + 4 → t + 3、t + 3 → t + 2），結論不變；舊呼叫點（`Rule54Mod23.lean` 第 161、250、296 行）都是 `(by omega)` 形式，重新編譯後 `rule54_mod4_two/three` 照樣通過、公理不變。另把 `cone_seg` 當成純粹關於 `Cf` 的等式數值檢查：所有 3 ≤ w ≤ 600（奇偶都有）、t + 3 ≤ m、d ≤ m，0 個反例；連 t + 2 ≤ m 在 3 ≤ w ≤ 60 也 0 個反例（所以放寬不是極限，只是夠用；不是錯）。

8. **紙本 proof.md 與 Lean 對照。** 逐步對過：第 1 步前提、第 2 步（m − 2 偶、m − 1 與 m 不 ≡ m − 2）、第 4 步四類分案、第 6 步 t mod 4 ∈ {2, 3, 0}、第 7 步見證格 5／6、第 8 步 E(w − 4, 0) = ee(1, 0) = 1 與 N(w, 0) = ee(2, 3) = 0（w ≡ 1 不是缺陷時刻），都和 Lean 一致。沒有找到數學錯誤或誇大；RESEARCH.md、record.json 都寫 PROVEN_KNOWN、「不宣稱新」。

9. **l05 的獨立性。** 方法一 import `research.r002.impl_b`，方法二是同檔自寫的 list 模擬，所以 l05 兩個方法並非完全不共用專案程式；本檔第 1 項的第三套實作補上了這一點。H2 在 l05 只核到 t = w + 8，之後由 `G_period`（Lean）與兩方法的週期結果推出，沒有漏洞。

## 獨立重算

- 程式：`research/r003/critic_c_mod1.py`（只 import numpy、sys；不 import 任何 repo 模組）。檔名不用 `impl_c.py`：r003 沒有 impl_a／impl_b，放一個 `impl_*` 會讓 `discovery.independence` 報「only one impl_*.py」。`python -m discovery.independence`：0 problems。
- 指令：`python research/r003/critic_c_mod1.py 1201`，完整輸出在 `logs/python_research_r003_critic_c_mod1.py_1201.log`。
- 數字：299 個寬度（9 ≤ w ≤ 1201）H1、H2 逐格與 H3 全部成立；w ≤ 401 暴力找重複 99 個寬度全為 (w − 3, 4)；例：w = 9 → (6, 4)，w = 13 → (10, 4)。
- Lean：本機重新編譯 `Rule54Mod23`、`Rule54Mod1` 成功，公理稽核如上（olean 輸出在 scratchpad，未寫入 repo）。
- 全部在 `config/limits.json` 上限內（最長一次約 2 分鐘）。

## 未解決的疑點

- **必修：無。**
- 建議：experiment.md「w = 17 反駁」改成「最小反例 w = 9（m ≡ 0 (mod 4) 的寬度都反駁）」；因為已完成紀錄不改，可在 review 或下一份紀錄附註。
- 建議：proof.md 第 1 步可註明 `cone_seg` 在 t + 2 ≤ m 也成立（數值，第 7 項），目前的放寬是「夠用」而非「最緊」，避免讀者以為 t + 3 是必要條件。
- 文獻：本紀錄沒有新查詢，沿用的 OEIS 查詢對 w ≡ 1 單段沒有辨別力（literature.md 已自承）。「相位牆」敘述是否在 Hanson–Crutchfield 等文獻中已有環上版本，未查，不影響證明正確性，只影響新穎性判定（目前判 PROVEN_KNOWN，本來就不宣稱新）。
