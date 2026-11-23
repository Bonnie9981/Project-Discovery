# OEIS A134559：Ratajczak 2019 猜想的反例 4933

紀錄 [DISC-0021](../../records/DISC-0021/)，Lean `lean/Discovery/A134559Counter.lean`，搜尋器登錄 `discovery/cxsearch/conjectures.py`（`A134559`）。

| 檔案 | 內容 |
|---|---|
| `../../paper/a134559-counterexample.md` | 英文短證明（反例＋另一半的證明），OEIS LINKS 要連的頁面（網址固定） |
| `a134559_oeis_edit_draft.md` | OEIS 編輯草稿，使用者自己送出 |
| `code/a134559.c` | 照「n mod u = k」定義掃 n ≤ 1.5·10^5 |
| `code/chk134559.py` | 用因數和形式 T(n−k, k+1) 獨立重算三個反例 |

重現：`gcc -O2 -o a134559 code/a134559.c && ./a134559 150000`（約 1 分鐘），或 `python -m discovery.cxsearch scan A134559 --nmax 5000`。
