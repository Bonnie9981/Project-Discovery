# DISC-0015 審查：規則 54 單細胞各列（A118109、A265225）的猜想公式

審查者：reviewer（獨立 subagent，不是作者，也不是 critic）。審查對象：分支 claude/project-thread-s8fb0i 上還沒 commit 的工作樹。

## 審查項目

1. **critic 必修 1（Ianakiev 原文）：已處理。** search_evidence S002 已經存了逐字原文：「Take the first 2n positive integers and choose n of them such that their sum: a) is divisible by n, and b) is minimal. It seems their sum equals a(n).」照字面讀，就是「從 1..2n 選 n 個數，最小和 = a(n)」。n = 1 時最小和是 1 = a(0)，不是 a(1) = 4，所以「差一個索引」在這個原文下是對的。論文和 A265225 草稿也寫了等價的讀法（從 1..2n+2 選 n+1 個 = a(n)），而且草稿是在原句後面另加一行說明，沒有改動原句，做法得當。限制：原文是協調者用瀏覽器讀的，本容器連不到 oeis.org，我沒辦法自己再抓一次。
2. **critic 必修 2（A093353 的定義）：已處理。** S003 逐字記下 A093353 的名稱就是 a(n) = (n + (n mod 2))*(n + 1)/2，是定義，不是猜想。所以 `a265225_veselovac` 證的就是原公式，沒有附加前提。
3. **critic 必修 3（論文 AI 聲明裡的「reviewed」「CI」）：有條件接受。** 和 DISC-0014 一樣：本檔寫好後「reviewed」就成立；「machine-checked … in CI」要等 PR 的 CI 跑綠才成立。論文要合併後才公開，所以條件是合併前 CI 必須是綠的。
4. **critic 必修 4（results/ 檔案）：已處理。** `results/A118109/`、`results/A265225/` 都有 README 和 OEIS 草稿；A265225 的 README 指向共用的 code。
5. **critic 建議：** 公式數已經改成 8 個、6 個 Lean 定理（RESEARCH.md、DEVLOG 都改了）；論文的邊界情況寫得比較清楚了。光錐引理沒有另外寫成 Lean 定理。不過 `row_eq` 的 C 裡已經有 −t ≤ x ≤ t，可以直接推出，而且最左格 x = −n、最右格 x = n 一定是 ON，所以讀 −n..n 這個視窗不會有前導 0 的問題。不列為必修。
6. **Lean 敘述有沒有對到 OEIS 公式和 offset：有。** 我逐條讀過：`rule` 取 54 的第 4l+2c+r 位；`row 0` 只有位置 0 是 ON；A118109 讀 −n..n，A265225 是第 0..n 列 ON 數的累加，offset 都是 0。
   - `a118109_rec`：a(n+4) + 10000a(n) = 10001a(n+2)。在自然數裡，這和「n > 3 時 a(n) = 10001a(n−2) − 10000a(n−4)」等價。
   - `a118109_floor`：自然數的 `/` 就是 floor，和 Keller 的式子逐字相同。
   - `a265225_barker`：寫成整數式 4a(n) = (n+1)(2n − (−1)^n + 5)，和原式等價，而且多說明了原式一定整除。
   - `a265225_rec`：把減號移到等號兩邊，我手算展開後和原遞迴一致。
   - `a265225_hurt`：和原式逐字相同。
   - `a265225_veselovac`：見第 2 項。
   - 我在暫存副本加了 `#eval`：a118109(0..6) = 1, 111, 10001, 1110111, 100010001, 11101110111, 1000100010001；a265225(0..8) = 1, 4, 6, 12, 15, 24, 28, 40, 45。和 critic 的結果、條目開頭都一致。
7. **有沒有空洞：沒有。** 檔案裡沒有 sorry、admit、axiom、native_decide、implemented_by、unsafe。6 條主定理的 `#print axioms` 都是 [propext, Classical.choice, Quot.sound]。`lean/Discovery.lean` 已經 import `Discovery.Rule54Rows`。
8. **結論有沒有說過頭：** 6 條公式是 Lean 證的，對所有 n 成立。兩個生成函數是由已證的遞迴加 4 個或 5 個初值推出來的，是標準而且嚴格的推導。論文、proof.md、RESEARCH.md 都寫明這兩條是「紙上」，沒有說成 Lean。Ianakiev 的部分是紙上證明，數值只驗到 n ≤ 11（critic 用動態規劃驗到 n ≤ 40）。我核對了這個紙上證明，是對的：n 元子集的和會連續取遍整個區間；n 奇時最小和 n(n+1)/2 = a(n−1)；n 偶時最小和 n(n+2)/2 = (2k+2)(k+2) = a(n−1)。**但是**，record.json 把 `A265225-ianakiev` 這個候選標成 `PROVEN_KNOWN`，違反 RESEARCH_STANDARDS 第 15 行的規定：只有 Lean 定理在 CI 編譯通過，才能標 `PROVEN_*`。見必修 2。
9. **新穎性：誠實。** 檔案寫明不宣稱新、屬於習題程度，也寫明圖樣在 NKS p.55、A118108 已經有十進位的封閉式。只查了 OEIS（S001～S003），沒查 arXiv、MathSciNet，這點有照實寫。Munarini 2021 沒讀，也有註明。
10. **OEIS 草稿：大致符合 A071052 草稿的規則。**
    - 署名是 `_Chi Hsia_, Nov 23 2026`；公式放在 FORMULA 欄；原作者保留；Ianakiev 原句不刪；有 AI 聲明（LINKS 欄寫「generated with an LLM (Claude) and machine-checked」）；也提醒了「不要寫成大發現」。
    - 少了 A071052 草稿裡的一條提醒：「送出前在 OEIS 上再看一眼 DATA 和 FORMULA 原句」。見建議 1。
    - LINKS 的「machine-checked」是對整頁說的，但兩個生成函數和 Ianakiev 那條沒有用 Lean 檢查。論文本身有講清楚，所以可以接受。
