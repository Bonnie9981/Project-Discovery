# DISC-0002 critic.md

作者：critic（獨立 subagent）

我讀過的檔案：`literature.md`、`hypotheses.md`、`experiment.md`、`experiment_data.json`、`research/r001/drill.py`、`research/r001/primality.py`、`discovery/verify.py`、`lean/Discovery/R001.lean`、`discovery/known_results.json`。這個環境沒辦法編譯 Lean，所以 Lean 的部分只做了閱讀檢查。

## 攻擊項目

### A1. H1～H5 的反例與邊界（p=2、p=3、端點）
- **做了什麼**：用獨立程式（見「獨立重算」）算出每個質數 p ≤ 100000 的 run 長度，也就是讓 n² + n + p 對所有 0 ≤ n ≤ k 都是質數的最大 k。再拿 run 長度和 p−2、⌊√(p/3)⌋ 比較。另外把 p=2、3、5、11、17、41 的端點逐一列出來。
- **結果**：H1～H5 都**沒有找到反例**。邊界情況如下：
  - p=2：⌊√(2/3)⌋ = 0，p−2 = 0。完整檢查和短檢查都只看 n=0（值為 2），兩者是同一個檢查。
  - p=3：⌊√(3/3)⌋ = 1，p−2 = 1。短範圍和完整範圍**完全相同**（n=0,1，值為 3、5）。
  - 所以 H5 在 p=2、3 時只是「Q_p ⇔ Q_p」，沒有資訊量。真正有內容的 lucky p 只有 5、11、17、41 這四個。
  - 在 p ≤ 100000 的質數中，沒有任何一個 p 使 ⌊√(p/3)⌋ > p−2，所以「完整 ⇒ 短」這個方向在範圍內都成立。
  - `range(0, upto + 1)` 包含 upto 本身，`range(0, 40)` 對應 n = 0..39，H1 的 `range(2, 10001)` 共 9999 個，和紀錄一致，**沒有 off-by-one**。

### A2. H5 的 `math.isqrt(p // 3)` 是否等於 ⌊√(p/3)⌋
- **做了什麼**：用純整數定義「滿足 3k² ≤ p 的最大 k」（這就是 ⌊√(p/3)⌋ 的精確值），對 p = 0..100000 的每一個整數逐一比較。
- **結果**：**0 個不一致**。這在數學上本來就成立，因為 ⌊√⌊x⌋⌋ = ⌊√x⌋ 對 x ≥ 0 都對。`isqrt_p_over_3` 沒有問題。

### A3. H5 的檢驗力不足（實質問題）
- **做了什麼**：
  - 統計非 lucky 質數的 run 長度分布。
  - 找出最小的常數 c，使「n ≤ min(c, p−2) 全為質數 ⇔ Q_p」在 p ≤ 100000 內也成立。
  - 把短範圍上界改成 ⌊√(p/3)⌋ − 1 重跑一次。
- **結果**：
  - 在 9586 個非 lucky 質數中，run 長度最長只有 7，出現在 p=21557 等兩個質數，而 p=21557 的上界是 84。分布為 {0: 8367, 1: 964, 2: 183, 3: 39, 4: 21, 5: 8, 6: 2, 7: 2}。
  - **常數上界 c = 8 在這個範圍內也能得到同樣的等價**。換句話說，這次實驗分不出 √(p/3) 和「只檢查到 n=8」哪個對。
  - 上界改成 ⌊√(p/3)⌋ − 1 時，**只有 p=7 一個反例**（run=0，上界=1）。所以上界在範圍內「不能再小」這件事，完全靠 p=7 一個數支撐。
  - 結論：H5「範圍內成立」是事實，但不能當作支持 √(p/3) 這個特定上界的證據。這個上界的根據只有 literature 第 5 條，而那一條本身未查證（見 A8）。

