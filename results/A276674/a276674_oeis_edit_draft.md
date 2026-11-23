# OEIS 編輯草稿：A276674（Ordowski 2016）「x ≤ 4m」猜想的證明

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **先看條目現況：** 確認 Conjecture 那行還在、沒有人先補上證明。
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。
- **原句不要刪：** 在 Conjecture 那行後面另加一行。
- 先讀 OEIS 對 AI 輔助內容的規定；用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：「x − λ(x) 是正偶數時，x 不是 1、2 或奇質數冪；偶數 x 有 λ ≤ φ ≤ x/2，至少兩個奇質因數時 λ ≤ φ/2。所以 λ(x) ≤ x/2，x ≤ 2(x − λ(x)) = 4m。」

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is true. If x - lambda(x) is even and positive, then x is not 1, 2 or an odd prime power p^k (there x - lambda(x) = p^(k-1) is odd). If x is even, lambda(x) <= phi(x) <= x/2; if x is odd with at least two distinct prime factors, lambda(x) is the lcm of even numbers whose product is phi(x), so lambda(x) <= phi(x)/2 < x/2. Hence x <= 2*(x - lambda(x)) = 4*m. - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Short proof of the conjecture x <= 4m (lambda(x) <= x/2 whenever x - lambda(x) is even and positive).
```
