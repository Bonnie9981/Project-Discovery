# OEIS A336662、A189722、A337353：一直轉彎的蛇與 Manhattan 格子

紀錄 [DISC-0032](../../records/DISC-0032/)。證明頁 [paper/a336662-manhattan.md](../../paper/a336662-manhattan.md)。序列關係挖掘（`discovery/relmine.py`，第四批：兩邊都沒有公式）找到。

| 檔案 | 內容 |
|---|---|
| `a336662_oeis_edit_draft.md` | OEIS 編輯草稿（先送 A337353 的更正，再送 A336662），使用者自己送出 |
| `code/check_a336662.py` | 三種暴力列舉 n ≤ 16、中點對應逐條檢查、比對三條條目的 OEIS 資料 |
| `code/independent_check.py` | critic 另寫的獨立重算（不 import 專案程式） |
| `證明方法說明.md`、`程式說明.md` | 高二版中文說明 |

結果：A336662(k) = 2·A189722(k+1)（k ≥ 1），A337353(n) = 4·A336662(n−1)（n ≥ 1）= 8·A189722(n)（n ≥ 2）。A337353 現有的「a(n) = 4*A336662(n)」下標錯一格。證明是 Watson 1970 覆蓋格子對應的特例（取每一步的中點）。審查判 SUPPORTED_KNOWN（A337353 已有同一關係、只是下標錯）。紙上證明，沒有 Lean。