### A4. 兩個實作是否真的獨立（實質問題）
- **做了什麼**：讀 `drill.py` 和 `verify.py`，看 holds_a 和 holds_b 有哪些共用的部分。
- **結果**：H4、H5 的 A、B 兩個實作**只有質數判定不同**，下面這些部分是共用的：
  1. 定義域 `primes` 只用 `is_prime_trial` 產生，B 沒有另外產生一次。如果試除法漏掉某個質數，兩個實作都不會檢查到它，`verify.check` 也不會報出不一致。（我的篩法驗證 π(100000) = 9592，和紀錄的 checked=9592 一致，所以這次實際上沒有漏。）
  2. `q_holds` 的範圍邏輯是共用的。
  3. lucky 集合 `{2,3,5,11,17,41}` 是同一個常數字面值。
  4. `isqrt_p_over_3` 是共用的。
  - 所以「兩個獨立實作」只對質數判定的錯誤有防護，對範圍或 off-by-one 的錯誤**沒有防護**。這次靠我的獨立重算（A1、A2）補上了這一塊。
  - 另外，`all()` 會短路，所以在 H4、H5 中兩個質數判定實際比對到的值最大只有 **99995**（約 1e5）。H1 比對到的最大值是 10000² = 1e8。B 實作在大數上的正確性在這次實驗中**幾乎沒有被用到**。

### A5. Miller–Rabin docstring 的決定性上界寫錯了（實質問題，已實測）
- **做了什麼**：`primality.py` 宣稱用前 12 個質數為底「Deterministic for n < 3.3e24 (Sorenson & Webster 2015)」。我用自己寫的 strong probable prime 測試，加上 Pollard rho 分解，檢查了 n = 318665857834031151167461（約 3.19e23）。
- **結果**：這個 n **通過 2..37 全部 12 個底**，但它是合數：399165290221 × 798330580441。我也直接用專案的 `is_prime_mr` 測了這個數，回傳 **True**，也就是誤判為質數。
  - 3.3e24 這個上界（3317044064679887385961981）其實要再加上底 41。我驗證了它也通過 12 個底、在底 41 失敗，因數是 1287836182261 × 2575672364521。
  - 結論：用 12 個底時，正確的上界是 n < 318665857834031151167461（約 3.18e23）。docstring 把上界多寫了約 10 倍。這不影響 DISC-0002，因為最大值才 1e8，但如果之後的研究線引用這個上界，就會出錯。

### A6. H3 的狀態標籤不合規
- **做了什麼**：對照 `experiment_data.json` 和 RESEARCH_STANDARDS §1 的狀態表。
- **結果**：H3 的 `"status": "REFUTED_EXTENSION"` **不在 §1 的合法狀態裡**。而且 H3 的敘述是「1681 不是質數」，這個敘述是**成立**的，「REFUTED」指的是「Q_41 不能延伸到 n=40」。程式如果用字串前綴判斷，會把它誤讀成 REFUTED。另外，H3 沒有經過 `verify.check`，是在 `h3()` 裡另外手寫的雙實作比對。結果本身是對的：兩個實作都回傳 False，而且 1681 = 41²。

### A7. Lean 敘述是否忠實對應 H1/H2/H3
- **做了什麼**：逐條閱讀 `R001.lean`，特別看自然數減法截斷的問題。我沒有編譯。
- **結果**：
  - `boundary_eq (p) (hp : 1 ≤ p)`：p ≥ 1 時 `p - 1` 不會截斷，敘述是對的。我也檢查了 p=0：截斷後是 0+0+0 = 0 = 0²，同樣成立，所以 `hp` 其實可以拿掉，但留著沒有壞處。證明的寫法 `p = k+1`、`Nat.add_sub_cancel`、`ring` 看起來合理。
  - `boundary_not_prime (hp : 2 ≤ p)`：和 H1 一致。p=1 時 1² = 1 本來就不是質數，所以 H1 限制 p ≥ 2 是為了配合 Q_p 的定義，不是漏洞。
  - `euler41 : ∀ n < 40, Nat.Prime (n^2 + n + 41)`：n ∈ ℕ、n < 40，等於 0..39，和 H2 一致。
  - `euler41_fails`：和 H3 一致。
  - **敘述差距**：檔頭註解提到 `Q p`，但 Lean 裡**沒有定義 `Q`**。H1 括號裡的「所以 Q_p 的範圍 n ≤ p−2 已是最長」也沒有被形式化。Lean 證明的只是「n = p−1 時不是質數」這個代數事實。
  - H4、H5 都沒有 Lean 定理，紀錄裡也寫明不嘗試，這一點沒有誇大。但 `record.json` 的 `lean_theorems` 目前是 []，所以引用的定理也還沒填。

