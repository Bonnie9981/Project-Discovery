# OEIS 編輯草稿：A084189、A084352「a(n) 永遠不大於 3」的證明

由使用者本人登入 OEIS 後送出。兩條要**分開送**（各一個編輯）。Claude 只準備文字，不代為送出。

送出前：
- **先看條目現況：** 打開條目確認 Conjecture 那行還在、沒有人先補上證明。
- **署名格式：** `- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。
- **原句不要刪：** Earls 的 Conjecture 那行保留，在後面另加一行。
- 先讀 OEIS 對 AI 輔助內容的規定；用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：「如果兩個質因數的每個數字都 ≥ 4，它們的首位 ≥ 4，乘積的位數剛好是兩者位數相加。A084352 兩因數位數一樣，A084189 兩因數都是回文質數（數字 ≥ 4 的回文質數一定是奇數位，因為偶數位回文是 11 的倍數），兩種情況乘積都是偶數位回文，所以被 11 整除，因數之一就是 11，但 11 的數字是 1。」

---

## A084189

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is true. Suppose p and q are palindromic primes whose digits are all >= 4. An even-length palindrome is divisible by 11 (alternating digit sum 0), so p and q have odd numbers of digits, say a and b. Their leading digits are >= 4, so 16*10^(a+b-2) <= p*q < 10^(a+b) and p*q has exactly a+b digits, an even number. If p*q were a palindrome it would be divisible by 11, forcing p = 11 or q = 11, whose digits are 1. Hence a(n) <= 3 for all n. - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Short proof of the conjecture a(n) <= 3 (an even-length palindrome is divisible by 11).
```

## A084352

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is true. If p and q are primes with the same number a of digits, all of them >= 4, then 16*10^(2a-2) <= p*q < 10^(2a), so p*q has exactly 2a digits. An even-length palindrome is divisible by 11 (alternating digit sum 0), so a palindromic p*q would force p = 11 or q = 11, whose digits are 1. Hence a(n) <= 3 for all n. - _Chi Hsia_, Nov 23 2026
```

**Reason for edit**：

```
Short proof of the conjecture a(n) <= 3 (an even-length palindrome is divisible by 11).
```

（可選 LINKS，兩條都可加：`Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/PalDigits.lean">Lean 4 proof</a>, 2026. Written with an LLM (Claude).`）
