# DISC-0003 critic.md

作者：critic（獨立 subagent）

我讀了 RESEARCH_STANDARDS.md、AGENTS.md、critic.md 角色檔、本紀錄所有檔案、`research/r001/disc0003/` 全部程式、`lean/Discovery/Consecutive.lean`、`tests/test_disc0003.py`。我沒有修改 impl_a.py、impl_b.py、run.py 或其他紀錄檔。外部資料（OEIS 名稱與數據、search_evidence.jsonl）只當資料讀，裡面沒有出現要 agent 做事的指令。

## 攻擊項目

### A1. H1～H4 的邊界值（N = 1、2 的冪、平方數、2N 是平方數、D > N）
- 做了什麼：寫了一個與專案程式無關的暴力計數 `brute(N, D)`，對所有 1 ≤ a, k ≤ N 檢查 `k·a + D·k(k−1)/2 == N`，在 N ≤ 300、D = 1..8 和 impl_c 的生成函數表比對。另外在 impl_c 的表上跑完整的 H1～H6，N ≤ 100000（H5 是 N ≤ 10000）。
- 結果：全部一致。我逐一看了幾類邊界：
  - N = 1：R(1) = 1，d_odd(1) = 1；H2b 中 1 = 2⁰ 被正確算成 2 的冪（impl_a 用 while 除 2，impl_b 用 `n & (n−1)`，impl_c 用明確的集合 {1, 2, 4, …}，三者都包含 1）。
  - 2N 是平方數（N = 2, 8, 18, 32, 50, …）：H3 中 d² = 2N 不可能發生（d 奇數），impl_c 用 `m > d²//2` 切分，三套一致。
  - 平方數：H4 中 ⌈τ/2⌉ 在 τ 為奇數時才和 ⌊τ/2⌋ 不同。impl_c 用 `2·R₂ ∈ {τ, τ+1}` 檢查，沒有發現不一致。
  - D > N：H5 的 N < 8 都在測試範圍內（例如 N = 1、D = 8：左邊 = 1，右邊只有 k = 1 符合，m = 2）。
- 敏感度檢查（確認這些檢查真的抓得到錯）：H3 的條件改成 d² < N、H4 改成 d² < N、H5 的「≥ 2」改成「≥ 0」，三種改法在 **N = 1** 就失敗。所以三個判準不是「怎麼寫都會過」。

### A2. 定義差異（是否算單項、首項能否為 0）
- 做了什麼：手算比較不同定義。
- 結果：結論取決於定義。如果允許首項為 0，N = 3 有 3、1+2、0+1+2 三種寫法，但 d_odd(3) = 2，H1 就失敗（每一組從 1 開始的寫法都多出一組從 0 開始的，所以差 [N 是三角數]）。如果公差 2 允許首項為 0，N = 6 多出 0+2+4，R₂(6) 變成 3，但 #{d ∣ 6 : d² ≤ 6} = 2。本紀錄的所有地方都一致用 a ≥ 1、k ≥ 1，包含單項：hypotheses.md、impl_a（`range(1, …)`）、impl_b（`rest // k >= 1`）、Lean（`Icc 1 N` 加上 `mem_reps`）、impl_c（s0(k) = k + D·k(k−1)/2，也就是 a = 1）。**沒有發現定義不一致**，但 literature.md 和 OEIS 名稱裡的「consecutive integers」不一定指正整數，見 A8。

### A3. H6 的反例與完整刻畫
- 做了什麼：用 impl_c 的表列出 N ≤ 100000 中所有 R₂(N) > R₁(N) 的 N。
- 結果：恰好有 25000 個，**正好是所有 4 的倍數**。R₂ = R₁ 的 N 是 N = 1 以及 N ≡ 2 (mod 4)。可以證明：令 N = 2^e·o（o 奇數），則 R₂ = ⌈(e+1)τ(o)/2⌉，R₁ = τ(o)。e = 0 時 R₂ ≤ R₁，e = 1 時兩者相等，e ≥ 2 時 R₂ ≥ 3τ(o)/2 > R₁。所以 H6 不只在 N = 4 失敗，而是「H6 ⇔ 4 ∤ N」。紀錄只寫了最小反例 4，不算錯，但可以補上這個刻畫。

