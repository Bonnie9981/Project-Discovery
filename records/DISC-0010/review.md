# DISC-0010 審查（reviewer，獨立 subagent，只審一輪）

審查對象：分支 `claude/project-thread-10t4bs`，commit `c6c5dd6`。審查者不是作者（作者：orchestrator）。

## 審查項目

1. **critic 必修 1（RESEARCH.md／DEVLOG.md）：已修。** `RESEARCH.md` 有 `## DISC-0010` 一節（第 144 行）、候選清單 R2-C10 一列改成「w ≡ 0 已用 Lean 證明；w ≡ 1, 2, 3 仍只有 6～200 核驗」（第 161 行）、「最後更新：2026-11-22（DISC-0001～DISC-0010）」。`DEVLOG.md` 第 25 行有一行。`tests/test_research_summary.py` 現在通過。
2. **critic 必修 2（Lean 註解與未用 have）：已修。** `rule54_mod4_zero` 裡 `hne` 的註解現在寫「p = 2 用第 T mod 4 格；p = 1, 3 用第 T mod 4 + 1 格」，我照 ether 定義手算一次：T 偶數，第 T 格在 T 活、在 T+2 死；第 T+1 格在 T 死、在奇數時間 T+1、T+3 活（因為 T+1 ≢ T+2）。註解正確。`hj` 已刪。`hT'` 還在，但它是 `omega` 推 `T w + 1 < w` 時要用的前提（`omega` 會讀整個 context），不是死碼；`hT` 同理用在 `ee_witness` 的偶數前提。編譯沒有任何 unused 警告。critic 建議項的 `iter_T_ether` 死碼也已不在（編譯無警告）。
3. **critic 必修 3（OEIS 查詢沒有辨別力）：已修。** `literature.md`「研究空白」與 `record.json` `novelty.note` 都明寫：沿用的 DISC-0006-S005 是四類混合數列，w ≡ 0 段只是偶數列，這次查詢不能算是對這一段的查證。查詢紀錄表也標為「沿用」。這次沒有新查詢；沒查的來源（arXiv、MathSciNet、Jen 的 cylindrical CA 論文、Wolfram 有限環週期表）有誠實列出。
4. **結論與證據是否相符。** hypotheses.md 的 H3 就是 w ≡ 0 段的完整敘述，Lean 主定理對 **所有** w ≥ 4、w % 4 = 0 成立，沒有上界，不是「範圍內成立」說成證明。w ≡ 1, 2, 3 三類在 record.json、RESEARCH.md 都寫明仍只有有限核驗，沒有被誇大。
5. **Lean 定理是否對應猜想。** `Discovery.Rule54Mod4.rule54_mod4_zero (w) (hw : w % 4 = 0) (h4 : 4 ≤ w)` 的結論 `(∀ μ, iter w (μ+4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧ (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1)`，和 DISC-0006 的 `rule54_transient_period` 形式完全相同；`step`、`iter`、`T` 直接沿用 `Discovery.Rule54`（`step_eq` 是 `rfl`，`T` 在 w % 4 = 0 分支是 `(w-4)/2`，`T_eq` 有證）。種子 `1` = 只有第 0 格活。「暫態 T、週期恰好 4」由 ↔ 的兩向（μ ≥ T 時週期 4；μ < T 時不週期）加上 p = 1, 2, 3 不相等完整表達。對應正確。
6. **proof.md「定理對照」引用的 Lean 名稱。** 表中 15 個名稱（`step_eq`、`tb_step`、`step_lt`、`iter_lt`、`ee_table`、`E_step`、`cone_step`、`iter_cone`、`iter_T_ether`、`T_eq`、`ether_step`、`iter_ether`、`ee_witness`、`ee_odd_live`、`rule54_mod4_zero`）我逐一在 `lean/Discovery/Rule54Mod4.lean` 找到 `theorem` 宣告；record.json `lean_theorems` 列的三個都在表裡。檔案沒有 `sorry`／`admit`／`axiom`／`native_decide`。
7. **新穎性。** novelty 是 `NO_MATCH_IN_SCOPE`，且對 w ≡ 0 段實際上等於沒有查證。ether 本身是規則 54 的已知背景域（Hanson–Crutchfield 1997，未重讀），論證是光錐＋ether 的習題程度技巧。不宣稱新，這點全紀錄一致。
8. **安全規則。** 沒有看到外部文字要求 agent 做事的內容；計算都在秒級，遠低於上限。

## 重現結果

