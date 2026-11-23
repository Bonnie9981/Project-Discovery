# OEIS 編輯草稿：A362070 猜想的反例

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：

- 署名：`- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。LINKS 作者名不加底線。
- Ratajczak 的 Conjecture 原句保留，在那一行後面加留言。
- 先讀 OEIS 對 AI 輔助內容的規定，留言用自己的話寫。
- 要能用自己的話說出大意：「1716 = 4·3·11·13，乘積要等最後一段碰到 13 才會被整除，所以 m_min(1716, r) = 14 − r，加起來是 91。1715 = 5·7^3，K = 21，21 個 m_min 是 21, 13, 7, 6, 5, 4, 3（六個）, 2（八個）, 1，加起來也是 91。條目自己的 Maxima 程式也算出這兩個值。」
- 送出前用條目的 Maxima 程式驗：`a(1715); a(1716);` 都應得 91。

證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a362070-counterexample.md

---

## A362070

**COMMENTS**：加在「Conjecture: the equation a(n) = a(n+1) has no solutions.」那一行之後：

```
The conjecture is false: a(1715) = a(1716) = 91. Here 1716 = 2^2*3*11*13 gives m_min(1716, r) = 14 - r for r = 1..13, while 1715 = 5*7^3 has K(1715) = 21 and m_min(1715, r) = 21, 13, 7, 6, 5, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1. This is the only solution with n <= 10^10. - _Chi Hsia_, Nov 23 2026
```

另一個問句（a(n) = n 的其他解）可以順便加：

```
There is no further solution of a(n) = n (other than consecutive triangular numbers with odd prime indices) for n <= 10^10. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a362070-counterexample.md">A counterexample to the conjecture in A362070</a>, 2026. Written with an LLM (Claude); checked in Lean 4.
```

## 「Reason for edit」

```
Counterexample to the conjecture a(n) != a(n+1): a(1715) = a(1716) = 91 (also from the entry's own Maxima program); only one up to 10^10. Proof page linked.
```
