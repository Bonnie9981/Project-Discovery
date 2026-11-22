STATUS: SUPPORTED_NOVELTY_UNCHECKED

# DISC-0006 審查（M1.3：C01、C02、R2-C10 初篩）

- 審查者：Reviewer agent（獨立，不是本紀錄的作者，也不是 critic 或 proof agent）
- 審查對象：分支 `claude/project-thread-m5yt21`，commit `58fb4c9`（工作樹乾淨）
- 讀過的檔案：`records/DISC-0006/` 的 `literature.md`、`hypotheses.md`、`experiment.md`、`critic.md`、`proof.md`、`record.json`、兩份 JSON；`research/r001/m13/extend_ab.py`、`research/r002/m13_rule54.py`；`lean/Discovery/{SigmaOdd,RadSigma,Rule54}.lean`、`lean/Discovery.lean`、`lean/AxiomCheck.lean`；`docs/RESEARCH_STANDARDS.md`。
- 審查者自己的程式放在 scratchpad，不進 repo，也沒有 import `research.*` 或 `discovery.*`：
  - C01／C02 用最小質因數篩做分解，再由分解公式算 σ、rad，和 repo 的試除（impl_a）、篩表（impl_b）、critic 的因數和篩都不同；
  - Mersenne 數用自寫的 Miller–Rabin 加 Pollard rho 分解，a = 11 的情形用 `Fraction` 精確計算；
  - 規則 54 用逐格查 Wolfram 規則表（`54 >> (4l+2c+r) & 1`）的 list 模擬，tuple 當 dict key 來偵測循環。

## 審查項目

### A. 自動檢查

1. `python -m discovery.check_record`：只有 `FAIL DISC-0006: missing review.md` 這一項。補上本檔後應該會通過，前提是 STATUS 和 record.json 一致，本檔已一致。
2. `python -m discovery.independence`：`checked 3 research dirs with impl_*.py, 0 problems`。
3. `python -m pytest -q`：47 passed，2 failed。
   - `tests/test_records.py::test_all_committed_records_pass`：原因是缺 review.md，本檔補上後就會通過。
   - `tests/test_research_summary.py::test_every_record_has_plain_summary`：**`RESEARCH.md` 沒有 `## DISC-0006` 這一節。本檔補不了，合併前必修。**
4. `python -m discovery.evidence check`：0 problems。不過那是因為 DISC-0006 **根本沒有** `search_evidence.jsonl`，見 E3。

### B. C02 紙本證明（proof.md 第 1–6 步、critic.md 第 3 點）

我逐步核對，**每一步都正確**：

- **rad n ∈ {1, 2, p, 2p}。** σ(rad n) = Π(q+1) 等於一個 radical，所以必須無平方因子。兩個相異奇質數會使 4 | (q₁+1)(q₂+1)。正確。Lean `odd_prime_factor_unique` 證了這一步。
- **n = 2^a。** 條件化成 2^(a+1) − 1 = 3^k。a ≥ 2 時左邊 ≡ 7 (mod 8)，3^k ≡ 1 或 3 (mod 8)，所以只剩 n = 2。proof.md 用 mod 8，critic 用 LTE，兩種都對。
- **n = 2^a·p^b 推出 b = 1。**
  - σ(rad n) 是偶數，所以 σ(p^b) 也要是偶數，b 是奇數。令 b + 1 = 2m，σ(p^b) = (p+1)·C，C = Σ_{i<m} p^{2i}。
  - C 的每個質因數 r 都必須屬於 σ(rad n) 的質因數集合，也就是 p + 1 的質因數，a ≥ 1 時再加上 3。
  - 對 r | p + 1（含 r = 2，因為 p² ≡ 1 mod 8），LTE 給出 v_r(p^{2m} − 1) = v_r(p² − 1) + v_r(m)，所以 v_r(C) = v_r(m)。
  - 對 r = 3 ∤ p + 1：p ≠ 3（p = 3 時 p + 1 = 4 不是無平方因子），所以 p ≡ 1 (mod 3)，3 | p² − 1，同一個式子仍然成立。
  - 於是 C | m。但 m ≥ 2 時 C ≥ 1 + p²(m−1) > m，矛盾。正確。
