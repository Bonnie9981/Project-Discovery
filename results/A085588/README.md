# OEIS A085588：規則 150 環的最終週期整除 2^D(2^s − 1)

紀錄 [DISC-0016](../../records/DISC-0016/)，Lean `lean/Discovery/A085588Period.lean`。

| 檔案 | 內容 |
|---|---|
| `../../paper/a085588-period.md` | 英文短證明，OEIS LINKS 要連的頁面（網址固定，留在 paper/） |
| `a085588_oeis_edit_draft.md` | OEIS 編輯草稿（更正留言的整除方向），使用者自己送出 |
| `code/l08_a085588_period.py` | 數值檢查（快速算子冪求精確週期、直接模擬兩種方法） |
| `code/critic_c_a085588.py` | critic 的獨立第三方檢查（GF(2)[x]/(x^n−1) 一般冪） |
| `code/bfile_check.js` | 瀏覽器內檢查整個 b-file（n ≤ 1000） |
