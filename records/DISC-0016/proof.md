# DISC-0016 證明：A085588 的週期整除 2^D(2^s − 1)

## 敘述

環上 n 格的狀態 = 以 n 為週期的函數 f : ℤ → {0,1}。F = 規則 150 一步。n = 2^D·m（m 不必是奇數，只要下面條件成立），s 滿足 m | 2^s − 1 或 m | 2^s + 1。則

- **恆等式：** F^(2^D + 2^D(2^s−1)) = F^(2^D)（對每個環上狀態）。
- **推論：** 任何狀態（特別是一個 ON 細胞）的最終週期整除 2^D(2^s − 1)，而且最多 2^D 步就進入週期。取 m 奇數、s = A309786(n)，就是 A085588(n) | 2^A007814(n)·(2^A309786(n) − 1)。

## 證明

1. **Frobenius。** 定義 G_a f(i) = f(i−a) xor f(i) xor f(i+a)，F = G_1。G_a 做兩次：f(i±a) 各出現兩次、f(i) 三次，抵銷後 G_a G_a = G_{2a}（`spread_spread`）。歸納得 F^(2^j) = G_{2^j}（`iter_pow_two`）。也就是 GF(2) 上 (x⁻¹+1+x)^(2^j) = x^(−2^j)+1+x^(2^j)。
2. **模 n。** 2^D + 2^D(2^s−1) = 2^(D+s)。若 2^s = 1 + mc，則 2^(D+s) = 2^D + c·n；若 2^s = mc − 1，則 2^(D+s) = −2^D + c·n。在週期 n 的 f 上，G_a 只看 ±a mod n（G_a = G_{−a}），所以 G_{2^(D+s)} f = G_{2^D} f（`spread_congr`、`iter_identity`）。
3. **週期整除。** 設 p 是最終週期（最小 p > 0 使 F^(k+p)f = F^k f 對某個 k）。取 K 夠大，F^(K+p) = F^K、F^(K+P) = F^K（P = 2^D(2^s−1)）。令 r = P mod p，則 F^(K+r) = F^(K+r+(P÷p)p) = F^(K+P) = F^K；若 r > 0 就和 p 最小矛盾，所以 p | P（`period_dvd`、`a085588_dvd`、`any_state_dvd`）。

## 條目原句寫反了

原句說 2^D(2^s − 1) 整除 a(n)。反例：n = 4，a(4) = 2，P = 4；n = 13，a(13) = 21，P = 63。條目自己列的「a(n) ≠ P 的 n」就是原句失敗的 n（b-file 共 174 個）。正確方向是 a(n) | P，上面已證。

## 第 2 條（a(n) = n ⇒ n ∈ A115770）只有部分結果

- 由上面定理，a(n) = n 時 m = n 的奇數部分 | 2^s − 1（n | 2^D(2^s − 1)）。所以 m | 2^s − 1，也就是 2 對 m 的乘法階 = s（−1 不是 2 的次方 mod m）。
- n = 2^i(2^j − 1)、j ≥ 3 一定在 A115770：k = 2^j − 1 時無進位乘法 11 ⊗ k = k ⊕ 2k ⊕ 8k，位元集合 {0, j} ⊕ {3, …, j+2} = {0} ∪ {3, …, j+2} \ {j}，值 = 1 + (2^(j+3) − 8) − 2^j = 7k；乘 2^i 兩邊都乘 2^i。
- n ≤ 1000 中 a(n) = n 的 n 全是這種形式（S003）。所以「a(n) = n ⇒ m 是梅森數 2^j − 1」足以推出第 2 條（不是等價：A115770 也有非梅森形式的數，如 455、903、910）。這一步本紀錄**沒證**，保持 OPEN。另：條目說反方向第一個例外是 445，但 445 不在 A115770，應是 455（a(455) = 4095）。

## 定理對照

| 敘述 | Lean 定理 | 檔案 |
|---|---|---|
| G_a G_a = G_{2a} | `Discovery.A085588Period.spread_spread` | `lean/Discovery/A085588Period.lean` |
| F^(2^j) = G_{2^j} | `Discovery.A085588Period.iter_pow_two` | 同上 |
| 週期函數上 G 只看 ±a mod n | `Discovery.A085588Period.spread_congr` | 同上 |
| F^(2^D+P) = F^(2^D) | `Discovery.A085588Period.iter_identity` | 同上 |
| 最終週期整除任何「回到原狀」的步數 | `Discovery.A085588Period.period_dvd` | 同上 |
| A085588(n) \| 2^D(2^s−1) | `Discovery.A085588Period.a085588_dvd` | 同上 |
| 任何狀態皆然 | `Discovery.A085588Period.any_state_dvd` | 同上 |

## 編譯結果

Lean 4.15.0，只用 core（無 Mathlib、無 `native_decide`），本機 `lean` 編譯 0 錯誤；`#print axioms a085588_dvd` = [propext, Quot.sound]。

## 敘述差異

- OEIS 的環是 n 個格子；Lean 用以 n 為週期的 ℤ → Bool，兩者一一對應，F 也對應。
- Lean 的 `EventualPeriod` = 最小 p > 0 使某個 k 起 F^(k+p) = F^k，就是條目名稱的「eventual period」。
- Lean 的定理對任意 D、m、s 成立（m 不必奇、s 不必最小）；套到條目時取 m 奇數、s = A309786(n)。實驗確認 s 的算法（最小 s 使 2^s ≡ ±1 mod m）與 A309786 的 DATA 前幾項一致：n = 5、7、9、11、13 得 2、3、3、5、6。
