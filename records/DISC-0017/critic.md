# DISC-0017 Critic 報告

對象：A294646 猜想「a(n) 永不為 2、2n、2n−2」。主張是 2n−2 那半被 n = 9814447404 推翻、這是最小反例，另外兩半有古典證明。
critic 自己的程式用 Go 寫，不 import、也不讀專案任何模組。原始碼在 scratchpad：`/tmp/claude-0/-home-user/67915a62-14ae-5522-8099-6c3d5fb5dee1/scratchpad/c/main.go`，這個位置會被清掉，沒有存進 repo，見「未解決的疑點」。
外部資料：oeis.org 被這次執行環境的代理擋掉（HTTP 403），所以沒能拿線上 DATA 或 b-file 來比對。讀到的檔案和工具輸出裡沒有出現要 agent 做事的文字。

## 攻擊項目

1. **反例本身（換語言、換演算法重算）**
   - 做法一：Go `math/big`，從最高位開始的平方乘法（不用 `big.Exp`），再用擴展歐幾里得求反元素。
   - 做法二：uint64 路徑，乘法取模用 `bits.Mul64` 加 `bits.Rem64`，不用 `__int128 %`。
   - 結果：a(9814447404) = 19628894806 = 2n−2；(3·2^(m−1)+1) mod m = 0；367·53484727 = 19628894809。全部成立。

2. **a(n) 的定義對不對**
   - 照定義算 a(1..30)：1,1,1,7,1,1,4,1,1,16,1,11,25,1,1,25,4,1,10,1,1,16,1,36,13,1,9,43,1,1。前 20 項和 verify.py 寫死的 DATA 一樣。
   - 限制：verify.py 裡的 DATA 是人工抄進去的。OEIS 連不上，所以「和線上條目一致」這點沒有獨立確認，只能確定和 verify.py 的抄本一致。
   - 數學上：a(n) ≡ 2^(−2n)，所以 a=2n−2 ⇔ −3·2^(2n) ≡ 1 ⇔ m | 3·2^(m−1)+1；a=2 ⇔ m | 2^m−1；a=2n ⇔ m | 2^(m−1)+1。三個對應都正確。

3. **最小性：篩選條件逐條推導**
   - m 是質數時，3·2^(p−1)+1 ≡ 4，不可能被 p 整除，所以 m 是合數。
   - 3 ∤ m。
   - (3x)² ≡ −3，其中 x = 2^((m−1)/2)，所以每個質因數 p ≡ 1 (mod 6)。由此 k = m/p ≡ 1 (mod 6)。
   - 2^(pk−1) ≡ 2^(k−1) (mod p)，所以 k ≡ 1+r (mod ord_p 2)。
   - 和 k ≡ 1 (mod 6) 相容 ⇔ r ≡ 0 (mod gcd(ord,6))。
   - 以上推導全部正確。
   - 界的部分：最小質因數 ≤ √(6.1e10) ≈ 246981 < 2e6，而且 k ≤ 6.1e10/61 = 1e9。界正確。

4. **gen_primes.py 和 critic 結果逐條比對**
   - critic 在 p < 247000 範圍內自己求 ord 和 r（逐步走 2 的冪，不用 sympy 的 `discrete_log`），同餘相容性用 CRT 搜尋決定，不套 gcd 公式。
   - 得到 2573 個質數，和 gen_primes.py 的輸出逐項比對：(p, ord, r) 全部相同，沒有任何一邊多出來的質數。
   - 最小的可用質數確實是 61。7、13、19、37 雖然 ≡ 1 (mod 6)，但同餘類不相容，所以被排除。

