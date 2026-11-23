# OEIS 編輯草稿：A058128 Rotondo 猜想的證明

由使用者本人登入 OEIS 後送出。

送出前：

- 署名 `- _Chi Hsia_, Nov 23 2026`（改成送出日）。原 Conjecture 留言保留。
- 大意：「a(n) = n·S，S = (n^(n−1)−1)/(n−1)^2。S 和 n 互質，n 是偶數時 S ≡ 1 (mod n−1)，所以 nS−1 是 n−1 的倍數，n^(nS) ≡ n (mod S)；模 n 兩邊都是 0。合起來 n^a(n) ≡ n (mod a(n))。」
- 送出前用 PARI 抽查：`a(n)=(n^n-n)/(n-1)^2; for(k=1,30,n=2*k;A=a(n);if(Mod(n,A)^A!=n,print(n)))` 不印任何東西。

證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a058128-proof.md

---

## A058128

**COMMENTS**：在 Rotondo 的 Conjecture 之後加：

```
The conjecture is true: for even n, a(n) = n*S with S = (n^(n-1)-1)/(n-1)^2 coprime to n and S == 1 (mod n-1); hence n-1 divides n*S-1, n^(n*S) == n (mod S), and so n^a(n) == n (mod a(n)). It can fail for odd n, e.g. n = 5: 5^195 == 125 (mod 195). - _Chi Hsia_, Nov 23 2026
```

**LINKS**：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a058128-proof.md">Proof of the conjecture in A058128</a>, 2026. Written with an LLM (Claude); checked in Lean 4.
```

## 「Reason for edit」

```
Proof of Rotondo's 2024 conjecture (even n: a(n) is prime or a weak pseudoprime to base n); proof page with Lean 4 check linked.
```
