# OEIS A294646：「a(n) 不會是 2n−2」的反例

紀錄 [DISC-0017](../../records/DISC-0017/)，Lean `lean/Discovery/A294646Counter.lean`。

| 檔案 | 內容 |
|---|---|
| `../../paper/a294646-counterexample.md` | 英文短證明，OEIS LINKS 要連的頁面（網址固定，留在 paper/） |
| `a294646_oeis_edit_draft.md` | OEIS 編輯草稿，使用者自己送出 |
| `code/verify.py` | 直接用大整數驗反例和前 20 項 DATA |
| `code/brute.c` | 對所有奇數 m < 10^10 逐一檢查三種情形（`./brute lo hi`） |
| `code/gen_primes.py` + `code/scan.c` | 結構搜尋：先列出可能整除 m 的質數 p < 2·10^6（`python3 gen_primes.py 2000000` 產生 plist.txt），再掃 m = p·k，k ≤ 10^9（`./scan 1000000000 0 1`），對 m ≤ 6.1·10^10 是完整的 |
