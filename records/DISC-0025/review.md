# DISC-0025 審查

審查者：reviewer（獨立 subagent，未參與搜尋、程式、critic）。檔案、網頁和工具輸出都當資料讀，沒看到要審查者做事的嵌入文字。

## 審查項目

1. **要排除的東西對不對。** 每個 (n, k) 問「n 點圖有沒有 ν ≤ k 且 τ ≥ 2k+1」。真的反例 ν = k0 時會被 k = k0 那一輪排除。k = 0 沒有三角形，不可能是反例。k 的上限 kmax(n) = ⌊(⌊n(n−1)/4⌋ − 1)/2⌋ 的根據是：任何圖都有至少一半邊數的二部子圖，所以 τ ≤ ⌊m/2⌋。我手算 n = 8 得 6、n = 9 得 8，和程式、summary.json 一致。補孤立點就能把較少點的圖變成 n 點，ν、τ 都不變。**成立。**
2. **剪枝不漏。** INT：不在任何三角形裡的邊刪掉後，ν、τ 都不變。LEX：每個相鄰對換一條「字典序 ≥」約束。輔助變數 eq 只有「被迫為真」這個方向，求解器可以把它設成假，所以這組約束剛好等於「≥lex」。每個同構類裡字典序最大的標號都會滿足。INT 在重新標號下不變，兩者可以一起用。**成立。** 測試做了 n ≤ 6 的圖譜比對；critic 用 n = 7 抽 38 張；我另外用 n = 8 抽 12 張隨機「每條邊都在三角形裡」的圖，窮舉 8! 種標號取字典序最大的一個，再丟進 `check.spec(8)` 的基本子句，12 張全被接受（腳本在審查者暫存區，不進 repo）。
3. **擋子句合法。** P 子句：k+1 個兩兩不共用邊的三角形，它們的邊不能全部出現（否則 ν ≥ k+1）。C 子句：C 最多 2k 條邊，必須至少有一個不碰 C 的三角形存在（否則 C 本身就是覆蓋，τ ≤ 2k）。C 不必是候選圖的子集，合法性也不受影響。**成立。**
4. **check.py 和 search.py 是否獨立。** check.py 只 import `discovery.egsat.check` 的 `RUP`、`read_cnf`（DISC-0022 審過）。它自己重建 TRI、INT、LEX，逐條比對 CNF 開頭，並確認變數數相同。之後每條擋子句都要對上 JSON 見證：P 要剛好 k+1 個不同的三角形、兩兩不共用邊，子句等於那些邊的負字面集合；C 要 |C| ≤ 2k，子句等於所有不碰 C 的三角形。不合法的三角形會在查表時出錯被擋下。DRAT 只接受 RUP 引理，比 RAT 嚴格。**獨立性足夠。** 唯一的共同失誤風險是兩邊的 LEX 出自同一份構造，見第 2 項的抽樣。
5. **主張範圍。** n ≤ 9 的每個 k 都有證書，在 600 秒內驗過，DRAT 最大 3.39 MB，低於 50 MB。n = 10 時 k = 1～3 有證書；k = 4～6 只有求解器結果，`certificate_checked: false`；k ≥ 7 沒跑。experiment.md、record.json、RESEARCH.md 第 289～296 行與第 318 行、DEVLOG 最後一行都寫「9 點內、10 點不主張」，**一致**。結論寫的是「證書已驗」，沒有寫成「證明」。也沒有 Lean，proof.md 有誠實註明。
6. **新穎性。** 有 3 筆查詢紀錄（S001～S003）。沒查到窮舉驗證，但紀錄明說「小範圍暴力列舉很常規，很可能有人做過沒發表」，MathSciNet／zbMATH 沒查也寫在 `open` 裡。Gupta 預印本的已知成果是依引言轉述，有註明。`NO_MATCH_IN_SCOPE` 加上「不宣稱新」的措辭合規。
7. **狀態。** `SUPPORTED_NOVELTY_UNCHECKED` 的意思是「範圍內成立，不可宣稱新」，符合現況。不屬於 PROVEN／POSSIBLY_NEW／里程碑，所以 critic 用 sonnet 合規（docs/TOKEN_BUDGET.md 第 1 節）。
8. **critic 的必修項（record.json 的 critic 欄位是事先填好的）。** critic.md 確實存在，而且是另一個 subagent 寫的，所以「critic (independent subagent)」與實情相符。`critic_model: "sonnet"` 我無法從 repo 內獨立核實，只能依總控的派工紀錄採信。這個狀態不要求 opus，所以這一點不影響判定。**視為已處理（附但書）。**
9. **critic 的建議沒有採納的部分（不擋判定）。** LEX 的 n = 7 抽樣沒有寫進 tests，`tests/test_tuzasat.py` 仍是 5 個測試；也沒有加「緊例黏接」的暴力測試。8、9 點只有 SAT 這一套實作，9 點結論完全靠證書鏈。這點在 experiment.md 已經寫清楚。
10. **資源上限的小瑕疵。** n = 10、k = 4～6 搜尋時產生的 DRAT 有 38～116 MB，超過 `max_output_mb` = 50。產生後沒有用、也沒有主張，但流程上應該在超過時停下來，而不是先寫出檔案。這不影響 n ≤ 9 的結論。

