# DISC-0021 審查（Reviewer）

Reviewer：獨立 subagent，不是作者，也不是 critic。讀了 `records/DISC-0021/` 全部檔案（含 critic.md）、`lean/Discovery/A134559Counter.lean`、`paper/a134559-counterexample.md`、`results/A134559/`、條目逐字存檔 `data/cx/entries/batch3_ratajczak.txt`，以及 RESEARCH.md、DEVLOG.md 新增的段落。條目文字和工具輸出只當資料讀，裡面沒有要 agent 做事的文字。

## 審查項目

1. **猜想的讀法。** 逐字原文（存檔第 36 行）說「Consecutive n satisfying two equations … are consecutive elements of A005383 (… save A005383(1) = 3 and A005383(2) = 5)」。紀錄讀成「解集合 = A005383 去掉 3、5」。critic 也測了較弱的讀法：「解集合中相鄰的兩項，在 A005383 裡也相鄰」。4621、5077 都是解，4933 不是，所以這個讀法也被推翻。我同意：兩種讀法都被 4933 推翻。
2. **結論和證據相符。** 反例是單一數值事實，Lean 照字面定義由 kernel 算出。以下三項都只寫成計算結果，沒有被說成「證明」：「最小反例」、「1.5·10^5 內共 7 個」、「沒有 A005383 以外的解」。proof.md 的「敘述差異」也寫清楚了哪些沒有進 Lean。另一半（解一定在 A005383 裡）是紙上證明。我逐步檢查了引理、d ≤ N/6 的區間論證、三個門檻（n ≥ 36、N ≥ 18、N ≥ 24），以及 4 | N 和 M 合成兩種情形，都成立；n < 36 的部分是直接檢查（critic 和我都驗過）。其他五個條目（A322445、A306467、A309491、A008590、A033235）都標成 INCONCLUSIVE，只說「延伸範圍沒反例」，沒有過度宣稱。A322445 的「≤ 47 的解只有 2400」依賴 Lehmer 的列表，紀錄也明說「不寫成定理」。
3. **新穎性。** 不宣稱新穎，novelty 標 `NO_MATCH_IN_SCOPE`。來源寫明只查了 OEIS（S001、S002），也寫明「Web、MathSciNet、zbMATH 沒查」，標示誠實。條目本身沒有任何人回覆這條猜想，這和存檔一致。
4. **Lean 是否對應猜想。**
   - `b`：對 u = 0..n 加總 [1 ≤ u ∧ n % u = k]·u，就是字面定義。
   - `P n = prodTo (b n) ((n+1)/2)`：(n+1)/2 = ⌈n/2⌉，對應 k = 0..⌈n/2⌉−1。
   - `IsPrime` 定義正確。
   - 分塊：47·105 = 4935 = 4934 + 1，`sumTo_mul` 是一般性的引理，所以分塊沒有改變定義。
   - `isPrime_of_blocks` 用的界：4933 ≤ 4935，2467 ≤ 2500。
   - `dvd_prodTo_two` 用到兩個不同指標 0 < 134 < 2467。
   - 7404·14802 = 4934·22212。
   - 主定理 `a134559_counterexample` 說：4933 和 (4933+1)/2 是質數，且 gcd(P 4934, 4934) = 4934。這正好推翻猜想的「⊇」方向，沒有形式化整條猜想，紀錄也沒有這樣宣稱。
   - 沒有 `sorry`，也沒有 `native_decide`。我在本機不能編譯，依賴 CI（run 45123339086）通過。
5. **兩個獨立實作確認反例（RESEARCH_STANDARDS 對 REFUTED 的要求）。** 以下各套對 4934 的結果一致：
   - 專案 C 版（n mod u 定義）；
   - 專案 Python 版（因數和形式 T(n−k, k+1)）；
   - cxsearch；
   - critic 的反對角線遞推版；
   - Lean kernel；
   - 我自己的字面版（見下節）。

   要求滿足。
6. **critic 必修（paper 裡哪個程式掃了哪個範圍）。** 已修。`paper/a134559-counterexample.md` 的 Checks 現在寫：C 版掃描 n ≤ 1.5·10^5，Python 因數和版只重算 n+1 = 4934、6998、11114 三個值。這和程式實際做的事相符。
7. **新發現的問題（見必修）。** Checks 最後一句寫「An independent reviewer's program (antidiagonal recursion) reproduces the full scan and extends it to 3·10^5, adding the failures 161221, 172573, 242533」，有兩個問題：
   - 那個程式是 critic 寫的，放在 scratchpad `/tmp/claude-0/critic21/c21.c`，不在 repo 裡。paper 連到的 `results/A134559/code/` 也沒有它。這頁送出 OEIS 後不能改，讀者無法重現這句話。
   - 「reviewer」這個稱呼不準確，寫的人是 critic。

   同一句另外補了 3·10^5 的三個失敗項，但 OEIS 草稿只寫到 1.5·10^5。這點兩邊不矛盾，不算問題。