### A4. 獨立性：H5 的 impl_b 是同義反覆（中度）
- 做了什麼：比對程式碼的代數。
- 結果：impl_b 在 H5 的左邊 `rest % k == 0 and rest // k >= 1`（rest = N − D·k(k−1)/2）和右邊 `general_b`（k ∣ 2N，2N/k − (k−1)D 是偶數且 ≥ 2）**代數上等價**，因為 N − Dk(k−1)/2 = k·a ⇔ 2N = k(2a + (k−1)D)。所以 impl_b 對 H5 只在檢查「`factorise` 列出的因數是否完整」，對猜想本身沒有任何證據力。experiment.md 說「獨立性比 H1 弱」太輕描淡寫了：在加入 impl_c 之前，H5 的實質證據**只有 impl_a 一套**（逐項列舉的左邊，對比試除法的右邊）。impl_c 用生成函數篩法算左邊、用 k 的倍數篩法算右邊，補上了第二個實質比對。
- 另外，run.py 中兩套 H5 的右邊（`general_a`、`general_b`）寫的是同一個式子，只是列舉 2N 因數的方法不同。這是猜想本身的敘述，可以接受，但應在 experiment.md 寫明。

### A5. 獨立性：impl_b 的 H4 沒有檢查前半（輕度）
- 做了什麼：讀 run.py 的 H4。
- 結果：`holds_b` 只檢查 `R₂ == ⌈τ/2⌉`，**沒有**檢查 `R₂ == #{d ∣ N : d² ≤ N}`。所以在 Python 端，H4 的前半只有 impl_a 檢查過（Lean 的 `card_reps_two` 有證明這半）。impl_c 兩半都檢查。這不影響結論，但「兩套實作都檢查了 H4」的說法對前半不成立。

### A6. 範圍與 off-by-one
- 做了什麼：讀 impl_a 的 `rep_table`、impl_b 的 `rep_count` 迴圈邊界，並和暴力計數比對（見 A1）。
- 結果：impl_a 先加總、再判斷 `s > n_max` 才停，所以剛好等於 n_max 的和會被記到；impl_b 的迴圈條件 `k + D·k(k−1)/2 <= n` 正好是最小的 k 項和。兩邊都沒有 off-by-one。兩套定義域都是 1..n_max，verify 回報 `domain_independent: True`。

### A7. E13 的質數集合寫死（輕度，目前不影響）
- 做了什麼：把 run.py 寫死的 `{2,3,5,7,11,13,17,19}` 和真正的質數判斷比較。
- 結果：兩者**從 N = 276 開始不同**（k = 23 時最小和是 23·24/2 = 276）。EXT_TERMS = 80，所以目前送查的序列是對的。但描述寫的是「prime number of terms」，如果以後把 EXT_TERMS 調到 ≥ 276，就會悄悄送出錯的序列。建議改成真正的質數判斷，或在描述註明 k ≤ 19。

### A8. 新穎性：E5 與 A239140 可以證明等價（修正 experiment.md 的「等價性未證明」）
- 做了什麼：推導，並用 OEIS 快照的全部 86 項驗證。
- 論證：設相異正整數 x₁ < … < x_k，母體標準差為 σ。k 個相異整數的最小變異數是連續整數時的 (k² − 1)/12。k ≥ 4 時這個值 ≥ 15/12 > 1，所以 σ ≥ 1。k = 1 時 σ = 0。k = 2 時 σ = (x₂ − x₁)/2 < 1 ⇔ 兩數相鄰。k = 3 時，連續整數的 σ² = 2/3 < 1；間隔 (1, 2) 或 (2, 1) 時 σ² = 14/9 > 1，間隔更大只會更大。所以「σ < 1 的相異部分分割」⇔「長度 ≤ 3 的連續正整數和」，對所有 n ≥ 1 成立，也就是 E5 = A239140。
- 前提：A239140 用的是**母體**標準差。如果用樣本標準差（除以 k − 1），三個連續數的 σ = 1，不滿足「< 1」，那 a(6) 會是 1。快照中 a(6) = 2，所以 OEIS 用的是母體標準差，前提成立。
- 附帶結果：E5 有封閉式 E5(n) = 1 + [n 奇數且 n ≥ 3] + [3 ∣ n 且 n ≥ 6]，n ≥ 6 起週期為 6。impl_c 在 n ≤ 100000 驗證通過。這進一步說明 E5 是平凡序列。
- 結論：E5 判為 `MATCH_FOUND` 是正確的，而且不只是前 80 項吻合，而是定義上等價。experiment.md 的「等價性未證明」可以改成「已證明等價（critic A8）」。

