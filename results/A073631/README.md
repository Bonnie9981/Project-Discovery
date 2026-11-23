# OEIS A073631 / A130058：Adamchuk 2007 猜想的反例 3842760169²

紀錄 [DISC-0023](../../records/DISC-0023/)，Lean `lean/Discovery/A073631Counter.lean`，搜尋器登錄 `discovery/cxsearch/conjectures.py`（`A073631`）。

| 檔案 | 內容 |
|---|---|
| `../../paper/a073631-counterexample.md` | 英文短證明（反例、最小性），OEIS LINKS 要連的頁面（網址固定） |
| `a073631_oeis_edit_draft.md` | OEIS 編輯草稿（A073631、A130058、A376896 三筆），使用者自己送出 |
| `code/wieferich32.c` | 掃 2^32 以下所有質數找 3/2 底 Wieferich 質數，約 30 秒 |
| `code/a073631_scan.c` | 直接掃 A073631 到 N，列出非無平方因數又不是 529 倍數的項 |
| `code/chk073631.py` | Python 大整數重算兩個反例 |

重現：`gcc -O2 -fopenmp -o w code/wieferich32.c -lm && ./w 1 4294967295`；`python -I code/chk073631.py`。
