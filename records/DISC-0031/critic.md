# DISC-0031 Critic

Critic：獨立 subagent（opus），2026-11-28。只讀了本紀錄、`paper/a212339-marked-mesh.md`、`results/A212339/code/check_a212339.py` 和離線 OEIS 的 `.seq` 檔。讀到的資料裡沒有要 agent 做事的文字。

## 攻擊項目

### 1. 證明本身

- **分解 σ = α n β**：論文只證了一個方向：α 的每個數都比 β 大，否則 x, n, y 會組成 132。反方向（任給兩個 132-避免排列 α、β，接起來的 α n β 也避免 132）沒有寫。我自己檢查過反方向成立：如果 132 的「1」在 β 裡，三個數都在 β 裡；如果「1」在 α 裡，「2」不可能在 β 裡，因為 β 的數都比「1」小，所以三個數都在 α ∪ {n} 裡，但 n 在最後又最大，不能當「2」。所以結論沒錯，只是證明少一句。**這點要補。**
- **左下方點數**：α 的元素、n、β 的元素三種情況我都逐一檢查過，都對。關鍵在 n 是最大數，而且 α 整段比 β 大。
- **「a ≤ k 時 Q_a(x) = C_a」**：對。長度 a 的排列裡，第 i 個位置前面只有 i − 1 ≤ a − 1 < k 個數。函數方程其實只用到 a < k 的情況。
- **函數方程與 x⁰、x¹ 係數**：Σ_a x^[a≥k] Q_a t^a = P_k + x(Q − P_k)，所以 Q = 1 + t(P_k + x(Q − P_k))Q 是對的。取 x⁰ 得 F = 1 + tP_kF；取 x¹ 得 G = tP_kG + t(F − P_k)F。兩式我都重新推過，結果一致。
- **代數**：F − P_k = (1 − P_k + tP_k²)/(1 − tP_k)，G = t(1 − P_k + tP_k²)/(1 − tP_k)³，對。另外補一個論文沒寫的合理性檢查：tP_k² 在 t^m（m ≤ k − 1）的係數是 Σ_{i+j=m−1} C_iC_j = C_m，所以分子 1 − P_k + tP_k² 到 t^{k−1} 都會消掉，第一個不為零的項是 C_k t^k。因此 g.f. 從 C_k t^{k+1} 開始：k = 2、3、4 分別是 2t³、5t⁴、14t⁵，和 OEIS 的 offset 3、4、5 以及首項 2、5、14 都吻合。
- **用程式驗分解本身**：獨立重算第 2 項，用 itertools 全排列加 O(n³) 的 132 檢查（不用專案的產生器）。對 k = 1～5、n ≤ 9，**完整**的分布 Q_n(x)（所有係數）都等於分解式遞推算出來的結果；x⁰ 項也等於 1/(1 − tP_k)。原程式只比了 x⁰、x¹ 兩個係數，這裡把整個分布都比了。

結論：證明正確，只缺反方向那一句。

### 2. k = 3、4 的特例、Dale 的 signature、「n ≥ 13」

- k = 3：P_3 = 1 + t + 2t²。1 − tP_3 = 1 − t − t² − 2t³ = (1 − 2t)(1 + t + t²)，分子 t(1 − P_3 + tP_3²) = t⁴(5 + 4t + 4t²)，我手算過，和 Barker 的式子相同。k = 4 由程式的精確多項式交叉相乘確認；我的獨立重算也用自己的冪級數程式對 k = 1～5 展開。
- Dale 的 signature：(1 − t − t² − 2t³)³ 的展開由原程式確認；我直接拿 A212339 的資料代入遞迴，結果一致。
- **「n ≥ 13」的理由寫錯了，而且 proof.md 和論文互相矛盾**：
  - 論文說「since the numerator has degree 6 < 9, the recurrence holds for all n >= 13」。分子 6 次推得出的是：把 a(n) 在 n < 4 補成 0 之後，遞迴對 **n ≥ 7** 成立。我實測：n = 4、5、6 不成立，n = 0～3 以及 n ≥ 7 都成立。「n ≥ 13」只是「只用條目裡存的項（a(n−9) 要有 n − 9 ≥ 4）」的條件，和分子次數無關。
  - proof.md 寫「分子 10 次、分母 9 次，對 n ≥ 11 成立（用到 a(2)、a(3) = 0）」。分子是 t⁴(5 + 4t + 4t²)，是 6 次，不是 10 次。「n ≥ 11」本身是對的，但不是最佳範圍。
  - **要修**：兩處統一寫成「a(n) 在 n < 4 補 0 時，遞迴對 n ≥ 7 成立；只用條目存的項時，對 n ≥ 13 成立」。