### A9. 新穎性：E7 對到 A072670 有索引位移（輕度）
- 做了什麼：檢查 A072670 的實際索引。名稱是「n = i·j + i + j, 0 < i ≤ j 的寫法數」。i = j = 1 給出 3，所以 a(3) = 1；4 + 1 = 5 是質數，所以 a(4) = 0。快照的資料是 0,0,0,1,0,1,…，代表 A072670 的 offset 是 0。
- 結果：E7(n) = A072670(**n − 1**)，原因是 (i+1)(j+1) = n + 1，而 E7(n) = #{d ∣ n : 2 ≤ d ≤ √n}。novelty 工具回報「identity, offset 0」，意思是資料位置對齊，不是 n 對齊。完全吻合判 `MATCH_FOUND` 沒錯，但 experiment.md 的表應註明 n 有位移一位。其他 12 個吻合我也和快照全部項數（86～105 項）比對過，數值都一致（見「獨立重算」）。
- 另外，A131576、A111775 的 OEIS 名稱寫「consecutive integers」，沒有說「正」。如果允許 0 或負數，N = 3 的偶數項寫法除了 1+2 還有 (−2)+(−1)+0+1+2+3（6 項），A131576(3) 就會 ≥ 2 而不是 1（一般地，把正整數寫法 a..b 延伸成 −(a−1)..b 會使長度 2a+k−1 的奇偶反轉，整數版的偶數項寫法數 = d_odd(N)）。快照資料和**正整數**版本一致，所以吻合是成立的，只是 OEIS 名稱的用字不精確。

### A10. 新穎性：E13 的 NO_MATCH_IN_SCOPE 是否被誠實標示
- 做了什麼：讀 S002、S003 的覆蓋限制，另外在離線快照中找 E13 從 n = 3 開始（去掉開頭的 0）的 20 項連續子字串，也在 names.gz 搜尋同時含「consecutive」和「prime number of」的名稱。
- 結果：快照中 0 筆吻合；名稱搜尋找到 9 筆，全部是關於「連續質數」或二進位/三進位數字，沒有一筆是 E13。紀錄的標示是誠實的：experiment.md、literature.md 都寫「不代表新」，S002 註明只查前 30 項、沒有做變換，S003 註明只讀了 11 頁中的第 1 頁。
- 補充一個反面證據：E13 有平凡的封閉式 E13(N) = [N 奇數且 N ≥ 3] + #{奇質數 p ∣ N : p² < 2N}（我在 N ≤ 20000 驗證通過；推導方式：H3 的雙射中，偶數長度且是質數只能是 k = 2，這對應到 N 是奇數）。這比「很可能沒有數學意義」更具體，建議寫進紀錄，**不應**把 E13 往 `PENDING_REVIEW` 推。

### A11. Lean 敘述的忠實度
- 做了什麼：逐條讀定義，並在本機編譯（`lake env lean Discovery/Consecutive.lean`，約 11 秒，沒有錯誤也沒有警告）。另外寫了一個只匯入此檔的 scratch 檔，跑 `#print axioms`，並用 `decide` 驗證 `(reps 1 15).card = 4`。
- 結果：
  - 公理檢查：`card_reps_one`、`card_reps_one_two_le`、`repsTwoLe_eq_empty_iff`、`card_reps_two` 都只依賴 [propext, Classical.choice, Quot.sound]。`decide` 的例子也通過。
  - `reps D N` 用 `Icc 1 N ×ˢ Icc 1 N` 做範圍，**不會漏解**：`mem_reps` 證明了任何 a ≥ 1、k ≥ 1、apSum = N 的 (a, k) 都在範圍內（由 2N + Dk = k(2a + Dk) 推出 a ≤ N、k ≤ N）。
  - `apSum D a k = ∑ i ∈ range k, (a + D·i)` 與 hypotheses.md 的定義一致。
  - N = 0：`Nat.divisors 0 = ∅`，`reps D 0 = ∅`，所以 H1、H4 在 N = 0 時兩邊都是 0。H2b 有加 `1 ≤ N` 的假設，這是必要的：N = 0 時 `repsTwoLe 0 = ∅` 為真，但不存在 m 使 0 = 2^m。
  - 和 hypotheses.md 的差異：
    1. H3 沒有形式化。
    2. H4 只形式化了 `#{d ∣ N : d·d ≤ N}` 那半，⌈τ/2⌉ 那半沒有。
    3. H5 沒有形式化（Lean 對一般 D 只有 `two_mul_apSum` 和 `mem_reps`）。
    4. H2a 是 ℕ 減法；因為 1 永遠是 N ≥ 1 的奇因數，不會截斷。
  - proof.md 已經如實寫出差異 1、2、4。H5 沒有 Lean 證明這點，proof.md 也有寫。**沒有發現 Lean 敘述與猜想不符的地方。**

