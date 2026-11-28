> 注意：審查判 `SUPPORTED_KNOWN`：A337353 本來就寫了這個關係（下標錯一格、沒有證明）。這是「更正＋補證明」的小編輯，不是新發現。

# OEIS 編輯草稿：A337353 公式更正；A336662 = 2·A189722 的關係

由使用者本人登入 OEIS 後送出。Claude 只準備內容清單，不代為送出。

送出前：
- **先讀** OEIS 對 AI 輔助內容的規定（docs/RESEARCH_STANDARDS.md 第 7 節）：下面英文只是參考，**留言用自己的話重寫**。
- **一次只送一條。** 建議先送 A337353（更正錯誤，最有用），等編輯處理完再送 A336662。
- **署名：** `- _Chi Hsia_, Nov 28 2026`（改成實際送出那天）。
- **自己驗一次：** 打開 A337353 和 A336662 的資料，A337353 是 1, 4, 8, 16, 24, 40, …，A336662 是 1, 2, 4, 6, 10, 16, …。4·A336662(1) = 8，但 A337353(1) = 4，所以原式不對（往後每一項也都對不上）；4·A336662(n−1) 才對（4·1 = 4、4·2 = 8 = A337353(2)、4·4 = 16、4·6 = 24、4·10 = 40）。A189722 是 1, 2, 3, 5, 8, 13, …（從 n = 2 開始），乘 2 就是 A336662 從 k = 1 開始的 2, 4, 6, 10, 16, 26。
- 要能用自己的話說出大意：「一直轉彎的路徑，每一步取中點連起來，轉 45 度，就變成 Manhattan 格子上的路徑；原路徑不碰到自己，等於新路徑不碰到自己、也沒有不相鄰卻挨在一起的點。」

## 第一條：A337353（更正）

**FORMULA**：把 `a(n) = 4*A336662(n).` 這行請編輯改成（或在下面加一行說明）：

```
a(n) = 4*A336662(n-1) for n >= 1, and a(n) = 8*A189722(n) for n >= 2. (The previous version a(n) = 4*A336662(n) does not match the data for any n >= 1.) - _Chi Hsia_, Nov 28 2026
```

**Reason for edit**：`Corrected the index in the formula (checked against the data).`

## 第二條：A336662

**FORMULA**：

```
a(n) = 2*A189722(n+1) for n >= 1. Proof: for an always-turning walk on the square lattice, the midpoints of its steps, after a 45-degree rotation, form a walk on the Manhattan lattice, and the walk is self-avoiding iff the midpoint walk is self-avoiding with no non-contiguous adjacencies (Watson's covering-lattice bijection); the factor 2 comes from the reflection x <-> y. This is the index-corrected form of the formula in A337353. - _Chi Hsia_, Nov 28 2026
```

**CROSSREFS**：加 `Cf. A189722, A322419, A337353.`（A189722 那邊也可加 `Cf. A336662.`，可選）

**LINKS**（可選，等 GitHub 合併後才有效）：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a336662-manhattan.md">Always-turning walks and contact-free walks on the Manhattan lattice</a>, 2026. Written with the help of an LLM (Claude).
```

**Reason for edit**：`Added the relation with A189722, with a short proof.`
