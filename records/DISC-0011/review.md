# DISC-0011 審查（reviewer，獨立 subagent，只審一輪）

審查對象：分支 `claude/project-thread-sro8tg`，commit `8fa1404`。審查者不是作者（作者：orchestrator）。這一輪沒有做網路查詢。

## 審查項目

1. **結論與證據是否相符。** hypotheses.md 的 H3 就是 R2-C10 的 w ≡ 2、w ≡ 3 兩段。Lean 主定理對**所有** w ≡ 2 (mod 4)、w ≥ 6 和所有 w ≡ 3 (mod 4)、w ≥ 7 成立，沒有上界，所以不是把「範圍內成立」說成證明。w ≡ 1 段在 record.json `candidates.R2-C10.proof` 和 proof.md 附註都寫明還沒證，沒有誇大。
2. **Lean 定理是否對應猜想。** `rule54_mod4_two` / `rule54_mod4_three` 的假設只有 `w % 4 = 2, 6 ≤ w`（或 `= 3, 7 ≤ w`）。結論是 `T w = (w-6)/2`（或 `(w-7)/2`）、`∀ μ, iter w (μ+4) 1 = iter w μ 1 ↔ T w ≤ μ`，以及 p = 1, 2, 3 時 `iter w (T w + p) 1 ≠ iter w (T w) 1`。形式和 DISC-0010 的 `rule54_mod4_zero` 相同。`step`、`iter`、`T` 都是從 `Discovery.Rule54` 用 `open` 引入，不是重新定義（我用 `#print` 確認 `iter` 是 `Discovery.Rule54.iter`）。`T` 的 w%4=2、3 分支和 R2-C10 的表一致。「暫態恰好 T、週期恰好 4」由 ↔ 的兩個方向，加上 p = 1, 2, 3 都不相等來表達：週期 4 的軌道，最小週期只能是 1、2、4。這一步在 proof.md 第 6 步有寫。對應正確。
3. **紙上證明和 Lean 對得上。** 我讀了 `defect_table`：a ∈ {0, 2}、r < 4，共 8 種情形，每種 3 條等式（中心旁一格、偶數寬的中心、奇數寬的中心），和 proof.md 第 5 步的「8 種情形各 3 條等式」一致，critic 建議 1 的疑慮已經消除。主證明 `rule54_core` 只用 `w/2 = T+3`、T 偶數、w ≥ 6 這三個前提，兩個包裝定理都用 `omega` 補上這三個前提。檔案沒有 `sorry`、`admit`、`axiom`、`native_decide`。
4. **proof.md「定理對照」。** 表中的 Lean 名稱都能在 `lean/Discovery/Rule54Mod23.lean` 找到 `theorem` 宣告，record.json `lean_theorems` 列的 5 個也都在表裡。`check_record` 沒有報這一類錯誤。
5. **新穎性。** novelty 是 `NO_MATCH_IN_SCOPE`，這次沒有新查詢。literature.md 和 record.json 都寫明：沿用的 OEIS / OpenAlex 查詢（DISC-0006-S005/S006）查的是四類混合數列，對單獨的 w ≡ 2 或 w ≡ 3 段沒有辨別力。沒查的來源（arXiv、MathSciNet、Jen、Wolfram 的有限環表）都有列出。ether 和缺陷是規則 54 已知的粒子語言，對折是 DISC-0009 的技巧。全紀錄都不宣稱新，前後一致。
6. **critic 的建議。** 「每 4 步閃一次」已改成「每 4 步中有一步比 ether 少亮」；週期整除的那一句也已補進 proof.md 第 6 步。critic 沒有提出必修項。
7. **流程閘門（新發現，必修）。** `python -m discovery.check_record` 報錯：`DISC-0011: status PROVEN_KNOWN needs record.json critic_model = "opus"`。docs/TOKEN_BUDGET.md 第 1 節規定，要判 `PROVEN_*` 的紀錄，critic 必須用 opus。但這份紀錄的 critic 是 sonnet（record.json `critic_model: "sonnet"`）。數學內容不受影響：critic 的攻擊做得完整（公理稽核、第三套獨立模擬到 w = 1000），我也自己重做了編譯和模擬。不過這是規範寫明的必做項目，不能把 `critic_model` 直接改成 `"opus"` 來過關。
8. **安全規則。** 沒有看到外部文字要 agent 做事的內容。計算都在秒級，遠低於上限。

## 重現結果

