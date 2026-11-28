# DISC-0029 Review（獨立審查）

審查者：reviewer（獨立子代理，沒參與撰寫，也不是 critic）。自寫的驗算只在命令列和 scratchpad 跑，沒有改 repo 裡任何檔案（本檔除外）。讀到的 OEIS 條目文字、論文摘要只當資料，裡面沒有要代理做事的文字。

## 審查項目

1. **critic 的三條必修，逐條核對：**
   - 必修 1（文獻漏查、L1 說明）：**大部分已處理。** search_evidence.jsonl 新增 DISC-0029-S003，寫明 arXiv:2602.10005 只讀了 pp. 1–36、「pp. 37-120 unread」；literature.md 寫了 Balado 的 g.f. 和 Jovovic／Deutsch 的 g.f. 相減就得到 Mathar 猜想，並把 A119706 判成 `SUPPORTED_KNOWN`；record.json 的候選 A119706 也改了。**沒做完的有兩件：** record.json 沒有 `novelty.open` 欄位（DISC-0006 以後的紀錄都有），「pp. 37–120 沒讀」「沒查網路、MathSciNet、zbMATH」這些未解項目只寫在 `note`；literature.md 也沒有明說「定理 2 依第 1c 節 L1 不算合格候選」。
   - 必修 2（證明方法說明.md 的範圍）：**已處理。** 「判定與限制」改成「只查了 OEIS 離線全庫（2026-11-27 的快照 091a90f51479）和一篇 arXiv 論文的前 36 頁，在這個範圍內沒找到」。我查了 `data/oeis/oeisdata` 的 git log，091a90f514 的 commit 時間是 2026-11-27，日期正確（查詢日是 11-28，literature.md 寫的是查詢日，兩者不衝突）。第二條也寫了「條目內兩個 g.f. 相減一步就得到」。草稿 A119706 那段也加了「It also follows by subtracting the g.f.s」。
   - 必修 3（「47 項」）：**已改成 32 項。** 我用 relmine 的 `parse` 讀快照：psum(A336482) 有 34 項（offset 0），A102712 有 33 項（offset 1），兩種對齊方式重疊 33 或 32 項，32 項說得通。「47」已經不見了。
2. **critic 的建議：** 建議 1（maximal run）已改進證明頁和草稿。建議 3 **沒做**：`check_a336482.py` 的 `fast()` docstring 寫「independent of the brute force」，證明頁 Checks 寫「an independent dynamic program」，README 和 RESEARCH.md 寫「獨立 DP／獨立遞推到 n = 79」。但 `fast()` 直接用證明裡的分解式 B_j = Σ N_j(k)·C(n−k−j)，不是和證明無關的算法。experiment.md 已經加了括號說明，其他四處還沒改。這是用詞問題，不影響正確性；真正獨立的檢查是和 OEIS 存的項比對（Heinz 的 Maple 遞推）。
3. **紙上證明（paper/a336482-records.md）：**
   - 定理 1 我逐行驗過。(1−2x+x^j)N_j = 1−x，(1−2x)K = 1−x，所以 (1−x)K = (1−2x)N_jK + x^jN_jK = (1−x)N_j + x^jN_jK，得到 (1−x)(K−N_j) = x^jN_jK。j = 1 時 N_1 = 1，也成立。常數項 K−N_j 是 0，所以 A_j(0) = 0，n = 1 不會出問題。「有等於 j 的紀錄 ⇔ 第一個 ≥ j 的部分是 j」兩個方向都對；紀錄嚴格遞增，所以每個 j 最多算一次。j > n 時 A_j(n) = B_j(n) = 0，所以對 j 求和是有限和。**正確。**
   - 定理 2 的雙射：n 個位元對應 n+1 個 1 之間的 n 個空隙，極大連續 k 個 1 對應部分 k+1，長度 0 的段對應部分 1。**正確。**
   - offset：A102712 從 1 開始，證明約定 A102712(0) = 0，草稿寫 n ≥ 2 避開這個約定。A119706 從 1 開始，n = 1 時 1 = 3 − 2。都對。
