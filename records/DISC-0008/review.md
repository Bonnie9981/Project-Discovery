STATUS: PROVEN_KNOWN

# DISC-0008 獨立審查（R3-L01：規則 26，奇數寬度環，單一種子的週期）

審查者：reviewer（獨立 subagent，不是作者，也不是 critic）。審查對象：branch `claude/project-thread-m5yt21`，HEAD cb549ac。Lean 與程式以 af98758 為準（`git diff af98758 HEAD -- lean/ research/` 為空）。

## 審查項目

1. **結論是否有證據支持，有沒有把「範圍內成立」說成「證明」。**
   - 一般證明有兩份：proof.md 的紙上證明，以及 `lean/Discovery/Rule26.lean` 的 Lean 證明，涵蓋所有奇數 w ≥ 3，不是有限範圍的驗證。數值結果（w ≤ 61、w ≤ 129）在 experiment.md 裡明確寫成「只是佐證」。**沒有把數值結果當成證明。**
   - 反過來的問題：record.json 的整體狀態和 `candidates.R3-L01.status` 都是 `SUPPORTED_NOVELTY_UNCHECKED`。依 RESEARCH_STANDARDS §1，`SUPPORTED_*` 的意思是「在測試範圍內成立」。這個猜想已經由 Lean 證明，而且 CI 通過，所以這個狀態**低估了證明的程度**。同時「NOVELTY_UNCHECKED」也和事實不符：新穎性查過了，結果是 `PARTIAL_MATCH`（見最終判定）。

2. **Lean 定理是否真的對應猜想。**
   - `rule26_odd_period (w) (hw : w % 2 = 1) (h3 : 3 ≤ w)` 包含三件事：x_P = x₀；對所有 μ，x_{μ+P} = x_μ；0 < p < P 時 x_p ≠ x₀。其中 `P w = w * 2 ^ Nat.log2 w`。三者合起來就是 (T, P) = (0, w·2^⌊log₂ w⌋)。`iter_eq_one_iff` 證的是 x_t = x₀ ⇔ P ∣ t，也就是 H1 的原文。
   - `step` 的三個項依序對應鄰域 100、011、001，也就是 26 = 00011010₂ 的第 4、3、1 位元。`rotL` 的第 i 位元是細胞 i−1，`rotR` 的第 i 位元是細胞 i+1，和 impl_b 的慣例相同。另外 `tb_step` 證明了 `step` 的每個位元都等於 `rule26 l c r`（`26 >>> (4l+2c+r)`）。我逐行看過，結論和 critic 第 1 項一致。
   - 前提不是空的。w = 1 確實不成立（T = 1），所以 3 ≤ w 是必要條件。
   - `grep` 結果：沒有 `sorry`、`admit`，沒有 `axiom` 宣告，也沒有 `native_decide`、`implemented_by`、`extern`（「native_decide」只出現在檔頭註解）。檔案只 import Lean core。`lean/Discovery.lean` 已經 import `Discovery.Rule26`。
   - CI：用 `gh run view 45017724157` 查到 `name=lean`、`conclusion=success`、`headSha=af98758…`。公理只用了 `propext`、`Quot.sound`、`Classical.choice`，這一點引用 critic 讀過的 log，我沒有再讀一次 log 全文。
   - 限制：`pas`（Pascal mod 2）在 Lean 裡沒有和 `Nat.choose` 連起來。這只影響輔助引理 `iter_testBit` 的解讀，主定理沒有用到 `pas`，所以不受影響。proof.md 已經如實寫出這一點。

3. **Critic 的必修項 F1–F3。**
   - **F1（proof.md 狀態行自相矛盾）：已修。** 第 3 行現在寫「CI `lean` 工作（含公理稽核）已通過：run 45017724157」，和文末一致。
   - **F2（紀錄檔沒有 commit）：已修。** cb549ac 把 `proof_draft.md` 改名為 `proof.md`，也 commit 了 hypotheses、experiment、literature、critic、record.json、search_evidence。experiment.md 寫明 `experiment_commit` af98758 是程式和 Lean 的版本，紀錄檔在之後的 commit 才加入。`git status` 是乾淨的。
   - **F3（Pascal mod 2 是已知事實，新穎性要收窄）：已修。** literature.md 新增一列，說明「規則 26 從單一種子出發，在無限直線上畫出規則 90 的 Sierpiński 圖樣」是已知事實（NKS／Wolfram Atlas），並標明「本輪未上網核對出處」。可能新的部分收窄為「環上的邊界分析加上 Lucas 收尾」，文件中也沒有寫成「新定理」。
   - 建議項也處理了：literature.md 註明 OEIS 公式只適用於 n ≥ 1；proof.md 解釋了腳本輸出中的「Lemma 3」指什麼。

4. **新穎性措辭是否誠實。**
   - 公式本身就是 OEIS A334504 FORMULA 欄的猜想（Zabolotskii 2024，原文「It seems that」）。record.json 記為 `PARTIAL_MATCH`，literature.md 也寫「公式不是我們提出的」。**正確。**
   - 證明的狀態是 `NO_MATCH_IN_SCOPE`，查過的範圍是 OEIS、arXiv、OpenAlex。沒查的來源列得很清楚：Math Fun 郵件列表（Klee 2020）、MathSciNet、zbMATH、Google Scholar。**正確**，而且 R3-L01 也放在 `novelty.open` 裡。
   - 核心想法（Pascal mod 2）是已知的，已經寫明。
   - 證據方面：search_evidence.jsonl 有 S001–S005，`discovery.evidence check` 回報 0 problems。我沒有自己上 OEIS 核對 A334504 的原文，只能依靠 S002 的紀錄（critic 當時也連不上，被 403 擋下）。
   - 小問題（非必修）：RESEARCH.md 第 15 行寫「在查過的範圍內還沒有人證明過」。比較精確的說法是「在查過的範圍內沒找到證明」，前者讀起來像在斷言世界上的事實。

