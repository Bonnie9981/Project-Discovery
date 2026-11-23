# DISC-0023 審查（Reviewer）

Reviewer：獨立 subagent，不是作者，也不是 critic。讀過的檔案：
- `records/DISC-0023/` 全部，包括 critic.md 和 proof.md 結尾的作者回應；
- `paper/a073631-counterexample.md`、`results/A073631/`（草稿、README、`code/`）；
- `lean/Discovery/A073631Counter.lean`；
- `data/cx/entries/A073631.txt`、`A130058.txt`、`A376896.txt`；
- `discovery/cxsearch/conjectures.py` 的 `a073631` 和對應的測試；
- RESEARCH.md、DEVLOG.md 的 DISC-0023 段落。

條目文字和工具輸出都只當資料讀，裡面沒有要 agent 做事的文字。

## 審查項目

1. **猜想的讀法。** 逐字原文在 `A073631.txt` 的 %C 和 `A130058.txt` 的 %C，有兩句：「Conjecture: All nonsquarefree terms … are the multiples of 23^2」，以及「It appears that … 1 and 529 … are the only perfect squares」。%N 寫的是「Nonprimes k」，所以 1 也算項。紀錄兩句都處理了，讀法正確。
2. **引理與最小性（紙上）。** 我逐步檢查過，沒有漏洞：
   - 差是奇數、不被 3 整除，所以 q ≥ 5；
   - 3/2 的階整除 gcd(k−1, q(q−1))，而 gcd(k−1, q) = 1，所以階整除 q−1；
   - 最小性：有平方因數 q² 且 q ≠ 23，則 q 在 A376896 裡；
   - 完全平方那一句分兩支，m 只含 23 和 m 含其他質因數。critic 必修 3 要補的後一支已補進 paper 和 proof.md。
   - 23³ 那一支依賴 (3/2)^22 mod 23³ = 9523 ≠ 1，我重算得到相同的值。
3. **沒有把「範圍內成立」說成「證明」。**
   - 「23 和 3842760169 之間沒有其他 3/2 底 Wieferich 質數」：paper、草稿、proof.md 都寫成電腦搜尋（2^32 以下所有質數）的結果。proof.md 也明說最小性沒有形式化。
   - 「掃到 10^9 有 60 個非無平方因數項，全是 529 的倍數」：寫成計算結果。
   - 「有沒有無限多個反例」：標為開放問題。
4. **新穎性。** 不宣稱新穎，`NO_MATCH_IN_SCOPE`。只查了 OEIS（S001、S002）；Web、MathSciNet、zbMATH 沒查，這點有寫明。critic 連不上 oeis.org，沒能重查，這點也誠實標在「未解決的疑點」。存檔的三個條目裡確實沒有 3842760169 和 A073631 之間的交叉引用。
5. **Lean 是否對應猜想。**
   - `InSeq k := 3^(k−1) % k = 2^(k−1) % k`。因為 3^(k−1) ≥ 2^(k−1)，這和「k 整除差」等價，自然數截斷減法不會出問題。
   - 「非質數」用 1 < q1 < q1·q1 且 q1 | q1·q1 表示；「非無平方因數、完全平方」由 k 字面寫成 q1·q1、q1 > 1 直接表明；「不是 529 的倍數」用 `% 529 ≠ 0` 表示。這是反例所需的全部性質。
   - `powModAux_eq` 是一般性的引理，所以用二進位模冪計算沒有改變定義。fuel 也夠：66 > log₂(q1²)，74 > log₂(q2²)。
   - 沒有 `sorry`，也沒有 `native_decide`。
   - CI 在 head 370bfee 上 `build` 通過（job 137597922997）。log 裡 9 個定理的公理都只有 propext / Quot.sound。另有一條 warning，出現在第 96 行 `inSeq_529` 的 exponent threshold，不影響結果。
   - q 是質數沒有進 Lean，反例本身也不需要它；這點 proof.md 已註明。
6. **兩個獨立實作（REFUTED 的要求）。** 以下各方的結果一致，要求滿足：
   - 專案的 C 和 Python 實作；
   - critic 的 Montgomery 搜尋和試除法；
   - Lean kernel；
   - 我自己的字面版（見下節）。
