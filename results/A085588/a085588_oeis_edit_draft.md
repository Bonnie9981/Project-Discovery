# OEIS 編輯草稿：A085588 週期整除（更正方向）

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天，美東時間）。LINKS 欄的作者名不加底線。
- **加的內容放對欄位：** 公式放 FORMULA；Khrabrov 的原句不要刪。
- **乘號要寫出來：** `2^A007814(n)*(2^A309786(n)-1)`。
- 先讀 OEIS 對 AI 輔助內容的規定；留言用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：「規則 150 走 2^j 步等於隔 2^j 格走一步。2^(D+s) 和 ±2^D 對 n 同餘，所以走 2^(D+s) 步和走 2^D 步結果一樣，週期就整除兩者的差 2^D(2^s−1)。原留言把整除方向寫反了，a(13) = 21 不是 63 的倍數。」
- 語氣客氣：原留言下一句已經列出「不相等」的 n，作者多半只是筆誤，不要寫成「錯誤」。
- 送出前在 OEIS 上再看一眼留言原句（2026-11-23 讀過）。

證明連結（PR 合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a085588-period.md

---

## A085588

**FORMULA**：加一行

```
a(n) divides 2^A007814(n)*(2^A309786(n)-1): with n = 2^D*m, m odd, s = A309786(n), 2^j steps of rule 150 equal one step of x(i-2^j) XOR x(i) XOR x(i+2^j) (Frobenius over GF(2)) and 2^(D+s) == +-2^D (mod n), so F^(2^D+2^D*(2^s-1)) = F^(2^D) for every state. - _Chi Hsia_, Nov 23 2026
```

**COMMENTS**：Khrabrov 的原句保留，在他那段 (End) 後面另加一行：

```
The divisibility in the first comment holds in the other direction: a(n) divides 2^A007814(n)*(2^A309786(n)-1) (see FORMULA); e.g., a(4) = 2 and a(13) = 21 are not multiples of 4 and 63. The n where the two differ are those listed in the comment above. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a085588-period.md">Proof that a(n) divides 2^A007814(n)*(2^A309786(n)-1)</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked.
```

**CROSSREFS**：加 A007814、A309786（原本只有 A085587-A085595）：

```
Cf. A007814, A309786.
```

## 送出時的「Reason for edit」欄

```
The divisibility conjectured in the comment holds in the reverse direction (a(4) = 2, a(13) = 21 are counterexamples as written); proof of a(n) | 2^A007814(n)*(2^A309786(n)-1) and Lean 4 formalization linked.
```

## 另一個小更正（可選，同一次編輯）

第二條留言寫「the first exception is 445」，但 445 不在 A115770（11⊗445 ≠ 7·445）；最小的例外是 455（在 A115770，a(455) = 4095）。可在 COMMENTS 加：

```
The first n in A115770 with a(n) != n is 455 (a(455) = 4095); 445 is not in A115770. - _Chi Hsia_, Nov 23 2026
```

送出前自己在 A115770 的 DATA/b-file 確認 455 在、445 不在。

## 沒做的

第二條「a(n) = n only if n in A115770」本身沒證，不提。
