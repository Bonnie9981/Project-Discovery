# DISC-0002 experiment.md

作者：orchestrator（主執行緒扮演 experiment 角色）

## 方法

- 程式：`research/r001/drill.py`，每個猜想透過 `discovery.verify.check` 用兩個獨立的質數判定（試除法 A、Miller–Rabin B）各算一次，結果不一致就判 INCONCLUSIVE。
- H1 在 p = 2..10000 檢查（一般情形交給 Lean，所以範圍取小）。
- H4、H5 在所有質數 p ≤ 100000（共 9592 個）檢查。
- 程式版本：`5288d723beb169dfc2a614c808c52f9ec9a142b2`，Python 3.13.18，Linux x86_64，耗時約 1 秒。
- 原始輸出：[experiment_data.json](experiment_data.json)
- 這是第二版。第一版（commit `9a837f1`）除 H3 的狀態名稱外結果相同，但 critic 指出 H3 用了規範外的狀態名稱、MR 文件的上界寫錯，修正後重跑。

## 結果

| 猜想 | 狀態 | 檢查數 | 反例 | 實作不一致 |
|---|---|---|---|---|
| H1 | 範圍內成立 | 9999 | 無 | 0 |
| H2 | 成立（完整範圍） | 40 | 無 | 0 |
| H3 | 成立：1681 = 41² 不是質數，兩個實作一致 | 1 | — | 0 |
| H4 | 範圍內成立 | 9592 | 無 | 0 |
| H5 | 範圍內成立 | 9592 | 無 | 0 |

已知限制（critic 第 3、4 點）：
- H4/H5 的兩個實作只有質數判定不同，範圍、`q_holds`、清單都是共用程式碼，所以無法防範這些共用部分的錯誤。critic 用完全不依賴專案的程式獨立重算過，結果一致。
- H5 的資料很弱：p ≤ 100000 內，非 lucky 質數連續成立最多只到 n = 7，所以「只檢查到 n = 8」也會得到同樣的等價。這個實驗無法區分 √(p/3) 與更小的常數上界。

## 重現方式

```bash
git checkout 5288d723beb169dfc2a614c808c52f9ec9a142b2
python -m research.r001.drill 100000 > out.json
```

`out.json` 的 `results` 應與 `experiment_data.json` 相同（`seconds`、`env` 欄位除外）。