- **n = 2^a·p（a ≥ 1）。** 3 ∤ p + 1，而 3 | σ(n) = (2^(a+1) − 1)(p+1)，所以 3 | 2^(a+1) − 1，a 是奇數。a = 1 落在 A065301。正確。
- **H2′ 的反方向**（符合條件的 2^a·p 都是解）：proof.md 沒有寫，critic 第 (iv) 點有寫。我自己補驗：3(p+1) 無平方因子，且 rad((2^(a+1) − 1)(p+1)) = rad(3(p+1))，因為 a 奇時 3 | 2^(a+1) − 1，而且 rad(2^(a+1) − 1) | 3(p+1)。成立。
- **結論：C02 和 H2′ 都有完整而正確的紙本證明。** 這是約一頁的初等論證（無平方因子 + LTE）。Lean 只覆蓋其中容易的部分，見 D。

### C. C01 紙本證明，以及「已證範圍」到底是多少

1. **奇數 n：** 正確，Lean `c01_odd` 已完整證明。
2. **偶數化約：**
   - 記 n = 2^a·m，σ(m) = 2^b·t，q = 2^(a+1) − 1。
   - 等式 ⇔ σ(qt) = (2^(b+1) − 1)σ(t)。
   - 由 qσ(t) < σ(qt) ≤ σ(q)σ(t) 推出 b ≥ a + 1，再推出 σ(q) ≥ 2q + 1。
   - 嚴格不等式的理由：q > 1 時 qt 是 qt 的因數，但不是 t 的因數。
   - 每一步都正確，Lean `c01_even_of_not_abundant` 已證。
3. **「奇部分是平方數」分支：** 正確。q ≡ 3 (mod 4) 不是平方數，Lean 已證。
4. **過剩的 Mersenne 數：** 我自己分解 2^k − 1（k ≤ 60），過剩的只有 k ∈ {12, 24, 36, 40, 48, 60}，和 critic 一致。
5. **a = 11（q = 4095 = 3²·5·7·13，σ(q) = 8736）：**
   - 比值 σ(qt)/σ(t) = Π_{p|q} σ(p^{e+f})/σ(p^f) 只依賴 f_p = v_p(t)，而且對每個 f_p 遞減。
   - 目標是 2^(b+1) − 1，其中 b ≥ 12，所以目標 ≥ 8191；又因為 8736 < 16383，唯一可能的目標就是 8191。
   - 全部 f_p = 0 時比值是 8736 ≠ 8191。
   - 只要有一個 f_p ≥ 1，比值最大是 8156.57（取 p = 13、f = 1，我用 `Fraction` 精確算出）< 8191。
   - **所以 a = 11 確實排除，論證完整，而且只是有限的手算。**
   - critic 給的近似值 8155.6 有些微誤差，不影響結論。
6. **已證範圍的結論：**
   - **Lean：** v₂(n) ≤ 10（`c01_of_not_two_pow_eleven_dvd`，也就是 2¹¹ ∤ n）。
   - **紙本：** 所有 v₂(n) = a 且 a + 1 ∉ {12, 24, 36, 40, 48, 60, …}（2^(a+1) − 1 不過剩）的 n，加上 a = 11。因此 **v₂(n) ≤ 22 全部成立**。另外 23 ≤ v₂(n) ≤ 34 中除了 v₂(n) = 23 以外也都成立。仍然開放的是：v₂(n) + 1 屬於過剩 Mersenne 指數（24、36、40、…），而且 σ(m) 的奇部分不是平方數。
   - record.json 寫「paper up to v2(n) <= 22」，**正確**。
   - **但 proof.md 的總表寫「v₂(n) = 11 … 仍開放」，和 critic、record.json 不一致**（proof agent 沒有採用 critic 的 a = 11 論證）。要修，見「最終判定」。
7. **數值證據的效力：** 我同意 critic。依上面的引理，偶數反例必須 v₂(n) ≥ 23，所以 10⁶、2×10⁶ 的檢查對偶數情形沒有證據力。experiment.md 說「反例最小約 5.5×10⁶」是排除 a = 11 之前的下界，偏保守，不算錯。

### D. Lean 敘述與 proof.md「定理對照」

- **編譯：** 用 proof agent 在 scratchpad 建好的環境：Lean 4.15.0，Mathlib `git describe` = `v4.15.0`，和 `lakefile.toml` 一致。我把三個檔各自加上 `AxiomCheck.lean` 的 `#check_discovery_axioms` 重新編譯。
  - 三檔都 exit 0，`THEOREM_COUNT` 分別是 21、7、7，和 proof.md 一致。
  - 公理只有 `propext`、`Classical.choice`、`Quot.sound` 的子集，沒有 `sorryAx`，也沒有 `Lean.ofReduceBool`。
  - `grep` 找不到 `sorry|admit|native_decide|axiom|implemented_by|extern|unsafe`，只有兩處 `set_option maxRecDepth`，這是無害的。
  - 我**沒有**編譯 `lean/Discovery.lean`（它匯入全部模組），也沒有跑完整的 `lake build`，**要以 GitHub CI 的 lean 工作為準**。
