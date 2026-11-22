# DISC-0010 Critic

- 對象：DISC-0010（R2-C10 的 w ≡ 0 (mod 4) 段），工作分支 `claude/project-thread-10t4bs` 的未提交狀態。
- 審查範圍：`literature.md`、`hypotheses.md`、`experiment.md`、`proof.md`、`record.json`、`lean/Discovery/Rule54Mod4.lean`、`research/r003/l03_rule54_mod4.py`。
- 外部文字：本次沒有讀任何論文、網頁或 OEIS 文字，沒有遇到嵌入的指令。

## 攻擊項目

### 1. Lean 敘述是不是 R2-C10 在 w ≡ 0 的內容

- **做了什麼：** 在暫存複本加 `#check @Discovery.Rule54Mod4.rule54_mod4_zero` 和 `#print axioms`，Lean 4.15.0、`LEAN_PATH=/tmp/lb` 編譯。
- **結果：**
  - 型別是 `∀ w, w % 4 = 0 → 4 ≤ w → (∀ μ, iter w (μ+4) 1 = iter w μ 1 ↔ T w ≤ μ) ∧ (∀ p, 0 < p → p < 4 → iter w (T w + p) 1 ≠ iter w (T w) 1)`。前提只有 `w % 4 = 0`、`4 ≤ w`，沒有別的前提，也沒有上界。`step`、`iter`、`T` 都直接 `open` 自 `Discovery.Rule54`，沒有重新定義。
  - 公理：`propext, Classical.choice, Quot.sound`（`rule54_mod4_zero`、`iter_cone` 都是）。三個檔案（Rule26、Rule54、Rule54Mod4）用 grep 找 `sorry/admit/axiom/native_decide/implemented_by/extern/unsafe`，只在註解文字裡出現 `native_decide` 這個字。
  - 編碼：DISC-0006 的 `step` 是 `x xor (rotL ∨ rotR)`，`step_eq` 用 `rfl` 證明，等於借用 Rule26 已證的旋轉位元引理。我用自己的程式**直接查 Wolfram 規則表**（54 = 00110110，鄰域 (l,c,r) 查第 4l+2c+r 位）模擬，結果和「中 XOR（左 OR 右）」一致（見獨立重算），所以編碼沒錯。
  - 量詞：「x_{μ+4} = x_μ ⇔ μ ≥ T」加上「x_{T+p} ≠ x_T（p = 1, 2, 3）」已經完全決定 (μ, λ) = (T, 4)：λ 是 x_T 的最小週期，等於 4；μ 是第一個在循環上的位置，等於第一個 x_{μ+λ} = x_μ 的位置。所以 proof.md「敘述差異」第 2 點說的「標準等價沒有形式化」其實不是缺口，只是寫得比需要的保守。
  - 非空洞性：暫存複本裡從主定理推出 `iter 8 5 1 ≠ iter 8 1 1`（μ = 1 < T = 2）以及 `iter 1000 502 1 = iter 1000 498 1`，都編譯通過。所以定理可以實際套用，前提也可以滿足。
- **結論：** 敘述就是 R2-C10 在 w ≡ 0 (mod 4) 的內容，而且還多涵蓋 w = 4（DISC-0005 原本的敘述是 w ≥ 6；w = 4 時 (0, 4) 也對，我實際算過）。沒有找到偷加的前提。

### 2. 紙上證明逐步檢查

- **第 1 步（ether 自己走一步）：** `ee_table` 第一個合取項是 16 種 (t mod 4, i mod 4) 的 `decide`。用 i+3 代表 i−1，在 w ≡ 0 時成立（`iL_mod` 用 `4 ≤ w` 處理 i = 0 → w−1）。沒問題。
- **第 2 步（光錐歸納）：** 逐類核對：
  - 歸納條件 2t+6 ≤ w 時，錐外有 w − 2t − 1 ≥ 5 格，所以 i = t+1 的右鄰 t+2 在錐外（需要 2t+2 < w，成立），左前緣也一樣。「只有一個鄰居活」成立。
  - 右緣 i = t、左鄰 t−1：t ≥ 1 時在錐內，用到 E(t+1,t) = E(t,t) XOR E(t,t−1)，在 `ee_table` 第 4 項。t = 0、i = 0：E(1,0) = 1（奇數時刻只有 i ≡ 2 是死的），Lean 用 `rfl`。
  - 錐內兩鄰都在錐內，跨過 0 和 w−1 的接縫時餘數一致要靠 w ≡ 0，Lean 的 `E_congr (iL_mod …)` 有處理。
  - Lean `cone_step` 的每個 `hit` 都是由 `omega` 從 `iL/iR` 的 if 展開推出，沒有漏掉的分支（例如 i = 0 屬於錐內、i = w−1 屬於左錐）。
  - **邊界是否收得太緊：** 我另外檢查 t = T+1（2t+4 = w+2，超出引理範圍），錐形公式在 w ≤ 1600 的 400 個寬度**仍然成立**。所以引理的條件 2t+4 ≤ w 是夠用而非最緊，不影響正確性。
