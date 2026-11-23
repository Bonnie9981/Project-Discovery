# DISC-0019 證明

檔案：`lean/Discovery/CxBatch1.lean`（namespace `Discovery.CxBatch1`），已加進 `lean/Discovery.lean`。`lean/AxiomCheck.lean` 會自動走訪 `Discovery` 底下所有定理，不需要手動列名。

## 定理對照

| Lean 定理 | 數學敘述 |
|---|---|
| `Discovery.CxBatch1.powModAux_eq`（及 `Discovery.CxBatch1.mul_mod_mod'`、`Discovery.CxBatch1.pow_mod'`） | 二進位快速冪 `powModAux f b e m = b^e % m`（任意 fuel），從 DISC-0017 照抄 |
| `Discovery.CxBatch1.prime_61`、`Discovery.CxBatch1.prime_151`、`Discovery.CxBatch1.prime_331` | 61、151、331 是質數（`IsPrime p`：p ≥ 2 且沒有 2 ≤ d < p 整除 p） |
| `Discovery.CxBatch1.psp_N` | N = 3048841 時 2^(N−1) mod N = 1 |
| `Discovery.CxBatch1.psp_Q` | Q = 49981 時 2^(Q−1) mod Q = 1 |
| `Discovery.CxBatch1.factor_ge` | p ≥ 1 時 (m+1)p − m ≥ p |
| `Discovery.CxBatch1.small_div` | p < 146 且 p 整除 3048841 ⇒ p = 1 或 61 |
| `Discovery.CxBatch1.small_div2` | 121 ≤ a < 414、a 整除 49981、a ≡ 1 (mod 60) 的 a 不存在 |
| `Discovery.CxBatch1.not_coman_form` | 對所有自然數 p、m、k（m、k ≥ 1），p·((m+1)p−m)·((k+1)p−k) ≠ 3048841 |
| `Discovery.CxBatch1.a215944_counterexample` | H1 反例總整理：N = 3048841 = 61·151·331，三個因數都是質數，N 是 psp2；Q = 49981 = 151·331 < N 也是 psp2 且整除 N；N 不能寫成 p((m+1)p−m)((k+1)p−k)；N 不是 5461 的倍數 |
| `Discovery.CxBatch1.tri_two`、`Discovery.CxBatch1.expand`、`Discovery.CxBatch1.geo_pow` | 輔助：2·T(j) + j = j²；(1+m)^j = 1 + jm + T(j)m² + m³c；(1 + Sx)^t ≡ 1 (mod S) 的形式 |
| `Discovery.CxBatch1.a058128_weak_psp` | H2：對所有偶數 n ≥ 2，令 a = (n^n − n)/(n−1)²，則 (n−1)²·a = n^n − n（整除）且 n^a mod a = n mod a |
| `Discovery.CxBatch1.a058128_n4` | 檢查 n = 4：a = 28，4^28 mod 28 = 4 |
| `Discovery.CxBatch1.a218483_no_psp` | H3：對所有 n ≡ 15 (mod 40)，2^(n−1) mod n ≠ 1 |

逐項比對：
- H1：定義（psp2 = 合數且 2^(n−1) ≡ 1 mod n）—Lean 給出 N、Q 的同餘式和分解，合數性由分解直接看出；假設（三個質因數、被較小 psp2 整除）—由 `N = 61·151·331`、三個 `IsPrime`、`N % Q = 0`、`Q < N`、`psp_Q` 給出；量詞（「存在 p、m、k」的否定）—`not_coman_form` 對所有 p、m、k 量化；結論（也不是 5461(42k−13)）—以「不是 5461 的倍數」證明，更強。
- H2：定義 a(n) = (n^n − n)/(n−1)² 照條目原式，用自然數除法；量詞為所有偶數 n ≥ 2；結論 n^a ≡ n (mod a) 原樣。
- H3：量詞為所有 n ≡ 15 (mod 40)，結論比原猜想強（見下）。

證明想法：H1 先用三個因數都 ≥ p 得 p³ ≤ N，p ≤ 145，再枚舉得 p = 61，另外兩個因數 ≡ 1 (mod 60) 且 ≥ 121，但 49981 在 [121, 413] 的因數只有 151、331，都不 ≡ 1 (mod 60)。H2 照 Jianing Song 對 A343009 的方法：令 m = n − 1（奇數），由二階展開 n^m = 1 + m²S，S = 1 + m·u，所以 a = nS 且 a − 1 = m·t，於是 n^a = n·(n^m)^t = n·(1 + S·w) = n + a·w。不需要 gcd。H3：5 | n，n − 1 ≡ 2 (mod 4)，所以 2^(n−1) ≡ 4 (mod 5)，若 2^(n−1) ≡ 1 (mod n) 則 mod 5 也 ≡ 1，矛盾。

## 編譯結果

容器沒有 elan；照專案慣例下載 Lean 4.15.0 官方 linux release（`lean-4.15.0-linux.tar.zst`），用 pip `zstandard` 解壓，直接跑：

- `lean lean/Discovery/CxBatch1.lean`：無錯誤、無警告，約 3 秒。
- 另編成 `.olean` 後 `#print axioms`：`a215944_counterexample`、`a058128_weak_psp`、`a218483_no_psp`、`not_coman_form`、`psp_N` 只用 `[propext, Quot.sound]`；`a058128_n4`、`prime_331` 不依賴任何公理。
- `python -m discovery.lean_decls` 的 `theorems_in` 抓到本檔 19 個定理。
- 反向檢查（確認 `decide` 不是空洞通過）：把模數改成 3048843 的快速冪等式、把 `small_div` 結論改成只有 `p = 1`，兩者 `decide` 都報錯。
- 沒有 `sorry`、`admit`、`axiom`、`native_decide`，不用 Mathlib。`small_div`、`small_div2`、三個 `prime_*` 用 `set_option maxRecDepth 100000 in`（只是放寬遞迴深度，不影響可信度）。
- CI 的 `lean` 工作尚未跑（未推送）；以 CI 結果為準。

## 敘述差異

- 質數用自己定義的 `IsPrime`（試除到 p−1），不是 Mathlib 的 `Nat.Prime`；兩者等價，但本檔沒證這個等價。
- H1：Lean 不直接定義「psp2」，而是分別給出同餘式 2^(N−1) ≡ 1 和分解（顯示是合數）。「n = 5461(42k−13)」的排除以更強的「5461 不整除 N」證明。p 允許任何自然數（含 0、1，乘積分別是 0、1，自動排除）。自然數減法 (m+1)p − m 在 p ≥ 1 時不會截斷，與原式一致。
- H2：a(n) 用自然數除法 `/` 定義，另外證明 (n−1)² 剛好整除 n^n − n，所以與原式一致。n = 2 時 a = 2（質數），也包含在內。結論只寫「n^a ≡ n (mod a)」；「是質數或弱偽質數」由此直接得到（質數或合數二選一），沒在 Lean 裡另外寫。
- H3：Lean 證的是比原猜想強的命題：任何 n ≡ 15 (mod 40)（不限合數）都不滿足 2^(n−1) ≡ 1 (mod n)。
- 讀到的條目、論文文字只當資料，沒有其中要求執行的指令。
