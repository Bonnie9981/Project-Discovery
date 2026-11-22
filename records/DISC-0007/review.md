STATUS: SUPPORTED_NOVELTY_UNCHECKED

# DISC-0007 審查（M1.4：C02 完整刻畫的 Lean 證明、C01 延伸、R-003 試點）

- 審查者：Reviewer agent（獨立，不是本紀錄的作者，也不是 critic 或 proof agent）
- 審查對象：分支 `claude/project-thread-m5yt21`，HEAD `407efb9`。工作樹**不乾淨**：`record.json` 未追蹤，`r003_pilot.json`、`RESEARCH.md`、`DEVLOG.md` 有未 commit 的修改。`lean/` 從 `57ec73d` 之後沒有變動（`git log -- lean/` 確認）。
- 讀過的檔案：`records/DISC-0007/` 全部（hypotheses、experiment、literature、critic、proof、record.json、r003_pilot.json、search_evidence.jsonl）；`lean/Discovery/RadSigmaIff.lean`、`SigmaOddExt.lean`，以及它們依賴的 `RadSigma.lean`、`SigmaOdd.lean`、`lean/Discovery.lean`、`lean/AxiomCheck.lean`；`research/r003/`；`research/r001/m14/c02_iff_check.py`；`tests/test_r003.py`；`RESEARCH.md`、`DEVLOG.md` 中 DISC-0007 的段落；`docs/RESEARCH_STANDARDS.md`；`discovery/check_record.py`。
- 審查者自己的程式放在 scratchpad，不進 repo，也不 import repo 的程式碼。

## 審查項目

### A. Critic 必修項目 M1～M4 是否已處理

| 項目 | 處理情形 | 判定 |
|---|---|---|
| **M1**（H3 結論過強） | `experiment.md` 已把結論縮小成「對每個剩餘類都吻合的線索，H3 是負面結果」，24 組部分吻合線索列在 `r003_pilot.json` 的 `partial_leads_unanalysed`，`run.py` 也會輸出 `partial_unanalysed: 24`。我逐條檢查了這 24 組：公式全部是 `v2pow` 型（7 組）或 `2^sord2-1` 型（17 組），和 experiment.md 的說法一致。`record.json` 的 R3-pilot 也寫了「for full-class leads」。**但 `RESEARCH.md` 仍然寫「這是負面結果：這個公式庫找不到新東西」，這正是 M1 要求拿掉的過強說法**（見必修 F1）。 | 紀錄本身已修，摘要未修 |
| **M2**（化約的適用範圍） | `run.py` 的 `REDUCTION` 字串已寫上「for w >= 2 … (fails at w = 1)」和「for w >= 4 … (fails at w = 1, 2, 3)」；experiment.md 同步更新；`tests/test_r003.py` 改成明確檢查 w ≥ 2、w ≥ 4 成立，而且小寬度確實不成立。 | 已修 |
| **M3**（來源紀錄） | `c02_iff_check.py` 已放進 `research/r001/m14/` 並 commit。`record.json` 有 `experiment_commit = 407efb9…`。重跑後 `r003_pilot.json` 的 `meta.commit = 407efb9`，這個 commit 確實包含 `research/r003/`。**但新的 `r003_pilot.json` 和 `record.json` 都還沒 commit**：已 commit 的版本仍然是 `meta.commit = 8ff88e6`，而且沒有 `partial_leads_unanalysed`（見必修 F2）。 | 內容已修，尚未 commit |
| **M4**（CI 未跑） | 我用 `gh` 查了兩次 CI：run 45014528005（`e6c3e79`）和 run 45014862688（`57ec73d`，headSha `57ec73d4…`），`lean` 工作的 build 都是 success。後者的 log 裡有 `AXIOMS Discovery.RadSigma.c02_iff: [propext, Quot.sound, Classical.choice]`、`AXIOMS Discovery.SigmaOdd.c01_even_v2_eq_eleven: [...]`、`AXIOMS Discovery.SigmaOdd.c01_of_not_two_pow_twentythree_dvd: [...]`、`THEOREM_COUNT 100`。`57ec73d` 之後 `lean/` 沒有改動，所以這次 CI 涵蓋目前的 Lean 原始碼。 | 已修 |

### B. Lean 定理是否真的對應猜想

