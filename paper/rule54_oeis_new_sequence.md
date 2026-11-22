# OEIS 新序列投稿草稿：規則 54 單一細胞在環上的暫態長度

由使用者本人登入 OEIS 後送出（New sequence 表單）。Claude 只準備文字，不代為送出。

## 送出前要知道的事

- **署名格式（2026-11-22 OEIS 編輯 Michel Marcus 指正）：** 一律寫成 `- _Chi Hsia_, Nov 23 2026`：名字前後各一個底線（OEIS 會把它變成可點的個人頁連結），底線緊貼名字、不要把逗號包進去，後面接「月 日 年」完整日期（月份英文縮寫、日、年，中間不加逗號）。日期改成你實際送出那天（美東時間）。LINKS 欄的作者名不加底線。
- **加的內容放對欄位：** 公式放 FORMULA，不要放 CROSSREFS；別人原本的句子不要刪。
- **乘號要寫出來：** OEIS 慣例寫 `2*n`、`a(2*n+1)`，不寫 `2n`（引用別人原句時照原樣）。
- **OEIS 帳號：** 2026-11-22 查詢時，OEIS 頁面顯示目前登入的帳號是學校帳號，狀態「waiting to be approved」。要等帳號核准後才能投稿。帳號姓名要和署名 Chi Hsia 一致。
- **查重（2026-11-22，用瀏覽器查 OEIS）：** 暫態數列 `0,5,0,0,2,6,2,2,4,10,4,4,6,14` 查無；「進入循環前的總步數」`4,6,4,4,6,10,6,6,8,14,8,8,10,18` 查無；週期數列 `1,1,1,4,1,4,4,4,...` 查無；`"rule 54" period` 只找到 A204714（所有初始狀態的最大週期）。單一細胞的「eventual period」家族 A180001、A334496、A334499–A334515、A085587、A085588 裡沒有規則 54 的條目，也沒有任何一條是「暫態長度」。所以這是新序列，不是編輯舊條目。
- **為什麼選暫態而不選週期：** 規則 54 從單一細胞出發，寬度 ≥ 6 時週期永遠是 4，數列沒有內容；暫態才有結構（四個餘數類四條公式）。週期 4 寫在 COMMENTS 裡。
- **OEIS 對新序列的要求：** 要「有趣」。這條的賣點是：規則 54 是有名的「粒子型」非線性規則，而這條暫態有完整的證明（四種情形分別對應不同的粒子圖像），而且有 Lean 形式化。編輯可能會問為什麼不是 A334499 家族的一員；可以在留言說「這個家族記錄的是週期，規則 54 的週期是常數 4，所以改記暫態」。
- **證明連結（合併後有效）：** `https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/rule54_transient.pdf`
- **b-file：** `paper/b_rule54_transient.txt`（n = 1..1000，用 repo 的位元模擬逐一算出，不是用公式填的）。送出新序列後，在條目頁面用「b-file」上傳。
- 要能用自己的話說出證明大意（見 PDF 第 2 節）：圖樣左右對稱 → 對折成線段；光錐裡是週期 4 的背景花紋（ether）；光錐碰到正對面時，餘 0 剛好接平，餘 2、3 留下一個不動的缺陷，餘 1 則冒出一道相位牆走回種子，所以暫態長一倍。

---

## 表單各欄（英文是給 OEIS 的文字，送出前請自己讀過、必要時用自己的話改寫）

**Name（%N）**

```
Length of the transient (preperiod) of a single cell in rule 54 cellular automaton in a cyclic universe of width n.
```

**Data（%S，n = 1..93）**

```
1,2,2,0,5,0,0,2,6,2,2,4,10,4,4,6,14,6,6,8,18,8,8,10,22,10,10,12,26,12,12,14,30,14,14,16,34,16,16,18,38,18,18,20,42,20,20,22,46,22,22,24,50,24,24,26,54,26,26,28,58,28,28,30,62,30,30,32,66,32,32,34,70,34,34,36,74,36,36,38,78,38,38,40,82,40,40,42,86,42,42,44,90
```

