# OEIS A334504：規則 26 環上的週期

- 奇數寬度 w 的週期 = w·2^⌊log₂ w⌋：紀錄 [DISC-0008](../../records/DISC-0008/)，Lean `lean/Discovery/Rule26.lean`
- 偶數寬度 a(2n+2) = A268754(n)：紀錄 [DISC-0009](../../records/DISC-0009/)，Lean `lean/Discovery/Rule26Even.lean`

| 檔案 | 內容 |
|---|---|
| `a334504.tex` | 英文證明短文原始檔；編好的 PDF 在 `paper/a334504.pdf`（OEIS 連結的網址，固定不動）。PDF 內文提到的 `paper/spec_audit.md` 現在是本資料夾的 `spec_audit.md` |
| `oeis_edit_draft.md` | A334504、A268754 的 OEIS 編輯草稿，使用者自己送出 |
| `spec_audit.md` | Lean 敘述和 OEIS 定義逐項對照 |
| `literature_check.md` | 文獻補查紀錄 |
| `code/l01_check.py`、`code/l02_check.py` | 奇數、偶數寬度的數值檢查（兩種獨立方法） |