- **Lean**：本機 Lean 4.15.0，`cd lean && LEAN_PATH=/tmp/claude-0/olean lean Discovery/Rule54Mod23.lean`，約 30 秒，無錯誤、無警告。scratch 檔 `/tmp/claude-0/review/ax11.lean` 的 `#print axioms` 結果：`rule54_mod4_two`、`rule54_mod4_three`、`iter_defect` 都只依賴 `[propext, Classical.choice, Quot.sound]`。
- **數值（照 experiment.md 的指令）**：`python research/r003/l04_rule54_mod23.py 400` 輸出 `OK: w ≡ 2, 3 (mod 4), 6 <= w <= 400 (198 widths) ...`，耗時 0.8 秒，和預期一致。W = 1200 沒有重跑（critic 已經用獨立程式跑到 1000）。
- **我自己的獨立重算**：`/tmp/claude-0/review/sim.py`，不 import repo，用 `python -I` 執行。它直接用 Wolfram 編號 54 的位元表在 tuple 上模擬，再用字典找第一次重複的狀態。結果：6 ≤ w ≤ 300、w ≡ 2, 3 共 148 個寬度，全部等於 (T, 4)，0 個反例。
- **`python -m pytest -q tests`**：63 passed，2 failed。兩個失敗是 `test_records`（missing review.md，以及上面第 7 項的 critic_model）和 `test_research_summary`（RESEARCH.md 還沒有 `## DISC-0011` 一節）。
- **`check_record`**：加上本檔之前是 3 個問題。加上之後剩 2 個：`proof.md: missing section '## 敘述差異'`，以及 critic_model（見第 7 項）。

## 最終判定

STATUS: PROVEN_KNOWN

理由：
- H3（R2-C10 的 w ≡ 2、3 段）有紙上證明，也有 Lean 證明，對所有寬度成立。沒有 `sorry`，也沒有新公理，我在本機編譯通過。數值由三套實作（紀錄的程式、critic 的程式、我的程式）互相確認。所以不該停在 `SUPPORTED_*`。
- 不能判 `PROVEN_POSSIBLY_NEW`：新穎性只有 `NO_MATCH_IN_SCOPE`，而且那次查詢對這兩段沒有辨別力。`PROVEN_KNOWN` 照 DISC-0008～0010 的慣例，意思是「已證明、用已知技巧、不宣稱新」，不是說我們找到了既有出處。
- R2-C10 整條候選保持 `SUPPORTED_NOVELTY_UNCHECKED`，因為 w ≡ 1 段還沒證。record.json 已經這樣寫，正確。

合併前必修（這個判定以下列兩項為前提）：
- **M1（critic_model）**：照 TOKEN_BUDGET 第 1 節，總控要用 `model: opus` 重跑一輪 critic。critic.md 可以用附加段落的方式補上，再把 `critic_model` 改成 `"opus"`。如果不重跑，本紀錄就必須降回 `SUPPORTED_NOVELTY_UNCHECKED`，不能為了過關直接改欄位。
- **M3（proof.md 少一節）**：proof.md 缺少必要的 `## 敘述差異` 一節（DISC-0010 有）。要補寫：Lean 敘述和猜想的差別，例如前提沒有上界、「在循環上 ⇔ x_{μ+4} = x_μ」沒有另外形式化、w ≡ 1 段未涵蓋。
- **M2（摘要與 CI）**：RESEARCH.md 要加 `## DISC-0011` 一節，並更新候選清單中 R2-C10 那一列（w ≡ 0, 2, 3 已證，w ≡ 1 只有 6～200 的有限核驗）和「最後更新」日期；DEVLOG.md 加一行。之後 `check_record`、`pytest` 要全綠，CI 的 `lean` 工作（含公理稽核）也要通過。如果 CI 失敗，本判定不成立。

## 給 CEO 的摘要

- 規則 54 從單一活格出發，在格數除以 4 餘 2 或餘 3 的環上，分別經過 (w−6)/2、(w−7)/2 步後進入週期恰好 4 的循環。Lean 已對所有寬度證完，只用標準公理。
- 判定 `PROVEN_KNOWN`：已經證明，但用的是已知技巧（對折加 ether 加中心缺陷），不宣稱新；這兩段的文獻查證其實沒有做到，紀錄裡有誠實寫出來。
- R2-C10 四段中已證三段（餘 0、2、3），只剩餘 1 那段（暫態 w−3）。整條候選仍是 `SUPPORTED_NOVELTY_UNCHECKED`。
- 合併前有一個流程缺口：這份紀錄的 critic 用的是 sonnet，規範要求 opus。要補一輪 opus critic，否則要降級。另外要補 proof.md 的「敘述差異」一節，以及 RESEARCH.md 和 DEVLOG。