5. **scan.c 的程式邏輯**
   - 起點搜尋 `k<L+d` 一定找得到相容類，不會漏。`k<7` 只跳過 k = 1，也就是 m 是質數的情況，前面已證明不可能。
   - p·k ≤ 2e15，不會溢位。
   - 有一處死碼：`if(!k0 && 1%6!=1)` 永遠為假。找不到相容類時 k0 會是 0，程式會去掃 ≡ 0 (mod 6) 的 k，白做工但不影響結果。因為 gen_primes 已經保證相容類存在，實際上不會發生。
   - 重跑：用 gen_primes.py 2000000 產生 17446 個質數，scan 分 4 段跑 17 秒，只印出 `HIT m=19628894809 p=367 k=53484727`，可以重現。

6. **突變測試：scan 有解時真的找得到嗎**
   - 把 gen_primes.py 和 scan.c 改成 c = 15 版：3 換成 15，模 6 的條件換成「k 為奇數」，拿掉 p ≡ 1 (mod 6) 的篩選。
   - 結果找到 987677（從 p = 19、227、229 三個質數各找到一次）和 1589597，正好是 critic 窮舉在 2e7 以內的全部解。
   - 結論：起點和步長的程式邏輯是對的。

7. **古典證明（paper 第 1、2 節）**
   - 第 1 節：逐步檢查過。d > 1 是因為 p 是奇數；d | gcd(m, p−1)；d 的任一質因數都 < p，矛盾。沒有漏洞。
   - 第 2 節：d | 2(m−1) 而 d ∤ m−1，所以 v₂(d) = k+1，推出 p ≡ 1 (mod 2^(k+1))。m 是這些質因數（含重數）的乘積，所以 m ≡ 1 (mod 2^(k+1))，和 v₂(m−1) = k 矛盾。沒有漏洞。
   - 措辭小問題：「m, a product of such primes」最好寫明「含重數」。

8. **Lean 檔**
   - Lean 4.15.0 編譯 0.46 秒通過。
   - `#print axioms`：兩個主定理只依賴 `propext`、`Quot.sound`，沒有 `sorryAx`，也沒有 `Lean.ofReduceBool`。
   - 負向測試：把 2N−2 改成 2N−3，`decide` 回報命題為假。
   - 檢查 `IsA294646` 的定義：在 critic 的測試檔裡證明了 `IsA294646 4 7` 和 `¬ IsA294646 4 6`（a(4) = 7），定義和 DATA 對得上。
   - `IsA294646` 寫成「最小正 k」，雖然沒寫 k < m，但最小性已經隱含這點。它和 OEIS 的 (1/2)^(2n) mod (2n+1) 等價，因為 2n+1 ≥ 3 而且 2 可逆。
   - Lean 只證明了這一個 n 的值，沒有證明最小性，也沒有證明第 1、2 節。proof.md 已經寫明這點。

9. **「兩支獨立程式支持最小性」的說法和實際涵蓋範圍不符（必修）**
   - brute.c 只跑到 m < 1e10，反例卻是 m ≈ 1.96e10。
   - 所以 m 在 [1e10, 1.96e10) 這段「沒有更小的解」，在專案裡只有 scan.c 一支程式支持。
   - 以下幾處的說法都超過實際涵蓋範圍：paper 開頭「every claim below is checked by computer ... two independent programs for the search」、proof.md「只由兩支程式（brute.c 到 10^10、scan.c 到 6.1·10^10）支持」。
   - 另外，paper 第 1、2 節是紙本證明，沒有用電腦檢查。「every claim below is checked by computer」這句因此不成立。
   - 本 critic 的獨立 scan（見下節）已經補上這段區間的第二套實作，但要寫清楚是誰、用什麼做的。

10. **OEIS 草稿**
    - 英文數學敘述正確：2^(2*n+1)−1 和 2^(2*n)+1 的對應都對，EXAMPLE 的推導也對。
    - 「This is the least such n.」沒有附理由。建議改成「This is the least such n (exhaustive search, see link).」，避免讀者以為這是證明出來的。
    - 「The parts ... are true」建議加「(classical; proofs in link)」。
    - LINKS 寫「the counterexample is machine-checked in Lean 4」是精確的，沒有過度宣稱。

## 獨立重算

