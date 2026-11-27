# OEIS 離線全庫（`discovery/oeisdb.py`）

資料來源：OEIS 官方 git 鏡像 <https://github.com/oeis/oeisdata>（每條一個 `seq/Annn/Annnnnn.seq`，內部格式，每天同步，CC BY-SA 4.0）。**資料不進 repo**（`data/oeis/oeisdata/`、`data/oeis/index/` 都在 .gitignore）。

```
python -m discovery.oeisdb fetch     # 淺層 sparse clone seq/（約 1.6 GB、40 萬檔，幾分鐘）；已有就 pull
python -m discovery.oeisdb build     # 解析成 data/oeis/index/oeisdb.sqlite（約 40 秒）
python -m discovery.oeisdb stats     # 總數、各題型、各年份
python -m discovery.oeisdb conj --kind never --since 2020 --open --new --limit 30
python -m discovery.oeisdb conj --text "pseudoprime" --keyword nonn --json
python -m discovery.oeisdb grep "is never" --tag C
python -m discovery.oeisdb show A294646
python -m discovery.oeisdb export A294646    # 存到 data/cx/entries/，給 cxsearch
```

- `conj`：%C/%F 裡含 Conjecture、It seems、apparently、empirical 等字的行。已經在講「反例／已證」的行不算猜想。
- `--kind`：never、no_solutions、always_prime、divides、periodic、finite、infinite、base_digits、gf、recurrence、asymptotic、inequality（正規式粗分，可多選，交集）。
- 年份：猜想行自己的署名日期，沒有就用條目建立年份（%A）。
- `--open`：去掉條目其他行出現 counterexample、disproved、proved、confirmed 等字的（粗篩，**還是要讀全文**，A218483 的教訓）。
- `--new`：去掉 `data/cx/triage.json` 和 `results/` 已經處理過的條目。
- 每次查詢第一行印出快照 commit，紀錄裡照抄這行當出處。快照裡找不到不代表新。
- `cxsearch.entry.load(anum)`：`data/cx/entries/` 沒有存檔時，自動從離線庫匯出再讀，判斷用的原文因此留在 repo 裡。

2026-11-27 快照 091a90f51479：402,063 條、56,012 行猜想（42,426 條條目），其中 never 361、no_solutions 559、divides 3238、periodic 364、base_digits 931 行。
