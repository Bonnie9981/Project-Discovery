# DISC-0027 實驗

程式版本：commit 9686613 之後的工作樹（本 PR）。Python 3、numpy；檢查腳本只用標準函式庫。

## 方法

三套互相獨立的算法：

- **A 暴力**：`discovery/newseq/graphsets.py`（numpy 向量化，所有 2^|V| 子集，|V| ≤ 20）與 `results/locating-dominating-path/code/check_paths.py` 的 `is_ld`、`is_id`（照定義逐一判斷，n ≤ 20）。
- **B 轉移矩陣**：`discovery/newseq/transfer.py`，把每個性質寫成「S 要碰到每個遮罩」，只記最後 W = 5 個位元（環另記前 5 位），算到 n = 70；以及 `check_paths.py` 的字串規則（引理 1、3）和 8 狀態矩陣。
- **C 公式**：遞迴與生成函數（sympy 展開比對）。

## 結果

- P_n 定位支配集：A、B、C 在 n ≤ 20 全一致；B 與 C 在 n ≤ 60 一致。
- C_n 定位支配集：暴力在 3 ≤ n ≤ 20 與 A001642 一致，唯一例外 n = 4（9 vs 11）；轉移矩陣（B）到 n = 39 與 A001642 一致。
- P_n 識別碼：A、字串規則、8 狀態矩陣、遞迴在 n ≤ 20 一致；矩陣與遞迴到 n = 39 一致；B 到 n = 60 一致。
- 矩陣特徵多項式 = x·(x^7 − x^6 − x^5 + x^4 − x^3 − x^2 + 1)（sympy 精確計算）。
- 小 n 的另兩種圖（梯子、稜柱等）也算了，但沒有完整證明，不在這份紀錄主張。

## 重現方式

```
python -m discovery.oeisdb fetch && python -m discovery.oeisdb build
python -m discovery.newseq.graphsets data/newseq/graphsets.json   # 約 4 分鐘
python -m discovery.newseq.screen data/newseq/graphsets.json      # 約 1 分鐘
python results/locating-dominating-path/code/check_paths.py       # 約 15 秒
```