所有原始輸出都在 scratchpad 的 `c/`、`g/`、`m/`、`l/` 子目錄（scratchpad 路徑見開頭）。

| 檢查 | 範圍 | 結果 | 時間 |
|---|---|---|---|
| Go big.Int 加擴展歐幾里得 | n = 9814447404 | a(n) = 2n−2 | 瞬間 |
| Go 窮舉（不用結構，每個奇數 m 都算） | 奇數 m < 2e8，c = 3 | 無解 | 22 秒 |
| Go 窮舉 | 奇數 m < 2e7，c = 15、5、31、7 | 15：{987677, 1589597}；5、31 各有若干解；7：無解 | 秒級 |
| Go 一般結構搜尋（不假設 mod 6，只用「最小質因數 p ≤ √M、k ≥ p 且為奇數、k ≡ 1+r (mod ord)」，另外處理 m 為質數的情況） | 上面 c = 3、5、7、15、31，M = 2e7 | 每個 c 的解集合都和窮舉完全相同 | 秒級 |
| 同上，c = 3 | M = 1e10 | 無解 | 80 秒，4 核 |
| Go 結構搜尋，只加 p ≡ 1 和 k ≡ 1 (mod 6) 的條件，CRT 用搜尋求 | c = 3，M = 6.1e10 | 只有 19628894809 | 13 秒 |
| 專案的 scan.c 重跑 | K = 1e9，p < 2e6 | 只有 m = 19628894809 | 17 秒 |
| 突變版 scan（c = 15） | K = 2e6，p < 5000 | 找到 987677、1589597 | 瞬間 |

結論：在 m ≤ 6.1e10 內，m | 3·2^(m−1)+1 只有 m = 19628894809，所以 n = 9814447404 是最小反例。這個結論現在有兩套演算法和程式都獨立的實作支持。其中 m < 1e10 這段還有第三套：不用 mod 6 假設的一般結構搜尋。

## 未解決的疑點

- **DATA 沒有對線上條目確認。** oeis.org 被代理擋掉，所以只確認了和 verify.py 抄的前 20 項一致。送出 OEIS 前，使用者應該照草稿說的，用 PARI 自己驗一次。
- **critic 的程式沒有存進 repo。** 照總控指示，本 critic 只寫這份檔案。所以系統規則要求的 `research/<線>/impl_c.py` 沒有建立，`python -m discovery.independence` 沒有對本線跑過。Go 原始碼在 scratchpad，那裡會被清掉。
- **brute.c 的 H1、H2 跑到 1e10 的結果沒有重跑。** 那要 40 核分鐘，超過本次的時間預算。這兩半本來就有紙本證明，風險低。
- **paper 對 A050259 最小項 4700063497 的說法沒有用電腦驗證。** 這只是類比用的旁證，不影響主結論。

### 必修
1. 修正 paper 開頭「every claim below is checked by computer ... two independent programs for the search」：第 1、2 節是紙本證明；brute.c 只涵蓋 m < 1e10，所以 m 在 [1e10, 1.96e10) 的最小性原本只有 scan.c 支持。proof.md 的對應句子也要一起改。改寫時可以引用本 critic 的獨立結構搜尋，它已補上第二套實作。
2. 把 critic 的獨立搜尋留存進 repo，例如放成 `results/A294646/code/` 下的檢查腳本或 `research/` 下的 impl_c。否則「兩套獨立實作」這個說法沒有可重現的依據。

### 建議
- OEIS 草稿：「This is the least such n」後面加「(exhaustive search, see link)」；「are true」後面加「(classical; proofs in link)」。
- paper 第 3 節補一句 r ≡ 0 (mod gcd(ord_p 2, 6)) 這個相容條件，scan 實際上用了它；第 2 節寫明「product of such primes (with multiplicity)」。
- scan.c 那行永遠不成立的 `if(!k0 && 1%6!=1)` 改成 `if(!k0) continue;`，讓意圖清楚。
