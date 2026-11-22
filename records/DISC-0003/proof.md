# DISC-0003 proof.md

作者：orchestrator（proof 角色）。檔案：`lean/Discovery/Consecutive.lean`（Lean 4.15.0 + Mathlib v4.15.0）。

## 定理對照

定義（Lean）：
- `apSum D a k = ∑ i ∈ range k, (a + D * i)`，即 a + (a+D) + … + (a+(k−1)D)。
- `reps D N = {(a, k) ∈ [1, N] × [1, N] : apSum D a k = N}`。`mem_reps` 證明 `(a,k) ∈ reps D N ↔ 1 ≤ a ∧ 1 ≤ k ∧ apSum D a k = N`，所以 [1, N] 的上界不會漏解。
- `oddDivisors N = N.divisors.filter Odd`（`Nat.divisors 0 = ∅`）。
- `repsTwoLe N = (reps 1 N).filter (2 ≤ k)`；`smallDivisors N = N.divisors.filter (d * d ≤ N)`。

| 猜想 | Lean 定理 | 白話 | 與原猜想比對（定義／假設／量詞／結論） |
|---|---|---|---|
| H1 | `Discovery.Consecutive.card_reps_one` | 對所有 N：`(reps 1 N).card = (oddDivisors N).card` | 定義相同（首項 ≥ 1、項數 ≥ 1、單項算一種）；無額外假設；量詞為所有 ℕ（含 N = 0，兩邊皆 0，比原猜想更廣）；結論相同 |
| H2a | `Discovery.Consecutive.card_reps_one_two_le` | N ≥ 1 時，`(repsTwoLe N).card = (oddDivisors N).card - 1` | 相同；假設 N ≥ 1 與原猜想一致；ℕ 減法在此不截斷，因為 1 永遠是奇因數 |
| H2b | `Discovery.Consecutive.repsTwoLe_eq_empty_iff` | N ≥ 1 時，`repsTwoLe N = ∅ ↔ ∃ m, N = 2 ^ m` | 相同（「沒有 ≥2 項寫法」寫成集合為空） |
| H4（前半） | `Discovery.Consecutive.card_reps_two` | 對所有 N：`(reps 2 N).card = (smallDivisors N).card` | 只證了 R_2(N) = #{d ∣ N : d² ≤ N}；「= ⌈τ(N)/2⌉」那半**沒有形式化** |
| 輔助 | `Discovery.Consecutive.two_mul_apSum` | `2·apSum D a k + D·k = k·(2a + D·k)` | 求和公式，無減法 |
| 輔助 | `Discovery.Consecutive.mem_reps`、`mem_reps_one`、`mem_oddDivisors` | 成員判準 | — |

H1 的證明是明確的雙射（`Finset.card_nbij'`）：(a, k) ↦ k 與 2a + k − 1 之中奇數的那個；反方向奇因數 d ↦ 若 d < 2N/d 則 (k, a) = (d, (2N/d − d + 1)/2)，否則 (k, a) = (2N/d, (d − 2N/d + 1)/2)。

H3、H5 沒有 Lean 證明，只有範圍內檢查。H6 被反例推翻，不需證明。

## 編譯結果

- 雲端開發環境：直接安裝 Lean 4.15.0，本地從原始碼編譯所需的 Mathlib 子集（Mathlib 快取伺服器被 proxy 擋），`lake build Discovery.Consecutive` 成功，無錯誤、無警告。本地公理檢查（`AxiomCheck.lean` 只匯入 `Discovery.Consecutive`）：所有定理只用 `propext`、`Quot.sound`、`Classical.choice`。
- CI：GitHub Actions `lean` 工作在 commit `4668a62` 成功（https://github.com/Bonnie9981/Project-Discovery/actions/runs/45003700687 ，job 137150524481）：編譯整個 `Discovery`、`sorry/admit/axiom` 檢查通過、AxiomCheck 列出 THEOREM_COUNT 20，`Discovery.Consecutive.*` 全部只用 `propext`、`Quot.sound`、`Classical.choice`；`lean_decls` 回報「20 theorems axiom-checked, 13 in source, 0 problems」。之後的 commit 沒有改 Lean 檔，CI 會再跑一次確認。
- 檔案中沒有 `sorry`、`admit`、`axiom`。

## 敘述差異

1. Lean 的量詞含 N = 0（兩邊都是 0），原猜想只講 N ≥ 1。比原猜想更強，不影響。
2. 「至少兩項」在 Lean 中是 `reps 1 N` 上再過濾 `2 ≤ k`，與 Python 的 `k_ok = k >= 2` 相同。
3. H4 只形式化了「d² ≤ N 的因數個數」那半；與 ⌈τ(N)/2⌉ 的等式只有範圍內檢查。
4. `oddDivisors` 用 Mathlib 的 `Nat.divisors`，與 Python 的「奇因數個數」定義相同（正因數）。
