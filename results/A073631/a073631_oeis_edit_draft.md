# OEIS 編輯草稿：A073631 / A130058 的猜想反例（連到 A376896）

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：

- 署名：`- _Chi Hsia_, Nov 23 2026`（日期改成實際送出那天）。LINKS 作者名不加底線。
- 先讀 OEIS 對 AI 輔助內容的規定，留言用自己的話寫。
- 要能用自己的話說出大意：「q = 3842760169 是以 3/2 為底的 Wieferich 質數（A376896），q − 1 整除 q² − 1，所以 q² 是 A073631 的項；它不是 23² 的倍數。反過來，任何項的平方因數 q² 都會讓 q 成為 3/2 底 Wieferich 質數（3/2 的階同時整除 k−1 和 q(q−1)，而 q 和 k−1 互質），所以這是最小反例。」
- 送出前可用 PARI 驗：`k=3842760169^2; Mod(3,k)^(k-1)==Mod(2,k)^(k-1)` 應得 1，`k%529` 不是 0。
- 三筆分開送：先 A073631，再 A130058，最後 A376896（只加交叉引用）。

證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a073631-counterexample.md

---

## A073631

**COMMENTS**：加在 Adamchuk 那段留言之後：

```
The conjecture above is false, and so is the observation that 1 and 529 are the only squares: if p is a Wieferich prime to base 3/2 (A376896), then p^2 is a term, because p-1 divides p^2-1. So 3842760169^2 = 14766805716452908561 and 41975417117^2 are terms. Conversely, if q^2 divides a term k, the order of 3/2 mod q^2 divides both k-1 and q(q-1), hence q-1, so q is in A376896. Therefore 3842760169^2 is the smallest nonsquarefree term not divisible by 23^2 and the smallest square term after 529 (see link). - _Chi Hsia_, Nov 23 2026
```

**LINKS**：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a073631-counterexample.md">A counterexample to the conjecture in A073631 and A130058</a>, 2026. Written with an LLM (Claude); checked in Lean 4.
```

**CROSSREFS**：`Cf. A376896.` 加到最後一行。

「Reason for edit」：

```
The 2007 conjecture in the comments fails: p^2 is a term for every Wieferich prime p to base 3/2 (A376896); least counterexample 3842760169^2. Proof page linked.
```

## A130058

**COMMENTS**：加在「Conjecture: All nonsquarefree terms ...」那行之後：

```
This conjecture is false: 3842760169^2 is a nonsquarefree term of A073631 not divisible by 23^2, and it is the smallest one; see A073631 and A376896. - _Chi Hsia_, Nov 23 2026
```

**CROSSREFS**：`Cf. A376896.`

「Reason for edit」：`Conjecture refuted; see A073631.`

## A376896

**COMMENTS**（新增）：

```
If p is a term, then p^2 is in A073631. This gives counterexamples to the conjecture in A073631 and A130058. - _Chi Hsia_, Nov 23 2026
```

**CROSSREFS**：`Cf. A001220 (Wieferich primes to base 2), A073631, A130058.`

「Reason for edit」：`Added a consequence and crossrefs to A073631, A130058.`