- **對照表逐條比對：** proof.md 列的每個定理名稱都存在，假設和結論也都和表上一致。
  - `lt_sigma_mul` 要求 1 < q、0 < t。
  - `c01_even_of_not_abundant` 的 hdef 是 σ(q) ≤ 2q。
  - `c01_of_not_two_pow_eleven_dvd` 要求 0 < n、¬ 2¹¹ ∣ n，結論是 ⇔ Odd n ∧ IsSquare n。
  - `check_range` 的範圍是 w < 201、6 ≤ w。
  - **沒有發現漏掉 hypotheses、敘述偏弱或敘述錯置的情形。**
- **定義：**
  - `sigmaOdd` 是奇因數和，也就是 A000593。
  - `rad n = ∏ primeFactors`，rad 0 = 1，對 n ≥ 1 沒有影響。
  - 我逐一核對了 Rule54 的 `step` 位元運算：left 的第 i 位是 x_{i−1}，right 的第 i 位是 x_{i+1}，new = c ⊕ (l ∨ r)。8 種鄰域都等於 54 = 00110110₂。
  - `Check` 裡「T = 0 或 x_{T+3} ≠ x_{T−1}」配合 `periodic_from`，確實推出 T 是最小值。
- **要誠實標示的弱點**（proof.md 都已經寫明，我只是確認）：
  - C02 的主要分類（2^a·p^b 的 LTE 部分、b = 1、a 奇）**沒有任何 Lean 定理**。`c02b` 是一步推論（A065301 ⊆ 解集）。所以 C02 的 Lean 覆蓋只是「必要條件：至多一個奇質因數」加上容易的方向。
  - Rule54 的 `step` 和「逐格規則表」的等價沒有在 Lean 裡證明（我已人工核對）。
  - Rule54 只有 6 ≤ w ≤ 200 的有限核驗，不是一般定理。

### E. 新穎性與文獻

1. record.json 的 `novelty.status = NO_MATCH_IN_SCOPE`，note 寫明「not evidence of novelty」以及沒查 arXiv、MathSciNet。**沒有過度宣稱。**
2. **critic.md 已過時的部分：** critic.md 說 oeis.org 回 403、沒看到 COMMENTS（攻擊項目 C02 第 4 點、未解決疑點第 2 點），後來已由 literature.md 用 Chrome 讀 A065301 線上條目全文補上（查詢 #4）。**應以 literature.md 為準。**
   - literature.md 記錄了 Eldar（2025）的刻畫：k 無平方因子，質因數都在 A049097，而且 {p+1 : p | k} 兩兩互質。這和 critic 的「副產品」A065301 = {1,2} ∪ {p : p+1 無平方因子} ∪ {2p : 3(p+1) 無平方因子} **等價**：兩兩互質推出至多一個奇質數；和 2 並存時 3 ∤ p + 1。
   - **所以這個副產品是已知的，不能列為發現。** 我也數值確認了它到 2×10⁶ 和 A065301 相同。
3. **流程缺口：** 第 1b 節第 3 層要求每次瀏覽器查詢都用 `python -m discovery.evidence add` 寫進 `search_evidence.jsonl`，內容包括 UTC 時間、完整查詢字串、證據 URL、覆蓋限制。DISC-0006 **沒有這個檔**，只有 literature.md 的表格，而且表格沒有 URL 和時間。另外 `oeis_offline@sha256:c6d34403102c` 列在 sources_checked，但 literature.md 沒寫離線查了哪些序列（只有 critic.md 提到規則 54 那兩條）。
4. **序列抽查：** literature.md 查詢 #1–#3、#5 用的數列，我用自己的程式重算，完全相符。例如 397…461 這一段是連續的解；A065301 以外的前 7 個解是 416, 872, …, 6152；T₅₄ 從 w = 8 起是 2, 6, 2, 2, 4, 10, …。
5. **1c 的要求：**
   - record.json 的 `candidates` 是自由文字，沒有逐條列出合法狀態。
   - 沒有 `novelty.open` 欄位。依 1c，C01、C02、R2-C10 各自的新穎性未解問題都要列進去。

### F. R2-C10

