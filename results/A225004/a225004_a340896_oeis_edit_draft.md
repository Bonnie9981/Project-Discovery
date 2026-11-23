# OEIS 編輯草稿：A225004、A340896（J. Lowell 的兩條除數猜想）的證明

由使用者本人登入 OEIS 後送出。兩條要**分開送**（各一個編輯）。Claude 只準備文字，不代為送出。

送出前：
- **先看條目現況：** 打開條目確認 Conjecture 那行還在、沒有人先補上證明。
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。
- **原句不要刪：** Lowell 的 Conjecture 那行保留，在後面另加一行。
- 先讀 OEIS 對 AI 輔助內容的規定；用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：
  - A225004：「n·m 的除數個數是 ∏(a+x+1)，n 的是 ∏(a+1)。只要有一個質數在 m 裡的次方比在 n 裡大（包括 n 沒有的新質數），那一項至少翻倍，除數個數就 ≥ 2d(n)。所以 m 一定整除 n。」
  - A340896：「d(n²)/d(n) = ∏(2a+1)/(a+1)；一個質因數時 < 2，兩個以上時每項 ≥ 3/2，乘起來 ≥ 9/4 > 2。」

---

## A225004

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is true, and a(n) = n*m where m is the largest divisor of n with d(n*m) < 2*d(n). Indeed, for a multiple n*m let a = v_p(n), x = v_p(m) for each prime p | n*m. Then d(n*m)/d(n) = Product_p (a+x+1)/(a+1), each factor is >= 1, and a factor with x >= a+1 is >= 2. So d(n*m) < 2*d(n) forces x <= a for every p, i.e., m | n and n*m | n^2. - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Short proof of the conjecture a(n) | n^2 (compare exponents prime by prime).
```

## A340896

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is true. If n = Product p_i^(a_i) has k distinct prime factors, then d(n^2)/d(n) = Product (2*a_i+1)/(a_i+1). For k <= 1 this is < 2, so n^2 is in row n; for k >= 2 each factor is >= 3/2, so the ratio is >= 9/4 > 2 and n^2 is not in row n. - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Short proof of the conjecture (row n contains n^2 iff n is a prime power).
```

（可選 LINKS，A225004 可加：`Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/DivisorExp.lean">Lean 4 proof of the exponent inequality</a>, 2026. Written with an LLM (Claude).`）
