# DISC-0001: Prime-generating quadratics n^2+n+p

- 研究線：R-001
- 程式版本：`890b845333717f97fd066c2c8b709eec2801e539`
- 環境：Python 3.13.18，Linux-6.18.44-fc-v726-x86_64-with-glibc2.39
- 參數：`{'p_max': 2000, 'use_network': True}`
- 開始 / 結束：2026-11-22T07:22:52+00:00 / 2026-11-22T07:22:52+00:00

## 1. 問題（精確定義）

對每個質數 p ≤ p_max，猜想 Q_p：「對所有整數 0 ≤ n ≤ p−2，n² + n + p 都是質數」。
每個 Q_p 是有限命題，所以檢查完整個範圍就等於判定它的真假（前提是質數判定正確）。

## 2. 方法

- 實作 A：試除法判定質數。實作 B：Miller–Rabin（前 12 個質數為底，在本範圍內是確定性的）。
- 兩個實作對每個 n 都要給出相同答案，否則整筆結果判為 INCONCLUSIVE。
- 找到第一個兩邊都同意的反例就判定 Q_p 不成立。
- 成立的 p 組成一個數列，拿去做新穎性檢查。

## 3. 結果

- 測試的猜想數：303
- 被反駁：297
- 成立：6 → p = [2, 3, 5, 11, 17, 41]
- 實作不一致：0

被反駁的前 10 個（反例 n）：

| 猜想 | 反例 n | n²+n+p |
|---|---|---|
| Q7 | 1 | 9 |
| Q13 | 1 | 15 |
| Q19 | 1 | 21 |
| Q23 | 1 | 25 |
| Q29 | 2 | 35 |
| Q31 | 1 | 33 |
| Q37 | 1 | 39 |
| Q43 | 1 | 45 |
| Q47 | 1 | 49 |
| Q53 | 1 | 55 |

## 4. 新穎性檢查

- 已查來源：['local']
- 查詢失敗：['oeis: URLError: <urlopen error Tunnel connection failed: 403 Forbidden (agent proxy: no rule or network setting allows this host)>']
- 符合：A014556 — Euler's 'lucky' numbers: p such that n^2 + n + p is prime for n = 0..p-2（OEIS A014556; G. Rabinowitsch (1913), J. reine angew. Math. 142, 153-164. Completeness follows from the class number one theorem (Heegner 1952, Baker 1966, Stark 1967).）

## 5. 結論

**判定：`SUPPORTED_KNOWN`**

系統重新找到了一個已知結果（Euler 的 lucky numbers，Rabinowitsch 1913），新穎性檢查正確地把它標成「已知」。
這**不是新發現**。這次演練的價值在於證明整條流程（生成 → 反例搜尋 → 雙實作驗證 → 新穎性檢查 → 紀錄）能跑通，而且不會把已知結果誤報成新成果。

## 6. 限制

- 只測了 p ≤ p_max。「沒有更大的 p 成立」這件事本次沒有驗證，那需要類數 1 定理（文獻已證明），不是有限搜尋能給的。
- 新穎性檢查若只查到本地已知表，代表 OEIS 沒連上；本地表是人工輸入的，只能用來確認「已知」，不能用來確認「新」。
- 尚未有 Lean 形式化證明。