### A8. literature.md 有沒有誇大或沒有來源的說法（第 3 條是實質錯誤）
- **做了什麼**：逐條檢查，並用程式測試第 3 條的字面敘述。
- **結果**：
  - **第 3 條照字面是錯的**。原文是「Q_p 成立 ⇔ 虛二次體 ℚ(√(1−4p)) 的類數為 1」。p=7 就是反例：4·7−1 = 27 = 9·3，所以 ℚ(√−27) = ℚ(√−3)，類數是 1；但 Q_7 不成立，因為 1+1+7 = 9。p ≤ 2000 中這樣的反例有 30 個：7, 19, 37, 43, 61, 97, 127, 151, 223, 233, …, 1997（完整清單見獨立重算的輸出）。
    - 這裡我把「類數 1 的虛二次體是 d ∈ {1,2,3,7,11,19,43,67,163}」當作已知結果。
    - 正確的寫法應該是「判別式 1−4p 等於某個 Heegner 數的負值」，或者「4p−1 無平方因子，且 ℚ(√(1−4p)) 類數為 1」。第 4 條的推導其實用的是正確版本（直接代 4p−1 ∈ {3, …, 163}），所以結論清單沒有受影響，但第 3 條的敘述和第 4 條的推導互相矛盾。
  - 第 5 條（√(p/3) 判準）：已誠實標示「未查證」，但「研究空白」那一段寫「本題的所有問題在 1967 年以前就已完全解決」。第 5 條的出處和年代都沒查，所以這句話**沒有根據**，至少對第 5 條是如此。
  - 第 1、2、4 條和我記得的一致（Euler 1772；A014556 = 2,3,5,11,17,41；Heegner 1952 / Baker 1966 / Stark 1967）。但我也連不上網路，**一樣沒辦法線上複核**。
  - 其中 A014556 的 OEIS 原始定義是 m² − m + n 對 m = 0..n−1。這和本題的寫法等價：令 m = n+1，m=0 那一項就是 p 本身。但 `known_results.json` 的 name 欄寫成本專案的形式，並不是 OEIS 的原文。

### A9. 可重現性
- **做了什麼**：在目前的 HEAD 用專案程式重跑 `python -m research.r001.drill 100000`，再和 `experiment_data.json` 比較；另外查 `git log` 和 `git status`。
- **結果**：`results` **完全相同**（True）。git_commit = 9a837f12e2120bf9aab6be4ff141518982966ed0，和紀錄一致，沒有 -dirty。耗時 0.85 秒。Python 3.13.18 也一致。要注意 `git_commit()` 是用 `--untracked-files=no` 判斷 dirty 的，所以未追蹤的檔案不會讓版本被標成 dirty。目前未追蹤的只有 `records/DISC-0002/`，不影響程式碼。

## 獨立重算

檔案：
- `/tmp/claude-0/-home-user/26cc272d-3593-56cf-8163-f42a48c2ab20/scratchpad/critic/recheck.py`：不 import 任何專案程式。用篩法（上限 2,000,000）判定質數，用整數比較算精確的 ⌊√(p/3)⌋，用 `python3 -I` 執行。輸出存在 `/tmp/claude-0/-home-user/26cc272d-3593-56cf-8163-f42a48c2ab20/scratchpad/critic/recheck_output.txt`。
- `/tmp/claude-0/-home-user/26cc272d-3593-56cf-8163-f42a48c2ab20/scratchpad/critic/psi12.py`：自己寫的 SPRP 測試加 Pollard rho。輸出存在 `/tmp/claude-0/-home-user/26cc272d-3593-56cf-8163-f42a48c2ab20/scratchpad/critic/psi12_output.txt`。
- 用專案程式重跑的結果：`/tmp/claude-0/-home-user/26cc272d-3593-56cf-8163-f42a48c2ab20/scratchpad/critic/drill_rerun.json`（只用於 A9 的可重現性比對）。