### A12. literature.md 是否誇大
- 做了什麼：對照 search_evidence.jsonl。
- 結果：沒有發現誇大新穎性的地方。所有基準都標成已知，書本頁碼也註明是「抄自 OEIS，原書未開」。有一處用詞不精確：literature.md 的查詢紀錄表寫「OEIS 線上（使用者 Chrome）」，但 search_evidence 的 `searched_by` 是 `claude-in-chrome`，也就是 AI 操作瀏覽器，不是使用者本人查的。建議改成「claude-in-chrome」，以免被誤讀成人工查證（這會影響 NOVELTY_SUPPORTED 需要人參與的規則）。

## 獨立重算

impl_c：`research/r001/disc0003/impl_c.py`。只 import 標準函式庫，沒有 import 同目錄的其他模組。方法如下：
- 寫法數：從生成函數 Σ_k x^{k + Dk(k−1)/2}/(1 − x^k) 取係數，對每個 k 做步長為 k 的篩法。這和 impl_a（固定首項 a、累加部分和）、impl_b（對每個 n 測試整除性）都不同。
- 奇因數個數、H3 的大小切分、#{d ∣ N : d² ≤ N}、τ(N)：都用因數篩法（對每個 d 標記它的所有倍數）。這和 impl_a 的試除法、impl_b 的質因數分解都不同。
- 2 的冪：用明確產生的集合判斷。
- H5 右邊：對每個 k 篩出所有偶數倍數 M = 2N，再檢查 M/k − (k−1)D。

實際跑過的檢查：
1. `python -m discovery.independence` → `checked 1 research dirs with impl_*.py, 0 problems`。
2. `python -m research.r001.disc0003.run 100000`：總共 27.5 秒，遠低於 600 秒上限；impl_c 單獨跑全部檢查約 1.2 秒。七個猜想都是 `implementations: 3`、`disagreements: []`、`domain_independent: True`、`stopped_reason: None`。狀態如下：H1、H2a、H2b、H3、H4 在 1..100000 是 SUPPORTED_IN_RANGE；H5 在 1..10000、D = 1..8 是 SUPPORTED_IN_RANGE；H6 是 REFUTED，反例 N = 4（三套都同意）。除了 `implementations` 從 2 變 3 以外，結果與 `experiment_data.json` 完全相同，`extensions` 也完全相同。這次執行的 commit 是 `4668a62…-dirty`，dirty 的原因只是多了未追蹤的 impl_c.py，所以不能當最終證據，orchestrator 需要在 commit 後重跑。
3. `python -m pytest -q tests/test_disc0003.py` → 3 passed（含 impl_c 時）。
4. 暴力法比對：impl_c 的 `gf_table` 和 O(N²) 暴力計數在 N ≤ 300、D = 1..8 一致。
5. 延伸序列：用 impl_c 重算 H1_R1、E1～E12，和 novelty_data.json 的 query（80 項）一致，也和 OEIS 快照中對應 A 號在 offset 之後的**全部**項數一致：A001227 105 項、A069283 100、A082647 105、A131576 105、A111775 104、A239140 86、A038548 105、A072670 105、A117277 105、A243223 97、A334461/A334541/A334948 各 105 項。E13 的前 30 項和 S002 的查詢字串一致。
6. 其他數字：H6 反例集合 = {N ≤ 100000 : 4 ∣ N}，共 25000 個（A3）。E5 封閉式在 n ≤ 100000 成立（A8）。E13 封閉式在 N ≤ 20000 成立（A10）。E13 寫死的質數集合從 N = 276 起和真正的質數判斷不同（A7）。

## 未解決的疑點

1. impl_c 是在 dirty 的工作目錄上跑的（commit `4668a62…-dirty`）。三方一致的結果要等 orchestrator commit impl_c 後重跑，才能當正式證據。我沒有 commit。
2. H3、H5 仍然只有範圍內檢查，沒有 Lean 證明。H3 是 H1 雙射的直接推論（k 奇 ⇔ k = d < m），補上形式化的成本很低，建議做。H5 在本質上是定義的重述（A4），把它當成「猜想」的價值有限。
3. A8 的 E5 = A239140 證明依賴「A239140 用母體標準差」。這是從 a(6) = 2 反推的，我沒有讀 A239140 頁面上的程式或定義原文（線上 OEIS 從這個容器連不到）。如果頁面寫的是別的標準差定義，就需要重新檢查。
4. 我沒有查 OpenAlex、arXiv、Crossref，因為這次不需要。E13 的文獻查證仍然只有 OEIS。這不影響判定：根據 A10，E13 是平凡的組合，不值得進一步查新穎性。
