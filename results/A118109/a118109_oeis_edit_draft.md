# OEIS 編輯草稿：A118109 的猜想公式

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

## A118109

**FORMULA**：原句是

> Conjectures from _Colin Barker_, Dec 08 2015 and Apr 16 2019: (Start) a(n) = 10001*a(n-2)-10000*a(n-4) for n>3. G.f.: (1+111*x) / ((1-x)*(1+x)*(1-100*x)*(1+100*x)). (End)
> Conjecture: a(n) = floor((10000+1100*(n mod 2))*100^n/9999). - _Karl V. Keller, Jr._, Sep 24 2021

OEIS 慣例：保留原作者，把 "Conjectures from" 改成 "From"、刪掉 "Conjecture:"，並註明證明者。建議改成：

```
From _Colin Barker_, Dec 08 2015 and Apr 16 2019: (Start)
a(n) = 10001*a(n-2)-10000*a(n-4) for n>3.
G.f.: (1+111*x) / ((1-x)*(1+x)*(1-100*x)*(1+100*x)).
(End) [proved by _Chi Hsia_, Nov 23 2026]
a(n) = floor((10000+1100*(n mod 2))*100^n/9999). - _Karl V. Keller, Jr._, Sep 24 2021 [proved by _Chi Hsia_, Nov 23 2026]
```

再加一行（說明為什麼成立）：

```
Row n+2 is row n shifted by two cells followed by 0001 (n even) or 0111 (n odd), so a(n+2) = 10000*a(n) + 1 for even n and a(n+2) = 10000*a(n) + 111 for odd n, which gives the formulas above. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/rule54-rows.md">Rule 54 from a single ON cell: closed form of every row</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked.
```

## 「Reason for edit」欄

```
Proved the conjectured recurrence, g.f. and floor formula (row n+2 = row n shifted, plus 0001 or 0111); proof and Lean 4 formalization linked.
```
