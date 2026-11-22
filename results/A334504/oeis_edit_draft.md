# OEIS 編輯草稿（A334504、A268754）

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **署名格式（2026-11-22 OEIS 編輯 Michel Marcus 指正）：** 一律寫成 `- _Chi Hsia_, Nov 23 2026`：名字前後各一個底線（OEIS 會把它變成可點的個人頁連結），底線緊貼名字、不要把逗號包進去，後面接「月 日 年」完整日期（月份英文縮寫、日、年，中間不加逗號）。日期改成你實際送出那天（美東時間）。LINKS 欄的作者名不加底線。
- **加的內容放對欄位：** 公式放 FORMULA，不要放 CROSSREFS；別人原本的句子不要刪。
- **乘號要寫出來：** OEIS 慣例寫 `2*n`、`a(2*n+1)`，不寫 `2n`（引用別人原句時照原樣）。
- 署名已填 Chi Hsia；OEIS 註冊時用同一個拼法。
- 先讀一遍 OEIS 對貢獻者的規定（特別是 AI 輔助內容的規定），留言用自己的話寫。下面的英文只是參考。
- 要能用自己的話說出證明大意：奇數寬度是「Pascal 三角形 mod 2 在環上移動的窗口」，偶數寬度是「單點出發時規則 26 等於規則 90，再對折成零邊界導線」。編輯可能會追問。

證明連結（合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a334504.pdf

## 目前狀態（2026-11-22 晚上，美東時間）

- **A334504：已送出，編輯 Michel Marcus 已親自把署名改好並重新提交（#24、#25），現在等其他編輯核准。不用再動。**
- **A268754（偶數項那行）：已送出，還要改一次。** 目前草稿（#61）的署名寫成 `- _Chi Hsia, _, Nov 22 2026`，底線位置錯、多一個逗號。請在 https://oeis.org/draft/A268754 按 edit，把 FORMULA 那一行整行換成：

```
a(n) = A334504(2*n+2) for n >= 1 (proved, see link in A334504). - _Chi Hsia_, Nov 22 2026
```

  另外 #58 把 FORMULA 原本的第一句「No general formula for even-indexed terms is known.」刪掉了。那句是別人寫的、現在也還成立（我們給的不是封閉公式），建議加回去，FORMULA 欄改成兩行：

```
No general formula for even-indexed terms is known. For odd-indexed terms, a(2n+1) = 2*a(n), except when n is of the form (2^k - 1), in which case a(n) = 1.
a(n) = A334504(2*n+2) for n >= 1 (proved, see link in A334504). - _Chi Hsia_, Nov 22 2026
```

  改完按 Save，再按 Propose。「Discussion」欄可以寫：`Fixed the signature and restored the original sentence.`
- **A268754 奇數項（`a268754_oeis_edit_draft.md`）、A071052、規則 54 新序列：還沒送。** A268754 奇數項等上面那份核准、條目恢復 approved 之後再另開一次編輯，不要塞進同一份草稿。

---

## A334504

**FORMULA**：原本那行猜想（Zabolotskii 2024）**不要改**，直接在它下面加一行，交給編輯決定要不要把「It seems that」改掉：

```
The two formulas conjectured above, a(2*n+1) = (2*n+1) * 2^A070939(n) and a(2*n+2) = A268754(n) for n > 0, are true; see the proof in the links. - _Chi Hsia_, Nov 22 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a334504.pdf">Proof of the formulas for a(2n+1) and a(2n+2)</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked; see the acknowledgements.
```

**COMMENTS**（可選，簡短說明證明想法）：

```
For odd n >= 3, the orbit is purely periodic: at time t, cell i is alive iff s = (i+t) mod n is even and binomial(t, s/2) is odd, i.e., a window of Pascal's triangle mod 2 drifting around the ring. For even n = 2m >= 4, from time 1 on the orbit is a mirror-symmetric copy of rule 90 on m-1 cells with null boundaries started from an end cell, which is the system computed in A268754. - _Chi Hsia_, Nov 22 2026
```

## A268754

> **已作廢（2026-11-22）：** 編輯要求這句改放 FORMULA 並署名，照上面「目前狀態」的做法改，下面這段只留作紀錄。

~~**CROSSREFS**：~~ 原本的建議是把

> Seems to be a shifted bisection of A334504 and A334507.

改成（A334507 是規則 122，我們沒證，所以保留「Seems to be」）：

```
a(n) = A334504(2*n+2) for n >= 1 (proved, see link in A334504). Seems to be a shifted bisection of A334507.
```

## 送出時的「Reason for edit」欄

```
The conjectured formulas in A334504 are proved; proof (with Lean 4 formalization) linked.
```