**Offset（%O）**

```
1
```

**Comments（%C）**

```
Start from the configuration with exactly one ON cell on a ring of n cells and apply rule 54 (new cell = center XOR (left OR right)) synchronously. a(n) is the least t such that the configuration at time t recurs later, i.e., the number of steps before the orbit enters its cycle.

For n >= 6 the eventual period is exactly 4 (for n = 1, 2, 3, 5 it is 1: the ring becomes all OFF or stays all ON). A334499 lists the eventual periods of all 256 rules for n <= 10.

The four residue classes of n mod 4 correspond to different particle pictures for rule 54 (fold the mirror-symmetric orbit onto the segment from the seed to the opposite cell): the light cone fills with the period-4 "ether"; when the cone reaches the far side, for n == 0 (mod 4) the ether closes up seamlessly, for n == 2, 3 (mod 4) a stationary one-cell defect remains, and for n == 1 (mod 4) a phase wall appears at the far side and travels back to the seed at speed 1, which roughly doubles the transient.
```

**Formula（%F）**

```
For n >= 6: a(n) = n - 3 if n == 1 (mod 4); a(n) = (n-6)/2 if n == 2 (mod 4); a(n) = (n-7)/2 if n == 3 (mod 4); a(n) = (n-4)/2 if n == 0 (mod 4) (also true for n = 4). See the proof in the links.
a(n) = 2*a(n-4) - a(n-8) for n >= 14.
```

**Example（%e）**

```
For n = 6 the orbit is periodic from the start: 100000 -> 110001 -> 001010 -> 011111 -> 100000 (bit i = cell i, cell 0 first), so a(6) = 0.
```

> 這四步已用程式核對（2026-11-22）。

**Links（%H）**

```
Chi Hsia, <a href="/AXXXXXX/b_rule54_transient.txt">Table of n, a(n) for n = 1..1000</a>
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/rule54_transient.pdf">Proof of the formula for the transient</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked.
Eric Weisstein's World of Mathematics, <a href="https://mathworld.wolfram.com/Rule54.html">Rule 54</a>
<a href="/index/Ce#cell">Index entries for sequences related to cellular automata</a>
```

（b-file 的連結由 OEIS 在上傳後自動產生，AXXXXXX 會換成新編號。）

**Program（%o）**

```
(Python)
def a(n):
    x, seen, t = (1,) + (0,)*(n-1), {}, 0
    while x not in seen:
        seen[x] = t
        x = tuple(x[i] ^ (x[i-1] | x[(i+1) % n]) for i in range(n))
        t += 1
    return seen[x]
print([a(n) for n in range(1, 41)])
```

**Cross-references（%Y）**

```
Cf. A071030, A118108, A204714, A265225, A334499.
```

**Keywords（%K）**

```
nonn,easy
```

**Author（%A）**

```
_Chi Hsia_, Nov 23 2026
```

## 核對

- Data、b-file、Python 程式三者互相一致（2026-11-22 在雲端容器跑過；Python 程式印出的前 40 項和 Data 相同）。
- 公式：Lean 定理 `rule54_mod4_zero`（DISC-0010）、`rule54_mod4_two`、`rule54_mod4_three`（DISC-0011）、`rule54_mod4_one`（DISC-0012）。Lean 的敘述是「x_{μ+4} = x_μ ⇔ μ ≥ T(n)」再加上週期恰好 4；因為循環長度是 4，「x_μ 之後會再出現」和「x_{μ+4} = x_μ」等價，所以 T(n) 就是這裡的 a(n)。
- 遞迴 a(n) = 2a(n−4) − a(n−8)：由公式直接推出（同一餘數類的連續兩項差是常數 4 或 2）；數值上 14 ≤ n ≤ 1000 全部成立，n = 13 不成立（因為 a(5) = 5 是例外）。
- n = 1、2 時「左鄰」和「右鄰」是同一格或自己；程式和 Lean 的 `step` 都照環的定義處理。
