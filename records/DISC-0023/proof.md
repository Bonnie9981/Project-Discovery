# DISC-0023 證明

**引理。** 設 k > 1 整除 3^(k−1) − 2^(k−1)，且質數 q 滿足 q² | k。則 q 是以 3/2 為底的 Wieferich 質數：q² | 3^(q−1) − 2^(q−1)。

證明：3^(k−1) − 2^(k−1) 是奇數、不被 3 整除，所以 q ≥ 5，2 在 mod q² 可逆。令 x = 3·2^(−1) mod q²，則 x^(k−1) ≡ 1 (mod q²)。x 的階 d 整除 φ(q²) = q(q−1)，也整除 k − 1。因為 q | k，gcd(k−1, q) = 1，所以 d | q − 1，x^(q−1) ≡ 1，即 q² | 3^(q−1) − 2^(q−1)。∎

**反例。** q = 3842760169 是 3/2 底 Wieferich 質數（A376896；Lean `wieferich_q1`）。k = q²：q − 1 | k − 1 = (q−1)(q+1)，所以 3^(k−1) ≡ 2^(k−1) (mod q²)，k 是合數、是完全平方、不是無平方因數、不是 529 的倍數（Lean `a073631_counterexample` 直接用 kernel 算 mod k 的冪）。同理 41975417117²（`a073631_counterexample2`）。

**最小性。** 反例 k 有平方因數 q² 且 q ≠ 23（否則 23² | k）。由引理 q 是 3/2 底 Wieferich 質數且 q ≠ 23；實驗 1 顯示 2^32 以下只有 23 和 3842760169，所以 q ≥ 3842760169，k ≥ q² = 14766805716452908561，而它本身是項。**最小反例 = 3842760169² = 14766805716452908561。** 「1 和 529 是唯一完全平方項」的最小反例也是它：完全平方項 m² 的每個質因數都是 3/2 底 Wieferich 質數；m 只含 23 時，23³ | m² 會推出 (3/2)^22 ≡ 1 (mod 23³)，算過不成立（值是 9523），所以 m = 23；m 若有 23 以外的質因數，那個質因數就 ≥ 3842760169，m² ≥ 3842760169²。

**有沒有無限多個？** 每個 3/2 底 Wieferich 質數 q 都給一個反例 q²；反例存在 ⇔ 23 以外還有這種質數。已知 2 個（3842760169、41975417117），是否無限多是開放問題（同 Wieferich 質數）。對 q1 也可能有 q1²·r 這種反例（像 A130058 對 23），沒找。

最小性依賴實驗 1 的電腦搜尋（沒寫進 Lean）；Lean 只驗反例本身。

## 定理對照（`lean/Discovery/A073631Counter.lean`）

| Lean 定理 | 內容 |
|---|---|
| `Discovery.A073631Counter.pow_mod'` | (a mod m)^k mod m = a^k mod m |
| `Discovery.A073631Counter.powModAux_eq` | 二進位模冪 `powModAux` 等於 b^e mod m |
| `Discovery.A073631Counter.wieferich_q1` | 3842760169 是 3/2 底 Wieferich 數 |
| `Discovery.A073631Counter.wieferich_q2` | 41975417117 同上 |
| `Discovery.A073631Counter.inSeq_q1_sq` | 3842760169² 滿足 A073631 的整除條件 |
| `Discovery.A073631Counter.inSeq_q2_sq` | 41975417117² 同上 |
| `Discovery.A073631Counter.a073631_counterexample` | 3842760169² = 14766805716452908561 是項、合數（1 < q < q²、q 整除它）、有平方因數、不是 529 的倍數 |
| `Discovery.A073631Counter.a073631_counterexample2` | 41975417117² 同上 |
| `Discovery.A073631Counter.inSeq_529` | 對齊用：529 是項 |

## 編譯結果

本機下載不到 Lean 工具鏈（elan 被網路擋），靠 GitHub Actions 的 lean CI 編譯與公理檢查。結果見 PR 檢查。

## 敘述差異

- Lean 只驗反例本身；引理（平方因數必為 3/2 底 Wieferich 質數）和最小性是紙上證明加電腦搜尋，沒有形式化。
- 「q 是質數」沒有在 Lean 裡證：反例只需要 k = q·q、q ≥ 2，就已經是合數又有平方因數。q 的質數性由 Python Miller–Rabin（定底）確認，只用在最小性論證。
- `InSeq k` 寫成 3^(k−1) mod k = 2^(k−1) mod k（因為 3^(k−1) ≥ 2^(k−1)，等價於 k 整除差）；沒包含「非質數」條件，非質數另外用 1 < q < q² 且 q | q² 表示。

## 作者回應 critic 必修

1. Miller–Rabin 底改成 2～41 共 13 個（`chk073631.py`、`experiment.md`）。
2. OEIS 草稿：A073631 留言補上 2^32 搜尋；A376896 留言改成 p > 23；LINKS 改成「the counterexample is checked in Lean 4」。
3. paper 與本檔的完全平方段補上「m 有 23 以外的質因數則 m ≥ 3842760169」。
4. Lean：`Nat.sub_mod_eq_zero_of_mod_eq` 確實不在 core v4.15，CI 第一次失敗；已改成 `InSeq` 直接寫成同餘式，模冪燃料改 66／74 並加 `maxRecDepth`。CI 綠燈前不寫「checked in Lean 4」。
