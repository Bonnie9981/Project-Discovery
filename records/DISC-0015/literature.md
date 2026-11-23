# DISC-0015 文獻

## 問題

規則 54 從單一 ON 細胞出發，第 n 列長什麼樣？OEIS 有兩條條目把它寫成數列，FORMULA 欄的公式都標「Conjecture(s)」或「conjectured」，沒有證明（S001、S002，2026-11-23 讀全文）：

- **A118109**（第 n 列讀成 0/1 數字的十進位數）：Colin Barker 2015/2019 的遞迴 a(n) = 10001*a(n-2) - 10000*a(n-4) 與生成函數；Karl V. Keller, Jr. 2021 的 a(n) = floor((10000+1100*(n mod 2))*100^n/9999)。
- **A265225**（第 0..n 列 ON 細胞總數）：Barker 的封閉式 (n+1)*(2n-(-1)^n+5)/4、5 階遞迴、生成函數；Wesley Ivan Hurt 2016 的 n+1+(n+1)*floor((n+1)/2)；Matej Veselovac 2020 的 A093353(n)+n+1；COMMENTS 有 Ivan N. Ianakiev 2019 的「It seems」，原文（S002 逐字）：「Take the first 2n positive integers and choose n of them such that their sum: a) is divisible by n, and b) is minimal. It seems their sum equals a(n).」A093353 的定義（S003 逐字）：a(n) = (n + (n mod 2))*(n + 1)/2。

協調者轉來的題目是 A118109/A118110。A118110 其實是規則 150（不是規則 54 的 0 個數），條目沒有猜想，所以改做 A118109 和同一個規則 54 的 A265225。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| 規則 54 單細胞圖樣 | Wolfram, NKS p.55；A071030 | 看得出週期 4 的列，但沒寫證明 |
| A118108（同一列的十進位值）a(n) = 7*(4^(n+1)-1)/15 或 (4^(n+2)-1)/15 | A118108 FORMULA，沒有標 conjecture | 等於已經默認列的形狀；A118109 只是換成十進位數字 |
| Munarini 2021（反正則圖的拓樸指標） | A265225 LINKS | 同一串數字出現在別處，沒讀，不影響（我們證的是 CA 定義） |

## 研究空白

數學上是習題：列的封閉形一眼看得出來，歸納一步就證完。空白只在 OEIS 條目仍標猜想。另外 Ianakiev 的註解差了一個索引（應是 a(n-1)），可以順手指正。

## 查詢紀錄

- S001：OEIS A118108、A118109、A118110 全文（claude-in-chrome，fmt=text）。
- S002：OEIS A265225 全文；搜尋 `"rule 54"` 前 60 筆，列出有 conjectur/seems/appears 的條目，只有 A118109、A265225。
- S003：OEIS A093353 條目（Veselovac 公式用到的定義）。
- 沒查：arXiv、MathSciNet；不宣稱新。
