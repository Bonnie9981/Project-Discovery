# DISC-0007 文獻對照表（M1.4）

查詢日期：2026-11-22。管道：使用者的 Chrome。每筆查詢的 URL 和時間都記在 `search_evidence.jsonl`（DISC-0007-S001～S010）。DISC-0006 的 7 筆查詢（DISC-0006-S001～S007）也算在內。

## 問題

M1.4 的主線是 C02：

> rad(σ(n)) = σ(rad(n)) ⇔ n ∈ A065301（n 和 σ(n) 都無平方因子），或 n = 2^a·p，其中 p 是奇質數，a 是奇數且 ≥ 3，p+1 無平方因子，3 ∤ p+1，且 rad(2^{a+1}−1) | 3(p+1)。

這次要查的有四件事：

1. 原始等式。
2. 完整刻畫 H2′。
3. 它的等價說法，例如「σ 和 rad 可交換」「squarefree kernel of the sum of divisors」。
4. 副線 R2-C10：規則 54 在有限環上的暫態。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| A065301 的結構：k 無平方因子、質因數都在 A049097 裡、{p+1} 兩兩互質 | OEIS A065301，Eldar 2025 | **相同（已知）**：等於 H2′ 第一類的刻畫。不能列為發現 |
| σ(n) = rad(n)² 的解（De Koninck 猜想），例如 1782 | Broughan、De Koninck、Kátai、Luca，JIS 2012（Zbl 1291.11006）；Broughan、Delbourgo、Zhou，JNT 2014（Zbl 1298.11004） | **相關背景**：同樣在研究 σ 和 rad 的交互作用，但方程式不同，沒有提到 rad(σ(n)) = σ(rad(n)) |
| 規則 54 在無限線上、從單一種子出發的每一列 | OEIS A118108、A118109、A071030、A265225 | **相關背景**：無限線上的圖樣是規則的週期圖樣，和 critic 說的 ether 一致；但這些條目沒有提到有限環 |
| 規則 54 在寬度 n 的環上的最大週期（取遍所有初始狀態） | OEIS A204714 | **相關，但不是同一個量**：我們研究的是單一種子的暫態 |
| 規則 54 的粒子語言和碰撞 | Redeker 2017（Complex Systems 26:39）；Martínez 等 2005（Chaos Solitons Fractals） | **相關背景**：可以支撐「牆／缺陷」的結構解釋，但這幾篇都沒有暫態公式 |

## 研究空白

在已查的範圍內（OEIS、zbMATH、arXiv、OpenAlex、MathOverflow、Math.SE）：

- **沒有找到** rad(σ(n)) = σ(rad(n)) 這個等式。
- **沒有找到** 它的解集中 A065301 以外的那一部分（2^a·p 類）。
- **沒有找到** 規則 54 在有限環上、從單一種子出發的暫態公式。

這些都只能判定為 `NO_MATCH_IN_SCOPE`，不代表是新的。

**難度評估（critic 提醒）：** C02 的「⇐」方向是直接計算；「⇒」方向用 LTE（或 Zsigmondy 定理）加上簡短的分情形討論，大約是習題程度。這個刻畫就算沒有出現在文獻裡，也很可能被視為已知技巧的直接應用。它主要的價值在於完整的 Lean 形式化。

## 查詢紀錄

| ID | 平台 | 查詢 | 結果 |
|---|---|---|---|
| S001 | zbMATH | "sum of divisors" radical squarefree | 0 筆 |
| S002 | zbMATH | 標題含 sum、divisors、squarefree | Broughan 等 2012（σ = rad²），相關 |
| S003 | zbMATH | "sum of divisors" ＆（radical 或 kernel）＆ MSC 11A25 | Broughan、Delbourgo、Zhou 2014，相關 |
| S004 | arXiv | 摘要含 "sum of divisors" 和 radical | 1 筆，無關 |
| S005 | arXiv | 摘要含 squarefree 和 "sum of divisors" | 3 筆，無關 |
| S006 | MathOverflow | sigma rad squarefree kernel sum of divisors | 0 筆 |
| S007 | Math.SE | "sigma(rad" | 1 題，無關 |
| S008 | OEIS | "rule 54" | 25 筆；只看了第 1 頁，都在無限線上 |
| S009 | OEIS | "rule 54" cyclic | A204714（所有初始狀態的最大週期） |
| S010 | OpenAlex | Hanson Crutchfield … rule 54 | Redeker 2017 等，沒有暫態公式 |

**還沒查的管道和原因：**

- **MathSciNet：** 需要訂閱，使用者的瀏覽器沒有登入。
- **Google Scholar：** 會擋自動化查詢，而且可能跳 CAPTCHA，我們不會處理 CAPTCHA。
- **Semantic Scholar、Crossref：** 這一輪沒有查，留到下一輪。
- **論文全文：** 列為「相關」的論文都只看了摘要，沒有讀全文。

**判定：** C02 的新穎性狀態維持 `NO_MATCH_IN_SCOPE`，要升級需要人工審查。A065301 那一部分的狀態是 `MATCH_FOUND`。