11. **外部資料：** 我讀到的資料（search_evidence、論文、草稿、工具輸出）裡，沒有任何要我做事的文字。

## 重現結果

所有計算都用 `discovery.limits.run_limited` 跑，都在上限內：

- `python results/A118109/code/l08_rule54_rows.py 300`：status ok，約 0.3 秒，輸出「OK: 0 <= n <= 300: simulation = closed form; … DATA match; Ianakiev min-sum = a(n-1) for 1 <= n <= 11」。和 experiment.md 預期的開頭一致。
- `python results/A118109/code/critic_c_rule54_rows.py 400 40`：status ok，約 0.3 秒，輸出「OK critic_c: 0 <= n <= 400 … min-sum(n of 1..2n) = a(n-1) for 1 <= n <= 40, never a(n); 'n+1 of 1..2n+2' reading gives a(n)」。
- `lean lean/Discovery/Rule54Rows.lean`（Lean 4.15.0）：0 錯誤，約 10 秒。另外用暫存副本加 `#print axioms` 和 `#eval`，結果見審查項目 6、7，原檔沒動。
- `python -m discovery.independence`：0 problems。
- `python -m discovery.check_record`：寫 review.md 之前有 2 個問題：「DISC-0015/hypotheses.md: missing section '## 猜想'」和「missing review.md」。第一個要作者修，見必修 1。

## 最終判定

STATUS: PROVEN_KNOWN

理由：A118109 的遞迴和 Keller 式，以及 A265225 的 Barker 封閉式、5 階遞迴、Hurt 式、Veselovac 式，都有 Lean 證明（只用 core，沒有 sorry，也沒有額外公理），對所有 n ≥ 0 成立，定義和 offset 都和 OEIS 對得上。兩個生成函數是由已證遞迴加初值嚴格推出的，紙上。Ianakiev 那條是紙上證明加數值驗證，不屬於 PROVEN。整體是已知圖樣的習題，不宣稱新。

**必修：**
1. `records/DISC-0015/hypotheses.md` 缺 `## 猜想` 段落標題，`check_record` 因此失敗，CI 會擋。請照 DISC-0014 的格式，在 H1～H6 前面加上 `## 猜想`。
2. `record.json` 的 `candidates["A265225-ianakiev"].status` 不能是 `PROVEN_KNOWN`，因為它只有紙上證明，沒有 Lean，違反 RESEARCH_STANDARDS 第 15 行。請改成 `SUPPORTED_KNOWN`（數值驗到 n ≤ 40，另有紙上證明；註解本身已經在 OEIS 上），或者補一條 Lean 定理。整筆紀錄的 STATUS 不受影響。

（合併條件：PR 的 Lean CI 必須是綠的，論文 AI 聲明的「machine-checked … in CI」才成立。）

**建議：**
1. 兩份 OEIS 草稿各加一條提醒：「送出前在 OEIS 上再看一眼 DATA、FORMULA 和 Ianakiev 原句」。本容器連不到 oeis.org，原文只有協調者用瀏覽器讀過一次。
2. record.json 的 `A118109-formulas`、`A265225-formulas` 寫明生成函數是「paper, from proved recurrence + initial terms」。A265225 那條已經寫了，A118109 那條也寫了，維持現狀即可。可以考慮把 candidate 拆細，讓 PROVEN 只蓋到 Lean 證過的部分。
3. 可選：在 Lean 補光錐引理（|x| > n 時 `row n x = false`），讓「整列 = −n..n 視窗」這件事有明文依據。

## 給 CEO 的摘要

規則 54 兩條 OEIS 條目（A118109、A265225）一共 8 個標成「猜想」的公式都證完了：6 個是 Lean 證明，2 個生成函數是由這些證明直接推出來的。我重跑了兩支檢查程式和 Lean 編譯，全部通過，critic 的 4 項必修也都處理了。A265225 有一則 2019 年的註解，照原文字面確實差一個索引；草稿只在原句後面另加說明，沒有改動原句。這是習題程度，不是新發現，判定 PROVEN_KNOWN。合併前還要修兩件小事：hypotheses.md 補一個段落標題（否則 CI 會擋），以及 Ianakiev 那條的候選狀態要從 PROVEN 降為 SUPPORTED_KNOWN，因為它沒有 Lean 證明。送 OEIS 前請使用者自己再看一眼條目原文。
