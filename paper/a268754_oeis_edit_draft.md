# OEIS 編輯草稿：A268754 奇數項公式

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- 署名 Chi Hsia（和 A334504 草稿同一個拼法）。
- 先讀 OEIS 對 AI 輔助內容的規定；留言用自己的話寫，下面英文只是參考。
- 要能用自己的話說出證明大意：「把 n 格導線隔一格放進 2n+1 格導線，長的走兩步等於短的走一步；奇偶不同的時刻活格不重疊，所以週期一定是偶數，剛好加倍。n+1 是 2 的次方時兩條都會死光。」
- 建議和 A334504 那份草稿分開送（不同條目、不同編輯）。

證明連結（PR 合併後有效）：
https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a268754-odd.md

---

## A268754

**FORMULA**：原句

> No general formula for even-indexed terms is known. For odd-indexed terms, a(2n+1) = 2*a(n), except when n is of the form (2^k - 1), in which case a(n) = 1.

例外句的「a(n) = 1」其實是指 a(n) = a(2n+1) = 1。建議不要刪原句，在下面加一行：

```
For n >= 1, a(2n+1) = 2*a(n) if n+1 is not a power of 2, and a(n) = a(2n+1) = 1 if n+1 is a power of 2; see the proof in the links. - Chi Hsia, Nov 2026
```

**COMMENTS**：原句「Terms of the form 2^k-1 have a period of 1 since all cells die.」下面加：

```
Conversely, for n+1 not a power of 2 the cells never all die: for even n the update map is invertible over GF(2), and the wire of 2n+1 cells dies iff the wire of n cells does (put the n-wire on the even cells of the (2n+1)-wire; two steps of the long wire are one step of the short one). - Chi Hsia, Nov 2026
```

**LINKS**：加一行

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a268754-odd.md">Proof of the formula for a(2n+1)</a>, 2026. Proof and Lean 4 formalization generated with an LLM (Claude) and machine-checked.
```

## 送出時的「Reason for edit」欄

```
The odd-index formula and the death criterion are proved; short proof and Lean 4 formalization linked.
```
