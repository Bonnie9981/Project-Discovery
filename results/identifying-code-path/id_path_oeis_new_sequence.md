# OEIS 新序列草稿：路徑圖 P_n 的識別碼個數

由使用者本人送出；英文請用自己的話改寫；等前兩條處理完再送（一次一條）。

## 送出前要知道的事

- **查重（2026-11-27，離線全庫）：** 2,3,7,8,13,18,33,51,84,126 不在任何條目裡。
- **證明連結（PR 合併後有效）：** https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/locating-dominating-paths.md （第 3 節）
- **b-file：** `results/identifying-code-path/b_id_path.txt`（n = 1..500）。
- **證明大意：** 識別碼的條件化成三條字串規則：(a) 隔 3 格的兩個位置不能都是 0；(b) 第 3 個和倒數第 3 個一定是 1；(c) 不能連續三個 0、開頭兩格和結尾兩格各至少一個 1。規則只看連續 4 格，所以用「最後 3 格」當狀態（8 種）一格一格加，數法變成 8×8 矩陣的次方，矩陣的特徵多項式給出 7 階遞迴。

## 表單各欄

**Name**
```
Number of identifying codes in the path graph P_n.
```

**Data（offset 1）**
```
1,0,2,3,7,8,13,18,33,51,84,126,202,315,508,798,1268,1991,3158,4985,7903,12481,19750,31203,49369,78048,123460,195189,308692,488088,771896,1220572,1930213,3052209,4826645,7632417,12069550,19085848,30181263,47726410,75471583,119345483,188725350,298437373
```

**Comments**
```
A set C of vertices is an identifying code if the sets N[v] intersect C, where N[v] is v together with its neighbors, are nonempty and pairwise distinct (Karpovsky, Chakrabarty, Levitin).
For n >= 3, writing C as a binary word w_1..w_n, C is an identifying code if and only if w_j or w_{j+3} is 1 for 1 <= j <= n-3, w_3 = w_{n-2} = 1, there are no three consecutive zeros, and w_1 or w_2 and w_{n-1} or w_n is 1. See the link.
The minimum size of an identifying code of P_n is ceiling((n+1)/2) for n >= 3 (Bertrand, Charon, Hudry, Lobstein).
```

**Formula**
```
G.f.: x*(1 - x + x^2 + 2*x^3 + x^4 - x^5 - x^6)/(1 - x - x^2 + x^3 - x^4 - x^5 + x^7).
a(n) = a(n-1) + a(n-2) - a(n-3) + a(n-4) + a(n-5) - a(n-7) for n >= 8.
```

**Example**
```
For n = 3 the identifying codes are {1,3} and {1,2,3}, so a(3) = 2. P_2 has none, since its two vertices have the same closed neighborhood.
```

**Program（PARI）**
```
a(n) = polcoef(x*(1-x+x^2+2*x^3+x^4-x^5-x^6)/(1-x-x^2+x^3-x^4-x^5+x^7) + O(x^(n+1)), n)
```

**Links**
```
Chi Hsia, Counting locating-dominating sets and identifying codes in paths and cycles, 2026.
```

**Crossrefs**
```
Cf. A?????? (locating-dominating sets in P_n).
```

**Keywords:** nonn,easy

**AI 聲明（放 Comments 最後一行，用自己的話）：** 例如 "Found and proved with the assistance of an AI system (Claude)."，只有你自己讀懂並核對過證明，才加 "the author has checked the proof"。
