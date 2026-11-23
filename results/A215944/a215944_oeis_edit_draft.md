# OEIS 編輯草稿：A215944 Coman 猜想的反例

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：

- 署名：`- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。LINKS 作者名不加底線。
- Coman 的 Conjecture 原句保留，在「Conjecture is checked for ...」那行後面加留言。
- 先讀 OEIS 對 AI 輔助內容的規定，留言用自己的話寫。
- 要能用自己的話說出大意：「3048841 = 61·151·331 是 2 為底的偽質數，又被較小的偽質數 49981 = 151·331 整除。要寫成 p·(p+m(p−1))·(p+n(p−1))，三個因數都 ≥ p，p 只能是 61，另外兩個因數要除以 60 餘 1，但 151 除以 60 餘 31。它也不是 5461 的倍數，所以猜想不成立。它就是 b-file 的 a(36)。」
- 送出前用 PARI 驗：`N=3048841; [factor(N), Mod(2,N)^(N-1), Mod(2,49981)^49980]` 應得兩個 `Mod(1, …)`。

證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a215944-counterexample.md

---

## A215944

**COMMENTS**：加在 Conjecture 那兩行之後：

```
The conjecture is false: a(36) = 3048841 = 61*151*331 is divisible by the smaller Fermat pseudoprime 49981 = 151*331, it is not a multiple of 5461, and it cannot be written as p*((m+1)*p-m)*((n+1)*p-n): the three factors are >= p, so p = 61, but then the other two factors would be == 1 (mod 60), while 151 == 31 (mod 60). This is the least counterexample; 211 of the 798 terms below 10^10 are counterexamples. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a215944-counterexample.md">A counterexample to the conjecture in A215944</a>, 2026. Written with an LLM (Claude); checked in Lean 4.
```

## 「Reason for edit」

```
Counterexample to Coman's conjecture: a(36) = 3048841 = 61*151*331 (divisible by the psp 49981) is not of the stated form; least one. Proof page linked.
```
