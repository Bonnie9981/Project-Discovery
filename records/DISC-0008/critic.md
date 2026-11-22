# DISC-0008 Critic 報告（R3-L01：規則 26，奇數寬度環，單一種子）

結論先講：**H1 沒有被推翻。** Lean 主敘述忠實表達了 H1，`step` 確實是規則 26，而且和 impl_b 使用同一套位元慣例。紙上證明的每一步我都逐項核過，沒有找到漏洞。CI run 45017724157 的 log 顯示 `Discovery.Rule26` 已編譯，主定理只用到 `propext`、`Quot.sound`、`Classical.choice`。需要修的是文件的一致性，以及新穎性的措辭，見文末「必修」。

## 攻擊項目

1. **`step` 是否真的是規則 26，方向是否和 impl_b 一致。**
   - 做法：對照 26 = 00011010₂，第 1、3、4 位元為 1，也就是鄰域 (左,中,右) = 001、011、100。Lean 的 `step` 三個項依序是 `l & ~c & ~r`（100）、`~l & c & r`（011）、`~l & ~c & r`（001）。`rotL` 的第 i 位元是細胞 i−1，`rotR` 的第 i 位元是細胞 i+1，和 impl_b 的 `left`/`right` 定義逐字相同。另外 `rule26` 定義成 `26 >>> (4l+2c+r)`，`tb_step` 證明了 `step` 的每個位元等於 `rule26 左 中 右`。
   - 實測：我把 Lean 的 `step` 原樣轉寫成 Python（用 `x ^ m` 表示補數）。在 1 ≤ w < 30、每個 w 300 個隨機狀態上，結果和 `impl_b._step(x, 26, w, mask)` **完全相同**。
   - 補充：就算左右方向寫反，得到的也只是鏡像規則 82。單一種子左右對稱，所以週期不會變。方向錯誤只會讓封閉形式鏡像，不會影響 H1 的數字。
   - 結果：**通過。**

2. **主敘述是否忠實、前提是否空洞。**
   - `rule26_odd_period` 有三個合取項：x_P = x₀；對所有 μ，x_{μ+P} = x_μ（暫態 0）；0 < p < P 時 x_p ≠ x₀。x₀ 在循環上，所以循環的最小週期等於 x₀ 的最小回返時間。這三項合起來正好是 (T, P) = (0, P)。`iter_eq_one_iff` 給出更強的 x_t = x₀ ⇔ P ∣ t，就是 H1 的原文。
   - 前提是 `w % 2 = 1 ∧ 3 ≤ w`，不是空的：`check_small` 用 `decide` 在核心中算出 `iter 3 6 1 = 1`、`iter 11 88 1 = 1`、`iter 11 44 1 ≠ 1`、`iter 21 336 1 = 1`。
   - `Nat.log2` 是 core 的下取整 log₂。我的模擬以 `w.bit_length() − 1` 計算 ⌊log₂ w⌋，結果與 Lean 吻合。
   - 結果：**通過。**

3. **w = 3 與小 w 的邊界情況。**
   - 我寫了自己的模擬：字串狀態，1 鄰域集合 {100, 011, 001} 手寫，不讀 26 的位元。w = 3 得到 (T, P) = (0, 6) = 3·2¹。w = 1 得到 (1, 1)，確認排除 w = 1 是必要的。
   - 1 ≤ w ≤ 13 的週期序列是 1,1,6,1,20,2,28,1,72,6,88,4,104，與 literature.md 引用的 A334504 開頭相同。
   - 結果：**通過。**

4. **引理 1（封閉形式）的四種情形。** 逐一手推。
   - 細胞 i−1、i、i+1 在時間 t 的窗口座標分別是 s′−2、s′−1、s′，正確。
   - 情形 1 在 s′ = 2 時（j = 0）用到 b_t(0) = 1，與 b_{t+1}(1) = b_t(0) ⊕ b_t(1) 一致。
   - 情形 3 用到規則 26 的 110→0 與 010→0（第 6、2 位元為 0），正確。
   - 情形 4 用到 w−2 為奇數，w = 3 時 w−2 = 1，也成立。
   - w ≥ 3 保證 0、1、2 互不相同，四種情形確實窮盡且互斥。
   - 反例搜尋：腳本對 3 ≤ w ≤ 129 的每個奇數 w、0 ≤ t ≤ P+2w，逐狀態比對封閉形式，全部相符（見獨立重算）。
   - 結果：**通過。**

