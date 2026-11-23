# OEIS 編輯草稿：A231897 的猜想「a(n) is never -1」

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **先看條目現況：** 打開條目確認猜想那行還在、沒有人先補上證明。
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。
- **原句不要刪：** Sloane 的 Conjecture 那行保留，在後面另加一行。
- 先讀 OEIS 對 AI 輔助內容的規定；用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：「(2^n − 1)^2 = 2^(2n) − 2^(n+1) + 1，二進位剛好 n 個 1（例如 15^2 = 225 = 11100001），所以每個 n 都有答案，a(n) ≤ 2^n − 1，永遠不會是 −1。」
- 證明一行就完，不需要外部連結；要附 Lean 的話可以加 LINKS（PR 合併後有效）。

---

## A231897

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is true: for n >= 1, (2^n-1)^2 = (2^(n-1)-1)*2^(n+1) + 1 has binary weight n, so a(n) <= 2^n-1 for all n. - _Chi Hsia_, Nov 23 2026
```

**FORMULA**：加一行

```
a(n) <= 2^n - 1. - _Chi Hsia_, Nov 23 2026
```

**EXAMPLE**（可選）：

```
(2^4-1)^2 = 225 = 11100001_2 has 4 ones; a(4) = 13 <= 15.
```

**LINKS**（可選）：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/NeverEasy.lean">Lean 4 proof that wt((2^n-1)^2) = n</a>, 2026. Written with an LLM (Claude).
```

## 「Reason for edit」欄

```
Proof of the conjecture "a(n) is never -1": (2^n-1)^2 has exactly n binary ones, hence a(n) <= 2^n-1.
```

（編輯可能會建議把 %C 的 Conjecture 改成 "a(n) is never -1 (see formula)"，聽編輯的。）