- 只有有限範圍的核驗：Lean `decide` 6 ≤ w ≤ 200；三套實作到 w = 300；critic 到 1200；我到 400。proof.md 誠實標為「證明失敗」。
- critic 的光錐 + ether 草稿有說服力（w ≡ 0, 2, 3 的情形接近一步），但沒有寫成正式證明。w ≡ 1 只有數值支持的機制說明。
- critic 的 Hanson–Crutchfield 粒子對應是憑記憶，沒有查證原文，不可以引用為已知結果。

## 重現結果

| 項目 | 指令／方法 | 結果 |
|---|---|---|
| R2-C10 三套實作 | `python -m research.r002.m13_rule54 300`（3.5 s） | 和 `rule54_abc_300.json` **逐字相同**（failures = []，periods_seen = [4]） |
| C01／C02 A、B 實作 | `python -m research.r001.m13.extend_ab 1000000`（1 分 55 秒） | 和 `extend_ab_1e6.json` **逐字相同**：C01 的 A、B 各 0 個失敗；C02 解集相同，共 39234 個，0 個違反 |
| 審查者 C02／H2′ | 自己的 spf 篩，N = 10⁶ 和 2×10⁶ | 10⁶：解 39234，A065301 38563，額外 671，H2′ 預測 671，**集合完全相等**。2×10⁶：解 74471，A065301 73213，額外 1258，H2′ 預測 1258，**集合完全相等**；a 的分布是 3：1038、5：216、7：4，和 critic 一致。A065301 ⊆ 解集；A065301 結構式到 2×10⁶ 相等 |
| 審查者 C01 | 同一支程式，n ≤ 2×10⁶ | 0 個失敗（偶數情形依 C.7 沒有證據力） |
| Mersenne 過剩 | 自寫 MR + rho，k ≤ 60 | {12, 24, 36, 40, 48, 60} |
| a = 11 排除 | `Fraction` 精確計算 | 至少一個 f ≥ 1 時比值最大 8156.57 < 8191，f 全為 0 時是 8736 ≠ 8191：排除 |
| critic 的大 a 解 | 自寫分解，直接驗證等式 | 5935616 (a=9)、20498432 (a=11)、1699979264 (a=13)、41517350912 (a=15)：p 都是質數，等式都成立 |
| 規則 54 | 自己的查表模擬，6 ≤ w ≤ 400 | 0 個和公式不符；w = 1..7 是 (1,1),(2,1),(2,1),(0,4),(5,1),(0,4),(0,4)，和 critic 一致 |
| Lean | 三檔各自加上 axiom check，Lean 4.15.0 + Mathlib v4.15.0 | 全部通過，21/7/7 個定理，只用標準公理（見 D） |
| check_record／independence／pytest | 見 A | 除了 review.md 和 RESEARCH.md 摘要之外沒有其他問題 |

experiment.md 的重現指令可以照著跑，結果一致。但 critic 的 2×10⁶ 程式和 a = 11 的 DFS 放在 scratchpad，**不在 repo**，只能靠本審查的獨立重算佐證。experiment.md 也沒有記錄 Python 版本（本機是 3.13.18）和 commit。

## 最終判定

STATUS: SUPPORTED_NOVELTY_UNCHECKED

我同意 record.json 現在的狀態。理由：

- 依 1c，整份紀錄取研究目標的狀態。
- 三條都沒有完整的 Lean 證明，所以不能給 `PROVEN_*`。
- 新穎性只到 `NO_MATCH_IN_SCOPE`，沒有到 `PENDING_REVIEW`，所以不能給 `SUPPORTED_POSSIBLY_NEW`。
- 沒有反例，也沒有實作不一致，所以不是 `REFUTED`，也不是 `INCONCLUSIVE`。

逐條狀態：

| 候選 | 狀態 | 證明情形 | 新穎性 |
|---|---|---|---|
| C01 | `SUPPORTED_NOVELTY_UNCHECKED` | 奇數 n：Lean 已證。偶數：Lean 證到 v₂(n) ≤ 10；紙本證到 v₂(n) ≤ 22，而且凡是 2^(v₂+1) − 1 不過剩的都成立。開放的是 v₂(n) + 1 ∈ {24, 36, 40, 48, 60, …} 且 σ(奇部分) 的奇部分不是平方數 | NO_MATCH_IN_SCOPE（OEIS 比對不到這種刻畫，實際上沒有查） |
| C02（及 H2′） | `SUPPORTED_NOVELTY_UNCHECKED` | **紙本完整證明**，經本審查逐步核對正確；Lean 只有部分（A065301 ⊆ 解集、至多一個奇質因數） | 解集序列在 OEIS 查無。A065301 的結構副產品**已知**（Eldar 2025 的等價刻畫） |
| R2-C10 | `SUPPORTED_NOVELTY_UNCHECKED` | 只有有限核驗：Lean w ≤ 200，數值到 1200；一般證明失敗（有機制草稿） | 暫態序列在 OEIS 查無 |

