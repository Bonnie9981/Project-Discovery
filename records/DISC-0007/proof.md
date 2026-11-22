# DISC-0007 證明紀錄（Proof agent，M1.4）

對象：DISC-0004 C02（H2′ 形式）的完整「當且僅當」刻畫。紙本證明見 `records/DISC-0006/proof.md` 第 C02 節、`critic.md` 第 3 點、`review.md` B 節。

狀態：**Lean 已完整證明 `c02_iff`（兩個方向）。本機逐檔編譯通過；CI `lean` 工作尚未執行（未 push），依規則要等 CI 通過才算「已證明」。**

## 定理對照

Lean 檔案：`lean/Discovery/RadSigmaIff.lean`（新檔，命名空間 `Discovery.RadSigma`，import `Discovery.RadSigma`、`Discovery.SigmaOdd`、`Mathlib.NumberTheory.Multiplicity`、`Mathlib.Data.Nat.Factorization.Basic`）。`lean/Discovery.lean` 已加上 `import Discovery.RadSigmaIff`。`lean/Discovery/RadSigma.lean` 只改了檔頭註解（指向新檔），內容未改。

σ 是 Mathlib 的 `ArithmeticFunction.sigma 1`（檔內寫 `σ 1`）；rad 是 `RadSigma.lean` 既有定義 `rad n = ∏ p ∈ n.primeFactors, p`。

### 主定理

| 猜想 | Lean 定理 | 檔案 |
|---|---|---|
| C02 / H2′：n ≥ 1 時，rad(σ n) = σ(rad n) ⇔（n 與 σ(n) 都無平方因子）或（n = 2^a·p，p 奇質數，a 奇且 a ≥ 3，p+1 無平方因子，3 ∤ p+1，rad(2^(a+1) − 1) ∣ 3(p+1)） | `Discovery.RadSigma.c02_iff` | `lean/Discovery/RadSigmaIff.lean` |

Lean 敘述（逐字）：

```lean
theorem c02_iff (n : ℕ) (hn : 0 < n) :
    rad (σ 1 n) = σ 1 (rad n) ↔
      (Squarefree n ∧ Squarefree (σ 1 n)) ∨
        ∃ a p, n = 2 ^ a * p ∧ p.Prime ∧ Odd p ∧ Odd a ∧ 3 ≤ a ∧ Squarefree (p + 1) ∧
          ¬ 3 ∣ (p + 1) ∧ rad (2 ^ (a + 1) - 1) ∣ 3 * (p + 1)
```

與任務指定的敘述完全相同（`2^(a+1) - 1` 是自然數減法，a ≥ 0 時 2^(a+1) ≥ 2，沒有截斷問題）。

### 證明的主要步驟與對應引理

| 數學步驟 | Lean 定理 |
|---|---|
| rad x = y ⇔ y 無平方因子且 x、y 質因數集合相同 | `rad_eq_iff`（輔：`primeFactors_rad`） |
| x 的質因數都整除 y ⇒ rad x ∣ y；質數 q ∣ x ⇒ q ∣ rad x | `rad_dvd_of_primeFactors_subset`、`prime_dvd_rad` |
| rad(p^k) = p；rad(2^a·p^b) = 2p（a, b ≥ 1，p ≠ 2） | `rad_prime_pow`、`rad_two_pow_mul_prime_pow` |
| σ(p) = p+1；σ(2p) = 3(p+1) | `sigma_prime'`、`sigma_two_mul_prime` |
| Σ_{i<2m} p^i = (p+1)·Σ_{i<m} (p²)^i | `sum_range_two_mul` |
| 3^k mod 8 ∈ {1, 3} | `pow_three_mod_eight` |
| 3 ∣ 2^(a+1) − 1 ⇔ a 奇 | `three_dvd_mersenne_iff`（輔：`three_dvd_four_pow_sub_one`） |
| n = 2^a：2^(a+1) − 1 的質因數只有 3 ⇒ a ≤ 1（mod 8 論證） | `mersenne_primeFactors_three` |
| m ≥ 2、q ≥ 2 ⇒ m < Σ_{i<m} q^i | `lt_geom_sum` |
| **LTE 核心**：p 奇質數、m ≥ 2，C = Σ_{i<m} p^{2i} 的質因數不可能全都整除 3(p+1)（對每個質數 r ∣ C 證 v_r(C) = v_r(m)，r 奇用 `padicValNat.pow_sub_pow`，r = 2 用 `padicValNat.pow_two_sub_pow`；得 C ∣ m，與 C > m 矛盾） | `lte_core`（輔：`padicValNat_mul'`、`padicValNat_two_two`） |
| n = 2^a·p^b（p 奇質數，b ≥ 1）的正向分析：b 奇 → b = 1（LTE）→ a = 0 得 n = p；a ≥ 1 得 3 ∤ p+1、p+1 無平方因子、a 奇；a = 1 得 n = 2p（第一種情形），a ≥ 3 得第二種情形 | `c02_forward_prime_pow` |
| σ(n) ≠ 0（n > 0） | `sigma_pos''` |
| 主定理：正向先寫 n = 2^a·m（m 奇），m = 1 時 n = 1 或 n = 2（`mersenne_primeFactors_three`）；m > 1 時用既有的 `odd_prime_factor_unique` 得 m = p^b，交給 `c02_forward_prime_pow`。反向：第一種情形用既有的 `c02b`；第二種情形直接算 rad n = 2p、σ(rad n) = 3(p+1)、σ(n) = (2^(a+1) − 1)(p+1)，再用 `rad_eq_iff` | `c02_iff` |

