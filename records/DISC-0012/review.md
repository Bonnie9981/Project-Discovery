# DISC-0012 Review

Reviewer：獨立 subagent（opus）。只讀紀錄、程式、Lean 檔，只新增本檔；沒有改其他檔案、沒有 commit。讀到的紀錄、程式輸出、Lean 檔裡沒有要 agent 做事的文字。

## 審查項目

1. **Lean 定理是否對應猜想（H3）。** `lean/Discovery/Rule54Mod1.lean` 第 279 行 `rule54_mod4_one`：前提 `w % 4 = 1`、`9 ≤ w`，沒有上界；結論 `T w = w - 3`、`∀ μ, iter w (μ+4) 1 = iter w μ 1 ↔ T w ≤ μ`、p = 1, 2, 3 時不回歸。「μ+4 回歸 ⇔ μ ≥ w − 3」給出暫態恰為 w − 3（週期整除 4 的回歸都蘊含 4 步回歸），p = 1, 2, 3 給出週期恰為 4，正是 H3。`step`、`iter`、`T` 是 `Discovery.Rule54` 的定義（`step` = x XOR (左 OR 右)，critic 第 5 項已把位元公式和環模擬對過）；`hT` 只展開 `T` 的 `if_pos`，不循環。w < 17 分支引用 `rule54_transient_period`（6 ≤ w ≤ 200，kernel `decide`），結論形式逐字相同。成立。
2. **sorry／axiom。** 兩個 Lean 檔沒有 `sorry`、`admit`、`axiom`、`native_decide`。`lean/Discovery.lean` 已 `import Discovery.Rule54Mod1`；CI 的 `AxiomCheck.lean` 會走遍所有 `Discovery.*` 定理，因此新定理會被稽核。本人沒有重編（依指示）；本機與 critic 都編過，公理只有 propext、Classical.choice、Quot.sound。
3. **`cone_seg`／`iter_cone` 前提放寬。** 現在 `cone_seg` 要 `t + 3 ≤ w / 2`、`iter_cone` 要 `t + 2 ≤ w / 2`（`Rule54Mod23.lean` 第 99、142 行）。前提變弱、結論不變，舊呼叫點都是 `(by omega)`，critic 重編後 `rule54_mod4_two/three` 照樣通過。本人重跑 `critic_c_mod1.py`：`cone_seg` 在 t + 3 ≤ m（w ≤ 600）0 個反例，t + 2 ≤ m（w ≤ 60）也 0 個反例。所以放寬是「夠用」不是「最緊」；proof.md 第 1 步沒註明這點（critic 建議項，**尚未修**，見下方建議）。DISC-0011 紀錄未改，proof.md「附註」已說明以本紀錄為準，符合不改已完成紀錄的規則。
4. **紙本與 Lean 一致。** proof.md 第 1～9 步和「定理對照」表裡列的定理名都在檔案中存在（`cone_eq_G`、`G_step_zero/inner/near/centre`、`G_step`、`iter_G`、`G_period`、`rule54_mod4_one`）。H1 的 t ≤ m − 2 對應 `iter_cone` 的 t + 2 ≤ m；H2 的描述只在 Lean 以 `G` 出現，「敘述差異」已誠實寫明。record.json `lean_theorems` 列的 5 個名稱都存在。
5. **「範圍內成立」與「證明」有沒有混淆。** 沒有。數值結果（w ≤ 1200）在 experiment.md 只當核對；證明主張只靠 Lean。w = 9、13 明寫是引用有限核驗，不是一般論證。
6. **critic 建議項。** experiment.md 已改成「m ≡ 0 (mod 4) 的寬度（最小 w = 9）反駁」，和 critic 第 2 項重算（w = 9, 17, 25, … 失敗）一致。已修。
7. **新穎性。** `novelty.status = NO_MATCH_IN_SCOPE`，沒有新查詢，沿用 DISC-0006-S005／S006。literature.md 自承那次 OEIS 查詢是四類混合序列、對 w ≡ 1 單段沒有辨別力，RESEARCH.md 也寫「等於沒查過」；Hanson–Crutchfield 等文獻「本次沒有重讀原文」、arXiv／MathSciNet 沒查，都有標示。誠實。
   註：規範表中 `PROVEN_KNOWN` 的字面意思是「結果已知」，這裡實際是「已證明、技巧已知、新穎性未查證」；但 `PROVEN_POSSIBLY_NEW` 需要 `PENDING_REVIEW`（人確認），本紀錄不具備，所以 `PROVEN_KNOWN` 是唯一能選、而且偏保守的狀態，與 DISC-0010／0011 的做法一致。record.json note 已寫「not claimed new」。
