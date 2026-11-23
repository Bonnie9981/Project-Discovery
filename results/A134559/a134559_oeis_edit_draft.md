# OEIS 編輯草稿：A134559 裡 Ratajczak 猜想的反例

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：

- 署名：`- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。LINKS 作者名不加底線。
- Ratajczak 的留言（From _Lechoslaw Ratajczak_, Nov 01 2019: (Start) … (End)）原樣保留，新留言加在 (End) 那一行之後。
- 先讀 OEIS 對 AI 輔助內容的規定，留言用自己的話寫。
- 要能用自己的話說出大意：「4933 和 2467 都是質數，所以 4933 在 A005383 裡。可是 b_4934(134) 是 4800 大於 134 的因數和 = 14802 = 6·2467，b_4934(0) = 7404 是偶數，所以 4934 整除 P(4934)，gcd 是 4934 不是 2。反方向是對的：滿足兩個條件的 n 一定在 A005383 裡，因為 n 或 n+1 只要有不超過 N/6 的因數 d，(N/2, 2N/3] 裡 d 的倍數 m 就剛好等於 b_N(N−m)。」
- 送出前可用 PARI 驗：`sumdiv(4800, d, if(d > 134, d))` 應得 14802，`14802 % 2467` 應得 0。

證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a134559-counterexample.md

---

## A134559

**COMMENTS**：加在 Ratajczak 留言的 (End) 之後：

```
The conjecture of Lechoslaw Ratajczak above is false: p = 4933 is in A005383 ((p+1)/2 = 2467 is prime), but b_4934(134) = T(4800,135) = 14802 = 6*2467 and b_4934(0) = sigma(4934) = 7404 is even, so gcd(P(4934),4934) = 4934, not 2. The terms of A005383 (other than 3, 5) below 1.5*10^5 that fail the two equations are 4933, 6997, 11113, 48673, 50341, 54217, 92941 (for 54217, gcd(P(54217),54217) = 54217). The converse holds: every n satisfying both equations is in A005383, since b_N(N-m) = m whenever N/2 < m <= 2N/3. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a134559-counterexample.md">A counterexample to Ratajczak's conjecture in A134559</a>, 2026. Written with an LLM (Claude); checked in Lean 4.
```

## 「Reason for edit」

```
Counterexample 4933 to the 2019 conjecture in the comments (checked there for 2000 integers); the converse inclusion is proved. Proof page linked.
```