也用到既有定理：`RadSigma.lean` 的 `squarefree_rad`、`c02b`、`c02_of_squarefree`、`squarefree_sigma_rad`、`odd_prime_factor_unique`；`SigmaOdd.lean` 的 `sigma_two_pow`、`sigma_two_pow_mul`、`sum_range_pow_mod_two`、`sigma_pos'`。

紙本論證與 DISC-0006 proof.md 一致，只有兩處寫法不同：
- n = 2^a 的情形用 mod 8（3^k ≢ 7），不是 LTE。
- LTE 核心裡 r = 3 的情形不必另外假設 p ≠ 3：若 r ∣ C 則 r ∤ p（因為 C ≡ 1 mod p），所以 r = 3 時 3 ∤ p，於是 3 ∣ p² − 1。這同時涵蓋 a = 0（σ(rad n) = p+1）與 a ≥ 1（σ(rad n) = 3(p+1)）兩種情形，因為兩者都整除 3(p+1)。

## 編譯結果

**CI：尚未執行（本工作未 commit／push）。依規則，待 CI `lean` 工作通過後才算「已證明」。CI 連結：待補。**

**本機已編譯（非 CI）。** 環境：官方 Lean 4.15.0 工具鏈 + 從原始碼建的 Mathlib v4.15.0（與 `lean/lakefile.toml` 的 `rev = "v4.15.0"` 相同；前一個 proof agent 已建好的部分之外，這次另外 `lake build Mathlib.NumberTheory.Multiplicity Mathlib.Data.Nat.Factorization.Basic Mathlib.Tactic.IntervalCases`，輸出 `✔ [1007/1007] Built Mathlib.NumberTheory.Multiplicity` / `Build completed successfully.`）。

步驟：
1. 用 `lake env lean --root=<repo>/lean -o …` 把 `Discovery/RadSigma.lean`、`Discovery/SigmaOdd.lean` 編成 .olean（0 錯誤）。
2. `lake env lean --root=<repo>/lean lean/Discovery/RadSigmaIff.lean`：**0 錯誤、0 警告**，約 5 秒。
3. 把 `lean/AxiomCheck.lean` 的 `#check_discovery_axioms` 附在 `RadSigmaIff.lean` 後面編譯（環境含 `Discovery.RadSigma`、`Discovery.SigmaOdd`、`Discovery.RadSigmaIff`）：結束碼 0，`THEOREM_COUNT 49`，全部只用 `propext`、`Classical.choice`、`Quot.sound`。其中：
   ```
   AXIOMS Discovery.RadSigma.c02_iff: [propext, Quot.sound, Classical.choice]
   AXIOMS Discovery.RadSigma.c02_forward_prime_pow: [propext, Quot.sound, Classical.choice]
   AXIOMS Discovery.RadSigma.lte_core: [propext, Quot.sound, Classical.choice]
   AXIOMS Discovery.RadSigma.mersenne_primeFactors_three: [propext, Quot.sound, Classical.choice]
   ```
   沒有 `sorryAx`，沒有 `Lean.ofReduceBool`（即沒有 `native_decide`）。