5. **引理 2 與定理的兩個整除步驟。**
   - (b) 取 v = v₂(t)：2^m ∤ t 推得 t ≠ 0，且 v < m；Lucas 給出 C(t, 2^v) 為奇數，正確。
   - 2^k ∣ t 那一步：v ≤ k−1，所以 i = 2^{v+1} ≤ 2^k。w 奇且 ≥ 3，所以 2^k ≠ w，2^k < w。因此 0 < i < w。又因為 w ∣ t，(i+t) mod w = i。這樣 x_t(i) = b_t(2^v) = 1，和 x_t = x₀ 矛盾。**k ≥ 1 和 2^k < w 都需要 w 為奇數，這一步沒有漏洞。** Lean 中對應的是 `log2_facts`（2M = 2^k < w < 4M）以及 `hpow`。
   - w ∣ t 那一步：取 i = w − (t mod w) ∈ (0, w)，正確。
   - (⇐) 方向：2j < w < 2^{k+1} 推得 j < 2^k，正確。
   - gcd(w, 2^k) = 1 推得 lcm = P，正確（Lean 的 `odd_mul_two_pow_dvd`）。
   - 結果：**通過。**

6. **實驗程式的獨立性。**
   - 方法 1 用 impl_b，而 Lean 的 `step` 是照 impl_b 轉寫的。兩者共用同一套「旋轉位元字 + 補數」寫法，所以方法 1 加上 Lean 不算兩個獨立實作。
   - 腳本的方法 2 是串列模擬，用 `rule >> (4l+2c+r)` 查表，和 impl_b 確實獨立。
   - 我的字串模擬再加上一層，不經過位元運算查表。
   - 結果：**數字沒有問題；獨立性的說法可接受。**

7. **CI 與公理。**
   - 用 `gh run view` 讀了 run 45017724157 的 log：`Built Discovery.Rule26`；`rule26_odd_period`、`iter_eq_one_iff`、`iter_testBit` 都是 `[propext, Quot.sound, Classical.choice]`；「Reject unfinished proofs」步驟通過；`THEOREM_COUNT 143`（全 repo）。
   - CI 的 commit 是 af98758，裡面的 `lean/Discovery/Rule26.lean` 和工作目錄一致（`git status` 對它沒有 M）。
   - 結果：**通過。**

8. **文件一致性。** 發現 3 個問題（列為必修）：
   - **proof.md 第 3 行**寫「本機編譯通過……**未跑 CI**。依規則，CI 通過之前不算已證明」，但第 141、153 行說 CI 已通過。狀態行互相矛盾。
   - **proof.md 已 commit 的版本叫 `proof_draft.md`**。工作目錄裡是 `RM proof_draft.md -> proof.md`，`hypotheses.md`、`experiment.md`、`literature.md`、`record.json`、`search_evidence.jsonl` 都還是 untracked。record.json 的 `experiment_commit = af98758` 這個 commit 裡**沒有**這些紀錄檔。程式本身（`l01_check.py`、`Rule26.lean`）都在 af98758 裡，重現性沒問題。
   - **腳本輸出寫「Lemma 3」**，proof.md 卻只有引理 1、2，這一項對應的是「引理 1 的局部步驟」。名稱對不上。