**M1.3 是否達成：達成（有條件）。** 三條都存活 critic、都有證明嘗試（C02 成功，C01 部分成功，R2-C10 失敗但有機制說明，所以都不是數值巧合）、都做了文獻查證、也都經過本次獨立審查。條件是下面的「合併前必修」都完成，而且 CI 的 lean 工作通過。

**合併前必修：**

1. `RESEARCH.md` 補 `## DISC-0006` 白話摘要。目前 pytest 因為缺這一節失敗。
2. GitHub CI 的 lean 工作（包含 `lean/Discovery.lean` 匯入三個新模組、`AxiomCheck`、`lean_decls`）必須通過。proof.md 的「CI 連結：待推送後補上」要補上。
3. 建立 `records/DISC-0006/search_evidence.jsonl`，用 `python -m discovery.evidence add` 補記 literature.md 的 7 筆查詢，以及 critic 的離線快照查詢。要寫明 UTC 時間、完整查詢字串、證據 URL 和限制。
4. record.json 依 1c 補兩件事：一是逐條候選的合法狀態，用上表的狀態；二是 `novelty.open`，列出 C01、C02、R2-C10 各自的未解新穎性問題，並註明「A065301 結構式已知（Eldar 2025）」。

**建議修正（不阻擋合併）：**

5. proof.md 總表和 C01 段落寫「v₂(n) = 11 仍開放」，要改成「紙本已排除（critic 第 3 點的有限比值論證，已經 reviewer 核驗），只有 Lean 還沒有」。這樣才和 record.json 一致。
6. critic.md 的「OEIS 回 403、沒看到 COMMENTS」已過時。不改 critic 原文的話，請在 literature.md 加一句註明已由 Chrome 查詢 #4 取代。
7. experiment.md 補 Python 版本和 commit。把 critic 的 2×10⁶ 與 a = 11 程式放進 repo，或者寫明只有 reviewer 的獨立重算可以佐證。
8. 任何對外文字都不能把 C02 說成「已證明（PROVEN）」。正確寫法是「紙本已證、Lean 部分」。R2-C10 要寫「w ≤ 200 Lean 有限核驗」，不能寫成定理。

## 給 CEO 的摘要

- 三條候選都通過了初篩：沒有被反駁，數字我獨立重算都對得上，Lean 檔編譯通過，也沒有作弊（沒有 sorry，沒有非標準公理）。**M1.3 算達成**，但合併前還要補四件文書工作：RESEARCH.md 摘要、確認 CI 通過、補查詢證據檔、record.json 逐條狀態。
- **C02（rad∘σ = σ∘rad）是這批最好的成果：** 已經有完整、正確的紙本證明，而且證出的是比原猜想更精確的「完整刻畫」。不過它只是一頁的初等論證，Lean 也只證了一小部分，所以不能叫「已證明」。其中關於 A065301 結構的副產品，文獻（Eldar 2025）已經有了。
- **C01：** 奇數情形和大部分偶數情形已證（紙本證到 2 的次方數 ≤ 22，Lean 證到 ≤ 10）。剩下的情形，電腦數值檢查根本碰不到，要靠數學才能解決。
- **R2-C10（規則 54）：** 只驗證了有限範圍（Lean 到寬度 200，模擬到 1200），沒有一般證明。
- 三條在 OEIS、OpenAlex 都**查不到**，但這不代表是新的。目前一律不可以對外宣稱是新發現。

## 合併後追記（DISC-0007 整理時補）

上面「合併前必修」1～4 在 PR #13 合併前都已完成：`RESEARCH.md` 有 `## DISC-0006`；CI 的 lean 工作通過（https://github.com/Bonnie9981/Project-Discovery/actions/runs/45011976606），proof.md 已補連結；`search_evidence.jsonl` 有 S001～S007；record.json 有逐條狀態和 `novelty.open`。建議修正 5、6 也已處理（proof.md 總表、literature.md 補註）。第 7 項：experiment.md 已寫明 Python 版本與 commit，並註明 critic 的兩支程式不在 repo、只有審查員的獨立重算佐證。這段是作者追記，不是審查員的判斷。