4. `python3 -m discovery.lean_decls` 對上述輸出：`RadSigma.lean`、`SigmaOdd.lean`、`RadSigmaIff.lean` 的原始碼定理全部出現在公理檢查輸出中（其餘 FAIL 只來自本機沒有編譯的 Consecutive／R001／Rule54／Smoke）。
5. `grep -nE '\b(sorry|admit|native_decide)\b|^\s*axiom ' lean/Discovery/RadSigmaIff.lean`：無輸出。

**未做的事：** 沒有在 repo 的 `lean/` 專案內跑完整 `lake build`／`lake env lean AxiomCheck.lean`（`Smoke.lean` 等 import 整個 `Mathlib`，本機沒有完整 Mathlib 建置，cache 主機被代理擋下）。新檔使用的 Mathlib 模組（`Mathlib.NumberTheory.Multiplicity`）在 CI 的 Mathlib cache 中，新定理都在 `Discovery.RadSigma` 命名空間，與其他 Discovery 檔不衝突；但仍以 CI 為準。

### 數值核對（Lean 敘述 ↔ 數值）

`iffcheck.py`（在本機 scratchpad，未進 repo；自寫，最小質因數篩，不 import repo）對 1 ≤ n ≤ 10⁶ 逐一比較「rad(σ n) = σ(rad n)」與 Lean 右側敘述（逐字照 `c02_iff` 的條件實作，第二種情形取 a = v₂(n)、p = n/2^a）：

```
N 1000000 solutions 39234 mismatch 0 second-branch 671 [416, 872, 1832, 3272, 5672, 5792, 6152, 6632, 8072, 8552]
```

## 敘述差異

- **範圍**：原文對 n ≥ 1；Lean 有假設 `0 < n`。n = 0 時 Lean 中 σ 1 0 = 0、rad 0 = 1，不在原文範圍內。
- **rad**：`rad n = ∏ p ∈ n.primeFactors, p`，n ≥ 1 時就是通常的 radical（rad 1 = 1）。
- **自然數減法**：`2 ^ (a + 1) - 1` 是 ℕ 減法，因為 2^(a+1) ≥ 2，與整數意義相同。
- **H2′ 的條件檢查（任務要求核對）**：
  - `3 ∤ p + 1` 是必要條件：解必須使 σ(rad n) = 3(p+1) 無平方因子，故 3 與 p+1 互質。Lean 正向由 `Nat.squarefree_mul_iff` 推出。它不能換成「p ≠ 3」：p ≡ 2 (mod 3) 時 3 ∣ p+1 但 p ≠ 3。
  - `Odd a` 的推導正確：3 ∤ p+1，而 3 必須整除 σ(n) = (2^(a+1) − 1)(p+1)，所以 3 ∣ 2^(a+1) − 1 ⇔ a 奇（`three_dvd_mersenne_iff`）。
  - 有兩個條件**多餘但無害**（保留它們不影響等價，敘述照任務原文）：
    1. `Odd p`：p = 2 時 p+1 = 3，與 `¬ 3 ∣ (p+1)` 矛盾，所以由其他條件可推出。
    2. `3 ≤ a`：a = 1 的 2p 在反方向也是解（反方向的證明沒用到 `3 ≤ a`），而且正向把 a = 1 歸入第一種情形（n = 2p、σ(n) = 3(p+1) 都無平方因子）。拿掉 `3 ≤ a` 後兩種情形會重疊，但等價式仍然成立。
    
    數值上把這兩個條件都拿掉（只留 p 質數、a 奇、p+1 無平方因子、3 ∤ p+1、rad(2^(a+1) − 1) ∣ 3(p+1)）重跑到 10⁶，同樣 `mismatch 0`（第二種情形增為 9943 個，多出的都是 a = 1 的 2p）。
  - 沒有發現 H2′ 寫錯的條件。
- **卡住的引理**：無。`c02_iff` 兩個方向都完整證明，檔案中沒有 `sorry`／`admit`／`native_decide`／新 `axiom`。
