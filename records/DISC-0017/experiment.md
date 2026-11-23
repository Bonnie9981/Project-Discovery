# DISC-0017 實驗

## 方法

1. `results/A294646/code/brute.c`：對所有奇數 3 ≤ m < 1.964·10^10 直接算 2^(m−1) mod m（128 位元乘法），檢查三種情形。4 核平行。
2. `results/A294646/code/gen_primes.py` + `scan.c`（結構搜尋，和 1 是不同算法）：若 m | 3·2^(m−1)+1，則 m 非質數、3 ∤ m、每個質因數 p ≡ 1 (mod 6)（−3 是平方剩餘）、−1/3 ≡ 2^r (mod p) 有解，且 m/p ≡ 1 + r (mod ord_p(2))；又 m ≡ 1 (mod 6) 要求 r ≡ 0 (mod gcd(ord_p(2), 6))。列出 p < 2·10^6 中符合的 17446 個質數，對每個 p 掃 k ≤ 10^9 的同餘類，測 m = p·k。m 的最小質因數 ≤ √m，最小可用質數是 61，所以對 m ≤ 6.1·10^10 是完整搜尋。
3. `results/A294646/code/verify.py`：Python 大整數直接驗反例，順便核對前 20 項 DATA。
4. Lean：`lean/Discovery/A294646Counter.lean` 在 kernel 裡驗反例（見 proof.md）。

## 結果

- H1、H2：brute 到 10^10 沒有解（和古典證明一致）。
- H3：scan 只找到一個 m = 19628894809 = 367 × 53484727，即 n = 9814447404，a(n) = 19628894806 = 2n − 2。brute 逐一檢查到 1.964·10^10，H3 只有 m = 19628894809 這一個解，和 scan 一致。
- 結論：H3 被推翻，最小反例 n = 9814447404（在 m ≤ 6.1·10^10 範圍內唯一）。
- 對照：把 3 換成其他常數 c，m | c·2^(m−1)+1 在 c = 1、3、7 時 3·10^6 內無解，c = 15 的第一個解是 987677；c = 2^j − 1 時沒有質數解，只能是合數，所以最小解偏大。

## 重現方式

```
cd results/A294646/code
gcc -O2 -o brute brute.c && ./brute 1 10000000000      # 約 4 核 × 10 分鐘，可切段平行
pip install sympy && python3 gen_primes.py 2000000      # 產生 plist.txt
gcc -O2 -o scan scan.c && ./scan 1000000000 0 1         # 約 1 分鐘，印出 HIT m=19628894809
python3 verify.py
```