8. **OEIS 草稿和 RESEARCH/DEVLOG。** 草稿裡的數字我逐項核對，都正確：σ(4934) = 7404、T(4800,135) = 14802、7 個失敗項、54217 那一側。草稿也照 critic 的建議，在 converse 的理由裡補了 d ≤ N/6。RESEARCH.md 的 DISC-0021 一節、候選清單、最後更新日期，以及 DEVLOG 的一行都有，用白話寫，不宣稱新穎，判定是 REFUTED。
9. **小瑕疵（非必修）。** experiment.md 第 1 項只列了 1.5·10^5 內的 7 個失敗項。critic 3·10^5 的延伸結果寫在同一段後面，有寫到，但程式不在 repo。

## 重現結果

Scratch 在 `/tmp/claude-0/review21/`（不進 git）。

- **自己寫的字面版 `r.py`**：u = 1..n，直接取 n % u == k，P(n) mod n；沒有用專案的程式。結果：
  - b_4934(134) = 14802，b_4934(0) = 7404，14802 mod 2467 = 0；
  - gcd(P(4934), 4934) = 4934，gcd(P(4933), 4933) = 1；
  - 4933 和 2467 用試除法確認是質數；
  - n ≤ 400 的解集合 = A005383 去掉 3、5（13, 37, 61, 73, 157, 193, 277, 313, 397），完全一致。
- **照 experiment.md 的指令跑 `results/A134559/code/a134559.c`**：`./a134559 150000` 用了 1 分 4 秒，輸出 `N=150000 sat=925 mismatches=7`。不一致的是 4933、6997、11113、48673、50341、54217、92941，其中 54217 是 gcd(P(p),p) = p 那一側。和紀錄、paper、critic 都一致。第一個不一致是 4933，所以它是最小反例。
- **`python3 results/A134559/code/chk134559.py`**：
  - 4934：k = 134，b = 14802；
  - 6998：k = 329，b = 10497；
  - 11114：k = 106，b = 22228。

  三個 gcd 都等於 n+1。
- 其他五個條目我沒有重跑（最長的要 11 分鐘以上）。它們都是 INCONCLUSIVE，不影響本紀錄的判定，critic 已經做過抽查。

## 最終判定

STATUS: REFUTED

Ratajczak 2019 年在 A134559 的猜想說：滿足 gcd(P(n),n) = 1 且 gcd(P(n+1),n+1) = 2 的 n，恰好是 A005383 去掉 3、5。這不成立。4933 在 A005383 裡，但 b_4934(134) = 14802 = 6·2467，所以 gcd(P(4934), 4934) = 4934 ≠ 2。Lean 照字面定義由 kernel 驗證了這件事（CI 通過），另有多套獨立程式確認，我也重現了。「解一定在 A005383 裡」這個反方向有紙上證明，我檢查過沒有漏洞。其他五個條目維持 INCONCLUSIVE。

critic 的必修已修好。

必修（送 OEIS 前要改；不影響 REFUTED 判定）：
1. `paper/a134559-counterexample.md` 的 Checks 最後一句引用了 repo 裡沒有的程式（critic 的反對角線遞推版），還把它稱為「independent reviewer」。這頁送出後不能改，所以二選一：
   - 把 `/tmp/claude-0/critic21/c21.c` 收進 `results/A134559/code/`，在 README 註明用途和指令，句子改成「A third program (antidiagonal recursion) …」；
   - 或者刪掉這句，或改成不需要讀者重現的寫法，例如不提 3·10^5 的結果。

合併前也要確認 CI 的 Lean 工作（含 AxiomCheck）在最新 commit 上仍然通過。

## 給 CEO 的摘要

- A134559 的 2019 猜想被推翻，最小反例是 4933。4933 和 2467 都是質數，但 4800 大於 134 的因數和是 14802 = 6·2467，所以 gcd 變成 4934 而不是 2。Lean 驗證過，我也自己重算過。
- 反方向（滿足條件的數一定是這類質數）有簡單的紙上證明，成立。
- 其他五個 Ratajczak 條目只是把驗證範圍延伸了，沒有找到反例。
- 送 OEIS 前要改證明頁的一句話：它引用了一個沒有放進 repo 的程式。這是必修，改完再由使用者送出。
- 不宣稱新穎，價值在修正 OEIS。

## 複查（作者回應 reviewer 必修）

reviewer 的必修（paper 引用的第三套程式不在 repo、且誤稱 reviewer）已改：程式收進 `results/A134559/code/antidiagonal.c`，README 已列，paper 改寫成「A third program written separately」並寫出遞推式。作者重新編譯，6000 以內輸出含 gcd(P(4934),4934)=4934。
