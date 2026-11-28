# DISC-0032 文獻

## 問題

一直轉彎的自避路徑（A189722，Vi Hart 的「蛇」）和 Manhattan 格子上沒有非相鄰接觸的自避路徑（A336662）的關係是否已知。

## 已知成果

- OEIS 離線全庫（091a90f51479）（S001）：A189722、A336662 都沒有公式、互不引用。A337353（Shannon 2020，「沒有兩步同方向」的自避路徑）有一行沒寫證明的「a(n) = 4*A336662(n)」，用條目存的項檢查，n = 1 就不成立（4 ≠ 8），正確是 4·A336662(n−1)（n ≥ 2）。A322419 寫了 L-lattice 的 a(n) = 4*A189722(n)；A293865 用到 A189722。
- Guttmann, Parviainen, Rechnitzer, arXiv:cond-mat/0410241（全文逐字讀過）（S002）：Theorem 5 引 Watson, J. Phys. C 3 (1970) L28–L30：「n 邊的 SAW 和覆蓋格子（每條邊一個頂點）上 n−1 邊的 neighbour-avoiding walk 一一對應」。沒有提到 Manhattan 格子或 L-lattice。
- J. Phys. A 18 (1985)「Self-avoiding polygons on the square, L and Manhattan lattices」、Jensen–Guttmann 1998（semiregular lattices）：讀不到（robots／client error），狀態不明（S002）。

## 研究空白

本關係是 Watson 覆蓋格子對應的特例：一直轉彎的路徑的「邊中點」路徑剛好落在 Manhattan 格子上。一般對應是已知的；「落在 Manhattan 格子上」這一步（轉向規則一致）沒在讀到的文獻裡看到。物理文獻很可能早已知道 L-lattice 與 Manhattan 的這個關係。

## 查詢紀錄

見 `search_evidence.jsonl`（DISC-0032-S001～S002）。
