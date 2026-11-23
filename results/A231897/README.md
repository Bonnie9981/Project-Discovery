# OEIS A231897：「a(n) 永遠不是 −1」的證明

紀錄 [DISC-0018](../../records/DISC-0018/)，Lean `lean/Discovery/NeverEasy.lean`（`a231897_exists`）。

| 檔案 | 內容 |
|---|---|
| `a231897_oeis_edit_draft.md` | OEIS 編輯草稿，使用者自己送出 |
| `code/verify.py` | 數值檢查（也涵蓋 A215461、A215462） |

證明一行：(2^n − 1)^2 的二進位剛好 n 個 1，所以 a(n) ≤ 2^n − 1。