### 3. 程式有沒有真的檢查獨立的東西

- 跑過 `python results/A212339/code/check_a212339.py 11`：通過，約 5 秒。輸出：A212338 33 項、A212339 29 項、A212341 26 項、A212344 27 項、A212345 26 項（log 在 `logs/python_results_A212339_code_check_a212339.py_11.log`）。
- **象限定義**：程式的第三象限是「前面而且比較小」，第二象限是「前面而且比較大」。我把四個象限都算了，k = 2、3、4 的 x 係數只有第三象限和 OEIS 吻合（n ≤ 12）；(0,3,0,0) 用第二象限，和 5C(n−3)、9C(n−3) 吻合。所以程式的定義和 OEIS 資料一致。限制：KRT 原文我沒讀到（見下面「未解決的疑點」），這是用資料反推的。
- **產生器**：`av132` 最後只檢查「個數是 Catalan 數」。個數對不代表排列集合對。我用 itertools 過濾的結果比對，n ≤ 8 時集合完全相同。
- **實作二不獨立**：DP 就是證明裡的遞推，紀錄自己也承認了。真正獨立的只有暴力法（n ≤ 11）和 OEIS 資料。我把暴力法加到 n = 12，k 改成 1～5，也都通過（見獨立重算）。
- **原程式只測 k = 2、3、4**，但定理宣稱所有 k ≥ 1。我補測了 k = 1、5。
- **offset**：OEIS 資料我直接從 `data/oeis/oeisdata/seq/A212/*.seq` 的 %S/%T/%U 和 %O 讀，沒有用 terms.pkl。A212338/9/41/44/45 的 offset 是 3/4/5/3/4，全部吻合。
- 小毛病，不影響結論：
  - `check_oeis` 的後備路徑去 sqlite 的 `line` 表找 tag S/T/U，但這個資料庫裡沒有這幾種 tag（只有 N, C, D, H, F, Y, E），所以沒有 terms.pkl 時一定顯示 skipped，不會誤判成通過。
  - `sys.path.insert(0, '.')` 沒有作用。
  - 路徑都是相對路徑，一定要在 repo 根目錄執行。
  - try 只包住 connect，如果資料庫檔存在但內容是空的，會直接丟例外。

### 4. 新穎性的定位

- H1 的確只要從 KRT 的遞迴取 x 一次項就能得到，論文和 record 都老實寫了「習題程度、不宣稱新」。目前 A212339、A212341 標 `SUPPORTED_NOVELTY_UNCHECKED`、novelty 標 `NO_MATCH_IN_SCOPE`，我認為恰當：依規範，`SUPPORTED_KNOWN` 要文獻或 OEIS 裡有記載。現在只查到 KRT 說「沒有簡單辦法」，OEIS 只標 empirical，算不上「已知」。不過有兩點：
  - (a) 論文寫「This is the functional equation of KRT」，這是引用宣稱。literature.md 只記了 KRT 的遞迴 (21) 和閉式 (17)，沒有逐字記下 (21) 的樣子，所以沒法確認 (*) 就是 (21)。**要修**：在 literature.md 補上 (21) 的原文，或者論文改成「(*) is equivalent to KRT's recursion (21)」並附上對照。
  - (b) k = 2（A212338）已經有 Mathar 寫成 formula 的 g.f.，只是沒有證明。論文寫「already in A212338」，沒問題。
- 查詢範圍偏窄（沒查 MathSciNet、zbMATH、引用 KRT 的後續論文），已列在 open。依規範不能往上升級，目前狀態沒有越線。

### 5. A212344、A212345 與 KRT Theorem 13