1. **C02（H1）↔ `Discovery.RadSigma.c02_iff`**
   - 我逐字比對了敘述（`RadSigmaIff.lean` 的主定理）和 hypotheses.md 的 H1：前提只有 `0 < n`；左邊是 `rad (σ 1 n) = σ 1 (rad n)`；右邊是 `(Squarefree n ∧ Squarefree (σ 1 n)) ∨ ∃ a p, n = 2^a * p ∧ p.Prime ∧ Odd p ∧ Odd a ∧ 3 ≤ a ∧ Squarefree (p+1) ∧ ¬ 3 ∣ (p+1) ∧ rad (2^(a+1) - 1) ∣ 3*(p+1)`。這和 H1 完全一致。
   - `rad` 定義為 `∏ p ∈ n.primeFactors, p`，`σ` 是 Mathlib 的 `ArithmeticFunction.sigma`（經由 `open ArithmeticFunction`）。
   - 兩個方向都有實際證明：正向用 `Nat.exists_eq_two_pow_mul_odd` 拆開 n，分成 m = 1 和 m = p^b 兩種情形；反向的兩個分支都完整。
   - 我同意 critic 的結論：`Odd a` 是必要條件，`Odd p`、`3 ≤ a` 是多餘但無害的條件。
2. **C01（H2）↔ `Discovery.SigmaOdd.c01_of_not_two_pow_twentythree_dvd`**
   - 敘述是：`0 < n` 且 `¬ 2^23 ∣ n` 時，`σ 1 (sigmaOdd n) = sigmaOdd (σ 1 n) ↔ Odd n ∧ IsSquare n`，和 H2 一致。
   - 證明分成 a < 11（沿用舊定理）、a = 11（`c01_even_v2_eq_eleven`）、12 ≤ a ≤ 22（`mersenne_not_abundant_ext`，逐一寫出分解，用 `norm_num`）三段，涵蓋完整。
   - **只是部分結果**：v₂(n) ≥ 23 仍然開放，紀錄有如實寫出。
3. **禁用項目**
   - `grep` 四個相關 Lean 檔：沒有 `sorry`、`admit`、`native_decide`、`axiom` 宣告，也沒有自訂 notation 或 instance。
   - 只有小型 `decide`，用在 `Odd 0`、`Odd 2` 這類判斷，以及舊檔 a ≤ 10 的 Mersenne 檢查，這些都是核心可檢查的。
   - CI 的 AxiomCheck 也確認只用到三個標準公理。

### C. 結論是否被證據支持

- **C02：**
  - 這是 Lean 對所有 n ≥ 1 的證明，不是範圍內的檢查。數值核對（n ≤ 10⁶，0 不符）只是用來確認 Lean 敘述沒有寫錯。
  - 紀錄沒有把「範圍內成立」說成證明；反過來，它把「已證明」放在 `SUPPORTED_NOVELTY_UNCHECKED` 底下，這是規範的詞彙限制造成的（見 E1）。
- **C01：**
  - 紀錄寫的是「Lean 證到 v₂(n) ≤ 22，≥ 23 開放」，說法正確。
  - proof.md「C01 延伸／編譯結果」那一段開頭寫「本機編譯，沒有跑 CI」，結尾卻又寫「CI：通過」，前後矛盾（見建議 S1）。
- **R-003 試點：**
  - 9 條非平凡線索都撐到 w = 30。兩條新的化約（154、167）我也用自己的模擬器在 w ≤ 15 重新驗過。
  - 「全部化約到已知」只適用於「每個剩餘類都吻合」的線索。紀錄本身有寫清楚，但 RESEARCH.md 沒有（F1）。
  - 另外，24 組部分線索只在 w ≤ 22 擬合過，沒有在 23 ≤ w ≤ 30 重新核對，紀錄應該註明（S2）。
- **R3-L01：**
  - 我用自己的模擬器確認了奇數 3 ≤ w ≤ 27 時 P₂₆(w) = w·2^{⌊log₂ w⌋}，0 不符。
  - 這條線索標成 L0、沒有證明、新穎性未查，紀錄說法正確。

### D. 新穎性

- `literature.md` 已經補上 critic 要求的難度評估：「⇒」方向用 LTE 或 Zsigmondy，大約是習題程度，主要價值在 Lean 形式化。
- A065301 那一部分標成 `MATCH_FOUND`（已知）。
- 沒查到的管道都有誠實列出原因：MathSciNet、Google Scholar、Semantic Scholar、Crossref，以及論文全文。
- `python -m discovery.evidence check`：0 problems。10 筆存證都有平台與結果。
- 不足之處：
  - S008～S010 查的是規則 54，不是 C02 或 R-003。所以 C02 這一輪實際新增的查詢只有 S001～S007（zbMATH、arXiv、MathOverflow、Math.SE），OEIS 那一筆仍然是 DISC-0006-S003。
  - critic 建議用含 a = 7 解（413312、935552）的片段再查一次 OEIS，這一項沒有做（不是必修）。
