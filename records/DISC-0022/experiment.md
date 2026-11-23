# DISC-0022 實驗

## 方法

兩套獨立實作：C（128 位元模乘，分段篩）和 Python 大整數（Miller–Rabin 定底）。另用 C 直接照定義掃 A073631，和 OEIS b-file 的項數對齊。

## 結果

1. **Wieferich 搜尋（`wieferich32.c`）**：分段篩，對 5 ≤ p < 2^32 的每個質數比 3^(p−1) 和 2^(p−1) mod p²（p² < 2^64，用 128 位元乘法）。測了 203280219 個質數（= π(2^32) − 2，和已知 π(2^32) = 203280221 對得上），命中只有 **23、3842760169**，和 A376896 一致。`gcc -O2 -fopenmp -o w wieferich32.c -lm && ./w 1 4294967295`，4 核約 30 秒。
2. **Python 大整數獨立重算**：q = 23、3842760169、41975417117 都是質數（Miller–Rabin，前 12 個質數為底，在 3.3·10^24 內是確定的），都滿足 q² | 3^(q−1) − 2^(q−1)，都**不**滿足 q³ | …。k = q² 對 q = 3842760169、41975417117 都滿足 3^(k−1) ≡ 2^(k−1) (mod k)。23⁴、(23q)²、(q₁q₂)²、23²·q₁、q₁³ 都不是項。
3. **A073631 直接掃描（`a073631_scan.c`）**：k ≤ 10^9 的合數項 5419 個（加上 1 是 5420，和 Eldar b-file 裡 ≤ 10^9 的項數 5420 一致），其中非無平方因數的 60 個，全是 529 的倍數。所以小範圍內猜想成立，反例只在 10^19 等級才出現。
4. **搜尋器登錄**：`discovery/cxsearch/conjectures.py` 的 `A073631`，測試 `tests/test_cxsearch.py::test_a073631_counterexample`。

## 重現方式

```
gcc -O2 -fopenmp -o w wieferich32.c -lm && ./w 1 4294967295      # 約 30 秒（4 核）
gcc -O2 -fopenmp -o s a073631_scan.c && ./s 1000000000            # 約 2 分鐘
python -I ../../results/A073631/code/chk073631.py
python -m pytest -q tests/test_cxsearch.py -k a073631
```
