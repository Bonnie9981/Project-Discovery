# DISC-0030 實驗

程式版本：commit c72b579 之後的工作樹（本 PR）。

## 方法

- H1、H2：`results/open-locating-cycle/code/check_old.py`（只用標準函式庫）照定義暴力列舉所有子集，n ≤ 20，和公式比。
- H3、H4：三套算法：照定義暴力（n ≤ 9）、窗口 DP（n ≤ 15）、新的逐欄轉移矩陣 `discovery/newseq/strip.py`（n ≤ 54）。strip.py 另做「向量恆等式」驗證：狀態向量在某一欄滿足遞迴，之後每一步乘同一個矩陣，所以遞迴對所有 n 成立（LD n ≥ 29、ID n ≥ 24）。

## 結果

- H1、H2：n ≤ 20 暴力與公式全部一致（critic 的第三套程式另算 H1 到 n = 40、H2 到 n = 60）。
- H3：13 階遞迴，從 n = 14 起成立；向量恆等式在 t0 通過。三套算法在各自範圍一致。
- H4：10 階遞迴，從 n = 11 起成立；向量恆等式通過。三套算法一致。

## 重現方式

```
python results/open-locating-cycle/code/check_old.py        # 約 5 秒
python results/ladder-locating/code/check_ladder.py         # 約 20 秒（要 repo 的 discovery/）
```