- `novelty.status = NO_MATCH_IN_SCOPE` 是正確的，不能自動升級，`open` 也列出了 C02、C01、R3-L01。紀錄完全沒有宣稱新穎。

### E. 狀態詞彙的問題（給 CEO）

- **E1：** C02 已經由 Lean 完整證明並通過 CI，但規範裡沒有「已證明、新穎性未定」這種狀態。
  - `PROVEN_KNOWN` 要求結果已知，可是沒有找到出處，「習題程度」也不等於「已知」。
  - `PROVEN_POSSIBLY_NEW` 要求新穎性到 `PENDING_REVIEW` 以上，而這需要人確認。
  - 所以 C02 只能標 `SUPPORTED_NOVELTY_UNCHECKED`，並在 `proof` 欄寫明「Lean 完整證明，CI 通過」。我同意這個保守的做法。
  - 但讀者可能被「SUPPORTED（只在範圍內成立）」誤導。建議 CEO 決定以下兩者之一：
    - 修訂規範，加一個 `PROVEN_NOVELTY_UNCHECKED`；
    - 或者由人審查後把 C02 的新穎性改成 `PENDING_REVIEW`，C02 就可以升為 `PROVEN_POSSIBLY_NEW`。
- **E2：** R3-pilot 標 `REFUTED`。規範中 REFUTED 的定義是「反例由兩套實作確認」，而 H3 是存在性的探索假設，嚴格來說沒有「反例」可言。不過 hypotheses.md 事先寫好了推翻條件，「每個剩餘類都吻合」的線索也確實全部化約到已知，而且 `record.json` 寫了適用範圍（「for full-class leads」）。我接受 `REFUTED`，條件是任何對外說法都要附上這個限制。

## 重現結果

環境：Python 3.13.18，HEAD `407efb9`。

| 指令 | 結果 | 和紀錄一致？ |
|---|---|---|
| `python -m pytest -q tests/test_r003.py` | 4 passed（18 秒） | 是 |
| `python research/r001/m14/c02_iff_check.py 200000` | `solutions 8988 mismatch 0 second-branch 158`，前 10 個從 416 開始 | 是（和 critic 表格一致） |
| `python research/r001/m14/c02_iff_check.py 1000000` | `solutions 39234 mismatch 0 second-branch 671` | 是（和 experiment.md、proof.md 一致） |
| `python -m research.r003.run` | 37 秒；counts = {leads 150, mirror_reps 82, nontrivial 9, nontrivial_unreduced 0, partial_unanalysed 24} | 是 |
| `python -m discovery.check_record` | 補本檔之前只有 `FAIL DISC-0007: missing review.md`；STATUS 和 record.json 一致 | 補上本檔後應該會通過 |
| `python -m discovery.evidence check` | 0 problems | 是 |
| `gh run view 45014528005` / `45014862688` | 兩次都是 success；後者 headSha 是 `57ec73d`，log 中三個被引用的定理都只用標準公理 | 是 |
| 審查者自寫模擬器（scratchpad，不 import repo） | P₂₆ 奇數 3 ≤ w ≤ 27：0 不符；154 = 26（2 ≤ w ≤ 15）；(T,P)₁₆₇ = (T₂₆+1, P₂₆)（4 ≤ w ≤ 15） | 是 |

**關於 `r003_pilot.json`：**
- 重跑前我先把工作樹的版本備份到 scratchpad。重跑的輸出和工作樹上未 commit 的版本**逐位元組完全相同**，`meta.commit` 也同樣是 `407efb9`。
- 我**沒有**照任務說明執行 `git checkout records/DISC-0007/r003_pilot.json`。原因是那會把檔案還原成 git 裡已過時的版本（`meta.commit = 8ff88e6`、沒有部分線索），反而把作者已修好的 M3 改回去。
- 工作樹目前和我審查前完全相同。

## 最終判定

STATUS: SUPPORTED_NOVELTY_UNCHECKED

**各候選狀態：**

| 候選 | 狀態 | 理由 |
|---|---|---|
| C02（研究目標） | `SUPPORTED_NOVELTY_UNCHECKED` | Lean `c02_iff` 對所有 n ≥ 1 完整證明，CI 與 AxiomCheck 都通過。新穎性 `NO_MATCH_IN_SCOPE`，而且是習題程度，所以不能用 `PROVEN_POSSIBLY_NEW`；沒有出處，所以也不能用 `PROVEN_KNOWN`（見 E1）。 |
| C01 | `SUPPORTED_NOVELTY_UNCHECKED` | Lean 只證到 v₂(n) ≤ 22，不完整。 |
| R3-pilot（H3） | `REFUTED`（限「每個剩餘類都吻合」的線索） | 預先寫好的推翻條件成立；24 組部分線索沒有逐條化約（見 E2）。 |
| R3-L01 | `SUPPORTED_NOVELTY_UNCHECKED`（L0） | 有限範圍擬合，兩套實作加上審查者的模擬器都一致；沒有證明，新穎性 `NOT_CHECKED`。 |

