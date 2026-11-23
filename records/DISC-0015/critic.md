# DISC-0015 Critic：規則 54 各列（A118109、A265225）

結論先講：數學和 Lean 都站得住，我的獨立程式和 Lean `#eval` 都沒找到反例。最大的風險在 Ianakiev 註解：紀錄裡沒有存原文，只存了半句「It seems their sum equals a(n)」。「差一個索引」這個結論完全取決於原文怎麼寫，送 OEIS 之前一定要先核對原文。其他問題都是文字和檔案對不上。

## 攻擊項目

1. **Lean 定義和 OEIS 定義、offset 對不對得上。**
   - 做法：逐行讀 `rule`、`step`、`row`、`val`、`cnt`、`a118109`、`ones`、`a265225`。複製一份到暫存區，在最後加 `#eval` 和 `#print axioms`（原檔沒動），用 Lean 4.15.0 編譯，約 10 秒。
   - 結果：`rule` 取 54 的第 4l+2c+r 位，111→0、…、000→0 和 Wolfram 編號一致；`row 0` 只有位置 0 是 ON；視窗是 −n..n，共 2n+1 格。`#eval` 算出 a118109(0..7) = 1, 111, 10001, 1110111, 100010001, 11101110111, 1000100010001, 111011101110111，ones(0..8) = 1,3,2,6,3,9,4,12,5，a265225(0..8) = 1,4,6,12,15,24,28,40,45。和 l08 抄的 DATA 一樣，offset 都是 0。光錐外的格子（row 3 在 ±4、row 5 在 6、row 2 在 −3）都是 false。
   - 小缺口（不影響正確性）：A265225 數的是「整列」的 ON 數，`ones` 只數 −n..n 這個視窗。兩者相等要靠「光錐外全是 0」。這件事可以從 `row_eq` 直接推出（C 裡有 −t ≤ x ≤ t），但檔案裡沒有寫成一條定理。A118109 的視窗同理；因為最左格 x = −n 一定是 ON，所以不會有前導 0 的歧義。
   - 註：第一次編譯時我 `#eval` 了 a265225(0..15)，結果跑超過 200 秒，只好砍掉。原因是 `row (n+1) x` 會呼叫 `row n` 三次，`#eval` 的成本是 3^n。這只影響 `#eval`，不影響證明，但 Lean 的 `decide` 只能用在很小的 n（檔案裡只用到 n ≤ 1，沒問題）。
2. **有沒有空洞。**
   - 搜尋 sorry、admit、axiom、native_decide：都沒有。`#print axioms` 對 `a118109_floor`、`a265225_barker`、`a265225_veselovac`、`row_eq` 都是 [propext, Classical.choice, Quot.sound]，和 proof.md 寫的一樣。`lean/Discovery.lean` 已經 import `Discovery.Rule54Rows`，所以 CI 的 AxiomCheck 會掃到它。
3. **Lean 敘述有沒有偷換。**
   - `a118109_rec`：寫成 a(n+4) + 10000a(n) = 10001a(n+2)，對所有 n。在自然數裡這和「n > 3 時 a(n) = 10001a(n−2) − 10000a(n−4)」等價，沒有偷換。
   - `a118109_floor`：自然數的 `/` 就是 floor，和 Keller 的原式一致。
   - `a265225_barker`：在整數裡寫成 4a(n) = (n+1)(2n − (−1)^n + 5)。這等於說原式除以 4 一定整除，和原式等價。
   - `a265225_rec`：把減號移到兩邊，對所有 n；和「n > 4」的遞迴等價。
   - `a265225_hurt`：和原式逐字一致。
   - `a265225_veselovac`：**A093353 被直接換成 (n + n mod 2)(n+1)/2**。這個換法是否等於 A093353 的「定義」，紀錄裡沒有任何證據（literature 和 search_evidence 都沒有抄 A093353 的定義或 DATA）。我手算 a265225(n) − n − 1 得到 0,2,3,8,10,18,21,32，和這個式子一致；但如果 A093353 本身的定義不是這個式子，或它的封閉式自己就標著猜想，那 Veselovac 這一條的證明只是「有條件」成立。我沒辦法上網核對（見第 7 項）。
