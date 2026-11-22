# DISC-0008 證明：R3-L01（規則 26，奇數寬度環，單一種子的週期）

狀態：**紙上證明完整；Lean 一般性證明（所有奇數 w ≥ 3，非有限範圍）本機編譯 0 錯誤 0 警告，GitHub CI `lean` 工作（含公理稽核）已通過：run 45017724157。**

## 敘述

慣例同 `research/r002/impl_b.py`：環上有 w 個細胞 0..w−1，狀態的第 i 位元是細胞 i；細胞 i 的左鄰是 i−1 (mod w)、右鄰是 i+1 (mod w)。種子 x₀ = e₀（只有細胞 0 活）。規則 26 = 00011010₂：新值為 1 恰好在鄰域（左, 中, 右）= 100、011、001。

**定理（R3-L01）。** 設 w ≥ 3 為奇數，k = ⌊log₂ w⌋，P = w·2^k。則對所有 t ≥ 0：

  x_t = x₀ ⇔ P ∣ t。

因此軌道的暫態為 0（x₀ 本身在循環上），週期恰為 P26(w) = w·2^⌊log₂ w⌋。

附帶：w = 1 時不成立（impl_b 給出 (T, P) = (1, 1)），所以 w ≥ 3 是必要的；Lean 敘述也要求 3 ≤ w。

## 提示的核對

- 規則 26 的 1 鄰域是 {100, 011, 001}（位元 4、3、1）；規則 90 是 {110, 100, 011, 001}。兩者**只差在 110**（左=1、中=1、右=0），規則 90 給 1，規則 26 給 0。任務提示寫成「011」，是方向寫反了，實際差在 110。
- 「軌道從不出現相鄰的 11」：**奇數 w 不成立**（例如 w = 11、t = 5，細胞 5、6 都活）。偶數 w 時成立（見文末）。
- 有用的是另一個觀察：在「窗口座標」下，軌道就是 Pascal 三角形 mod 2（規則 90 的單一種子圖樣）截在一個寬度 w、每步左移一格的窗口裡。因此週期 = w（漂移）× 2^k（Pascal 列在窗口裡回到單點的週期），這正是提示猜的分解，但不需要 F₂[x]/(xʷ − 1) 的線性代數。

## 記號

- b_t(j) = C(t, j) mod 2（Pascal 三角形 mod 2；j > t 時為 0）。滿足 b_t(0) = 1，b_{t+1}(j+1) = b_t(j) ⊕ b_t(j+1)。
- 窗口函數：對 0 ≤ s < w，Y_t(s) = 1 ⇔ s 是偶數且 b_t(s/2) = 1。
  所以 Y_t(0) = 1，Y_t(奇數) = 0。
- 幾何意義：在覆蓋空間 ℤ 上，規則 90 單一種子第 t 列的位置 r 滿足 r ≡ t (mod 2)、b_t((t+r)/2) = 1。令 s = r + t，Y_t(s) 就是這一列在 r ∈ [−t, w − t) 的部分。

## 引理 1（封閉形式）

對奇數 w ≥ 3、所有 t ≥ 0、0 ≤ i < w：

  x_t(i) = Y_t((i + t) mod w)。

也就是說：細胞 i 在時間 t 活著 ⇔ s = (i + t) mod w 為偶數且 C(t, s/2) 為奇數。

**證明。** 對 t 歸納。t = 0：Y₀(s) = 1 ⇔ s = 0（b₀(j) = [j = 0]），所以 x₀ = e₀。

歸納步。固定 i，令 s′ = (i + t + 1) mod w（細胞 i 在時間 t+1 的窗口座標）。三個鄰居 i−1、i、i+1 在時間 t 的窗口座標分別是 s′−2、s′−1、s′（mod w）。只要證明

  f₂₆(Y_t(s′−2), Y_t(s′−1), Y_t(s′)) = Y_{t+1}(s′)（下標 mod w）。

分四種情形：

1. s′ ≥ 2 且 s′ 偶，s′ = 2j+2：三個值是 (b_t(j), 0, b_t(j+1))。中間是 0 時，f₂₆(l, 0, r) = l ⊕ r（100→1、001→1、101→0、000→0），所以結果是 b_t(j) ⊕ b_t(j+1) = b_{t+1}(j+1) = Y_{t+1}(s′)。
2. s′ ≥ 3 且 s′ 奇：s′−2、s′ 都是奇數，所以左右都是 0。f₂₆(0, c, 0) = 0（010→0、000→0），而 Y_{t+1}(奇) = 0。✓
3. s′ = 1：三個座標是 w−1、0、1。Y_t(0) = 1、Y_t(1) = 0。f₂₆(l, 1, 0) = 0（110→0、010→0）＝ Y_{t+1}(1)。✓（這裡正是規則 26 與 90 不同之處：w−1 是偶數，左鄰可能是 1，鄰域 110 在規則 90 會給 1。）
4. s′ = 0：三個座標是 w−2、w−1、0。**w 奇 ⇒ w−2 奇**，所以 Y_t(w−2) = 0；Y_t(0) = 1。f₂₆(0, c, 1) = 1（001→1、011→1）＝ Y_{t+1}(0)。✓

