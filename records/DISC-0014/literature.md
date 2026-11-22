# DISC-0014 文獻

## 問題

OEIS A071052（規則 150 三角形 A071036 第 n 列的 0 個數，offset 0）FORMULA 欄：「a(2n) = a(n) + 2n (conjectured). - Ralf Stephan, Mar 03 2004」。條目只有這一行公式，沒有證明或出處（S001，2026-11-22 讀全文）。

規格：第 n 列是規則 150 從單一 ON 細胞出發第 n 代的 2n+1 格（位置 −n..n），A071053 是同一列的 1 個數，所以 A071052(n) = 2n+1 − A071053(n)。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| A071053(2n) = A071053(n)；a(2n+1) = a(n) + 2a(⌊n/2⌋) | A071053 FORMULA，Peter J. Taylor 2020（S002） | 加上 A071052 = 2n+1 − A071053 就直接推出猜想；條目內寫成公式，沒附證明 |
| A071053(n) = (1+x+x²)^n mod 2 的奇數係數個數 | A071053 COMMENTS，Wolfram 1983（Rev. Mod. Phys.） | 標準事實；(1+x+x²)^(2n) ≡ (1+x²+x⁴)^n (mod 2) 即得奇數係數個數不變 |
| A071053 是 Jacobsthal 數的 Run Length Transform | A071053，Sillke、Sloane 2014；Ekhad–Sloane–Zeilberger 2015 | 包含 a(2n) = a(n)（二進位尾端補 0 不改 1 的串） |

## 研究空白

A071052 的 FORMULA 仍標「conjectured」（2004 年至今），但它是 A071053(2n) = A071053(n) 的一行推論，而後者是 GF(2) 上 Frobenius 的標準事實。空白只在 OEIS 條目沒更新，不是數學上的。本紀錄的價值：把「conjectured」改成有證明（附 Lean 檢查）並交叉引用 A071053。

## 查詢紀錄

- S001：OEIS A071052 全文（claude-in-chrome，/internal 格式）。
- S002：OEIS A071053 全文（同上）。
- 沒查：arXiv、MathSciNet；因為結果是已知事實的推論，不宣稱新。
