# DISC-0020 實驗

## 方法

A362070：
1. `results/A362070/code/brute.py`：照名稱逐字用大整數乘出 ∏ rf(t, r)，找最小 m；Kempner 數直接乘階乘。
2. `results/A362070/code/factored.py`（也收進 `discovery/cxsearch/conjectures.py` 的 `a362070_value`）：對每個 p^e || n 用 v_p 算最小 m，取最大值後相加。
3. `results/A362070/code/scan.c`：分段篩法分解 n；e = 1 的質因數只有最大的 P 有影響（m_min = max(1, P − r + 1)），e ≥ 2 的質數冪預先用 G(x) = Σ v_p(y!) 的前綴和與雙指標算好 m_min 表；總和用 128 位元整數（n 接近 10^10 時 P(P+1)/2 會超過 64 位元）。同時記錄 a(n) = a(n+1) 與「a(n) = n 但 n 不是奇質數編號的三角數」。
4. 條目自己的 Maxima 程式（`code/entry_program.mac`，裝 Maxima 5.x 跑）。
5. Lean kernel 計算（見 proof.md）。

A332786：`records/DISC-0020/a332786.c`對每個合數 m ≤ 10^5、每個 q^e || m，算 T = q^t·S(m) mod q^(t+2e)（t = ⌊log_q m⌋，S(m) = −1/m + Σ 2^(k−1)/k），由 v_q(S) 判斷 m | a(m) 與 m^2 | a(m)。m ≤ 600 與分數精確計算對過。

## 結果

- 四種算法在 n ≤ 57 與 DATA 完全一致；a(1714) = 367653，a(1715) = 91，a(1716) = 91，a(1717) = 5151，四邊一致。
- 篩法掃 n ≤ 10^10：a(n) = a(n+1) 只有 n = 1715。10^9 以內單程跑過一次（`./scan 1000000000`，輸出 `HIT n=1715 a=91`、`done N=1000000000 hits=1`）。10^10 分四段平行跑，參數 `./scan N 0 START`：
  - `./scan 2500000000 0 1` → `HIT n=1715 a=91`、`done N=2500000000 hits=1`
  - `./scan 5000000000 0 2500000001` → `done N=5000000000 hits=0`
  - `./scan 7500000000 0 5000000001` → `done N=7500000000 hits=0`
  - `./scan 10000000000 0 7500000001` → `done N=10000000000 hits=0`
  每段算 n = START..N+1，比較 (n−1, n) 當 n > START，也就是 (START, START+1) 到 (N, N+1)；下一段從 N+1 開始，所以所有相鄰對 (n, n+1)，n ≤ 10^10，都恰好比到一次，沒有漏接。
- a(n) = n 但 n 不是奇質數編號三角數的解：n ≤ 10^10 只有 1 和 16（回答條目的問句：10^10 以內沒有更大的）。
- A332786：m ≤ 10^5 的合數裡只有 49 滿足 m | a(m)（沒有任何合數滿足 m^2 | a(m)）；順帶確認質數 5 ≤ p ≤ 55100 都有 p^2 | a(p)，p^3 | a(p) 只有 7 和 16843（Wolstenholme 質數），與條目一致。

## 重現方式

```
python -m discovery.cxsearch scan A362070 --nmax 2000      # Python，找到 1715
gcc -O2 -o scan results/A362070/code/scan.c -lm
./scan 1000000000                                           # 約 2 分鐘，HIT n=1715
python results/A362070/code/brute.py 1715 1716               # 照定義逐字算
maxima -b results/A362070/code/entry_program.mac             # 條目自己的程式
```
