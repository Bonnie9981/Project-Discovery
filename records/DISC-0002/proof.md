# DISC-0002 proof.md

作者：orchestrator（主執行緒扮演 proof 角色）

## 定理對照

| 猜想 | Lean 定理 | 檔案 |
|---|---|---|
| H1 | `Discovery.R001.boundary_eq`：∀ p ≥ 1, (p−1)² + (p−1) + p = p² | `lean/Discovery/R001.lean` |
| H1 | `Discovery.R001.boundary_not_prime`：∀ p ≥ 2, ¬ Nat.Prime ((p−1)² + (p−1) + p) | 同上 |
| H2 | `Discovery.R001.euler41`：∀ n < 40, Nat.Prime (n² + n + 41) | 同上 |
| H3 | `Discovery.R001.euler41_fails`：¬ Nat.Prime (40² + 40 + 41) | 同上 |
| H4、H5 | 未形式化（一般情形需要類數 1 定理，Mathlib 目前沒有現成可用的版本，本次未查證） | — |

## 編譯結果

- 環境：Lean `v4.15.0`，Mathlib `v4.15.0`（commit `9837ca9d65`），依賴版本鎖定在 `lean/lake-manifest.json`。
- 開發用的雲端環境連不到 Lean 下載站，所以編譯在 GitHub Actions 的 `lean` 工作上進行。
- 第一次編譯失敗：`unknown constant 'Nat.Prime.pow_not_prime'`（猜錯了 Mathlib 的引理名稱）。改用 `Nat.prime_mul_iff` 加 `omega` 直接證明後通過。
- `Build completed successfully`，且 `#print axioms` 只用到標準公理：

```
'Discovery.R001.boundary_eq' depends on axioms: [propext, Quot.sound]
'Discovery.R001.boundary_not_prime' depends on axioms: [propext, Quot.sound]
'Discovery.R001.euler41' depends on axioms: [propext, Classical.choice, Quot.sound]
'Discovery.R001.euler41_fails' depends on axioms: [propext]
```

- 沒有 `sorry`、`admit`、自訂 `axiom`（CI 檢查）。

## 敘述差異

- H1 的 Lean 版本用自然數 ℕ。自然數減法會截斷，但 `boundary_eq` 要求 p ≥ 1，此時 p−1 是真正的減法，不受影響（critic 也檢查過）。
- H1 括號裡的「範圍 n ≤ p−2 已是最長」是由 `boundary_not_prime` 直接推得的口語說法，沒有另外定義 Q_p 來形式化。
- H2 寫成 `∀ n < 40`，與「0 ≤ n ≤ 39」對 ℕ 等價。
