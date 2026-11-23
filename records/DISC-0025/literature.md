# DISC-0025 文獻

## 問題

Tuza 猜想（1981）：任何圖都有 τ(G) ≤ 2ν(G)。下面先記選題經過。

**選題經過（副線第二題）。** 使用者要「還沒人大量電腦算過、適合 SAT 搜反例」的圖論猜想。查過的題目（S001）：
- 不平衡猜想（Kozerenko–Skochko）：2026-08 arXiv 2608.09191 已證明。
- Hajós 圈分解猜想：Heinrich–Natale–Streicher 2017 驗到 12 點；13 點要列舉近百億張 Euler 圖，而且是「∀ 分解」型，SAT 不好做。
- Sheehan 猜想（4-正則圖不會唯一 Hamilton）：Goedgebeur–Meersman–Zamfirescu 驗到 21 點。本執行緒的 CEGAR 原型（固定 Hamilton 圈、擋其他 Hamilton 圈、預加 k ≤ 5 的 k-opt 子句）17 點要 217 秒、每多一點慢 5～7 倍，放棄。
- 3-分解猜想：Zhang–Szeider（CP 2025）SAT 驗到 28 點。
- ChatGPT 建議的 Fan–Raspaud、Berge–Fulkerson、Barnette 都屬被大量計算的 snark／平面圖題；它建議沒有好題就暫停副線。Gemini 推 Tuza、Frankl 並閉集、Seymour 第二鄰域；後兩個是熱門題。

## 已知成果

**Tuza 猜想（1981）。** τ(G) ≤ 2ν(G)。已知（依 Gupta arXiv 2608.06538 的引言，S003，未逐篇核對原文）：mad(G) < 7 時成立（Puleo）、平面圖（Tuza）、treewidth ≤ 6、三角形可 3 著色、不含 K_{3,3} 細分（Krivelevich）、隨機圖；一般圖 τ ≤ (66/23)ν（Haxell）。Gupta 2026 宣稱 Δ ≤ 7 成立（電腦輔助、未審稿）。K4、K5 等號成立。

## 研究空白

**電腦驗證。** 在搜尋範圍內沒有找到「所有 n 點以內的圖都驗過」的發表紀錄（S002）。但 9～10 點的暴力列舉是常規計算，很可能有人做過沒發表；Gupta 的論文把所有 7 點標號圖當成引理檢查過。所以本紀錄**不宣稱新**。

## 查詢紀錄

見 `search_evidence.jsonl`（S001 選題、S002 Tuza 電腦驗證、S003 已知成果）。

**限制。** 沒查 MathSciNet／zbMATH；Wikipedia 頁抓取失敗；Puleo 等原文沒讀。
