# OEIS 編輯草稿：A215461、A215462 的「never zero」猜想

由使用者本人登入 OEIS 後送出。兩條要**分開送**（各一個編輯）。Claude 只準備文字，不代為送出。

送出前：
- **先看條目現況：** 打開條目確認猜想那行還在、沒有人先補上證明。
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。
- **原句不要刪：** Lawrence 的 Conjecture 那行保留，在後面另加一行。
- 先讀 OEIS 對 AI 輔助內容的規定；用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：
  - A215462：「偶數 2n ≥ 40 依除以 6 的餘數，寫成 9 + (2n−9)、25 + (2n−25) 或 35 + (2n−35)，後面那個是 3 的奇數倍且至少 9，所以是合數。這是老競賽題（AIME 1984 第 14 題：不能寫成兩個奇合數和的最大偶數是 38）。」
  - A215461：「2n−3、2n−5、2n−7 裡一定有一個是 3 的倍數，n ≥ 6 時它至少是 9，所以是合數，配上質數 3、5 或 7。」

---

## A215462

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture a(n) > 0 for n > 19 is true: write 2*n = 9 + (2*n-9), 25 + (2*n-25) or 35 + (2*n-35) according as 2*n == 0, 4 or 2 (mod 6); the second summand is an odd multiple of 3 that is at least 9. This is the classical fact that 38 is the largest even number that is not a sum of two odd composites (AIME 1984, Problem 14). - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Elementary proof of the conjecture a(n) > 0 for n > 19 (2n = 9, 25 or 35 plus an odd multiple of 3).
```

## A215461

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture a(n) > 0 for n > 5 is true: one of 2*n-3, 2*n-5, 2*n-7 is divisible by 3, and for n >= 6 it is at least 9, hence an odd nonprime; pair it with the prime 3, 5 or 7. - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Elementary proof of the conjecture a(n) > 0 for n > 5 (one of 2n-3, 2n-5, 2n-7 is an odd multiple of 3).
```

（可選 LINKS，兩條都可加：`Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/NeverEasy.lean">Lean 4 proofs</a>, 2026. Written with an LLM (Claude).`）