w ≥ 3 保證 0、1、2 互不相同，四種情形窮盡且互斥。∎

**解讀。** 窗口每步左移一格；窗口右端（覆蓋空間中原圖樣的右半部）被下一個複本的左邊界吃掉（情形 3、4）。w 奇是關鍵：它讓窗口兩端 s = w−1、s = 0 同為偶數、互相緊鄰，左邊界永遠是 1 而它的左鄰永遠是 0。

## 引理 2（Lucas 定理 p = 2 的兩個推論）

(a) 若 2^m ∣ t，則對 0 < j < 2^m，C(t, j) 為偶數。
(b) 若 2^m ∤ t，則存在 v < m 使 C(t, 2^v) 為奇數（取 v = v₂(t)）。

**證明。** 先證「一位數 Lucas」：b_{2a}(2b) = b_a(b)，b_{2a}(2b+1) = 0（例如 (1+x)^{2a} = (1+x²)^a 在 F₂[x]；Lean 裡用二步 Pascal 遞迴 b_{t+2}(k+2) = b_t(k) ⊕ b_t(k+2) 對 a 歸納）。另外 b_t(1) = t mod 2。
(a) 對 m 歸納：t = 2a 且 2^{m−1} ∣ a。j 奇 ⇒ b_t(j) = 0；j = 2j′ ⇒ b_t(j) = b_a(j′)，0 < j′ < 2^{m−1}，由歸納假設為 0。
(b) 對 m 歸納：t 奇 ⇒ v = 0，b_t(1) = 1。t = 2a ⇒ 2^{m−1} ∤ a，歸納得 v′ < m−1 使 b_a(2^{v′}) = 1，則 b_t(2^{v′+1}) = b_a(2^{v′}) = 1。∎

## 定理的證明

令 k = ⌊log₂ w⌋。w 奇且 w ≥ 3 ⇒ k ≥ 1、2^k 為偶數，所以 2^k < w < 2^{k+1}。

由引理 1，x_t = x₀ ⇔ 對所有 0 ≤ i < w，Y_t((i+t) mod w) = [i = 0]。

(⇒) 設 x_t = x₀。
- 先證 w ∣ t：若 r = t mod w ≠ 0，取 i = w − r（0 < i < w），則 (i + t) mod w = 0，x_t(i) = Y_t(0) = 1，但 i ≠ 0，矛盾。
- 於是 (i + t) mod w = i。若 2^k ∤ t，由引理 2(b) 有 v < k 使 C(t, 2^v) 奇。取 i = 2·2^v ≤ 2^k < w，i ≠ 0，但 x_t(i) = Y_t(2·2^v) = b_t(2^v) = 1，矛盾。所以 2^k ∣ t。

(⇐) 設 w ∣ t、2^k ∣ t。則 x_t(i) = Y_t(i)。i = 0：Y_t(0) = 1。i 奇：0。i = 2j ≠ 0：2j < w < 2^{k+1} ⇒ 0 < j < 2^k，由引理 2(a) b_t(j) = 0。所以 x_t = e₀。

w 奇 ⇒ gcd(w, 2^k) = 1，所以「w ∣ t 且 2^k ∣ t」⇔ P = w·2^k ∣ t。∎

**推論。** 最小正回返時間是 P，x₀ 在循環上（暫態 0），x_{μ+P} = x_μ 對所有 μ，而 0 < p < P 時 x_p ≠ x₀。這正是 R3-L01 的 (T, P) = (0, w·2^⌊log₂ w⌋)。
另外 x_{2^k} = e_{−2^k}（單點，往左平移 2^k）：Y_{2^k}(s) = 1 只在 s = 0（s = 2^{k+1} 已超出窗口）。所以軌道每 2^k 步是一個平移 σ^{−2^k}，而 gcd(2^k, w) = 1 使得平移要 w 次才回原位；引理 2 保證中間沒有更早的單點狀態。

## 偶數 w（不在定理範圍，只作說明）