- **第 3 步（T 時合攏）：** w = 4m、T = 2m−2，錐外是 i 滿足 i > T 且 i + T < w，也就是 2m−1 ≤ i ≤ 2m+1，三格，餘數 T+1、T+2、T+3。T 是偶數，ether 只在 i ≡ T 活，所以三格本來就該死。Lean `iter_T_ether` 用 `omega` 推出 `i % 4 ≠ T % 4`。w = 4 時 T = 0，錐外是 1、2、3，一樣成立。
- **第 4 步：** `ether_step` 只需要 w ≡ 0 和 `E_step`，對所有 k 歸納。沒問題。
- **第 5 步：** 見證格是 (T mod 4 + 1) mod 4（p = 1, 3）和 T mod 4（p = 2），都 < 4 ≤ w。我手算過：偶數相位 a，格 a+1 在 t = T 時死；在 T+1（奇數相位 a+1，死格餘數 a+2）和 T+3（死格餘數 a）時活；格 a 在 T 時活、在 T+2（偶數相位 a+2）時死。正確。
- **第 6 步（最小性）：** μ < T 時，`periodic_from` 推出 x_{T+3} = x_{T−1}。第 T+1 格在 t = T−1 時是否在錐外：T+1 > T−1，而且 (T+1)+(T−1) = 2T = w−4 < w，所以在錐外、是死的；在 T+3（奇數相位 T+3，死格餘數 T）時是活的。矛盾成立。w = 4 時 T = 0，`hlt : μ < 0` 不可能，不需要這一步。Lean 的 `iter_cone … (T w − 1)` 需要 2(T−1)+4 ≤ w，成立。
- **結論：** 五類光錐歸納、T 時合攏、最小性論證都沒有找到漏洞。

### 3. Lean 檔案裡的小問題（不影響正確性）

- `rule54_mod4_zero` 裡 `hne` 的註解寫「cell `j + 2` (dead at `T w`) is alive at `T w + 1` and `T w + 3`」，**這是錯的**：j+2 在 T+1 時剛好是奇數相位的死格（死格餘數是 (T+1)+1 = T+2）。程式實際用的見證是 `ee_witness` 的 j+1，所以證明沒錯，只是註解和程式碼不一致。
- `have hj : T w % 4 + 2 < w` 是配合錯誤註解留下來的，後面沒有用到；`hT'` 也沒用到。
- `iter_T_ether` 裡 `have ht : … ∨ True := Or.inr trivial; clear ht` 是沒有作用的死碼。

### 4. 數值腳本 `research/r003/l03_rule54_mod4.py`

- 錐形檢查的範圍 `t in range(0, T+1)` 剛好對應 2t+4 ≤ w，沒有 off-by-one。ether 檢查 T..T+8。
- 方法一（`impl_b` + Brent）和方法二（同一個檔案裡的 list 模擬）的實作方式確實不同（位元運算對串列）。但方法二寫在同一個檔案裡，而且錐形和 ether 的檢查只用方法二的歷史，所以「兩個獨立模擬」只涵蓋 (T, P)，不涵蓋 H1、H2 的逐格檢查。已經由第三方重算（下一節）補上。
- 我實際跑了 `python research/r003/l03_rule54_mod4.py 400`，輸出 `OK: w = 4, 8, ..., 400 (100 widths)`（log：`logs/python_research_r003_l03_rule54_mod4.py_400.log`）。

### 5. 措辭與文獻

- 沒有找到宣稱新穎的句子；`literature.md` 明說「屬於習題程度、新穎性不宣稱」，`record.json` 也是 `SUPPORTED_NOVELTY_UNCHECKED` / `NO_MATCH_IN_SCOPE`，符合 RESEARCH_STANDARDS 第 1 節（`PROVEN_*` 需要 CI 通過；本紀錄只有本機編譯，維持 SUPPORTED 是對的）。
- `literature.md`「研究空白」第 1 點的證據力弱：DISC-0006-S005 查的是四個餘數類混在一起的數列。w ≡ 0 這段單獨看是 0, 2, 4, 6, …（偶數），OEIS 一定查得到、也一定無法辨別。所以「沿用 S005 查無」對 w ≡ 0 這段**沒有任何資訊**，應該明說，不要寫成像是一項查證。
- 「Martínez 等 2005」：我記得的規則 54 滑翔機碰撞論文是 Martínez、Adamatzky、McIntosh 在 *Chaos, Solitons & Fractals*（2006 年左右）。這是我的記憶，**沒有查證**。作者也已經標註「沒有重讀原文」，建議出處寫成「年份與卷期待核對」，或在之後查證後再補。
- 沒有查過的相關方向：Jen 在 1980 年代後期關於「cylindrical cellular automata」（初等 CA 在環上的週期和暫態）的論文，以及 Wolfram 1980 年代初等 CA 在有限環上的循環結構表。這兩者最可能已經包含「規則 54 單種子在環上」的資料。這些是我憑記憶提出的查證方向，不是已確認的出處。
- `record.json` 的 `proof` 寫「two independent simulations」，見第 4 點：逐格錐形檢查只有一套實作。