`recheck.py` 的關鍵輸出：
```
pi(100000) = 9592
H2: values n=0..39 min/max 41 1601 composite at []
H3: 40^2+40+41 = 1681 = 41^2? True prime? False
isqrt(p//3) != floor(sqrt(p/3)) for p in 0..N: [] count 0
  p=2: floor(sqrt(p/3))=0, p-2=0
  p=3: floor(sqrt(p/3))=1, p-2=1
  p=41: floor(sqrt(p/3))=3, p-2=39
H4: primes p<=N with Q_p: [2, 3, 5, 11, 17, 41]
H5: primes passing short check: [2, 3, 5, 11, 17, 41] mismatches: []
primes with floor(sqrt(p/3)) > p-2: []
non-lucky prime with longest run: 21557 run 7 bound 84
smallest constant bound c giving same equivalence on p<=N: 8
largest n^2+n+p actually evaluated under short-circuit all(): 99995
distribution of run lengths among non-lucky primes: {0: 8367, 1: 964, 2: 183, 3: 39, 4: 21, 5: 8, 6: 2, 7: 2}
H1 p=2..10000 failures: []
H5 with bound floor(sqrt(p/3))-1: mismatches (first 8): [7] count 1
primes p<=2000 with Q(sqrt(1-4p)) of class number 1: [2, 3, 5, 7, 11, 17, 19, 37, 41, 43, 61, ...]
  ...of these, Q_p FALSE: [(7, 27, 3, 0), (19, 75, 3, 0), (37, 147, 3, 0), (43, 171, 19, 0), ...]  (共 30 個)
```

`psi12.py` 的輸出：
```
318665857834031151167461 passes all 12 bases: True | factor: 399165290221 x 798330580441 | check: True
   base 41 passes: False
3317044064679887385961981 passes all 12 bases: True | factor: 1287836182261 x 2575672364521 | check: True
   base 41 passes: True
```
專案的 `is_prime_mr(318665857834031151167461)` 回傳 `True`，是誤判。

結論：H2、H3、H4、H5 的關鍵數字（9592 個質數、lucky 清單、H5 沒有不一致、1681 = 41²）**都和紀錄一致**。

## 未解決的疑點

1. **Lean 沒有編譯**。`norm_num` 能不能直接證明 `Nat.Prime 1601` 這類目標、`Nat.add_sub_cancel` 在目前 Mathlib 版本的名稱和形式對不對，都要等 CI 編譯才能確認。在那之前，H1/H2/H3 都不能升級成 `PROVEN_*`。
2. **literature 第 1、2、4、5 條都沒有線上複核**，我也連不到網路。第 5 條（√(p/3) 判準）的出處、作者和年代完全沒有資料，而 H5 的上界又只靠這一條。A3 已經說明，實驗資料本身無法區分 √(p/3) 和常數 8。
3. **第 3 條要修**：改成判別式或 Heegner 數的版本，否則 p=7 就是反例。
4. **MR 的上界要修**：把 `primality.py` docstring 裡的 3.3e24 改成 3.18e23（用 12 個底時）。這次實驗不受影響，因為最大值才 1e8。
5. **H3 的狀態字串**：`REFUTED_EXTENSION` 應該改成 §1 的合法狀態，或者在規範裡明確定義它，避免被自動工具誤讀。
6. **H4/H5 的雙實作結構**：如果要對範圍錯誤也有防護，B 實作應該另外產生質數清單（例如用篩法），並且自己寫範圍迴圈，不要和 A 共用 `q_holds` 和 `isqrt_p_over_3`。

## 處理狀況（orchestrator 補記，非 critic 原文）

| critic 指出 | 處理 |
|---|---|
| literature 第 3 條敘述錯誤（p = 7 反例） | 已改為「判別式 1−4p 本身」的正確版本，並保留修正紀錄 |
| MR 12 個底的上界寫錯 | 加入第 13 個底 41，文件改正，新增測試確認 318665857834031151167461 被判為合數（commit `5288d72`） |
| H5 證據弱 | 寫入 experiment.md 的已知限制，H5 不升級 |
| H4/H5 兩實作共用範圍與判斷程式 | 寫入 experiment.md 的已知限制；以 critic 的獨立重算作為補強 |
| H3 狀態名稱不合規範 | 改為 `SUPPORTED_IN_RANGE`，重跑實驗 |
| literature「1967 年以前已解決」過度概括 | 已縮限到第 1～4 條 |
| Lean 檔頭提到未定義的 `Q` | 註解已改寫 |
