# DISC-0022 文獻

## 問題

Erdős–Gyárfás 猜想（1995；erdosproblems.com #64）：每個最小度數 ≥ 3 的有限簡單圖，都有一個長度是 2 的次方（4、8、16、…）的圈。這是專案第一條「不是數列」的副線（使用者 2026-11-23 選定）。

## 已知成果

2026-11-23 用網頁搜尋查到的計算結果（全部是前人的，本紀錄沒有超過任何一個）。arXiv 三篇只讀了摘要和前段，表中敘述依摘要，沒有逐節核對；critic 連不到 arXiv，沒有獨立查證。

| 來源 | 範圍 | 方法 | 證書 |
|---|---|---|---|
| Markström 2004（Congressus Numerantium 171） | 三正則圖到約 30 點 | 窮舉生成 | 無 |
| Garcia, arXiv:2609.04686（2026-09） | 所有最小度 ≥ 3 的圖，≤ 23 點 | PySAT＋CaDiCaL，CEGAR 擋 8 圈，字典序對稱破缺 | DRAT（drat-trim 檢查） |
| Balaji, GitHub `erdos-gyarfas-min-degree-3`（2026） | ≤ 31 點 | SAT Modulo Symmetries＋Glasgow 子圖求解器 | 沒提 |
| Olsen, GitHub `mcolsen/erdos-gyarfas`（2026-10，作者自己說沒審過） | 宣稱 ≤ 35 點、三正則 ≥ 50 | nauty、SMS、Glasgow | 不明 |
| Ducoffe–Dumitru, arXiv:2609.28594（2026-09） | 所有圖 ≤ 40 點、三正則 ≤ 48、二部 ≤ 66 | 見論文第 5 節（本執行緒沒讀到） | 不明 |

結構結果：Carr, arXiv:2605.22844（2026-05）證明最小反例至少 4/7 的點是 3 度，度 ≥ 4 的點互不相鄰；Ducoffe–Dumitru 證明最小反例 2-邊連通、邊數 ≤ 2n−2、至少 2n/3+1 個 3 度點。已知部分情形：平面三連通三正則圖（Heckman–Krakovski 2013）、無爪圖（Daniel–Shauger）、P10-free 圖（Discrete Math. 2024）。

## 研究空白

40 點以內已經有人用電腦排除，雲端容器的算力不可能推過這個前沿。本紀錄的定位是**重現加證書**：用跟前人不同的、可以逐行檢查的程式重做小範圍，並留下自己的檢查器可以驗的 RUP 證書，順便建立專案的 SAT＋證書工具。不宣稱新。

## 查詢紀錄

見 `search_evidence.jsonl`（DISC-0022-S001）。只讀了上表各頁的摘要（arXiv 兩篇只讀到前段，Ducoffe–Dumitru 的計算方法那節沒讀到）。
