# DISC-0020 證明

## 定理對照

| Lean 定理 | 白話 |
|---|---|
| `Discovery.A362070Counter.mmin_unique` | m_min(n, k) 的定義（最小 m ≥ 1）只會對應一個值 |
| `Discovery.A362070Counter.kempner_unique` | Kempner 數 K(n) 的定義只會對應一個值 |
| `Discovery.A362070Counter.sumTo_congr` | 前 K 項相同，總和就相同 |
| `Discovery.A362070Counter.avalue_unique` | 照條目定義的 a(n) 只有一個值（`AValue n s` 是函數） |
| `Discovery.A362070Counter.kempner_1715` | K(1715) = 21 |
| `Discovery.A362070Counter.kempner_1716` | K(1716) = 13 |
| `Discovery.A362070Counter.mmin_1715` | m_min(1715, r)，r = 1..21，依序是 21, 13, 7, 6, 5, 4, 3×6, 2×8, 1 |
| `Discovery.A362070Counter.mmin_1716` | m_min(1716, r) = 14 − r，r = 1..13 |
| `Discovery.A362070Counter.a_1715` | a(1715) = 91 |
| `Discovery.A362070Counter.a_1716` | a(1716) = 91 |
| `Discovery.A362070Counter.a362070_counterexample` | a(1715) = a(1716) = 91，猜想不成立 |

## 編譯結果

只用 core（無 Mathlib、無 `native_decide`），數值部分用 `decide` 交給 kernel 算（大整數乘法、取餘有 GMP 加速）。本機容器裝不到 Lean（elan 下載被代理擋），以 PR 的 GitHub CI（lean 工作，含 AxiomCheck）為準。

## 敘述差異

- 條目的 RisingFactorial(t, k) = t(t+1)⋯(t+k−1)，Lean 的 `rf t k` 一樣；`P k m` = ∏_{t=1..m} rf t k。
- 「smallest m」取 m ≥ 1（m = 0 時空積為 1，只有 n = 1 會整除，與本題無關）。
- Kempner 數取最小 K ≥ 1 使 n | K!，與 A002034 相同。
- 「沒有比 1715 更小的解」與「10^10 以下只有這一組」是計算結果，沒有寫進 Lean：n ≤ 2000 由 Python（`a362070_value`）與 scan.c 兩種程式各自確認，n ≤ 10^4 critic 另用自己的程式重算；10^10 只有 scan.c 跑過（critic 抽查 [9.99·10^9, 10^10] 一段）。
