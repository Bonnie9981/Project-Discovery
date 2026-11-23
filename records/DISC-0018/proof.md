# DISC-0018 證明

Lean 檔：`lean/Discovery/NeverEasy.lean`（只用 core，Lean 4.15.0 本機 `lean` 編譯通過，無 `sorry`、`native_decide`）。

## 紙上證明

- H1：(2^a − 1)^2 = 2^(2a) − 2^(a+1) + 1 = (2^(a−1) − 1)·2^(a+1) + 1，二進位是 a − 1 個 1、a 個 0、最後一個 1，共 a 個 1（a ≥ 1；a = 0 時 m = 0，wt(0) = 0 另外成立）。所以 a(n) ≤ 2^n − 1，永遠不是 −1。
- H2：2n ≥ 40。2n ≡ 0 (mod 6) 時 2n = 9 + (2n − 9)；2n ≡ 4 時 2n = 25 + (2n − 25)；2n ≡ 2 時 2n ≥ 44，2n = 35 + (2n − 35)。第二個加數都是奇數、3 的倍數、≥ 9，所以是合數。
- H3：2n ≥ 12。2n − 3、2n − 5、2n − 7 之中，依 2n mod 3 恰好一個是 3 的倍數（2n ≡ 0 取 3，≡ 1 取 7，≡ 2 取 5），它是奇數且 ≥ 9，所以是合數；配上質數 3、5、7。

## 定理對照

| Lean 定理 | 數學敘述 |
|---|---|
| `Discovery.NeverEasy.wt_sq_two_pow_sub_one` | wt((2^a − 1)·(2^a − 1)) = a |
| `Discovery.NeverEasy.a231897_exists` | ∀ n, ∃ m ≤ 2^n − 1, wt(m·m) = n |
| `Discovery.NeverEasy.a215462_pos` | n > 19 ⇒ ∃ 奇數 x, y 非質數，x + y = 2n |
| `Discovery.NeverEasy.a215461_pos` | n > 5 ⇒ ∃ 奇質數 p、奇非質數 c，p + c = 2n |
| `Discovery.NeverEasy.sq_identity` | (2^(b+1) − 1)^2 = (2^b − 1)·2^(b+2) + 1 |
| `Discovery.NeverEasy.wt_two_pow_sub_one` | wt(2^a − 1) = a |

## 編譯結果

Lean 4.15.0 只用 core，`lean NeverEasy.lean` 約 2 秒通過，沒有 `sorry`、`native_decide`。H2、H3 的情形分析全靠 `omega`（對常數取模），質數 3、5、7 逐一列因數。

## 敘述差異

- `wt` 是自己定義的二進位權重（遞迴：n mod 2 + wt(n/2)），對應 A000120。
- `NonPrime x` = x = 1 或有 1 < d < x 的因數；`IsPrime p` = p ≥ 2 且因數只有 1 和 p。這和條目「nonprime（含 1）」一致。
- Lean 證的是「存在一種拆法」，也就是 a(n) ≥ 1（有序計數其實 ≥ 2）；這正是「a(n) 不是 0」。
- 邊界（a(5) = 0、a(19) = 0）由實驗確認，不在 Lean 裡。
