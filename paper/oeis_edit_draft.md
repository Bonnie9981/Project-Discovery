# OEIS 編輯草稿（A334504、A268754）

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- 署名已填 Chi Hsia；OEIS 註冊時用同一個拼法。
- 先讀一遍 OEIS 對貢獻者的規定（特別是 AI 輔助內容的規定），留言用自己的話寫。下面的英文只是參考。
- 要能用自己的話說出證明大意：奇數寬度是「Pascal 三角形 mod 2 在環上移動的窗口」，偶數寬度是「單點出發時規則 26 等於規則 90，再對折成零邊界導線」。編輯可能會追問。

證明連結（合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a334504.pdf

---

## A334504

**FORMULA**：原本那行猜想（Zabolotskii 2024）**不要改**，直接在它下面加一行，交給編輯決定要不要把「It seems that」改掉：

```
The two formulas conjectured above, a(2*n+1) = (2*n+1) * 2^A070939(n) and a(2*n+2) = A268754(n) for n > 0, are true; see the proof in the links. - Chi Hsia, Nov 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a334504.pdf">Proof of the formulas for a(2n+1) and a(2n+2)</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked; see the acknowledgements.
```

**COMMENTS**（可選，簡短說明證明想法）：

```
For odd n >= 3, the orbit is purely periodic: at time t, cell i is alive iff s = (i+t) mod n is even and binomial(t, s/2) is odd, i.e., a window of Pascal's triangle mod 2 drifting around the ring. For even n = 2m >= 4, from time 1 on the orbit is a mirror-symmetric copy of rule 90 on m-1 cells with null boundaries started from an end cell, which is the system computed in A268754. - Chi Hsia, Nov 2026
```

## A268754

**CROSSREFS**：把

> Seems to be a shifted bisection of A334504 and A334507.

改成（A334507 是規則 122，我們沒證，所以保留「Seems to be」）：

```
a(n) = A334504(2*n+2) for n >= 1 (proved, see link in A334504). Seems to be a shifted bisection of A334507.
```

## 送出時的「Reason for edit」欄

```
The conjectured formulas in A334504 are proved; proof (with Lean 4 formalization) linked.
```
