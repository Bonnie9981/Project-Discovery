# DISC-0031 文獻

## 問題

OEIS marked mesh pattern 家族（A212338～A212349）裡的 empirical g.f. 與猜想能不能證明，是否早已有人證過。

## 已知成果

- OEIS 離線全庫（091a90f51479）：A212338 有 Mathar 的 g.f.（k = 2，沒寫證明）；A212339 只有 Barker 的「Empirical g.f.」和 Dale 的「Conjecture」遞迴；A212341 只有 Barker 的「Empirical g.f.」；A212344 有 Bala「appears to be 5*A000108」、Mathar 的 Conjecture 遞迴、Gladkovskii 兩條 conjecture g.f.；A212345 沒有公式。除了條目自己之外沒有序列提到 A212339/A212341（S001）。
- KRT, arXiv:1201.6243（條目引用的論文，第 1 篇）（S002，逐字讀了 Section 4、5、5.1）：
  - 遞迴 (21)、閉式解 (17)。
  - Theorem 13(1)：Q_{n,132}^{(0,k,0,0)}(x) 最高次 x^{n−k} 的係數是 C_k C_{n−k}；Theorem 13(2)：x^{n−k−1} 的係數 a_k C_{n−k}，a_3 = 9。所以 H2 是**已知定理**的特例。
  - Section 4 列出 (0,0,3,0) 的 x 係數「5, 19, 61, 188, 532, 1387, ... does not appear in the OEIS」（532 應為 523，論文自己的展開式寫 523），並寫「there does not seem to be any simple way to extract a simple formula for Q^{(0,0,k,0)}(t,x)|_x from (17)」。
- KRT 第 II 篇（strathprints PDF）、第 III 篇（arXiv:1303.0854）：前約 4 萬字元逐字讀過，後段只有模型摘要；Theorem 3 只重述 (0,0,k,0) 的閉式解，沒有 x 係數公式（S003）。
- Borie, arXiv:1311.6292（全文逐字）：只有 k = 1 的公式與二元樹的組合解釋，沒有 x 係數公式（S004）。

## 研究空白

H1 的式子只要從 KRT 的函數方程取 x 的一次項就出來，屬於習題程度；但 KRT 明說沒找到簡單公式，OEIS 也只標 empirical/conjecture。沒查 MathSciNet、zbMATH 與 KRT 之後引用這幾篇的其他論文。

## 查詢紀錄

見 `search_evidence.jsonl`（DISC-0031-S001～S004）。
