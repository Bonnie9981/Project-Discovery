# DISC-0008 文獻查證

查詢日期：2026-11-22。管道：使用者的 Chrome。每筆查詢記在 `search_evidence.jsonl`（DISC-0008-S001～S005）。

## 問題

R3-L01：初等細胞自動機規則 26，寬度 w 的環，單一種子出發。w 為奇數且 ≥ 3 時，暫態是 0，週期恰為 w·2^⌊log₂ w⌋。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| 規則 26 在寬度 n 的環上、單一種子的週期序列 | OEIS A334504（Sloane 2020；資料由 Klee、Wang、Dobbelaere 計算） | 序列本身已知 |
| 「It seems that a(2n+1) = (2n+1)·2^A070939(n)」，以及 a(2n+2) = A268754(n) | A334504 的 FORMULA 欄（Zabolotskii，2024 年 9 月） | **公式已被提出，但只是猜想。** w = 2n+1 時 A070939(n) = ⌊log₂ n⌋ + 1 = ⌊log₂ w⌋，和 R3-L01 相同。條目沒有證明 |
| A268754：B1/S 規則下 n×1 振盪器的週期（等於零邊界規則 90） | OEIS A268754 | 偶數寬度那一半猜想的另一邊；CROSSREFS 也只寫「Seems to be」 |
| 規則 26 從單一種子在無限直線上畫出的是規則 90 的 Sierpiński 圖樣（Pascal 三角形 mod 2） | Wolfram《A New Kind of Science》、Wolfram Atlas（critic 提出，本輪未上網核對出處） | **已知事實**：我們的引理 1 在無限直線上的版本是已知的。可能新的部分只剩「環上的邊界分析加上 Lucas 收尾」 |
| 加法型細胞自動機在環上的週期理論 | Martin、Odlyzko、Wolfram 1984 | 背景：規則 90 的週期。規則 26 不是加法規則，不能直接套用 |

## 研究空白

- 在查過的範圍內（OEIS、arXiv、OpenAlex），**沒有找到** A334504 奇數項公式的證明。
- 所以：公式本身已有人以猜想形式提出（record.json 記為 `PARTIAL_MATCH`）；證明是 `NO_MATCH_IN_SCOPE`。證明的核心想法（Pascal 三角形 mod 2）是已知的，可能新的只是把它用到環上並算出確切週期。
- OEIS 的公式只對 n ≥ 1 成立：代入 n = 0 會得到 a(1) = 2，實際是 1。
- 偶數項的猜想 a(2n+2) = A268754(n) 本輪沒有證明（紙上有思路，未完成）。

## 查詢紀錄

| ID | 平台 | 查詢 | 結果 |
|---|---|---|---|
| S001 | OEIS | P₂₆ 的奇數項 6, 20, 28, 72, … | 查無（OEIS 收的是全部 n） |
| S002 | OEIS | P₂₆ 全序列 1, 1, 6, 1, 20, 2, … | A334504，FORMULA 欄有猜想 |
| S003 | OEIS | A268754 條目 | 零邊界規則 90 週期；交叉引用只寫「Seems to be」 |
| S004 | arXiv | "rule 26" AND cellular | 1 筆，無關（Fukś 2013，密度回應） |
| S005 | OpenAlex | elementary cellular automaton cyclic boundary period single cell rule 26 | 前 8 筆沒有規則 26 環上週期的研究 |

**還沒查：** Math Fun 郵件列表（Klee 2020 的原貼文）、MathSciNet、zbMATH、Google Scholar。數學界可能有人證過但沒回報到 OEIS。
