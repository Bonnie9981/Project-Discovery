# 反例搜尋器（內部模組，暫不開源）

`discovery/cxsearch/`：把 A294646（DISC-0017）找反例的做法做成可重用的流程。

## 流程

1. **選題**：用 Chrome 在 OEIS 搜「Conjecture: a(n) is never」「no solutions」「always prime」「pseudoprimes conjecture」等，`fmt=text` 批次抓回，篩出「沒有人回覆過」的猜想。分流紀錄在 `data/cx/triage.json`。優先：is never > no solutions > always prime；避開 conjectured 線性遞迴。
2. **先看條目留言**：`entry.Entry.settled_hints()` 把含 counterexample、proved、is true… 的留言挑出來給人看（A214305、A215672、A218010 都已經有人推翻，不能重複報）。
3. **對齊**：判定函式先和 DATA、b-file 對齊（`entry.align`、或比項數與總和），offset 和定義讀錯是假反例的最大來源。
4. **目錄**：`catalog.py` 的 2 底偽質數（psp2）目錄到 10^10（`data/cx/psp2_1e10.txt.gz`），載入時用 Python 大整數逐項重驗，並對 OEIS A055550、A055553 的計數。Carmichael 數由 Korselt 判別從 psp2 篩出（完整）。
5. **掃描**：`conjectures.py` 一條猜想一個判定函式，全部用 Python int，不會溢位。
6. **自我測試**：每次都要能重新找到已知反例（A218010 的 3380740301）。
7. **候選複查**：獨立實作重算（critic）、查是否已有人發表（OEIS 搜數字、條目全文）、問最小性；能的話做結構搜尋（像 A321790：反例必須滿足的整除條件，對 p 窮舉、q 不設上限）。
8. **證書**：反例和證明寫成 Lean（只用 core），再走 critic、reviewer。

## 指令

```
python -m discovery.cxsearch list
python -m discovery.cxsearch catalog                    # 重驗目錄
python -m discovery.cxsearch scan [KEY ...]             # 掃描
python -m discovery.cxsearch catalog --build 1e10 --path /tmp/x_1e10.txt.gz   # 從頭建（切小段，每段走 run_limited）
```

## 新增一條猜想

在 `conjectures.py` 寫判定函式（成立回傳 None，不成立回傳說明 dict），加進 `REGISTRY`，`reading` 欄寫清楚怎麼解讀原句。在 `tests/test_cxsearch.py` 加對齊測試。
