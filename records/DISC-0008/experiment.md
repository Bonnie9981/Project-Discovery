# DISC-0008 實驗

## 方法

`research/r003/l01_check.py`，只用標準函式庫，兩種獨立方式：

1. 用 `research/r002/impl_b.py` 模擬，逐步比對 H1 的封閉形式，並核對 Brent 偵測到的 (T, P) = (0, w·2^⌊log₂ w⌋)。
2. 腳本內另寫的串列模擬（不 import repo 程式）：在 t ≤ 3P 內，x_t = x₀ 的 t 恰好是 P 的倍數。

另外檢查了 Lucas 定理 p = 2 的兩個推論（t ≤ 2000）、封閉形式歸納用到的四種局部情形，以及偶數 w 的軌道是否等於規則 90 的軌道（2 ≤ w ≤ 40）。

## 結果

- 奇數 3 ≤ w ≤ 61：全部 OK（約 0.8 秒）。證明 agent 另外跑到 w ≤ 129 也 OK（約 17 秒）。
- 偶數 2 ≤ w ≤ 40：規則 26 的軌道等於規則 90 的軌道。
- 數值只是佐證，H1 的根據是 proof.md 的一般證明和 Lean。

## 重現方式

```
python research/r003/l01_check.py
```

Python 3.13。record.json 的 `experiment_commit`（af98758）是程式和 Lean 檔的 commit；紀錄檔（本檔、literature、critic、review、record.json）在之後的 commit 才加入。