9. **文獻與新穎性措辭。**
   - literature.md 把公式定為 MATCH_FOUND（猜想）、證明定為 NO_MATCH_IN_SCOPE，並明白列出還沒查 Math Fun、MathSciNet、zbMATH、Scholar。**這個陳述是誠實的。**
   - 但有兩個疏漏：
     - (a) 機制本身接近民間知識。在無限直線上，規則 26 從單一種子出發的圖樣和規則 90 的 Sierpiński 圖樣相同：圖樣永遠沒有相鄰的 11，所以鄰域 110 不會出現。這在 Wolfram《A New Kind of Science》與 Wolfram Atlas 的規則 26 頁面一類資料中是常見事實。我在本機驗證了「t < w/2 時封閉形式就是完整的 Sierpiński 列」，但**沒能上網核對出處**：oeis.org 被代理擋下（HTTP 403）。literature.md 沒提這一點，容易讓人以為「Pascal mod 2 窗口」這個觀察是本專案新發現的。真正可能新的部分只有環上的邊界分析（情形 3、4）和 Lucas 收尾。這是一個短論證，被 Math Fun 討論串或 A334504 的作者私下證過的可能性不低。
     - (b) A070939(0) = 1，代入 n = 0 會得到 a(1) = 2，但實際 a(1) = 1。OEIS 的公式應只適用於 n ≥ 1。literature.md 寫「A070939(n) = ⌊log₂ n⌋ + 1」時沒有寫 n ≥ 1。內容沒錯，但應註明。
   - A334504 的 FORMULA 引文（Zabolotskii 2024 的「It seems that」）我無法獨立連上 OEIS 核對，只能依賴 S002 的紀錄。

## 獨立重算

- `python3 research/r003/l01_check.py`：`OK: odd 3 <= w <= 61 ...`，0.78 秒。
- `python3 research/r003/l01_check.py 129`：`OK: odd 3 <= w <= 129 ...`，17.2 秒。確認了 experiment.md 中「證明 agent 跑到 129」的說法。
- 自寫腳本 `/tmp/claude-0/-home-user/806b7a32-aefd-5e00-9bbe-a95f27dab2af/scratchpad/crit.py`。字串狀態，手寫鄰域表，用 dict 記錄做循環偵測，不使用 Brent 演算法：
  - 奇數 3 ≤ w ≤ 79：(T, P) 全部等於 (0, w·2^⌊log₂ w⌋)，`bad = []`。
  - 1 ≤ w ≤ 79：前 4w+10 步的軌道和 `impl_b._step` 逐步相同。
  - 1 ≤ w ≤ 13 的 (T, P)：(1,1) (1,1) (0,6) (2,1) (0,20) (1,2) (0,28) (4,1) (0,72) (1,6) (0,88) (2,4) (0,104)，與 `impl_b.orbit` 完全相同。
  - Lean `check_small` 的六個數值（x₁ = 2+2¹⁰、x₈ = 2³（w=11）、w=3 時 x₆ = 1、w=11 時 x₈₈ = 1 且 x₄₄ ≠ 1、w=21 時 x₃₃₆ = 1）用我的模擬重算，全部為 True。
  - Lean `step` 的 Python 轉寫和 impl_b 在隨機狀態上相同（1 ≤ w < 30，每個 w 300 筆）。

## 未解決的疑點

**必修（合併或標「已證明」之前）：**

- **F1** proof.md 第 3 行的狀態要改成「CI 通過（run 45017724157）」，不能再寫「未跑 CI」，與第 141、153 行統一。
- **F2** 把 `proof.md`（rename）和 hypotheses/experiment/literature/record/search_evidence 一起 commit。若 record.json 的 `experiment_commit` 是指程式版本，維持 af98758 沒問題，但要寫明「紀錄檔在之後的 commit」。
- **F3** literature.md 要補上：「規則 26 單一種子在無限直線上等於規則 90 的 Sierpiński 圖樣」是已知事實（NKS／Wolfram Atlas，待核對出處），並把本專案可能新的部分收窄為「環上邊界分析 + Lucas 收尾得到的週期證明」。新穎性目前仍是 NO_MATCH_IN_SCOPE，不能寫成「新定理」。

**建議（非必修）：**

- literature.md 註明 OEIS 公式只適用於 n ≥ 1（w ≥ 3）。
- 把腳本的「Lemma 3」改成「Lemma 1 local step」，或在 proof.md 裡命名一個引理 3。
- 查 Math Fun 2020 年 Klee 的原貼文；Zabolotskii 的猜想也可能附有討論。這是新穎性判定最可能翻盤的地方。

**仍無法排除：**

- OEIS 條目原文（是否確實寫「It seems that」、有沒有後來補的證明連結）我無法連上核對：oeis.org 被代理擋下（403），只能依賴 S002 的紀錄。
- 偶數 w 的「軌道等於規則 90 軌道」只有兩行紙上論證和 w ≤ 40 的數值，沒有形式化。這部分不在 H1 範圍內，不影響本結論。
