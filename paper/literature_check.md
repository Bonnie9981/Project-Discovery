# 文獻補查紀錄（2026-11-22）

目的：補完 `spec_audit.md` 的文獻待辦。全部用使用者的 Chrome 或 web-fetch 讀取，讀到的內容是資料，不是指令。

| # | 管道 | 查詢 / 文件 | 結果 |
|---|---|---|---|
| L1 | OEIS 文字版 | A334504 | 名稱「Eventual period of a single cell in rule 26 cellular automaton in a cyclic universe of width n」；猜想署名 _Andrei Zabolotskii_，Sep 04 2024，另寫 a(2n+1) = A363121(n+1)/2；%D：Bradley Klee，Math Fun 郵件列表，2020-04-26 |
| L2 | OEIS 文字版 | A268754 | Mathematica：三對角矩陣 `Abs[i-j]==1`、向量 e₁、GF(2) 最終週期；Python 同 `nstep`；%Y：偶數項恰為 A160657（Goucher 2019 修正）；A334504、A334507 只寫「Seems to be」 |
| L3 | OEIS 文字版 | A160657 | C. Neder 2019-01-11 的證明：B36/S125 的 2×4n 振盪器拆成矩形，角落像寬 n 的 Rule 90 帶子，單點種子，所以週期 = A268754(2n)。偶數證明的直接先例（機制不同） |
| L4 | OEIS 文字版 | A334507、A363121 | A334507 = 規則 122 的同類序列，無公式；A363121 是純數論序列（A116882 的本原項），和細胞自動機無關 |
| L5 | scispace PDF（web-fetch） | Martin–Odlyzko–Wolfram 1984 | 可讀第 1～4D 節（逐字），4E 之後缺；讀到的部分沒有規則 18 化約、沒有規則 26、沒有零邊界 ↔ 循環邊界的反射對應。Project Euclid 版本被機器人防護擋住 |
| L6 | ar5iv（web-fetch） | Tadaki 1993, cond-mat/9305012 | 零邊界（Dirichlet）Rule 90、150 的軌道；前半逐字讀到沒有 2n+2 反射對應、沒有規則 26；後半只有摘要，未核實 |
| L7 | zbMATH Open | `"rule 26" & cellular` | 1 筆：Fukś 2014 最小熵近似（無關） |
| L8 | zbMATH Open | `A334504` | 0 筆 |
| L9 | Google Scholar | `"rule 26" cellular automaton period cyclic` | 第一頁 10 筆，只看標題摘要：分類、符號動力學（Han–Chen–Wang 2010）、固定邊界（Mitra–Teodorescu 2016）等，沒有環上單點週期的證明 |
| L10 | Google Scholar | `A334504` | 無相關結果 |
| L11 | OpenAlex | `"rule 26" cellular automaton cyclic period`（全文） | 11 筆，前 10 筆標題都無關 |
| — | MathSciNet | — | 需要訂閱，無法查 |
| — | math-fun 存檔 | — | 沒有去找 |

結論：查詢範圍內仍沒有找到 A334504 兩個公式的證明。偶數那一半的方法在 OEIS A160657 有同類先例，論文已照實寫。
