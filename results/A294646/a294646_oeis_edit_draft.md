# OEIS 編輯草稿：A294646 猜想的反例

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天，美東時間）。LINKS 欄的作者名不加底線。
- **原句不要刪：** Israel 和 Ordowski 的 Conjecture 那行保留，在後面另加留言。
- **乘號要寫出來：** `3*2^(2*n)+1`、`367*53484727`。
- 先讀 OEIS 對 AI 輔助內容的規定；留言用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：「a(n) 是 2^(2n) 對 2n+1 的倒數。a(n)=2n−2 等於 2n+1 整除 3·2^(2n)+1。n = 9814447404 時 2n+1 = 367·53484727，真的整除，所以猜想的『不會是 2n−2』不成立；這是最小的反例。另外兩半（不會是 2、不會是 2n）是對的，是古典結果。」
- 語氣客氣：反例遠超過 b-file 的範圍（n ≤ 10000），原作者沒算到是正常的。
- 送出前自己用 PARI 驗一次：`n=9814447404; (1/Mod(2,2*n+1))^(2*n)` 應得 `Mod(19628894806, 19628894809)`。

證明連結（PR 合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a294646-counterexample.md

---

## A294646

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture fails for 2*n-2: a(9814447404) = 19628894806 = 2*n-2, since 2*n+1 = 19628894809 = 367*53484727 divides 3*2^(2*n)+1. This is the least such n. The parts a(n) != 2 and a(n) != 2*n are true: they say that 2*n+1 > 1 never divides 2^(2*n+1)-1 or 2^(2*n)+1. - _Chi Hsia_, Nov 23 2026
```

（如果編輯希望拆開，可以把第二句「This is the least such n.」改成「No smaller n exists (exhaustive search).」）

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a294646-counterexample.md">A counterexample to the conjecture a(n) != 2n-2, and proofs of a(n) != 2, 2n</a>, 2026. Written with an LLM (Claude); the counterexample is machine-checked in Lean 4.
```

**EXAMPLE**（可選）：

```
For n = 9814447404, 2*n+1 = 367*53484727 and 3*2^(2*n) == -1 (mod 2*n+1), so (-3)*2^(2*n) == 1 and a(n) = 2*n+1-3 = 2*n-2.
```

## 送出時的「Reason for edit」欄

```
Counterexample to the conjecture "a(n) is never 2n-2": n = 9814447404 (2n+1 = 367*53484727 divides 3*2^(2n)+1), least one by exhaustive search; the other two parts are proved. Proof page with Lean 4 check linked.
```
