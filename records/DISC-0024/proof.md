# DISC-0024 證明

這筆紀錄沒有 Lean 定理。沒有找到反例，所以沒有要在 Lean 裡重驗的圖；UNSAT 的部分靠 DRAT 證書加自寫 RUP 檢查器。

## 定理對照

無。

## 編譯結果

不適用（沒有 Lean）。證書檢查結果見 `experiment.md`。

## 敘述差異

- 證書證明的是「最終 CNF 不可滿足」。CNF 到猜想之間靠：(1) INT、LEX 剪枝不漏（`docs/TUZASAT.md` 的論證，加 n ≤ 6 的圖譜比對）；(2) `check.py` 照規格重建基本子句，並用 JSON 見證逐條確認 P、C 擋子句合法；(3) k 的範圍 1..kmax(n) 的論證（τ ≤ ⌊m/2⌋）。
- RUP 檢查器是 `discovery/egsat/check.py` 自寫的那一個（DISC-0022 審過），不是形式化驗證過的工具。