5. **狀態是否合法（`discovery/check_record.py`、`discovery/novelty.py`）。**
   - `SUPPORTED_NOVELTY_UNCHECKED` 和 `PARTIAL_MATCH` 都在合法清單裡，所以原本的寫法程式檢查得過。問題出在語意，見第 1 項和最終判定。
   - `PROVEN_POSSIBLY_NEW` 需要 novelty 到 `PENDING_REVIEW` 以上，而 `PENDING_REVIEW` 要由人確認。所以這個狀態現在不能給。

## 重現結果

環境：Python 3.13.18，工作目錄 `/tmp/claude-0/pd`，HEAD cb549ac。

- `python research/r003/l01_check.py`：輸出 `OK: odd 3 <= w <= 61: closed form (impl_b), period w*2^floor(log2 w) (impl_b Brent + own list sim, return set = multiples of P up to 3P); Lemma 2 (t <= 2000); Lemma 3; even 2 <= w <= 40: orbit = rule 90 orbit`，耗時 0.77 秒。和 experiment.md 一致。
- `python -m discovery.evidence check`：`0 problems`。
- 我另外寫了一個模擬，不用 repo 的任何程式（scratchpad 的 `rev8.py`）：狀態存成 tuple，規則表直接從 26 的位元讀，用 dict 偵測循環。
  - 奇數 3 ≤ w ≤ 47：(T, P) 全部等於 (0, w·2^⌊log₂ w⌋)，沒有任何不符。
  - 1 ≤ w ≤ 13 的 (T, P) 依序是 (1,1) (1,1) (0,6) (2,1) (0,20) (1,2) (0,28) (4,1) (0,72) (1,6) (0,88) (2,4) (0,104)，和 critic 的結果完全相同，週期序列也和 A334504 的開頭相同。
- CI：`gh run view 45017724157` 回報 success，headSha 是 af98758。lean/ 從那之後沒有變動。我沒有在本機重新編譯 Lean。
- 依指示，`python -m discovery.check_record` 和 `python -m pytest -q` 在寫完本檔後執行。結果寫在交給 CEO 的報告裡。

## 最終判定

STATUS: PROVEN_KNOWN

理由：
- 研究目標 R3-L01 有完整的一般證明。Lean CI 通過，沒有 `sorry`、`admit`，也沒有新公理。這符合 §1 升級到 `PROVEN_*` 的條件。
- 敘述本身已經記載在 OEIS（A334504 FORMULA，雖然是猜想形式），novelty 是 `PARTIAL_MATCH`。`PROVEN_POSSIBLY_NEW` 需要人把 novelty 確認到 `PENDING_REVIEW`，目前沒有。所以合法而且保守的選擇是 `PROVEN_KNOWN`。
- 「證明本身可能是新的」這件事依 §1c 留在 `novelty.open`（R3-L01）和 `novelty.note`（proof NO_MATCH_IN_SCOPE），主狀態不能蓋過它。
- 這個狀態**不**代表我們找到了既有的證明，只代表「這個敘述不是我們發現的」。

**合併前必修：**

- **M1** 把 record.json 的 `status` 和 `candidates.R3-L01.status` 改成 `PROVEN_KNOWN`。改之前，`check_record` 會因為 review 和 record 的狀態不一致而失敗。`lean_theorems` 列出的兩個定理都存在，也都在 proof.md「定理對照」表裡。建議在 `novelty.note` 加一句：「PROVEN_KNOWN 指敘述已見於 OEIS（猜想形式），不代表已有既有證明。」
  - 如果 CEO 不接受這個判定、想保留 `SUPPORTED_NOVELTY_UNCHECKED`，就要把本檔的 STATUS 改成一致，並寫明理由。不過依現行規範，這等於說「只在測試範圍內成立、沒查新穎性」，兩點都和事實不符。

除了 M1，沒有其他必修項。

**建議（非必修）：**
- RESEARCH.md 第 15 行的「還沒有人證明過」改成「沒找到證明」。
- 查 Math Fun 2020 年 Klee 的原貼文，以及 MathSciNet、zbMATH、Google Scholar。
- 上網核對 NKS／Wolfram Atlas 的出處。
- 之後如果要升級到 `PROVEN_POSSIBLY_NEW`，要由人確認 novelty 到 `PENDING_REVIEW`。

## 給 CEO 的摘要

- **結果：** 規則 26 在奇數寬度 w ≥ 3 的環上，單一種子的週期恰好是 w·2^⌊log₂ w⌋，暫態是 0。這個結果有紙上證明，也有 Lean 證明，CI run 45017724157 通過，沒有 sorry 或新公理。我照指令重跑結果相同，自己另寫的模擬（w ≤ 47）也吻合。
- **新穎性：** 公式是 OEIS A334504 裡別人提出的猜想。我們的貢獻是證明，而在查過的範圍內（OEIS、arXiv、OpenAlex）沒找到既有證明。證明的核心想法（Pascal mod 2）是已知的。Math Fun、MathSciNet、zbMATH、Scholar 都還沒查。現有文件的措辭是誠實的。
- **Critic 的 F1–F3 都已修正。**
- **判定是 `PROVEN_KNOWN`。** 唯一的必修是 M1：record.json 的狀態從 `SUPPORTED_NOVELTY_UNCHECKED` 改成 `PROVEN_KNOWN`，兩處都要改，否則 `check_record` 會失敗。改完就可以合併。