### 6. 專案規則

- `RESEARCH.md` 沒有 `## DISC-0010` 這一節，`DEVLOG.md` 也沒有提到。我跑了 `pytest tests/test_research_summary.py`，**失敗**：`RESEARCH.md 缺少這些紀錄的白話摘要：['DISC-0010']`。
- `python -m discovery.check_record`：DISC-0010 只缺 `critic.md`（本檔）和 `review.md`，沒有其他問題。`python -m discovery.independence`：0 個問題（本紀錄沒有新增 `impl_*.py`）。

## 獨立重算

- 程式：critic 自己寫的兩支程式，都不 import repo 任何模組，用 `python -I` 跑，放在 scratchpad（`crit_r54.py`、`crit_r54c.py`）。
  - `crit_r54.py`：bytearray 環，**直接查規則 54 的 Wolfram 表**（`(54 >> (4l+2c+r)) & 1`），用字典找第一次重複，得到 (μ, λ)。
  - `crit_r54c.py`：自己寫的整數位元模擬（自己的旋轉），用字典找重複；對每個 t ≤ T 逐格比對錐形公式，對 T..T+3 逐格比對 ether；另外記錄 t = T+1 時錐形公式是否仍然成立。
- 結果：
  - w = 4, 8, …, 400（100 個寬度）：`crit_r54.py` 全部 (μ, λ) = ((w−4)/2, 4)，0 失敗，約 0.3 秒。
  - w = 4, 8, …, 1600（400 個寬度），用 `discovery.limits.run_limited` 跑（timeout/cpu/memory/file_size 都有套用）：(μ, λ) 全對，錐形（t ≤ T）和 ether（T..T+3）逐格全對，0 失敗，17.8 秒。樣本：w = 4 → (0, 4)，8 → (2, 4)，12 → (4, 4)，400 → (198, 4)。
  - 附帶檢查其他餘數，w ≤ 40：w = 5 是 (5, 1)；6 ≤ w ≤ 40 全部符合 DISC-0006 的 `T` 公式、週期 4。和 DISC-0006 critic 的結果一致。
- 規則表版和「中 XOR（左 OR 右）」版給出同樣的 (μ, λ)，這也獨立確認了 `Rule54.step` 的編碼就是規則 54。

## 未解決的疑點

1. **CI 還沒有跑。** 本機編譯通過、公理只有 propext、Classical.choice、Quot.sound；但 `lean/Discovery.lean` 已經 import `Rule54Mod4`，最後要以 CI 的 `lean` 工作和公理稽核為準。
2. **新穎性和已知程度都沒有查。** 本紀錄沒有新增任何查詢；OEIS 查詢對 w ≡ 0 這段沒有辨別力（見攻擊項目 5）；Jen 的 cylindrical CA 論文和 Wolfram 的有限環表都沒有查。依目前證據，最可能的情況是「已知或屬於民間常識」，但沒有出處可以確認。
3. **文獻出處的年份和卷期**（Hanson–Crutchfield 1997、Boccara–Nasser–Roger 1991、Martínez 等）都是憑記憶，沒有核對。
4. w ≡ 1, 2, 3 (mod 4) 仍然只有 DISC-0006 的有限核驗（6 ≤ w ≤ 200），本紀錄沒有處理。紀錄裡已經寫明，沒有誇大。

## 必修

1. 在 `RESEARCH.md` 加上 `## DISC-0010` 白話摘要、更新候選清單和「最後更新」日期（`tests/test_research_summary.py` 目前失敗）；依 CLAUDE.md 在 `DEVLOG.md` 加一行。
2. 修正 `rule54_mod4_zero` 裡 `hne` 的錯誤註解（j+2 → 實際用的見證是 j+1；j+2 在 T+1 時是死的），刪掉沒用到的 `hj`、`hT'`。
3. `literature.md`「研究空白」第 1 點和 `record.json` 的 `novelty.note` 要說明：沿用的 OEIS 查詢是四類混合數列，對 w ≡ 0 這段（就是偶數列）沒有辨別力，不能算是對這一段的查證。

## 建議

1. 刪掉 `iter_T_ether` 裡 `have ht … clear ht` 這段死碼。
2. `record.json` 的 `proof` 把「two independent simulations」改成精確的說法：(T, P) 有兩套實作；H1、H2 的逐格檢查只有一套實作，另外由 critic 的第三套實作在 w ≤ 1600 複核。
3. `proof.md`「敘述差異」第 2 點可以改寫：主定理的兩個合取項已經唯一決定 (μ, λ) = (T, 4)，不需要另外形式化那個等價。
4. 之後補查 Jen 的 cylindrical CA 論文、Wolfram 的有限環循環表，以及 arXiv；「Martínez 等 2005」的年份和期刊要核對。
5. 可以在 `proof.md` 註明光錐公式在 t = T+1 也成立（w ≤ 1600 實測），表示引理的條件 2t+4 ≤ w 是夠用而非最緊。