7. **critic 必修是否處理。**
   - (1) 已修。`chk073631.py` 改用 13 個底（2～41），註解寫「deterministic for n < 3.3e24」，現在正確。experiment.md 第 2 點也已改。
     - critic 提過「附加更正」的做法。這份紀錄在本審查之前還沒完成，直接改不算改已完成的紀錄，我接受。
   - (2) 已修。A073631 留言補上了 2^32 搜尋；A376896 留言改成「p > 23」；LINKS 改成「the counterexample is checked in Lean 4」。
   - (3) 已修，同第 2 項。
   - (4) 已修。CI 綠燈，`Nat.sub_mod_eq_zero_of_mod_eq` 已不再使用。
8. **OEIS 草稿用語。**
   - 沒有宣稱新穎。
   - 最小性明寫「A search of all primes below 2^32 finds …」。
   - Lean 只說反例本身被檢查。
   - 草稿裡的數字我逐項核對過，都正確：14766805716452908561、k mod 529 = 349。
   - A130058 的留言寫「it is the smallest one; see A073631」，依據就在 A073631 的留言裡，可以接受。
9. **小瑕疵（非必修）。**
   - RESEARCH.md 把 A073631 寫成「合數 k」。條目原文是「nonprimes」，含 1，白話摘要可以順手改。
   - experiment.md 說「≤ 10^9 共 5420 項，和 b-file 一致」：critic 和我都沒有 b-file，這個總數沒有核對。下節的重跑只確認了程式輸出 5419（不含 1）。

## 重現結果

Scratch 在 `/tmp/claude-0/-home-user/209cc254-616b-5226-a48d-c7b3cb63a113/scratchpad/r22/`，不進 git。全部經 `discovery.limits.run_limited` 執行。

- **`wieferich32.c`**：`gcc -O2 -fopenmp`，跑 `./w 1 4294967296`，涵蓋整個 [1, 2^32)，用了 29.5 秒。
  - 輸出 `HIT 23`、`HIT 3842760169`、`primes_tested 203280219`（= π(2^32) − 2）。
  - 和 experiment.md、critic 一致。
- **`a073631_scan.c 1000000000`**：用了 1 分 58 秒，輸出 `terms(k>1)=5419 nonsquarefree=60 not_mult_529=0`，和 experiment.md 第 3 點一致。
- **`python -I results/A073631/code/chk073631.py`**：印出兩個反例和 `ok`。
- **自己寫的 `mine.py`**（字面定義，不用專案程式）：
  - q1 用試除法確認是質數；
  - (3^(k−1) − 2^(k−1)) mod k = 0，k = q1² 和 q2² 都成立；
  - k mod 529 分別是 349 和 443；
  - (3/2)^22 mod 23³ = 9523；
  - 2·10^5 以下的 3/2 底 Wieferich 質數只有 23；
  - 2·10^5 以下的 A073631 前 12 項和條目 DATA 一致，非無平方因數項全是 529 的倍數。
- **`python -m pytest -q`**：77 passed，1 failed。唯一失敗的是 `test_records.py`，原因是 `DISC-0023: missing review.md`，本檔就是補這個。

## 最終判定

STATUS: REFUTED

A073631 / A130058 裡 Adamchuk 2007 年的兩句話都不成立：
- 「有平方因數的項都是 23² 的倍數」；
- 「1 和 529 看起來是唯一的完全平方項」。

k = 3842760169² 是項，它不是 529 的倍數，也是完全平方數。Lean kernel 照字面定義驗證了這件事（CI 通過，公理乾淨），多套獨立程式和我的重算也一致。

「它是最小反例」由兩部分組成：一是紙上引理，我檢查過正確；二是 2^32 以下的完整搜尋，我重跑過。紀錄、paper、草稿都把這點寫成電腦搜尋的結果，沒有過度宣稱。

critic 的 4 項必修都已處理。我沒有新的必修。

## 給 CEO 的摘要

- OEIS A073631 一條 2007 年的猜想被推翻。最小反例是 3842760169²（約 1.5·10^19），它同時推翻了「只有 1 和 529 是平方數」這句話。
- 原因很簡單：3842760169 是一種罕見的質數（以 3/2 為底的 Wieferich 質數，2024 年才收進 OEIS A376896），只是一直沒人把兩個條目連起來。
- Lean 驗證過反例；最小性靠一段短證明加 2^32 以下的搜尋，我都重做過。
- 不宣稱新穎，價值在修正 OEIS。草稿可以交給使用者自己送出，沒有必修。
