# OEIS A372430：Wiseman 2024 猜想的反例 2^87 + 2^49

紀錄 [DISC-0026](../../records/DISC-0026/)，Lean `lean/Discovery/A372430Counter.lean`（`a372430_counterexample`）。

| 檔案 | 內容 |
|---|---|
| `a372430_oeis_edit_draft.md` | OEIS 編輯草稿，使用者自己送出 |
| `code/a372430_dfs.c` | 結構剪枝窮舉：`./dfs 120`，k < 2^120 只有 4100 和 2^87 + 2^49 |
| `code/check372430.py` | 獨立的 Python 檢查：10^6 內暴力；≤ 4 個 1 位元的數直接枚舉 |