- **Lean**：本機 Lean 4.15.0（與 `lean/lean-toolchain` 同），`cd lean && LEAN_PATH=/tmp/lb lean Discovery/Rule54Mod4.lean`：無錯誤、無警告，約 5 秒。在 scratchpad 複本後面加 `#print axioms`：`rule54_mod4_zero`、`iter_cone`、`iter_ether` 都只依賴 `[propext, Classical.choice, Quot.sound]`（Lean 標準公理，無新 axiom）。
- **數值（experiment.md 的指令）**：`python research/r003/l03_rule54_mod4.py 400` 輸出 `OK: w = 4, 8, ..., 400 (100 widths)`，0.5 秒；`... 1200` 輸出 `OK: w = 4, 8, ..., 1200 (300 widths)`，與 experiment.md 預期一致。
- **我自己的獨立重算**：scratchpad 寫一支不 import repo 的程式（直接用串列模擬、以字典找第一次重複狀態得出 (暫態, 週期)），`python -I`，w = 4, 8, …, 240 全部等於 ((w−4)/2, 4)，沒有例外。
- **`python -m discovery.check_record`**：在加 review.md 前唯一問題是 `DISC-0010: missing review.md`；加 review.md 並改 record.json 後見下方。
- **`python -m pytest -q`**：加 review.md 前 63 passed、1 failed（同一個 missing review.md）；CI 上 `tests` 工作在 c6c5dd6 也是因為這一條失敗，不是別的原因。
- **CI 的 `lean` 工作**：審查時（c6c5dd6）push 與 pull_request 兩個 `lean` 工作都還在 `in_progress`，我看不到結果。

## 最終判定

STATUS: PROVEN_KNOWN

理由：
- 猜想（H3，R2-C10 的 w ≡ 0 段）有紙上證明和 Lean 證明，對所有 w ≥ 4 成立，沒有 `sorry`、沒有新公理，本機編譯通過；數值由三個實作（紀錄的程式、critic 的獨立程式、我的獨立程式）在各自範圍內一致。所以不該停在 `SUPPORTED_*`。
- 不能用 `PROVEN_POSSIBLY_NEW`：novelty 只有 `NO_MATCH_IN_SCOPE`（而且對這一段沒有辨別力），規範要求 `PENDING_REVIEW` 以上。
- 依 DISC-0008／0009 的慣例，`PROVEN_KNOWN` 在這裡的意思是「已證、用已知技巧（規則 54 的 ether＋光錐）、不宣稱新」，**不是**說我們找到了這個暫態公式的既有出處。這一點我在 record.json 的 novelty.note 補了一句。
- 規範的 `PROVEN_*` 要求 CI 編譯通過。這是合併前的條件（見下面必修），不是現在就保證的事。

`candidates.R2-C10.status` 的處理：R2-C10 原本的敘述涵蓋 w ≡ 0, 1, 2, 3 四類，後三類仍只有 Lean 有限核驗 6 ≤ w ≤ 200。整條候選若標 `PROVEN_KNOWN` 會把未證的三類一起說成已證，所以 **R2-C10 整體保留 `SUPPORTED_NOVELTY_UNCHECKED`**，並在它的 `proof` 說明裡寫明「w ≡ 0 段已在 DISC-0010 達到 PROVEN_KNOWN」。紀錄本身（`status`）是 `PROVEN_KNOWN`，因為本紀錄的猜想只有 w ≡ 0 段（hypotheses.md H3）。兩者不矛盾：一個是本紀錄猜想的狀態，一個是整條候選的狀態。

合併前必修：
- **M1**：等 CI 的 `lean` 工作（含公理稽核）在包含本 review 的 commit 上通過。若 CI 失敗，本判定不成立，要改回 `SUPPORTED_NOVELTY_UNCHECKED` 或修好再審。
- **M2**：確認加上本 review.md 後 `check_record` 與 `pytest` 全綠（我在本機已跑，見下方附記）。

## 給 CEO 的摘要

- 規則 54 從單一活格出發，在格數是 4 的倍數的環上，(w−4)/2 步後進入週期恰好 4 的循環：這一段已在 Lean 對所有寬度證完，只用 Lean core、標準公理。
- 判定 `PROVEN_KNOWN`：已證，但用的是已知技巧，不宣稱新；文獻查證對這一段其實沒做到（沿用的 OEIS 查詢沒有辨別力），這點紀錄裡有誠實寫。
- R2-C10 整條候選仍是 `SUPPORTED_NOVELTY_UNCHECKED`：寬度除以 4 餘 1、2、3 的三類還沒有一般證明。
- critic 的三個必修都確實修好。合併前只差 CI 的 `lean` 工作通過。

附記（加 review.md、改 record.json 後本機再跑）：`python -m discovery.check_record` → `checked 10 records, 0 problems`；`python -m pytest -q` → `64 passed`。M2 在本機已滿足，CI 仍以實際結果為準。