w 偶時「奇偶類」在環上有定義。若 x_t 的支撐都在 i ≡ t (mod 2)，則沒有相鄰的 11，鄰域 110 不出現，F₂₆ = F₉₀ 在這種狀態上；而 F₉₀ 把它送到支撐在 i ≡ t+1 的狀態。種子 e₀ 滿足條件（t = 0），所以偶數 w 時規則 26 的單一種子軌道**和規則 90 完全相同**，(T, P)₂₆ = (T, P)₉₀（規則 90 為加法規則，週期屬 Martin–Odlyzko–Wolfram 1984 的範圍；R2-C04 已處理暫態）。這段論證只用到上面兩行，沒有寫進 Lean。數值：2 ≤ w ≤ 40 的偶數 w，軌道 4w² 步內從不出現 11，且 impl_b 給出的 (T, P)₂₆ = (T, P)₉₀。
引理 1 對偶數 w 不成立：情形 4 需要 w−2 為奇數。

## 數值檢查

`research/r003/l01_check.py`（只用標準函式庫）：

- 方法 1：用 `impl_b._step` 模擬，對每個奇數 3 ≤ w ≤ W_MAX、0 ≤ t ≤ P + 2w，逐一比對狀態與引理 1 的封閉形式（`math.comb`）；並比對 impl_b 的 Brent 偵測結果 = (0, w·2^⌊log₂ w⌋)。
- 方法 2：腳本內自寫的 list 模擬（規則表直接讀 Wolfram 編碼，不 import repo），在 1 ≤ t ≤ 3P 內列出所有 x_t = x₀ 的 t，要求恰為「w ∣ t 且 2^k ∣ t」的 t，且第一個是 P。
- 引理 2：t ≤ 2000、m ≤ 11，用 `math.comb` 直接檢查 (a)、(b)。
- 引理 1 的局部步驟（四種情形）：每個奇數 w、0 ≤ s′ < w、t ≤ 64 窮舉。
- 偶數 2 ≤ w ≤ 40：無相鄰 11，且 (T, P)₂₆ = (T, P)₉₀。

執行結果：

```
$ python3 research/r003/l01_check.py          # W_MAX = 61，約 0.8 秒
OK: odd 3 <= w <= 61: closed form (impl_b), period w*2^floor(log2 w) (impl_b Brent + own list sim, return set = multiples of P up to 3P); Lemma 2 (t <= 2000); Lemma 3; even 2 <= w <= 40: orbit = rule 90 orbit
$ python3 research/r003/l01_check.py 129      # 約 17 秒
OK: odd 3 <= w <= 129: ...（同上）
```

（腳本輸出中的「Lemma 3」指引理 1 歸納步驟裡的局部一步：在窗口座標 s′ 下，對所有 s′ ∈ [0, w)、t ≤ 64 窮舉。）

## 定理對照

| 猜想／引理 | Lean 定理 | 檔案 |
|---|---|---|
| R3-L01：奇數 w ≥ 3，暫態 0、週期恰為 w·2^⌊log₂ w⌋ | `Discovery.Rule26.rule26_odd_period` | `lean/Discovery/Rule26.lean` |
| x_t = x₀ ⇔ P ∣ t | `Discovery.Rule26.iter_eq_one_iff` | 同上 |
| x_t = x₀ ⇔ w ∣ t ∧ 2^⌊log₂ w⌋ ∣ t | `Discovery.Rule26.iter_eq_one_iff'` | 同上 |
| 引理 1（封閉形式） | `Discovery.Rule26.iter_testBit`（局部步驟：`local_step`、`step_X`） | 同上 |
| 引理 2(a)、(b)；一位數 Lucas | `pas_eq_false_of_dvd`、`exists_pas_of_not_dvd`；`pas_double` | 同上 |
| `step` 的位元描述（第 i 位 = f₂₆(左, 中, 右)） | `tb_step`、`tb_step_high`、`step_lt` | 同上 |
| 抽查（w = 3、11、21 回返；w = 11 的 x₁、x₈；x₄₄ ≠ x₀） | `check_small`（`decide`） | 同上 |

主定理的 Lean 敘述（逐字）：

```lean
def P (w : Nat) : Nat := w * 2 ^ Nat.log2 w

theorem iter_eq_one_iff {w : Nat} (hw : w % 2 = 1) (h3 : 3 ≤ w) (t : Nat) :
    iter w t 1 = 1 ↔ P w ∣ t

theorem rule26_odd_period (w : Nat) (hw : w % 2 = 1) (h3 : 3 ≤ w) :
    iter w (P w) 1 = 1 ∧
    (∀ μ, iter w (μ + P w) 1 = iter w μ 1) ∧
    (∀ p, 0 < p → p < P w → iter w p 1 ≠ iter w 0 1)
```

## 編譯結果

