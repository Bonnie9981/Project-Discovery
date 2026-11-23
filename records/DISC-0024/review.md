# DISC-0024 Review（獨立審查）

## 審查項目

1. **critic 的兩條必修**：都已處理（commit dea1dcf）。
   - experiment.md 不再說「所有 k 的 k/φ(k) < 6」，改成只要求奇數原像都在範圍內。我複核了這個論證：奇數 k 有 ω ≤ 10 個質因數時，k/φ(k) ≤ 3.30（3～31 連乘）。所以 φ ≤ 2·10^9 推得 k ≤ 6.6·10^9。ω ≥ 11 時 φ(k) ≥ ∏(p−1) 遠大於 2·10^9，不可能。結論成立。
   - A276674 草稿的 Reason for edit 已改成「x − λ(x) is even and positive」。
2. **定義**：A084189、A084352、A046376、A225004、A340896、A276674、A015126、A058383 的定義和猜想原句，都和 `data/cx/entries/` 的逐字摘錄一致。摘錄裡沒有要 agent 做事的文字。
3. **Lean 是否對應猜想**：
   - `PalDigits.a084189` 和 `a084352` 忠實表達「兩個因數的數字不可能全 ≥ 4」，也就是 a(n) ≤ 3。p、q、pq 都以小端數字串表示。pq 最高位 ≥ 1，所以沒有前導零。質數用一般定義。A084189 另要求 p、q 是回文，和 A046376 的定義一致，p = q 的情形也涵蓋在內。沒有空泛或過強的假設（`a084352` 的 `hlen` 多餘，但無害）。
   - `DivisorExp.exponents_le` 只證了乘積不等式：∏(a+x+1) < 2∏(a+1) 推得每個 x ≤ a。中間缺一步：d(n) = ∏(v_p(n)+1)，這是教科書公式，沒有形式化。檔頭和草稿都寫明了這點。我接受它算 PROVEN_KNOWN，理由與 DISC-0015 的生成函數相同：由 Lean 結果加上標準事實嚴格推出。
   - CI 狀態依呼叫方提供：只用 core，axiom 只有 propext、Quot.sound、Classical.choice。本機沒有 lean/lake，我沒有重編，但讀過原始碼，沒有 `sorry`。
4. **紙上證明**：
   - A340896 完整。k = 0 的 n = 1 屬於 A000961，k = 1 時比值 < 2，k ≥ 2 時比值 ≥ 9/4。
   - A276674 完整。x − λ(x) 為正偶數，排除了 x = 1、x = 2 和奇質數冪；x = 4 恰好等號。x 為偶數時 λ ≤ φ ≤ x/2。x 為奇數且至少有兩個質因數時，λ = lcm(偶數們) ≤ ∏/2 = φ/2。
   - A225004 的 m | n 論證正確，新質數（a = 0）也已涵蓋。
   - A058383 反方向正確。
5. **沒有說過頭**：A015126、A058383 只寫「範圍內沒反例」。草稿沒有宣稱新穎。novelty 標為 `NO_MATCH_IN_SCOPE`，也寫明只查了 OEIS，沒有查 web、MathSciNet、zbMATH。
6. **草稿**（results/A084189、A225004、A276674）：數學正確，署名 `_Chi Hsia_`，保留原 Conjecture 行，分開送出，LINKS 註明有 LLM 協助。改好下面的必修 2 之後就可以送。LINKS 指向 GitHub `main` 上的 Lean 檔，所以要等合併後連結才有效。
7. **狀態用詞（問題所在）**：
   - `OPEN_NO_CX` 不是 RESEARCH_STANDARDS 第 1 節的狀態。這類「延伸範圍沒反例」的條目，先例（DISC-0021、DISC-0019）都標 `INCONCLUSIVE`。
   - A340896、A276674 只有紙上證明。第 1 節規定只有 Lean 定理在 CI 編譯通過才能標 `PROVEN_*`，先例是 DISC-0015 的 Ianakiev 那條，改成了 `SUPPORTED_KNOWN`。

## 重現結果

都在 3 分鐘內完成。程式編譯到 scratchpad，沒有修改 repo 裡的程式。