- **紀錄層級新穎性：** `NO_MATCH_IN_SCOPE`（不升級）。A065301 那一部分是 `MATCH_FOUND`。`NOVELTY_SUPPORTED`／`NOVELTY_CONFIRMED` 只能由人給，本審查不給。
- **M1.4（至少一個完整成果）：達成。**
  - C02 有精確敘述、Lean 完整證明（CI 通過、沒有 sorry、沒有額外公理）、敘述對數值的核對（10⁶）、文獻查證（限制有如實寫出）、critic 和獨立審查。
  - 它是「完整成果」，**不是「新發現」**。
- **習題等級與各項限制有沒有誠實寫出：** 有。literature.md、record.json 的 `novelty.note`、RESEARCH.md 都寫了「習題程度」和「不宣稱新」。C01 的開放範圍、R3-L01 的 L0 等級、沒查的管道也都有寫。唯一例外是 RESEARCH.md 對 R-003 的說法過強（F1）。

**合併前必修：**

- **F1：** `RESEARCH.md` 的 DISC-0007 段落「R-003 試點」那一條，把「這是負面結果：這個公式庫找不到新東西」改成縮小後的說法，例如「對每種情形都吻合的 9 條線索是負面結果；24 組部分吻合的線索形式上屬於規則 90 家族，但沒有逐條化約，不下結論」。同一段「約一萬種公式」也請核對：9 種 G × 6 種 h × 3 個 a × 7 個 b = 1,134 種形狀，再乘上剩餘類數，不是「約一萬種公式」。
- **F2：** 把 `records/DISC-0007/record.json`（目前未追蹤）、重跑後的 `r003_pilot.json`（`meta.commit = 407efb9`，含 `partial_leads_unanalysed`）、`RESEARCH.md`、`DEVLOG.md` 和本檔一起 commit。否則 git 裡的 `r003_pilot.json` 仍然指向沒有程式的 `8ff88e6`，M3 等於沒修。commit 之後再跑一次 `python -m discovery.check_record` 和 `python -m pytest -q`。

**建議（不擋合併）：**

- **S1：** proof.md「C01 延伸／編譯結果」刪掉開頭「沒有跑 CI」那句，或改成「先本機編譯，之後 CI 通過」。
- **S2：** experiment.md 註明 24 組部分線索只在 w ≤ 22 擬合過，沒有在 w ≤ 30 重新核對。
- **S3：** `run.py` 的 `meta.commit` 在工作樹有改動時應該加上 `-dirty`，和 RESEARCH_STANDARDS §2c 一致。
- **S4：** 用含 a = 7 解（413312、935552）的片段再查一次 OEIS；下一輪把 Semantic Scholar、Crossref 補上。
- **S5：** 請 CEO 處理 E1 的詞彙缺口。

## 給 CEO 的摘要

- **M1.4 達成。** C02「rad(σ(n)) = σ(rad(n)) 的完整解集」已經在 Lean 兩個方向都證完，GitHub CI 編譯和公理檢查都通過，我親自查過 CI 紀錄。這是專案第一條從電腦探索走到完整形式證明的結果。
- **不是新發現。** 查過的資料庫裡沒有它，但證明只用標準技巧（LTE），大約是習題程度，第一類解也早就在 OEIS（A065301）。紀錄沒有宣稱新穎，我也不建議宣稱。
- **C01** 推進到「n 裡 2 的次方 ≤ 22」都已證明；≥ 23 仍然開放。
- **R-003 試點** 是負面結果，但只限「每種情形都吻合」的 9 條公式。另外有 24 組只部分吻合的公式沒有逐條分析；critic 另外找到一條公式庫表達不了的線索 R3-L01（規則 26 奇數寬度的週期），留到下一輪。
- **所有數字我都重跑過，結果一致。**
- **合併前要修兩件事：**
  1. RESEARCH.md 對 R-003 的說法太強。
  2. record.json 和更新後的結果檔還沒 commit。
- **需要您決定：** 規範沒有「已證明、但新穎性未定」這種狀態，所以 C02 現在只能掛 `SUPPORTED_NOVELTY_UNCHECKED`。這個標籤字面上是「只在範圍內成立」，會低估它已經被證明這件事。請決定要新增狀態，還是由人審查後把新穎性改成 `PENDING_REVIEW`。