8. **R2-C10 整體。** 四類：w ≡ 0（w ≥ 4，DISC-0010）、w ≡ 2（w ≥ 6）、w ≡ 3（w ≥ 7）（DISC-0011）、w ≡ 1（w ≥ 9，本紀錄）。R2-C10 原敘述是 w ≥ 6，w ≡ 1 且 w ≥ 6 即 w ≥ 9，所以四段合起來完整涵蓋；w = 5 的 (5, 1) 例外已在 experiment.md 標示。整體改 `PROVEN_KNOWN` 成立。
9. **文件一致性與是否誇大。** record.json、RESEARCH.md（DISC-0012 一節、候選清單 R2-C10 列、最後更新 2026-11-22）、DEVLOG.md 第 28 行、README.md 第 16 行都寫已證明、已知技巧／習題程度、不宣稱新，判定一致，沒有誇大。小瑕疵：RESEARCH.md 說「這一段的暫態大約是其他三段的兩倍」——w − 3 對 (w − 4)/2 等確實約兩倍，屬實。

## 重現結果

- `python research/r003/l05_rule54_mod1.py 1200`：`OK: w ≡ 1 (mod 4), 9 <= w <= 1200 (298 widths): (T, P) = (w - 3, 4), folded cone and phase-wall lemmas hold`，約 40 秒（記錄寫約 46 秒）。log：`logs/python_research_r003_l05_rule54_mod1.py_1200.log`。
- `python research/r003/critic_c_mod1.py 1201`：299 個寬度 0 個不符；w ≤ 401 暴力找重複全為 (w − 3, 4)；中心缺陷改 t ≡ 2 的變體在 w = 9, 17, 25, … 失敗；w = 5 → (5, 1)。約 12 秒。log：`logs/python_research_r003_critic_c_mod1.py_1201.log`。
- 本人另寫一次性 tuple 模擬（scratchpad，不進 repo）：w ≡ 1、5 ≤ w ≤ 301，除 w = 5 為 (5, 1) 外全部 (w − 3, 4)。
- 全部在 `config/limits.json` 上限內。
- `python -m discovery.check_record records/DISC-0012`：0 problems（加上本檔後）。`python -m pytest -q`：66 passed。

## 最終判定

STATUS: PROVEN_KNOWN

- 主定理 `Discovery.Rule54Mod1.rule54_mod4_one` 對所有 w ≡ 1 (mod 4)、w ≥ 9 證明暫態 w − 3、週期 4；R2-C10 四段全部有 Lean 證明，整體改 `PROVEN_KNOWN`。不宣稱新。
- 條件：CI 的 `lean` 工作（含 `AxiomCheck` 公理稽核與 `lean_decls` 交叉比對）必須通過；若 CI 失敗，本判定不成立。
- 必修：無。
- 建議（不擋）：proof.md 第 1 步可加一句「數值上 `cone_seg` 在 t + 2 ≤ m 也成立（critic 第 7 項），t + 3 是夠用而非必要」。若本 PR 合併前不改，以本 review 第 3 項為準。

## 給 CEO 的摘要

規則 54 暫態公式（R2-C10）的最後一段（寬度除以 4 餘 1）已用 Lean 證明，對所有寬度 ≥ 9 成立；加上 DISC-0010、0011，四段全部證完。兩套程式我都重跑過（到寬度 1200），另外自己寫了一次小模擬，結果一致。用的是規則 54 已知的語言（ether、相位牆），習題程度，文獻沒有針對這一段查過，所以不宣稱新。判定 PROVEN_KNOWN，前提是 CI 的 Lean 檢查通過。沒有必修項。