## 重現結果

- `python -m pytest -q tests/test_tuzasat.py tests/test_records.py tests/test_research_summary.py`：審查前 9 個通過、1 個失敗。失敗的是 `test_records`，原因只有「DISC-0025: missing review.md」，就是本檔還沒寫。其餘全部通過。
- `python -m discovery.tuzasat.search 9 3 5 --out /tmp/rev24`：k = 3 UNSAT，2521 條擋子句（1.6 秒）；k = 5 UNSAT，5922 條擋子句（7.2 秒）。擋子句數和 experiment.md 相同。總耗時 9.8 秒。
- `python -m discovery.tuzasat.check /tmp/rev24 9 3 5`：k = 3 證書通過（692 條基本子句、2521 條擋子句、9963 個引理）；k = 5 證書通過（692、5922、25288）。總耗時 31.8 秒。
- SHA-256 和 `data/tuzasat/summary.json` **完全相同**：
  - n=9 k=3：CNF 1faee4a5…a1bcc480，DRAT 9b4b4509…ff31e
  - n=9 k=5：CNF f396b2ba…1806274，DRAT bb939181…a6fcb0
- LEX 抽樣：n = 8 共 12 張，0 張被誤殺（見審查項目 2）。
- 沒重跑 n = 9 的其他 k（1、2、4、6、7、8），這些依賴 summary.json 的記錄；critic 已重跑 n = 8 全部的 k。

## 最終判定

STATUS: SUPPORTED_NOVELTY_UNCHECKED

- 候選 `TUZA-n<=9`：SUPPORTED_NOVELTY_UNCHECKED。「9 點以內沒有 τ > 2ν 的圖」在下面三個前提下成立：DRAT 證書驗過、check.py 核對了見證、INT／LEX／kmax 的論證成立。這是在範圍內成立，不是 Lean 證明，也不宣稱新。
- 候選 `TOOL-symmetry`：SUPPORTED_KNOWN，維持原判。
- n = 10：不主張。如果日後要寫，應寫成 INCONCLUSIVE（計算未在上限內完成）。

必修：無（判定不需要修改任何檔案）。

建議（非必修）：
1. 把 n = 7（或 8）的 LEX 抽樣比對放進 `tests/test_tuzasat.py`，降低 search／check 共用同一個 LEX 構造的風險。
2. 往後的大型搜尋在寫出 DRAT 前先估大小，超過 `max_output_mb` 就停下來，直接記成 INCONCLUSIVE。
3. 如果要把新穎性往上推，要補查 MathSciNet／zbMATH，並查 OpenAlex 上的 "Tuza" 加 "small graphs"／"computer"。

## 給 CEO 的摘要

Tuza 猜想（刪邊拆光三角形最多只要「互不共用邊三角形數」的 2 倍）在 9 點以內沒有反例。每個情況都有 SAT 證書，由獨立檢查器在上限內驗過。我重跑了 9 點的 k = 3、5，雜湊和紀錄完全相同。10 點沒做完，不主張。這種小範圍驗證很可能有人做過，所以不宣稱新，研究價值有限。判定：SUPPORTED_NOVELTY_UNCHECKED，沒有必修項。