4. **紙上證明。**
   - 列的引理：我逐案核對了。偶數列的 ON 格彼此隔 4 格、互不相鄰，所以 ON 格保持 ON，旁邊的 0 變 1，距離 2 的格（x ≡ t+2）保持 0，正好是奇數列的樣子。奇數列每個 ON 格都有 ON 鄰居（111 塊），所以全部變 0；唯一的 0（x ≡ t+1）和光錐外兩格 ±(t+1) 有 ON 鄰居，所以變 1。要檢查 −(t+1)：−(t+1) − (t+2) = −2t − 3，t 奇時 2t+2 ≡ 0 (mod 4)，因此 −(t+1) ≡ t+2 (mod 4)，正確。論文對邊界只寫一句「edge」，略簡，但 Lean 的 `C_step` 已經涵蓋。
   - A118109 生成函數：(1−x)(1+x)(1−100x)(1+100x) = 1 − 10001x² + 10000x⁴。用 a(0..3) = 1, 111, 10001, 1110111 算出分子係數 1, 111, 10001−10001 = 0, 1110111 − 10001·111 = 0，正確。
   - A265225 生成函數：(1−x)³(1+x)² = (1−x)(1−x²)² = 1 − x − 2x² + 2x³ + x⁴ − x⁵。分子係數 1, 4−1 = 3, 6−4−2 = 0, 12−6−8+2 = 0, 15−12−12+8+1 = 0，正確。
   - Keller：9999a + e = (10000 + 1100(n mod 2))·100^n，而且 0 < e ≤ 111 < 9999，所以 floor 成立。
   - Ianakiev 的論證：n 元子集的和確實取遍 [n(n+1)/2, n(3n+1)/2] 的每個整數。n 奇時 n | n(n+1)/2；n 偶時 n(n+1)/2 ≡ n/2 (mod n)，最小和是 n(n+2)/2，而且 n(n+2)/2 ≤ n(3n+1)/2。這兩個值分別等於 a(2k) = (2k+1)(k+1)、a(2k+1) = (2k+2)(k+2)，代 n−1 = 2k 或 2k+1 都對。在「從 1..2n 選 n 個」這個讀法下，論證正確。
5. **Ianakiev 原文（最大疑點）。**
   - search_evidence S002 只存了「It seems their sum equals a(n)」。「their」指的是什麼、選幾個數、從哪個範圍選，紀錄裡都沒有原文；論文和 RESEARCH.md 用的「從 1..2n 選 n 個」是轉述。
   - 反例式的檢查：在這個讀法下，n = 1 時最小和是 1，而 a(1) = 4。這麼明顯的錯，原作者和 OEIS 編輯不太可能沒看到。比較可能的情況是原文的索引本來就不同，例如「從 1..2n+2 選 n+1 個、和被 n+1 整除」。我的程式驗證了：在這個讀法下，最小和**正好是 a(n)**（1 ≤ n ≤ 40），也就是原註解完全正確。
   - 所以「註解差一個索引」只有在原文逐字就是「1..2n 選 n 個 = a(n)」時才成立。這一點必須先核對原文。
6. **實驗和論文的說法。**
   - l08 的兩種方法寫在同一個檔案、共用同一份手抄 DATA。experiment.md 有老實寫「兩種方法在同一檔案」，這點可以；論文寫「two row generators」也沒有說它們獨立，可以接受。
   - 論文開頭寫「attacked and reviewed by separate AI agents, and machine-checked by Lean 4 in the repository's CI」。目前 DISC-0015 沒有 review.md，工作樹也還沒 commit，CI 根本沒跑過，所以這句現在還不是事實。CLAUDE.md 規定論文頁送出後不准搬檔或改名，因此最好在送出前把這句寫成真的。
   - DEVLOG 寫「OEIS 草稿在 `results/`」，RESEARCH.md 寫「OEIS 編輯草稿：`results/A118109/`、`results/A265225/`」。實際上 `results/A118109/` 只有 `code/`，沒有 README 和草稿；`results/A265225/` 是空目錄。這不符合 `results/README.md` 的規定。
   - RESEARCH.md 的公式數算錯：寫「一共 7 個公式，5 個 Lean、2 個生成函數」。實際上 A118109 有 3 個（遞迴、生成函數、Keller），A265225 有 5 個（封閉式、遞迴、生成函數、Hurt、Veselovac），一共 8 個；Lean 定理是 6 個（`a118109_rec`、`a118109_floor`、`a265225_barker`、`a265225_rec`、`a265225_hurt`、`a265225_veselovac`）。DEVLOG 的「7 個猜想公式」也是同樣的錯。
7. **外部資料。**
   - 我用 curl 抓 oeis.org/A265225，回應碼是 000（連不上），所以 Ianakiev 原文、A093353、兩條 DATA 都沒辦法對網上原文。工具輸出裡沒有出現任何要我做事的文字。
