# DISC-0020 審查

審查者：獨立 reviewer subagent（不是作者，也不是 critic）。重跑的原始輸出只放在 scratchpad，不進 git。條目原文（`data/cx/entries/A362070.txt`）、search_evidence 和工具輸出都當資料讀，裡面沒有要 agent 做事的文字。

## 審查項目

1. **critic 必修 1（10^10 是幾套程式跑的）：已改好。** proof.md「敘述差異」最後一條現在寫明：n ≤ 2000 有 Python 和 scan.c 兩套程式，n ≤ 10^4 critic 另外重算，10^10 只有 scan.c 跑過（critic 抽查了接近 10^10 的一段）。沒有誇大。
2. **critic 必修 2（四段參數與輸出）：已改好。** experiment.md 列出四段的 `./scan N 0 START` 參數和每段的 `done ... hits=` 輸出。我核對過：下一段的 START 都等於上一段的 N + 1，相鄰對 (n, n+1)，n ≤ 10^10，都剛好比到一次。
3. **Lean 定理有沒有照條目的 %N 寫：有。**
   - `rf t k` 就是 t(t+1)⋯(t+k−1)，`P k m` 就是 ∏_{t=1..m} rf(t, k)。
   - `IsMMin` 是「最小的 m ≥ 1」，`IsKempner` 是「最小的 K ≥ 1 使 n | K!」（與 A002034 一致）。
   - `AValue` 是 Σ_{r=1..K} m_min(n, r)（r = i + 1）。
   - 另外有 `avalue_unique` 證明 `AValue` 對每個 n 只有一個值，所以 `a362070_counterexample` 確實說的是「a(1715) = a(1716)」，不是在一個多值關係裡挑巧合。只用 core 和 `decide`，沒有 `native_decide`。本機沒有 Lean，能不能編譯要看 CI。
4. **結論有沒有證據支持：有，符合 REFUTED。** 這個反例有五方確認：Lean kernel、條目自己的 Maxima 程式、brute.py、factored.py、scan.c，另外還有我自己的程式（見下節）。RESEARCH_STANDARDS 要求的「兩個獨立實作」綽綽有餘。「最小、而且 10^10 以下唯一」是篩法窮舉的結果，paper 和草稿都寫成「a sieve … finds」，沒有說成證明。
5. **paper 與 OEIS 草稿：沒有誇大，也沒有主張新穎。** 1716 的推理（m_min = 14 − r）是對的。1715 的 21 個值和 r = 2 的例子，我都重算對上了。草稿說的「only one up to 10^10」和「a(n) = n 在 10^10 以內沒有新解」，experiment.md 都有支撐。草稿也要求送出者自己能說明、用條目的程式驗過再送。
6. **新穎性：** 只查了 OEIS（S001、S002），coverage_limits 有誠實寫出來。紀錄只主張「指出反例」，`NO_MATCH_IN_SCOPE` 用得恰當。
7. **次要（不必修）：**
   - experiment.md 重現指令裡的 `entry_program.mac` 也會算 a(1714)。1714 = 2·857，所以 K = 857，Maxima 在 100 秒內跑不完。只算 a(1715)、a(1716) 的話不到 1 秒。
   - `a332786.c` 要用 `lo hi` 兩個參數呼叫，experiment.md 沒寫，不給參數會 segfault。這不影響 A362070 的判定。

## 重現結果

- `python3 results/A362070/code/brute.py 1715 1716` 輸出 `1715 91 21`、`1716 91 13`。
- 我自己寫的程式：用 sympy 分解，對每個 p^e 用 v_p(m!) 的差求最小 m，不 import 專案的程式碼。
  - n = 1..57 與 DATA 完全相同。
  - a(1714..1717) = 367653, 91, 91, 5151。
  - n ≤ 10^4 時，a(n) = a(n+1) 只有 n = 1715；a(n) = n 但 n 不是「奇質數 p 的 p(p+1)/2」的，只有 1 和 16。
- 條目的 Maxima 程式（Maxima 本機有裝）：n = 2..20 和 DATA 相同，`a(1715), a(1716)` 印出 `91 91`。
- `scan.c` 重新編譯，跑 `100000000`：`FIX n=1`、`FIX n=16`、`HIT n=1715 a=91`、`done N=100000000 hits=1`，約 12 秒。10^10 沒有重跑，依 experiment.md 的四段紀錄與 critic 的抽查。
- `a332786.c 1 5000` 只輸出 `WEAK m=49`，和紀錄一致。
- `pytest tests/test_cxsearch.py tests/test_records.py tests/test_research_summary.py`：寫 review.md 前只有「DISC-0020 缺 review.md」這一項失敗，寫完後重跑 15 passed；`python -m discovery.check_record` 為 0 problems。

## 最終判定

STATUS: REFUTED

A362070 的猜想「a(n) = a(n+1) 無解」不成立：a(1715) = a(1716) = 91。Lean 照定義逐字形式化，並由 kernel 算出這兩個值；有多套獨立程式和條目自己的程式確認；我自己也重現了。critic 的兩項必修都已改好。其他候選的狀態（A332786、A349093 為 INCONCLUSIVE，A266651 為 SUPPORTED_KNOWN）維持不變。

必修：無必修。合併前要確認 CI 的 Lean 工作（含 AxiomCheck）通過；如果 `decide` 逾時或編譯失敗，就不能合併。

## 給 CEO 的摘要

OEIS A362070 的作者猜「相鄰兩項永遠不相等」，並說驗到了 10^4。其實 1715 和 1716 兩項都是 91，而 1715 < 10^4，條目自己附的程式就算得出來。我照定義另外寫了程式，也跑了條目的 Maxima 程式，都得到 91、91。Lean 證明照定義逐字寫，等 CI 編譯通過。10^10 以內只有這一組，這是電腦窮舉的結果，不是證明，文件也是這樣寫的。判定為推翻（REFUTED），可以交給使用者決定要不要送 OEIS。
