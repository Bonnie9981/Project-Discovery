# DISC-0017 證明

## 定理對照

| Lean 定理 | 數學敘述 |
|---|---|
| `Discovery.A294646Counter.powModAux_eq` | 二進位快速冪 `powModAux f b e m = b^e % m`（任意 fuel） |
| `Discovery.A294646Counter.key` | n = 9814447404 時 (2n−2)·2^(2n) ≡ 1 (mod 2n+1) |
| `Discovery.A294646Counter.dvd_three_pow_add_one` | 同一個 n，2n+1 整除 3·2^(2n)+1 |
| `Discovery.A294646Counter.modulus_factor` | 2n+1 = 367 × 53484727 |
| `Discovery.A294646Counter.inv_unique` | 模 m 的倒數在 [0, m) 內唯一 |
| `Discovery.A294646Counter.a294646_counterexample` | 2n−2 是最小的 k > 0 使 k·2^(2n) ≡ 1 (mod 2n+1)，即 a(9814447404) = 2n−2 |

H1、H2 的證明是古典的，只有紙本（`paper/a294646-counterexample.md` 第 1、2 節），沒寫進 Lean。

## 編譯結果

Lean 4.15.0 只用 core，`lean A294646Counter.lean` 0.4 秒通過（Nat 乘、除、模在 kernel 有 GMP 加速，`decide` 只算 64 層快速冪）。把 2n−2 改成 2n−3 時 `decide` 回報命題為假，確認不是空洞通過。沒有 `sorry`、`native_decide`。

## 敘述差異

- Lean 用條目留言的刻畫「最小 k > 0 使 k·2^(2n) ≡ 1」當 a(n) 的定義（`IsA294646`），不是 Maple 的 `(1/2 mod m)^(2n) mod m`；兩者相等，因為 2 模奇數 m 可逆。
- 「這是最小反例」只由兩支程式（brute.c 到 10^10、scan.c 到 6.1·10^10）支持，不在 Lean 裡。