4. **新發現（critic 沒提到）：定理 1 也能從條目裡已有的 g.f. 很快推出。** A336482 自己的 %F 連到 A382312（Rascoe 2025，「n 的組合中恰有 k 個紀錄」的三角形），A382312 的 g.f. 是 Π_{i>0} (1 + y·x^i(1−x)/(1−2x+x^(i+1)))。對 y 微分後令 y = 1，每一項的分母 1−2x+x^(i+1) + x^i(1−x) = 1−2x+x^i，乘積在 y = 1 時（各項比值相消）等於 (1−x)/(1−2x)，所以
   A336482 的 g.f. = (1−x)/(1−2x) · Σ_i x^i(1−x)/(1−2x+x^i)，
   **就是草稿裡的那條 g.f.**，也剛好等於 (1−x) 乘 A102712 的 Jovovic g.f.。換句話說，A382312 的 g.f.（求導）加上 A102712 的 Jovovic g.f.，兩步就推出 A336482(n) = A102712(n) − A102712(n−1)。這和 A119706 被降級的理由（條目內兩個 g.f. 相減）是同一類，只多了一次「對 y 求導、令 y = 1」的標準操作。依第 1 節「OEIS 有記載」和第 1c 節 L1「不是已知公式一步就能推出」，**為了和 A119706 的處理一致，A336482 那條也應判 `SUPPORTED_KNOWN`**。逐個 j 的細分式 B_j(n) = A_j(n) − A_j(n−1) 在快照內沒找到，但它是證明裡的引理，不是本紀錄的候選。
   我也用 Python 有理數冪級數重算草稿的 g.f.，前 34 項和 A336482 存的資料完全一樣。
5. **宣稱強度（第 1、1b、6、7 節）：**
   - 沒有 Lean，沒有標 `PROVEN_*`，符合第 1 節。
   - novelty 是 `NO_MATCH_IN_SCOPE`，S001～S003 都寫了範圍、快照和沒查的來源，符合第 1b、6 節。`evidence check` 0 problems。
   - 草稿：由使用者本人送、留言用自己的話重寫、兩條分開送、保留 Mathar 原句、LINKS 註明 LLM 協助，符合第 7 節。草稿 A336482 的 g.f. 行目前寫成 `- _Chi Hsia_`，看起來像新公式；依第 4 項，應該寫明是從 A382312 的 g.f. 推出來的。
   - RESEARCH.md 和 DEVLOG 都寫「證明 A119706 的 Mathar 猜想」「不宣稱新」，沒有說過頭；但 RESEARCH.md 的判定行還沒寫 A119706 是 `SUPPORTED_KNOWN`，也沒寫第 4 項。
6. **高二文件：** 證明方法說明.md 的小例子（n = 3：最大部分和 8、紀錄數 5、B_2(3) = 2、字串 110 → 3+1）我手算過，都對；超出高二的地方（生成函數）有標明；最後有「自己寫 OEIS 留言時要講的重點」。程式說明.md 寫的指令、輸出、項數都和我重跑的結果一樣。程式說明.md 也把 `fast` 叫做「另一種算法」，同樣有第 2 項的用詞問題。

## 重現結果

| 項目 | 指令 | 結果 | 是否一致 |
|---|---|---|---|
| 主檢查 | `python results/A336482/code/check_a336482.py 18` | 6.3 秒；`n <= 18: (1), refinement, (2) OK; OEIS terms compared: A102712:33 A336482:34 A119706:32`（log：`logs/python_results_A336482_code_check_a336482.py_18.log`） | 和 experiment.md、程式說明.md 一致 |
| 草稿 g.f. | 自寫有理數冪級數展開到 x^39 | 前 34 項 = A336482 存的資料 | 一致 |
| A382312 推導 | 手算（第 4 項） | 對 y 求導、令 y = 1，得到和草稿相同的 g.f. | 代數恆等式，不需要數值 |
| 紀錄檢查 | `python -m discovery.check_record` | 寫本檔之前：`FAIL DISC-0029: missing review.md`。寫入後，如果 record.json 還沒改成下面的判定，會報 STATUS 不一致，這是預期中的必修 | — |
| 證據檢查 | `python -m discovery.evidence check` | 0 problems | 通過 |