- 照 literature.md 的引述：a_1 = 1，a_k = C_k + Σ_{i=1}^{k−1} C_{i−1}a_{k−i}。我算出 a = 1, 3, 9, 28, 90（k = 1～5），a_3 = 9 正確。
- 暴力法驗了 Theorem 13 兩部分的一般 k（k = 1～5，n ≤ 12）：最高次是 x^{n−k}，係數 C_kC_{n−k}；x^{n−k−1}（n ≥ k + 1）的係數是 a_kC_{n−k}。沒有任何失敗。所以 A212344 = 5C(n−3)、A212345 = 9C(n−3) 標 `SUPPORTED_KNOWN` 是對的。
- **Gladkovskii 的連分數不是 Theorem 13 的直接推論**：論文寫「A212344(n) = 5 C_{n−3} (the conjectures by Mathar, Bala and Gladkovskii in A212344)」，等於把 Gladkovskii 的兩條連分數也一起算成解決了。
  - 第一條 5T(0)，T(k) = 1 − x/(x − 1/T(k+1))：每一層都一樣，不動點滿足 T = 1/(1 − xT)，也就是 Catalan g.f.。要嚴格地說，還得補「截斷收斂」的論證，但這很簡單。
  - 第二條 10/T(0)，T(k) = 2x(2k+1) + k + 2 − 2x(k+2)(2k+3)/T(k+1)：每一層的係數都不同。我用截斷 30 層和 36 層實際展開，前 15 項都是 5C_n，兩種截斷結果相同，但這只是數值，沒有證明。
  - Mathar 的 (n−2)a(n) = 2(2n−7)a(n−1) 可以從 C_m/C_{m−1} = 2(2m−1)/(m+1) 直接得到，n ≥ 4 成立。
  - **要修**：論文改成「the closed form 5(1 − sqrt(1 − 4x))/(2x)（Gladkovskii 第二條等號左邊）、Bala、Mathar 的猜想」，連分數部分另外註明是另一個恆等式（第一條是不動點論證；第二條只驗了 15 項），或者乾脆不提連分數。

## 獨立重算

- `/tmp/claude-0/-home-user/42085a49-7fe0-547f-a189-598f156f561a/scratchpad/crit.py`（不 import 專案任何模組；自己寫的 132-避免排列產生器，先在 n ≤ 8 和 itertools 過濾比對；自己寫的有理數冪級數；直接讀 `.seq` 檔）。`python -I crit.py 12` 約 30 秒，結果：
  - H1 暴力法和公式比對，k = 1～5、n ≤ 12：全部相等。
  - A212338/39/41 的 offset 是 3/4/5；33/29/26 項和公式展開全部相等；四個象限裡只有第三象限和資料吻合。
  - Theorem 13（0,k,0,0）兩部分，k = 1～5、n ≤ 12：0 個失敗。A212344 有 27 項 = 5C(n−3)，A212345 有 26 項 = 9C(n−3)。
  - Dale 的遞迴：a(n<4) 補 0 時，n = 4、5、6 不成立，其餘 n 都成立（資料到 n = 32）。
  - Gladkovskii 第二條連分數：前 15 項 = 5C_n（數值）。
- `/tmp/claude-0/-home-user/42085a49-7fe0-547f-a189-598f156f561a/scratchpad/crit2.py`：itertools 加 O(n³) 132 檢查。k = 1～5、n ≤ 9，完整分布 = 分解式遞推；x⁰ = 1/(1 − tP_k)。
- 依交辦，這兩個檔沒有放進 repo（交辦說不改其他檔）。如果要長期保存，請總控放到 `research/r003/impl_c.py`，再跑 `python -m discovery.independence`。

## 未解決的疑點

- KRT 原文沒有重新讀到：export.arxiv.org 的連線被 proxy 擋了，回 403。所以「(*) 就是 KRT 的函數方程」、Theorem 13 的原文和適用範圍（是不是要 n ≥ k + 1）、Section 4 那句「532」的引述，都只能依 literature.md 的轉述。暴力法支持 Theorem 13 在 n ≥ k + 1 成立。
- 文獻範圍：MathSciNet、zbMATH、引用 KRT 的後續論文（例如 Kitaev–Remmel 其他 marked mesh 論文，或 Qiu、Remmel 等人的作品）都沒查。有人寫過 x 係數 g.f. 的可能性不低，因為這是一步就能推出來的結果。
- Gladkovskii 第二條連分數沒有證明。
- `results/A212339/` 目前只有 `code/`。CLAUDE.md 要求的 README、OEIS 草稿、`證明方法說明.md`、`程式說明.md` 都還沒有。這不是數學錯誤，但這個結果的檔案還沒交齊。

## 必須修正的項目

1. `paper/a212339-marked-mesh.md`：分解那段補上反方向的一句（α n β 一定避免 132）。
2. `paper/a212339-marked-mesh.md` 與 `records/DISC-0031/proof.md`：改正 Dale 遞迴的成立範圍和理由。分子是 6 次不是 10 次；a(n<4) 補 0 時 n ≥ 7 成立，只用存的項時 n ≥ 13 成立。因為 proof.md 屬於已完成的紀錄，更正要用附加項目。
3. `paper/a212339-marked-mesh.md`：不要把 Gladkovskii 的連分數算成 Theorem 13 直接解決的，要分開說明，或者刪掉。
4. `records/DISC-0031/literature.md`（附加）或論文：補 KRT (21) 的原文，確認 (*) 和它等價；否則把「This is the functional equation of KRT」改成比較弱的說法。
5. 依 CLAUDE.md 補齊 `results/A212339/` 的 README、草稿和兩份中文說明。