| 項目 | 指令（參數由我推斷，experiment.md 沒寫） | 結果 | 是否一致 |
|---|---|---|---|
| A084189 | `palprime_pairs 11 1e22` | 2082 個回文質數，2168403 對，found 0 | 一致 |
| A084352 | `digit_pairs 7 100000000000000` | 126 個回文乘積，126 個的兩因數位數都不同，最小 33433 = 67·499 | 一致 |
| A046376、brilliant | `check_pal.py`（預設 10^8） | 325 項、170 項，最小數字的最大值都是 3，DATA 一致 | 一致（紀錄跑的是 10^9，我只跑到 10^8） |
| A225004、A340896 | `check225004.py` | n ≤ 150，公式等於暴力結果，質數冪等價成立 | 一致 |
| A276674 | `check276674.py` | x ≤ 10^6 沒有違反，DATA 一致 | 一致 |
| A015126 | `a015126_scan 30000000 6` | reports = 0，偶數最小原像 1 個 | 和 critic、自我檢查一致 |
| A058383 | `a058383_scan 1e8` | 52 個解，non-A058383 = 0 | 範圍內一致 |

以下兩項超過 3 分鐘，我沒有重跑：A015126 的 2·10^9 掃描、A058383 的 10^10 掃描。

## 最終判定

STATUS: PROVEN_KNOWN

紀錄層級：研究目標是關掉這幾條猜想，其中 A084189、A084352 有完整 Lean 證明，A225004 由 Lean 不等式加上標準公式推出，所以整份紀錄是 PROVEN_KNOWN。

各候選應有的狀態：

| 候選 | 狀態 |
|---|---|
| A084189 | PROVEN_KNOWN |
| A084352 | PROVEN_KNOWN |
| A225004 | PROVEN_KNOWN（除數個數公式沒有形式化，要註明） |
| A340896 | **SUPPORTED_KNOWN**：紙上證明完整，但沒有 Lean |
| A276674 | **SUPPORTED_KNOWN**：紙上證明完整，但沒有 Lean |
| A015126 | **INCONCLUSIVE**：φ ≤ 2·10^9 沒有反例 |
| A058383 | **INCONCLUSIVE**：x ≤ 10^10 沒有反例，反方向已證 |

MUST-FIX：
1. `record.json`：A015126、A058383 的 `OPEN_NO_CX` 改成 `INCONCLUSIVE`（這個狀態名不合法）。
2. `record.json`：A340896、A276674 改成 `SUPPORTED_KNOWN`，或者補上 Lean 定理再維持 PROVEN_KNOWN。A340896 可以仿照 DivisorExp，證明「長度 ≥ 2 且 a ≥ 1 時 ∏(2a+1) > 2∏(a+1)；長度 ≤ 1 時 <」。RESEARCH.md 的「判定」那行也要跟著改，寫清楚是三條 Lean、兩條紙上。OEIS 草稿本身不受影響，數學是對的，可以照送。
3. `experiment.md`：補上每支程式的確切指令和參數，例如 `palprime_pairs 11 1e22`、`digit_pairs 7 1e14`、`a015126_scan 2000000000 6`、`a058383_scan 1e10`、`check_pal.py 1e9`。目前無法照文件直接重現，要自己讀原始碼猜參數。

Nice-to-have：
- `results/A058383/README.md` 和 A015126 的 README 內容完全一樣，裡面的 `code/a015126_scan.c` 連結在 A058383 資料夾下是斷的。
- RESEARCH.md 寫「除了奇質數冪，λ(x) 都不超過 x/2」，漏了 x = 1。
- `a084352` 的 `hlen` 可以刪。

## 給 CEO 的摘要

- 五條猜想的數學證明都正確，我逐步檢查過。A084189、A084352 的 Lean 證明確實對應原猜想。A225004 是 Lean 加上一條教科書公式。
- A340896、A276674 只有紙上證明。依規範要標 SUPPORTED_KNOWN，除非補 Lean。
- A015126、A058383 只是範圍內沒反例，要標 INCONCLUSIVE，`OPEN_NO_CX` 不是合法狀態。
- 我重跑了數值檢查，都在 3 分鐘內完成，結果全部一致。experiment.md 缺指令參數，要補。
- 三份 OEIS 草稿正確、署名 Chi Hsia、沒有宣稱新穎，可以送出。Lean 連結要等合併到 main 才有效。
- 整份紀錄：PROVEN_KNOWN。有三條必修，都是標籤和文件，不涉及數學。

## 必修處理（orchestrator）

1. record.json：A015126、A058383 改為 `INCONCLUSIVE`。
2. A340896、A276674 改為 `SUPPORTED_KNOWN`，RESEARCH.md 判定行同步。
3. experiment.md 補「重現指令」一節。
Nice-to-have：A058383 README 改寫、RESEARCH 的 λ 句補上 x = 1、2 例外。
