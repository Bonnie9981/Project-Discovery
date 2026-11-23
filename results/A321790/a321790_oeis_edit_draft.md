# OEIS 編輯草稿：A321790 補上「?」和搜尋範圍

由使用者本人登入 OEIS 後送出。這條沒有證明猜想，只補資料。

送出前：

- 署名 `- _Chi Hsia_, Nov 23 2026`（改成送出日）。
- 大意：「條目寫『341, 2701, ?, 721801』，問號是 873181 = 661·1321：它是 2、3、5 為底的偽質數、7 不是，比它小的半質數偽質數都不是。另外猜想在 10^10 以下全部成立；如果有反例 pq（p < q），q 必須整除所有 a^(p−1) − 1（a < p），對 p ≤ 10^5 算過都沒有。」
- PARI 抽查：`k=873181; [factor(k), vector(4,i,Mod(prime(i),k)^(k-1))]` 前三個是 Mod(1,k)，第四個不是。

---

## A321790

**COMMENTS**：把「The smallest such semiprimes are 341, 2701, ?, 721801, ...」的問號改成 873181，或另加一行：

```
The missing term in "341, 2701, ?, 721801" is 873181 = 661*1321. The conjecture holds for all semiprime pseudoprimes below 10^10. A counterexample p*q (p < q) needs p-1 | q-1 and q | a^(p-1)-1 for every prime a < p; there is none with p <= 10^5. - _Chi Hsia_, Nov 23 2026
```

## 「Reason for edit」

```
Fill the "?" (873181) and record a search bound for the conjecture.
```
