# OEIS 編輯草稿：A265225 的猜想公式與 Ianakiev 註解

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **署名格式：** 一律 `- _Chi Hsia_, Nov 23 2026`（底線緊貼名字，日期改成實際送出那天，美東時間）。LINKS 欄作者名不加底線。
- 公式放 FORMULA，別人原句不要刪；乘號寫出來（`2*n`）。
- 先讀 OEIS 對 AI 輔助內容的規定；留言用自己的話寫，下面英文只是參考。
- 要能用自己的話說出證明大意：「規則 54 的第 t+2 列就是第 t 列往左移兩格、右邊多 4 格（0001 或 0111），所以每兩列多一段固定的尾巴，所有公式都從這裡算出來。」
- 送出前在 OEIS 上再看一眼 DATA、FORMULA 原句（和 A265225 的 Ianakiev 原句），2026-11-23 讀過。
- 這是習題程度，A118108 早就寫出同一列的十進位公式，不要寫成大發現。
- A118109、A265225 是兩個條目，分開送；兩個都連同一頁證明。

證明連結（PR 合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/rule54-rows.md

---

## A265225

**FORMULA**：原句是

> Conjectures from _Colin Barker_, Dec 08 2015 and Apr 20 2019: (Start) a(n) = (n+1)*(2*n -(-1)^n +5)/4. a(n) = a(n-1) + 2*a(n-2) - 2*a(n-3) - a(n-4) + a(n-5) for n>4. G.f.: (1+3*x) / ((1-x)^3*(1+x)^2). (End)
> a(n) = n + 1 + (n+1) * floor((n+1)/2), conjectured. - _Wesley Ivan Hurt_, Dec 25 2016
> a(n) = A093353(n) + n + 1, conjectured. - _Matej Veselovac_, Jan 21 2020

建議改成（去掉 Conjectures/conjectured，原作者保留）：

```
From _Colin Barker_, Dec 08 2015 and Apr 20 2019: (Start)
a(n) = (n+1)*(2*n -(-1)^n +5)/4.
a(n) = a(n-1) + 2*a(n-2) - 2*a(n-3) - a(n-4) + a(n-5) for n>4.
G.f.: (1+3*x) / ((1-x)^3*(1+x)^2).
(End) [proved by _Chi Hsia_, Nov 23 2026]
a(n) = n + 1 + (n+1) * floor((n+1)/2). - _Wesley Ivan Hurt_, Dec 25 2016 [proved by _Chi Hsia_, Nov 23 2026]
a(n) = A093353(n) + n + 1. - _Matej Veselovac_, Jan 21 2020 [proved by _Chi Hsia_, Nov 23 2026]
```

再加一行：

```
Row 2*k of the automaton has k+1 ON cells and row 2*k+1 has 3*k+3, so a(2*k) = (2*k+1)*(k+1) and a(2*k+1) = (2*k+2)*(k+2), which gives the formulas above. - _Chi Hsia_, Nov 23 2026
```

**COMMENTS**：Ianakiev 的原句

> Take the first 2n positive integers and choose n of them such that their sum: a) is divisible by n, and b) is minimal. It seems their sum equals a(n). - _Ivan N. Ianakiev_, Feb 16 2019

字面上差一個索引：n = 1 時最小和是 1 = a(0)，不是 a(1) = 4。**不要自己改別人的原句**，在後面加一行說明，讓編輯決定：

```
The minimal sum in the previous comment is a(n-1), not a(n) (for n = 1 it is 1 = a(0)): the sums of n-subsets of {1..2*n} fill the interval [n*(n+1)/2, n*(3*n+1)/2], so the minimum divisible by n is n*(n+1)/2 for odd n and n*(n+2)/2 for even n, which is a(n-1). Equivalently, choosing n+1 numbers from {1..2*n+2} gives exactly a(n). - _Chi Hsia_, Nov 23 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/rule54-rows.md">Rule 54 from a single ON cell: closed form of every row</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked.
```

## 「Reason for edit」欄

```
Proved the conjectured formulas (row 2k has k+1 ON cells, row 2k+1 has 3k+3); noted that the min-sum comment gives a(n-1), with proof; proof and Lean 4 formalization linked.
```
