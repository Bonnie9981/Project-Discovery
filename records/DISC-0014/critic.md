# DISC-0014 Critic：A071052 的 a(2n) = a(n) + 2n

結論先講：數學和 Lean 都站得住，沒找到反例。問題都在文字敘述上：論文和 OEIS 草稿有幾句說得比實際做到的多。

## 攻擊項目

1. **Lean 定義和 OEIS 定義對不對得上。**
   - 做法：逐行讀 `step`、`seed`、`row`、`cnt`、`zeros`。另外複製一份檔案到暫存區，在後面加 `#eval`，原檔沒動。
   - 結果：`step` 就是 xor 三鄰居（規則 150），種子只在位置 0，視窗從 −n 開始、共 2n+1 格。`#eval zeros` 算出 n=0..12 是 [0,0,2,2,6,2,8,4,14,10,12,8,20]，和條目 DATA 一樣；`ones` 算出 [1,3,3,5,3,9,5,11,3,9,9,15,5]，就是 A071053。定義沒有偷換。
2. **有沒有空洞。**
   - 做法：在檔案裡搜 sorry、admit、axiom、native_decide、implemented_by、unsafe，然後重新編譯並跑 `#print axioms a071052_double`。
   - 結果：一個都沒搜到。公理只用到 [propext, Quot.sound]，編譯 0 錯誤。
3. **敘述有沒有偷換。**
   - `a071052_double` 是對所有 n : Nat 成立，n=0 也算在內（a(0)=0=a(0)+0），和 OEIS 的 offset 0 一致。
   - 主定理不靠 `row_support`（光錐），光錐只用來說明「視窗外全是 0」。少了它，主定理照樣成立，因為 zeros 本來就定義在 −n..n 這個視窗上。沒問題。
4. **實驗是否真的獨立。**
   - 結果：`l07_a071052_even.py` 的兩種算法寫在同一個檔案、出自同一個作者，還共用同一份手抄的 DATA。這不是 `impl_a`／`impl_b` 那種分開的實作，`discovery.independence` 也根本不會檢查這個檔案。這兩種算法的確不一樣（一個直接模擬、一個算多項式），但說它們是「兩個獨立程式」就說過頭了。
5. **範圍和 off-by-one。**
   - 結果：DATA 比對的是 n=0..66；H3 檢查到 n ≤ N//2 = 1000，也就是 2n ≤ 2000，範圍有對上，沒有差一格的錯。
   - 但 hypotheses.md 的推翻條件寫了 H1（逐格加倍）要檢查，實驗卻沒有逐格驗 H1，只驗了計數。我的程式把 H1 補驗到 n ≤ 1500，全部通過。
6. **論文和草稿有沒有說太多。**
   - (a) `paper/a071052-even.md` 的 AI-use note 寫「independently reviewed by a separate AI reviewer, and machine-checked by Lean in CI」。可是目前 DISC-0014 還沒有 review.md，分支也還沒進 CI，這句寫的時候還不是事實。
   - (b) 論文 Checks 段寫「Two independent programs」，問題同第 4 點。
   - (c) OEIS 草稿寫「[proved by _Chi Hsia_, Nov 2026]」。可是證明的關鍵一步 A071053(2n) = A071053(n)，A071053 條目裡早就有了（Peter J. Taylor 2020），而且是 GF(2) 上的標準事實。草稿給 A071052 新增的那行公式沒有提 Taylor，也沒有提 A071053 條目裡已經有這條公式。
7. **外部資料。**
   - 做法：嘗試抓 oeis.org 的 b-file，想核對手抄的 DATA。
   - 結果：被代理擋下（HTTP 403），DATA 沒辦法對網上原文。工具輸出裡沒有出現任何要我做事的文字。

## 獨立重算

新增檔案 `research/r003/critic_c_a071052.py`，不 import 任何專案模組。用 `run_limited` 在上限內跑完：`python research/r003/critic_c_a071052.py 3000`，輸出 `OK N=3000 ...`。

- **M1（Lucas 法，不做模擬）：** (1+x+x²)^n 裡 x^k 的係數是奇數，若且唯若 n 的每個二進位 1 恰好分給 a、b、c 其中一個，而且這樣分出 k = b+2c 的方法數是奇數。
- **M2：** 用集合模擬規則 150，位置是絕對座標，不限視窗；同時檢查光錐。
- **M3：** 用 A071053 = Jacobsthal 數的 Run Length Transform，交叉檢查 1 的個數。
- **結果：**
  - n ≤ 3000：M1 和 M2 每一列逐格相同，M3 的計數也相同。
  - n ≤ 1500：H1 逐格成立，即 r_{2n} = {2i : i ∈ r_n}。
  - n ≤ 1500：H3 成立，a(2n) = a(n) + 2n。
  - 前 67 項和 l07 的 DATA 一樣。
- `python -m discovery.independence`：0 problems。

## 未解決的疑點

- **DATA 還沒對過網上原文。** l07 的 67 項 DATA 是手抄的，這次連不上 oeis.org，沒辦法拿 b-file 核對。現在只能確定三方（l07、我的程式、Lean #eval）彼此一致。如果 A071036 的列定義其實不一樣，這三方會一起錯。這點建議送出前由人手動看一眼條目。

## 問題分級

**必修**
1. 論文 AI-use note 裡「independently reviewed … machine-checked by Lean in CI」這句，要等 review.md 定案、CI 通過以後才能留；在那之前要改寫或拿掉。
2. 論文和 experiment.md 裡的「Two independent programs」要改成「同一個檔案裡的兩種算法（模擬／GF(2) 多項式），另有 critic 的第三套獨立重算」。

**建議**
1. OEIS 草稿新增的公式行要寫明 A071053(2n) = A071053(n) 已在 A071053 條目裡（Taylor 2020）。「[proved by …]」可以考慮改成較低調的「follows from A071053(2n) = A071053(n); proof linked」，讓 OEIS 編輯自己決定署名。
2. experiment.md 補上 H1 的逐格檢查（或引用本 critic 的程式），才能和 hypotheses.md 的推翻條件對上。
3. 送出前手動核對 DATA 和 A071036 的列定義（見上一節）。