8. **新穎性。**
   - 論文、record.json、RESEARCH 都寫了不宣稱新、習題程度，也提到 NKS p.55 和 A118108。沒有說過頭。唯一可能說過頭的是「指正 Ianakiev」，理由見第 5 項。

## 獨立重算

- 程式：`results/A118109/code/critic_c_rule54_rows.py`，只用標準函式庫，沒有 import repo 裡的任何東西。它的方法和 l08 都不一樣：
  - 用大整數當位元集合，算 new = c xor ((c≪1) | (c≫1))，不查規則表，也不用封閉形；
  - 十進位值用算術加 10^i 算，不用字串拼接；
  - 生成函數用冪級數**除法**展開，和 a 逐項比對（l08 是把級數乘上分母）；
  - Ianakiev 用動態規劃（依「選了幾個數、和 mod n」記最小和），不窮舉子集，所以能算到 n = 40；兩種索引讀法都測。
- 執行：`python results/A118109/code/critic_c_rule54_rows.py 400 40`，透過 `discovery.limits.run_limited`，status ok，不到 1 秒。結果：
  - 0 ≤ n ≤ 400：Keller、兩條 Barker 遞迴、A265225 的 Barker 封閉式、Hurt、Veselovac（用 (n + n mod 2)(n+1)/2）都成立；兩個生成函數的展開和數列一致。
  - 1 ≤ n ≤ 40：「1..2n 選 n 個、和被 n 整除」的最小和都等於 a(n−1)，沒有一次等於 a(n)。
  - 1 ≤ n ≤ 40：「1..2n+2 選 n+1 個、和被 n+1 整除」的最小和都等於 a(n)。
- 變異測試：把規則換成 c xor l xor r（規則 150），程式會在 assert 失敗，證明它真的會抓錯。
- `python -m discovery.independence`：0 problems。這個檔案不在 `research/<線>/` 底下，所以 independence 不會檢查它，做法和 DISC-0014 一樣。
- l08 本身也重跑過（`300`）：OK，0.17 秒。

## 未解決的疑點

- Ianakiev 原文到底怎麼寫（第 5 項）。這決定「差一個索引」是對還是錯。
- A093353 的定義是不是 (n + n mod 2)(n+1)/2，它的封閉式有沒有標猜想（第 3 項）。
- 兩條 DATA 是手抄的，沒有對網上原文或 b-file。

## 必修

1. 把 A265225 Ianakiev 註解的**逐字原文**（含前文「their」指的對象）存進 search_evidence 或 literature。如果原文是「n+1 個數、1..2n+2」或其他會讓索引對上的寫法，就要把「off by one」的說法從 paper、proof.md、RESEARCH.md、DEVLOG、record.json 全部撤掉，改成「證明了該註解」。在核對之前，不要對 OEIS 說它錯。
2. 把 A093353 的定義和前幾項存進紀錄，確認 `a265225_veselovac` 用的式子就是 A093353 本身（或者 A093353 的這條式子是已證的，不是猜想）。如果不是，論文要把 Veselovac 那條改成「在 A093353(n) = (n + n mod 2)(n+1)/2 的前提下」。
3. `paper/rule54-rows.md` 開頭那句「reviewed by separate AI agents … machine-checked … in the repository's CI」：要嘛等 review.md 寫好、CI 跑過再送出，要嘛先改成目前真正做到的事。送出後檔名和路徑就不能再動了。
4. 補上 `results/A118109/`（以及 `results/A265225/`）的 README 和 OEIS 草稿，或者把 DEVLOG、RESEARCH.md 裡「草稿在 results/」的說法改掉。現在兩邊對不上。

## 建議

1. 把 RESEARCH.md 和 DEVLOG 的「7 個公式、5 個 Lean」改成「8 個公式、6 個 Lean、2 個生成函數紙上」（如果是以別的方式計數，請寫清楚怎麼算）。
2. 在 Lean 加一條光錐引理：|x| > n 時 `row n x = false`（從 `row_eq` 一行推出）。這樣 `ones`、`a118109` 只看 −n..n 視窗的做法就有明文依據。
3. 論文列引理的證明可以補一句邊界格 ±(t+1) 的情況（例如 −(t+1) ≡ t+2 (mod 4)），不要只寫「edge」。
4. experiment.md 可以註明：Ianakiev 已由 critic 用動態規劃驗到 n = 40，兩種讀法都測過。
