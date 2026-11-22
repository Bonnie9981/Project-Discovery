# OEIS 編輯草稿：A071052 偶數項公式

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **署名格式（2026-11-22 OEIS 編輯 Michel Marcus 指正）：** 一律寫成 `- _Chi Hsia_, Nov 23 2026`：名字前後各一個底線（OEIS 會把它變成可點的個人頁連結），底線緊貼名字、不要把逗號包進去，後面接「月 日 年」完整日期（月份英文縮寫、日、年，中間不加逗號）。日期改成你實際送出那天（美東時間）。LINKS 欄的作者名不加底線。
- **加的內容放對欄位：** 公式放 FORMULA，不要放 CROSSREFS；別人原本的句子不要刪。
- 署名 Chi Hsia。
- 先讀 OEIS 對 AI 輔助內容的規定；留言用自己的話寫，下面英文只是參考。
- 要能用自己的話說出證明大意：「規則 150 走兩步，在 GF(2) 上剛好等於隔兩格走一步，所以第 2n 列就是第 n 列每格中間插一個 0。1 的個數不變，列長多 2n，所以 0 多 2n 個。」
- 送出前在 OEIS 上再看一眼 DATA 和 FORMULA 原句（2026-11-22 讀過，仍標 conjectured）。
- 這條和 A268754、A334504 是不同條目，分開送。

證明連結（PR 合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a071052-even.md

---

## A071052

**FORMULA**：原句

> a(2n) = a(n) + 2n (conjectured). - _Ralf Stephan_, Mar 03 2004

OEIS 慣例是保留原作者署名、去掉 "(conjectured)"，並在後面註明證明者。建議改成：

```
a(2n) = a(n) + 2n. - _Ralf Stephan_, Mar 03 2004 [proved by _Chi Hsia_, Nov 23 2026]
```

再加一行（證明本身短到可以直接寫在條目裡）。注意：關鍵的 A071053(2n) = A071053(n) 早已在 A071053 條目（Peter J. Taylor 2020），這裡只是把它接到 A071052，不要寫成大發現：

```
a(n) = 2n + 1 - A071053(n). Since (1+x+x^2)^(2n) == (1+x^2+x^4)^n (mod 2), A071053(2n) = A071053(n) (see A071053), which gives a(2n) = a(n) + 2n. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a071052-even.md">Proof of a(2n) = a(n) + 2n</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked.
```

**CROSSREFS**：原本已有 A071053，不用改。

## 送出時的「Reason for edit」欄

```
The conjectured formula follows from a(n) = 2n+1 - A071053(n) and A071053(2n) = A071053(n); proof and Lean 4 formalization linked.
```