**本機編譯（非 CI）。** 工具鏈 Lean 4.15.0（與 `lean/lean-toolchain` 相同）。本檔只用 Lean core（沒有 import Mathlib），所以不需要 Mathlib 建置。

1. `lake env lean lean/Discovery/Rule26.lean`（在 scratchpad 的 Mathlib v4.15.0 目錄下執行）：0 錯誤、0 警告，約 4.5 秒。
2. 公理檢查：把檔案以 `lean --root=… -o …/Discovery/Rule26.olean` 編成 .olean，再用 repo 的 `AxiomCheck.lean`（只把 `import Discovery` 換成 `import Discovery.Rule26`）執行：`THEOREM_COUNT 43`，全部只用 `propext`、`Classical.choice`、`Quot.sound`（`check_small` 只用 `propext`），沒有 `sorryAx`、沒有 `Lean.ofReduceBool`。
3. `discovery.lean_decls.theorems_in` 從原始碼找到 40 個定理，全部出現在上述公理輸出中（缺漏 0）。
4. `grep` 沒有 `sorry`、`admit`、`axiom` 宣告；沒有用 `native_decide`（只在檔頭註解裡出現這個字）。
5. `lean/Discovery.lean` 已加上 `import Discovery.Rule26`。整個 `Discovery` 的 `lake build`、完整 `AxiomCheck.lean` 沒有在本機跑（`Smoke.lean` 等需要完整 Mathlib，cache 主機被擋）。新檔命名空間 `Discovery.Rule26` 與 `Discovery.Rule54` 的 `step`、`iter` 不衝突。

**CI：通過。** https://github.com/Bonnie9981/Project-Discovery/actions/runs/45017724157（commit af98758，`lean/Discovery.lean` 匯入 Rule26，全環境 AxiomCheck）。

## 敘述差異

- **狀態編碼：** 和 Rule54.lean 一樣，狀態是自然數 x < 2^w，第 i 位元 = 細胞 i，種子是 `1`。`step` 是把 impl_b 的通用迴圈對規則 26 展開：同樣的左右旋轉字，對 1 鄰域 100、011、001 取 AND 再 OR；impl_b 的 `~a & mask` 寫成 `a ^^^ mask`（a ≤ mask 時相同）。這個對應是靠閱讀程式碼建立的，Lean 裡沒有 impl_b；`check_small` 的數值（例如 w = 11 時 x₁ = 2 + 2¹⁰、x₈ = 2³）和 Python 模擬一致，可作佐證。另外 `tb_step` 證明了 `step` 的第 i 位元等於 `rule26 (左) (中) (右)`，而 `rule26 l c r` 的定義就是「26 的第 4l+2c+r 位元」。
- **奇數：** 寫成 `w % 2 = 1`；⌊log₂ w⌋ 是 core 的 `Nat.log2 w`。
- **「暫態 0、週期 P」的寫法：** `iter w (P w) 1 = 1`（回到種子）、對所有 μ 有 x_{μ+P} = x_μ（暫態 0），以及 0 < p < P 時 x_p ≠ x₀（P 是最小的）。因為 x₀ 在循環上，循環的週期就等於 x₀ 的最小回返時間，所以這和 impl_b 的 (T, P) = (0, P) 是同一件事。
- **Pascal 三角形：** Lean 中的 `pas t j` 直接用 Pascal 遞迴定義成 Bool；它等於 C(t, j) mod 2，但這個等式沒有寫進 Lean（證明不需要）。所以 `iter_testBit` 的敘述用的是 `pas`，不是 `Nat.choose`。主定理 `rule26_odd_period`、`iter_eq_one_iff` 不涉及 `pas`，不受影響。
- **未形式化：** 偶數 w 的說明（軌道 = 規則 90 軌道）；規則 154、167 的化約（DISC-0007，L0）。若接受那兩條化約，則 P154(w) = P26(w)（奇數 w ≥ 3）、P167(w) = P26(w)（奇數 w ≥ 5）也跟著成立，但這不是 Lean 證明的一部分。

## 誠實說明／缺口

- 一般證明在紙上和 Lean 都已完整（對所有奇數 w ≥ 3）；CI `lean` 工作已通過（run 45017724157）。
- 規則 26 ↔ impl_b 的對應見上（閱讀＋抽查），與 Rule54.lean 的作法相同。
- 新穎性：見 literature.md。公式本身已在 OEIS A334504 以猜想形式出現（「It seems that」），條目沒有證明；證明在查過的範圍內沒有找到。
- 提示中「規則 26 與 90 差在 011」不正確，實際差在 110；「軌道不含 11」對奇數 w 不正確（只對偶數 w 正確）。
