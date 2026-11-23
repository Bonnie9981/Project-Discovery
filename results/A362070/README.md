# OEIS A362070：猜想「a(n) = a(n+1) 無解」的反例 n = 1715

紀錄 [DISC-0020](../../records/DISC-0020/)，Lean `lean/Discovery/A362070Counter.lean`，搜尋器登錄 `discovery/cxsearch/conjectures.py`（`A362070`）。

| 檔案 | 內容 |
|---|---|
| `../../paper/a362070-counterexample.md` | 英文短證明，OEIS LINKS 要連的頁面（網址固定） |
| `a362070_oeis_edit_draft.md` | OEIS 編輯草稿，使用者自己送出 |
| `code/brute.py` | 照定義逐字用大整數算 |
| `code/factored.py` | 用質因數賦值算 |
| `code/scan.c` | 篩法掃到 10^10 |
| `code/entry_program.mac` | 條目自己的 Maxima 程式 |

重現：`python -m discovery.cxsearch scan A362070 --nmax 2000`
