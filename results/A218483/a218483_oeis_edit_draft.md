# OEIS 編輯草稿：A218483 三條猜想的證明

由使用者本人登入 OEIS 後送出。

送出前：

- 署名 `- _Chi Hsia_, Nov 23 2026`（改成送出日）。原留言保留。
- 大意：「40n+15 是 5 的倍數；2 模 5 的階是 4，所以 2^(N−1) ≡ 1 (mod 5) 要 4 整除 N−1，但 N−1 除以 4 餘 2。另外兩條：N = 8pk + p^2 等於 N ≡ 1 (mod 8)，和選哪個質因數無關；兩個質因數時 8n = p2 − p1，同一個 n 反過來也成立。」
- 這三條都是習題程度，語氣客氣即可。

證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a218483-proof.md

---

## A218483

**COMMENTS**：在三條 Conjecture 之後加：

```
All three conjectures are true. If N == 15 (mod 40) then 5 | N, and 2^(N-1) == 1 (mod 5) would need 4 | N-1, but N-1 == 2 (mod 4). For odd N and a prime p | N, N = 8*p*k + p^2 with integer k iff N == 1 (mod 8), independently of p; for N = p1*p2 this gives 8*n = p2 - p1, so N = 8*p2*(-n) + p2^2 with the same n. - _Chi Hsia_, Nov 23 2026
```

**LINKS**：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a218483-proof.md">Proofs of the conjectures in A218483</a>, 2026. Written with an LLM (Claude); the first is checked in Lean 4.
```

## 「Reason for edit」

```
Short proofs of the three conjectures (no psp2 == 15 mod 40; the 8*p*k + p^2 conditions are equivalent to N == 1 mod 8). Proof page linked.
```