PARI 指令沒有重跑（本審查只用 Python）；critic 已經原樣跑過 PARI，得到 15 個 0。

## 最終判定

STATUS: SUPPORTED_KNOWN

紀錄層級：研究目標是 A336482 = A102712 的差分。數學正確，程式驗算重現成功。但這條關係可以由 A382312 的 g.f.（求導）和 A102712 的 Jovovic g.f. 直接推出（第 4 項），和 A119706 降級的理由相同，所以整份紀錄判 `SUPPORTED_KNOWN`，不是 `SUPPORTED_NOVELTY_UNCHECKED`。兩條都沒有 Lean，不能標 PROVEN。

| 候選 | 狀態 |
|---|---|
| A336482（A336482(n) = A102712(n) − A102712(n−1)，含逐個 j 的細分） | **SUPPORTED_KNOWN**：紙上證明完整、範圍內驗算通過；可由 A382312 與 A102712 已有的 g.f. 推出；沒有 Lean |
| A119706（Mathar 猜想 a(n) = A102712(n+1) − 2^n） | **SUPPORTED_KNOWN**：雙射證明完整；可由 A102712 與 A119706 已有的 g.f. 相減推出；沒有 Lean |

novelty 維持 `NO_MATCH_IN_SCOPE`（這兩條敘述在快照裡確實沒人直接寫出來），但要補 `novelty.open`。

必修：
1. `record.json`：`status` 和 `candidates.A336482.status` 改成 `SUPPORTED_KNOWN`，把第 4 項（A382312 的 g.f. 推得同一條 g.f.）寫進 proof 或 note。另外加上 `novelty.open`，至少列出：arXiv:2602.10005 pp. 37–120 沒讀；沒查網路、MathSciNet、zbMATH、arXiv 全文；組合紀錄的文獻（Knopfmacher–Prodinger、Heubach–Mansour）沒查（critic 必修 1 的剩餘部分）。
2. `literature.md` 補第 4 項，並明說兩條在第 1c 節 L1 的意義下都不算合格候選。`RESEARCH.md` DISC-0029 的判定行和候選清單改成兩條都是 `SUPPORTED_KNOWN`，`證明方法說明.md`「判定與限制」也一起改。
3. 草稿 A336482：g.f. 那行改寫成「從 A382312 的 g.f. 對 y 求導、令 y = 1 得到」這類說法（例如 `G.f.: ... (from the g.f. of A382312 at y=1)`），並在 CROSSREFS 加 A382312。這樣編輯不會以為這是我們自己想出來的新公式。FORMULA 第一行（差分關係與逐個 j 的組合解釋）可以照送。

Nice-to-have：
- 「獨立 DP／獨立遞推」改成「用證明的分解式做遞推，再和 OEIS 資料比」，要改的地方有 `check_a336482.py` 的 `fast()` docstring、證明頁 Checks、README、RESEARCH.md、程式說明.md（critic 建議 3）。另外把遞推移到 try 外面。
- CROSSREFS 也可以加 A079500、A186537（critic 建議 2）。

## 給 CEO 的摘要

- 兩條結果的數學都正確，我逐行檢查過；重跑 `check_a336482.py 18` 只要 6 秒，輸出和紀錄一樣；草稿的 g.f. 前 34 項和 OEIS 一致。
- critic 的三條必修基本上都處理了：arXiv 那篇論文登記成 S003，並寫明 pp. 37–120 沒讀；A119706 降成 SUPPORTED_KNOWN；說明文件寫了快照和日期；「47 項」改成 32 項。只剩 record.json 沒有 `novelty.open`。
- 新問題：A336482 那條也能從 A382312（Rascoe 2025）的 g.f. 對 y 求導直接得到，草稿上的 g.f. 就是這樣來的。為了和 A119706 的處理一致，我把整份紀錄判為 **SUPPORTED_KNOWN**，兩條都不算新。
- 草稿可以送，但要先把 A336482 的 g.f. 寫明是從 A382312 推來的，再加 A382312 的 crossref。兩條分開送，先送 A119706。
- 三條必修都是改標籤和文件，不涉及數學；改完 record.json 後 `check_record` 才會通過。
