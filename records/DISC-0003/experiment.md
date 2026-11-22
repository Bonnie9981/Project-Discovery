# DISC-0003 experiment.md

作者：orchestrator（experiment 角色）

## 方法

兩套實作放在 `research/r001/disc0003/`，彼此不 import（`python -m discovery.independence` 通過）：

| | impl_a.py | impl_b.py |
|---|---|---|
| 寫法數 R_D^{條件}(N) | 對每個首項 a 逐項加 a, a+D, a+2D…，每個部分和直接記進表格，超過 N_max 就停。不用任何公式。 | 固定項數 k：和 = k·a + D·k(k−1)/2，所以有解 ⇔ N − D·k(k−1)/2 是 k 的正倍數。對 k 迴圈。 |
| d_odd(N)、τ(N) | 試除 d ≤ √N，列出因數對 {d, N/d} 再數 | 質因數分解，乘積 Π(e_p + 1)（d_odd 跳過 p = 2） |
| 定義域 | `list(range(1, n+1))` | while 迴圈自己產生 |

第三套 `impl_c.py` 由獨立 critic 撰寫（生成函數 Σ x^{k+Dk(k−1)/2}/(1−x^k) 的步長篩法取係數、因數篩法），`run.py` 會自動接上。

每個猜想用 `discovery.verify.check` 跑：兩邊都必須給同一個答案，否則 `INCONCLUSIVE`；兩邊定義域也要相同。上限照 `config/limits.json`（600 秒、10⁶ 次迭代）。H5 對每個 N 要算 8 個公差，所以範圍縮到 N ≤ 10000。

延伸序列 E1～E13：兩套實作各算 N = 1..80，比對後送 `discovery.novelty.check_sequence`（本地表、離線 OEIS 快照、線上 OEIS）。

## 結果

`experiment_data.json`（第二版：commit `506e0bced1a0fa782f86f77db9366263f0f1bcbf`，無 `-dirty`；Python 3.13.18，Linux；39.9 秒；H1～H6 三套實作、H7 兩套）。第一版（commit `4668a62`，兩套實作）的 H1～H6 與延伸序列除實作數外相同；H7 是第二版新增（reviewer 更正）。

| 猜想 | 範圍 | 狀態 | 檢查數 | 反例 |
|---|---|---|---|---|
| H1 R(N) = d_odd(N) | 1..100000 | SUPPORTED_IN_RANGE | 100000 | 無 |
| H2a 至少兩項 = d_odd − 1 | 1..100000 | SUPPORTED_IN_RANGE | 100000 | 無 |
| H2b 沒有 ≥2 項寫法 ⇔ 2 的冪 | 1..100000 | SUPPORTED_IN_RANGE | 100000 | 無 |
| H3 奇/偶項數 ↔ 奇因數 d² < 2N / > 2N | 1..100000 | SUPPORTED_IN_RANGE | 100000 | 無 |
| H4 R_2 = #{d∣N, d² ≤ N} = ⌈τ/2⌉ | 1..100000 | SUPPORTED_IN_RANGE | 100000 | 無 |
| H5 一般公差的因數判準，D = 1..8 | 1..10000 | SUPPORTED_IN_RANGE | 10000 | 無 |
| H6 R_2 ≤ R_1 | 1..100000 | **REFUTED** | 4 | **N = 4**：4 = 4 = 1+3，R_2(4) = 2 > R_1(4) = 1 |
| H7 R_2 > R_1 ⇔ 4 ∣ N（critic A3 建議補上的反例完整刻畫） | 1..100000 | SUPPORTED_IN_RANGE | 100000 | 無 |

H6 被三套實作一致推翻，表示反例搜尋有作用。

延伸序列新穎性（`novelty_data.json`，快照 `sha256:c6d34403102c`）：

| 序列 | 意義 | 新穎性狀態 | 完全吻合 |
|---|---|---|---|
| H1_R1 | R(N) | MATCH_FOUND | A001227 |
| E1 | ≥ 2 項 | MATCH_FOUND | A069283 |
| E2 | 奇數項 | MATCH_FOUND | A082647（OEIS 名稱是「項數 d 為 n 的因數」；與「項數為奇數」等價，因為由 2N = k(2a+k−1)，k ∣ N ⇔ k 奇） |
| E3 | 偶數項 | MATCH_FOUND | A131576 |
| E4 | ≥ 3 項 | MATCH_FOUND | A111775 |
| E5 | ≤ 3 項 | MATCH_FOUND | A239140（定義寫成「σ < 1 的相異部分分割」；critic A8 給出等價論證，前提是 A239140 用母體標準差，此前提只從快照數值反推，未讀 OEIS 原文） |
| E6 | 公差 2 | MATCH_FOUND | A038548 |
| E7 | 公差 2、≥ 2 項 | MATCH_FOUND | A072670（索引位移：E7(n) = A072670(n−1)，該條 offset 為 0） |
| E8 | 公差 3 | MATCH_FOUND | A117277 |
| E9 | 公差 3、≥ 2 項 | MATCH_FOUND | A243223 |
| E10 | 公差 4 | MATCH_FOUND | A334461 |
| E11 | 公差 5 | MATCH_FOUND | A334541 |
| E12 | 公差 6 | MATCH_FOUND | A334948 |
| E13 | 項數為質數 | NO_MATCH_IN_SCOPE | 無（線上 OEIS 也查無，S002）。**不代表新**；critic 指出它有平凡封閉式 [N 奇且 ≥ 3] + #{奇質數 p ∣ N : p² < 2N}，不值得送審 |

所有延伸序列兩套實作都一致（`impl_agree: true`）。程式端線上 OEIS 連不到（proxy 403），已記在 `sources_failed`。

已知限制：
- 有限範圍的檢查不是證明。H3、H5 沒有 Lean 證明。
- **H5 在 impl_b 是同義反覆**（critic A4）：impl_b 的左邊「n − Dk(k−1)/2 是 k 的正倍數」與右邊的因數判準在代數上等價，對 H5 沒有證據力。H5 的實質證據只有 impl_a（逐項列舉）與 impl_c（生成函數篩法）。H5 本身也只是 2N = k(2a + (k−1)D) 的重述，而且 impl_a 與 impl_b 在 H5 右邊用的是同一個式子（只是列舉因數的方法不同）。
- A131576、A111775 的 OEIS 名稱寫「consecutive integers」，資料其實對應「正整數」版本（critic A9）。
- 第一版 E13 把質數寫死成 {2,…,19}（critic A7），N ≥ 276 會出錯；第二版改成真正的質數判定，80 項結果不變。
- 延伸序列只查了前 80 項。

## 重現方式

```bash
git checkout 506e0bced1a0fa782f86f77db9366263f0f1bcbf
python -m research.r001.disc0003.run 100000 > out.json      # 約 40 秒
python -m research.r001.disc0003.novelty_run > nov.json     # 需要 data/oeis/raw/ 快照
python -m pytest -q tests/test_disc0003.py
```
`out.json` 的 `results` 應與 `experiment_data.json` 完全相同（`seconds`、`env` 除外）。
