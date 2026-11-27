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

- `conj`：%C/%F 裡含 Conjecture、It seems、apparently、empirical 等字的段落。OEIS 一則留言常拆成好幾行、只在最後一行署名，所以段落從這行接到下一個有署名的同類行（最多 6 行）；後面沒有署名就只算這一行。已經在講「反例／已證」的段落不算猜想，但「no counterexample up to…」「verified up to…」這類只是在說檢查過，不算。
- `--kind`：never、no_solutions、always_prime、divides、periodic、finite、infinite、base_digits、gf、recurrence、asymptotic、inequality（正規式粗分，可多選，交集）。
- 年份：猜想段落的署名日期；**約六成段落沒有署名**（多半是條目原作者寫的），這時用條目建立年份（%A），所以 `--since` 不等於「最近提出的猜想」，舊條目裡沒署名的新留言會被排掉。
- `--open`：去掉條目其他行出現 counterexample、disproved、proved、confirmed 等字的（粗篩，**還是要讀全文**，A218483 的教訓）。
- `--new`：去掉 `data/cx/triage.json` 和 `results/` 已經處理過的條目。
- 每次查詢第一行印出快照 commit，紀錄裡照抄這行當出處。快照裡找不到不代表新。
- `cxsearch.entry.load(anum)`：`data/cx/entries/` 沒有存檔時，自動從離線庫匯出再讀，判斷用的原文因此留在 repo 裡。

2026-11-27 快照 091a90f51479：402,063 條、49,307 段猜想（42,015 條條目），其中 never 371、no_solutions 608、divides 3182、periodic 377、base_digits 1012 段。
