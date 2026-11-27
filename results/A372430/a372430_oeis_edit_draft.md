# OEIS 編輯草稿：A372430（Wiseman 2024）猜想的反例

由使用者本人登入 OEIS 後送出。Claude 只準備文字，不代為送出。

送出前：
- **先看條目現況：** 確認 Conjecture 那行還在、沒有人先補上反例。
- **署名格式：** `- _Chi Hsia_, Nov 27 2026`（日期改成實際送出那天）。
- **原句不要刪：** Wiseman 的 Conjecture 那行保留，在後面另加一行。
- **自己驗一次（PARI）：** `k = 2^87 + 2^49; [prime(50), prime(88)]` 應該是 `[229, 457]`；`k % 229` 和 `k % 457` 都是 0；`binary(k)` 只有兩個 1。
- 先讀 OEIS 對 AI 輔助內容的規定；用自己的話寫，下面英文只是參考。
- 要能用自己的話說出大意：「k = 2^87 + 2^49 只有兩個 1 位元，在第 50 和第 88 位；第 50 個質數 229 和第 88 個質數 457 都整除 2^38 + 1，所以都整除 k。用『每個 1 位元都逼一個質數整除 k』來剪枝，窮舉到 2^120，只有 4100 和這個數。」

**COMMENTS**：在 Conjecture 那行之後加：

```
The conjecture is false: k = 2^87 + 2^49 = 154742504911235484315811840 has binary indices {50, 88}, and prime(50) = 229 and prime(88) = 457 both divide k, since 2^38 + 1 = 5*229*457*525313. An exhaustive search of all k < 2^120 (using that each binary index j forces prime(j) | k) finds only 4100 and this k. - _Chi Hsia_, Nov 27 2026
```

**Reason for edit**：

```
Counterexample to the conjecture: 2^87 + 2^49 (binary indices {50, 88}; prime(50) = 229 and prime(88) = 457 divide it); exhaustive search below 2^120.
```

（可選 LINKS：`Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/lean/Discovery/A372430Counter.lean">Lean 4 verification of the counterexample</a>, 2026. Written with an LLM (Claude).` 要等 GitHub 合併後連結才有效。）
