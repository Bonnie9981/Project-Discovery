# DISC-0003 review.md

作者：reviewer（獨立 subagent）

我沒有參與這份研究。讀過的檔案：`docs/RESEARCH_STANDARDS.md`、`docs/AGENTS.md`、`.claude/agents/reviewer.md`、`records/DISC-0003/` 全部檔案（literature、hypotheses、experiment、experiment_data.json、novelty_data.json、search_evidence.jsonl、critic.md、proof.md、record.json）、`research/r001/disc0003/` 全部程式（impl_a、impl_b、impl_c、run、novelty_run）、`lean/Discovery/Consecutive.lean`、`lean/Discovery.lean`、`lean/AxiomCheck.lean`、`.github/workflows/lean.yml`、`tests/test_disc0003.py`、`discovery/check_record.py`（相關段落），以及 `git log` 和 `4668a62..122a190`、`506e0bc..122a190` 的 diff。格式參考 `records/DISC-0002/review.md`。

外部文字（OEIS 名稱與數據、search_evidence.jsonl 內容、工具輸出）我只當資料讀，裡面沒有出現要 agent 做事的指令。

## 審查項目

### R1. 各猜想的判定（對照證據）

| 猜想 | 證據 | 判定 | 理由 |
|---|---|---|---|
| H1 R(N) = d_odd(N) | Lean `card_reps_one`（CI 在 `4668a62` 通過，之後沒有改 lean/）；N ≤ 100000 三套實作一致；OEIS A001227 頁面由 AI 開過（S001），離線快照完全吻合 | `PROVEN_KNOWN` | 一般 N 由 Lean 證明，不是只靠有限檢查。A001227 的註解明寫這是已知結果（Sylvester）。 |
| H2a ≥2 項 = d_odd − 1 | Lean `card_reps_one_two_le`（假設 N ≥ 1）；三套實作；離線快照 A069283 完全吻合 | `PROVEN_KNOWN` | ℕ 減法不會截斷（1 永遠是奇因數），Lean 敘述與猜想等價。A069283 的名稱就是 d_odd(n) − 1。 |
| H2b ≥2 項無解 ⇔ 2 的冪 | Lean `repsTwoLe_eq_empty_iff`（假設 N ≥ 1）；三套實作 | `PROVEN_KNOWN` | 由 H2a 直接推出；「不禮貌數 = 2 的冪」是教科書結果，A069283 的零點就是 2 的冪。 |
| H3 奇/偶項數 ↔ 奇因數 d² < 2N / d² > 2N | 只有 N ≤ 100000 三套實作，無 Lean；E2、E3 在快照完全吻合 A082647、A131576 | `SUPPORTED_KNOWN` | 範圍內成立，**不是證明**。兩邊的計數序列都在 OEIS（依 hypotheses.md 預先寫好的規則，完全吻合就只能是 `*_KNOWN`）。附註：A082647 的 OEIS 名稱是「寫成 d 項連續正整數之和、d 是 n 的因數」，不是「奇數項」；兩者等價（k 項和 = k·a + k(k−1)/2，k ∣ N ⇔ k ∣ k(k−1)/2 ⇔ k 奇），紀錄沒有寫出這一步（見 R4-3）。literature 第 3 條的「< √(2N) 的奇因數」公式並沒有在任何實際讀過的來源原文中看到（快照只有名稱與數值），所以「已知」的依據是序列吻合，不是公式原文。 |
| H4 R_2 = #{d∣N : d² ≤ N} = ⌈τ/2⌉ | 前半：Lean `card_reps_two`；兩半：三套實作 N ≤ 100000（impl_b 已補上前半，見 R3 的 A5）；E6 完全吻合 A038548（名稱即「≤ √n 的因數個數」） | `SUPPORTED_KNOWN` | 前半已由 Lean 證明（單看那半是 `PROVEN_KNOWN` 等級），但整條猜想還包含「= ⌈τ/2⌉」，這半只有範圍內檢查，所以整條不能升級為 `PROVEN_*`。proof.md 有如實寫出這個差異。 |
| H5 一般公差的因數判準，D = 1..8 | N ≤ 10000，impl_a 與 impl_c 是實質證據；impl_b 對 H5 是同義反覆（critic A4，紀錄已承認）；無 Lean | `SUPPORTED_NOVELTY_UNCHECKED` | 範圍內成立，不是證明。它只是 2N = k(2a + (k−1)D) 的改寫，幾乎確定不是新的；但這條判準本身沒有任何來源被查證，D = 7、8 的序列也沒有送去新穎性層（只查了 D = 1..6）。依 §1 不能標 `KNOWN`。紀錄沒有宣稱它是新的。 |
| H6 R_2 ≤ R_1（對照組） | 三套實作一致的反例 N = 4；我手算 4 = 4 = 1+3 得 R_2(4) = 2，R_1(4) = 1（只有「4」）；我自己的列舉也得到同樣數值 | `REFUTED` | 反例由三個獨立實作確認，符合 §1。反例搜尋有作用。 |
| H7 R_2 > R_1 ⇔ 4 ∣ N（critic 追加） | N ≤ 100000 兩套實作（impl_c 沒有 `holds_h7`）；critic A3 有手寫證明草稿；我自己的列舉 N ≤ 20000 也一致；無 Lean | `SUPPORTED_NOVELTY_UNCHECKED` | 範圍內成立，不是證明。兩套實作已符合 §2b 的最低要求。這條陳述沒有送任何來源查證，所以不能標 `KNOWN`；它是 H1、H4 公式的初等推論，紀錄沒有宣稱它是新的。 |

「範圍內成立」與「證明」的區分：hypotheses.md、experiment.md、proof.md 都把 H3、H4 後半、H5、H7 寫成只有範圍內檢查，experiment.md「已知限制」第一條明寫「有限範圍的檢查不是證明」。**沒有發現誇大。**

### R2. Lean 定理是否忠實對應猜想

我逐條讀了定義與敘述，並在本機重新編譯（見「重現結果」）。

- `apSum D a k = ∑ i ∈ range k, (a + D·i)` 就是 a + (a+D) + … + (a+(k−1)D)，與 hypotheses.md 的記號一致。
- `reps D N` 是 `Icc 1 N ×ˢ Icc 1 N` 上的過濾。`mem_reps` 證明 (a, k) ∈ reps D N ⇔ 1 ≤ a ∧ 1 ≤ k ∧ apSum D a k = N，所以 [1, N] 的上界**不會漏解**，也沒有多算首項為 0 的寫法（critic A2 指出首項為 0 會讓 H1 失敗，Lean 的定義排除了這種情形）。
- `oddDivisors N = N.divisors.filter Odd`：正的奇因數，與 d_odd 相同。
- `card_reps_one : ∀ N, (reps 1 N).card = (oddDivisors N).card` ↔ H1（多涵蓋 N = 0，兩邊都是 0）。
- `card_reps_one_two_le : ∀ N, 1 ≤ N → (repsTwoLe N).card = (oddDivisors N).card - 1`，`repsTwoLe` = 過濾 `2 ≤ k` ↔ H2a。
- `repsTwoLe_eq_empty_iff : ∀ N, 1 ≤ N → (repsTwoLe N = ∅ ↔ ∃ m, N = 2 ^ m)` ↔ H2b。N ≥ 1 的假設是必要的，與猜想一致。
- `card_reps_two : ∀ N, (reps 2 N).card = (smallDivisors N).card`，`smallDivisors` = 過濾 `d * d ≤ N` ↔ H4 前半。⌈τ/2⌉ 沒有形式化。
- H3、H5、H7 沒有 Lean 定理；proof.md 寫了 H3、H5 沒有，H7 是事後追加，proof.md 沒提到它，但也沒有宣稱它被證明。
- 我另外用 `decide` 確認 `(reps 1 15).card = 4`、`(reps 2 4).card = 2`，與手算值和 H6 的反例一致。

結論：四個列在 `record.json` 的 `lean_theorems` 都存在，敘述忠實對應 H1、H2a、H2b、H4 前半。**沒有發現 Lean 敘述與猜想不符的地方**，與 critic A11 的結論一致。

### R3. critic 的每一項是否真的被處理（對照程式與文件）

| critic 項目 | 處理狀況 | 我查到的 |
|---|---|---|
| A1 邊界值 | 不需處理 | 沒有發現錯誤。 |
| A2 定義差異 | 不需處理 | 全紀錄一致用 a ≥ 1、k ≥ 1；我核對 impl_a（`range(1, …)`）、impl_b（`rest // k >= 1`）、impl_c（s0 = k + Dk(k−1)/2）、Lean（`mem_reps`）都一致。 |
| A3 H6 反例的完整刻畫 | **已處理** | 新增 H7（`run.py`、hypotheses.md、experiment.md 都有）；N ≤ 100000 兩套實作 SUPPORTED_IN_RANGE。 |
| A4 H5 的 impl_b 同義反覆 | **已記錄為限制** | experiment.md「已知限制」第二條寫明 impl_b 對 H5 沒有證據力，實質證據只有 impl_a 與 impl_c。critic 的附帶建議（兩套 H5 的右邊 `general_a`/`general_b` 是同一個式子，只是列舉因數的方法不同）沒有逐字寫進 experiment.md，只用「H5 本身也只是重述」帶過，屬輕微遺漏。 |
| A5 impl_b 的 H4 沒查前半 | **已修** | `run.py` 的 H4 `holds_b` 現在同時檢查 `== -(-τ // 2)` 與 `== small_b(n)`（commit `506e0bc`）。 |
| A6 off-by-one | 不需處理 | 我讀了三套迴圈邊界，同意 critic。 |
| A7 E13 的質數寫死 | **已修** | `EXTENSIONS["E13"]` 改成 `k >= 2 and all(k % p for p in range(2, isqrt+1))`，是真正的質數判斷；80 項結果不變（我在 `4668a62` 與 `506e0bc` 各跑一次，`extensions` 完全相同）。 |
| A8 E5 = A239140 等價 | **已寫入** | experiment.md 的 E5 列寫了 critic 的等價論證與「母體標準差」前提，並註明前提只從快照數值反推、沒讀 OEIS 原文。誠實。 |
| A9 E7 索引位移；A131576/A111775 名稱寫「consecutive integers」 | **已寫入** | experiment.md E7 列與「已知限制」第三條。 |
| A10 E13 的 NO_MATCH 誠實標示、封閉式 | **已寫入** | experiment.md E13 列寫了封閉式並說「不值得送審」；沒有把 E13 推往 `PENDING_REVIEW`。 |
| A11 Lean 忠實度 | 不需處理 | 見 R2。 |
| A12 literature「使用者 Chrome」用詞 | **已修** | literature.md 查詢紀錄表改成「AI 經 claude-in-chrome 操作使用者的 Chrome，**不是人工查證**」。 |
| 未解決 1：impl_c 結果在 dirty 目錄上跑 | **已處理** | `experiment_data.json` 的 `git_commit` 是 `506e0bc…`，沒有 `-dirty`，三套實作；我在乾淨 worktree 重現成功。 |
| 未解決 2：H3 補 Lean | 未做，已記錄 | proof.md 與 experiment.md 都寫 H3 沒有 Lean 證明，所以 H3 停在 `SUPPORTED_KNOWN`。 |
| 未解決 3：A239140 的標準差定義原文 | 未做，已記錄 | experiment.md E5 列有註明。 |
| 未解決 4：OpenAlex/arXiv/Crossref 未查 | 未做，已記錄 | literature.md 查詢紀錄表寫「未查」。 |

### R4. 其他發現（小問題）

1. **必要**：`record.json` 的 `status` 還是佔位的 `INCONCLUSIVE`。`check_record` 會比對本檔的 `STATUS:`，不改就會失敗（目前 `tests/test_records.py::test_all_committed_records_pass` 也因 review.md 還是佔位而失敗）。
2. experiment.md 寫「第一版（commit `4668a62`，兩套實作）結果除了實作數之外完全相同」。我在 `4668a62` 重跑：H1～H6 除 `implementations` 外確實完全相同，`extensions` 也相同，但**第一版沒有 H7**（7 筆 results，第二版 8 筆）。措辭應改成「H1～H6 與延伸序列除實作數外相同；H7 是第二版新增」。
3. literature.md 第 3 條與 experiment.md 的 E2 列把 A082647 寫成「奇數項的寫法數」，但它的 OEIS 名稱是「Number of ways n can be expressed as the sum of d consecutive positive integers where d>0 is a divisor of n」。兩者等價（見 R1 的 H3 列），但紀錄應寫出這一步，並註明「< √(2N) 的奇因數」公式不是從讀過的來源原文抄來的。
4. impl_c 沒有 `holds_h7`，H7 只有兩套實作。experiment.md 有如實寫「H7 兩套」，符合最低要求，但與 H1～H6 不對稱。
5. `experiment_data.json` 的 `env` 只有 Python 版本與平台，沒有 §2c 所說的套件、Lean toolchain、資料快照 SHA-256 等 provenance（§2c 針對 `python -m discovery run`，這裡是自訂的 run.py，所以不算違規，但之後的研究線最好統一）。`novelty_data.json` 的每筆結果有快照 SHA-256，這部分有記錄。
6. 狀態慣例：DISC-0002 的整體狀態是「取最弱、且已查證的那一項」（見其 review.md 最終判定第 3 點），不是單純「取主結果」。這次我取主結果 H1（理由見「最終判定」）。兩份紀錄的取法不同，建議在 RESEARCH_STANDARDS 明文寫下紀錄層級狀態的規則。
7. 我沒辦法自己開 CI 頁面（`gh` 需要另外取得權限，我沒有用）。CI 通過的依據是 orchestrator 提供的 run 45003700687 與 proof.md 的描述，加上我自己確認 `git diff 4668a62 HEAD -- lean` 是空的、`git log -- lean` 最後一次修改就是 `4668a62`，以及本機重新編譯成功。orchestrator 應確認 HEAD 的 CI（`lean` 與 `tests`）也是綠燈。

### R5. 新穎性判定

九級新穎性狀態（§1b），各序列：

| 序列 | 新穎性狀態 | 依據 |
|---|---|---|
| H1_R1（R(N)） | `MATCH_FOUND` | A001227（另有 A318874 也完全吻合；2φ(d) > d ⇔ d 奇，所以兩條本來就相同） |
| E1 ≥2 項 | `MATCH_FOUND` | A069283 |
| E2 奇數項 | `MATCH_FOUND` | A082647（名稱用字不同但等價，見 R4-3） |
| E3 偶數項 | `MATCH_FOUND` | A131576（名稱寫「integers」，資料是正整數版，critic A9） |
| E4 ≥3 項 | `MATCH_FOUND` | A111775（同上） |
| E5 ≤3 項 | `MATCH_FOUND` | A239140（等價依賴母體標準差的前提，未讀原文） |
| E6 公差 2 | `MATCH_FOUND` | A038548 |
| E7 公差 2、≥2 項 | `MATCH_FOUND` | A072670（n 位移一位） |
| E8 公差 3 | `MATCH_FOUND` | A117277 |
| E9 公差 3、≥2 項 | `MATCH_FOUND` | A243223 |
| E10 公差 4 | `MATCH_FOUND` | A334461 |
| E11 公差 5 | `MATCH_FOUND` | A334541 |
| E12 公差 6 | `MATCH_FOUND` | A334948 |
| E13 項數為質數 | `NO_MATCH_IN_SCOPE` | 離線快照 0 筆（80 項與「去掉開頭 0 的 20 項」我都自己掃過）；線上 OEIS 前 30 項查無（S002），關鍵字搜尋只讀第 1 頁（S003）。**不代表新**，且有平凡封閉式（critic A10）。不應升級，我也不建議提出 `PENDING_REVIEW`。 |

整份紀錄：`novelty.status = MATCH_FOUND`（基準 H1、H2a、H4 都有完全吻合），與 `record.json` 一致。

- 沒查成功的來源有被誠實標示：程式端線上 OEIS 是 proxy 403，每筆 `sources_failed` 都有記；OpenAlex/arXiv/Crossref 寫「未查」；claude-in-chrome 的查詢標明是 AI 操作、不是人工查證，所以不能拿來支持 `NOVELTY_SUPPORTED`。
- 沒有任何序列或猜想被標成 `PENDING_REVIEW`、`NOVELTY_SUPPORTED` 或 `NOVELTY_CONFIRMED`；AI 也不能給後兩者。
- **整份紀錄沒有任何「新發現」的宣稱。** literature.md「研究空白」、experiment.md 的 E13 列、record.json 的 `note` 都明寫 E13 不代表新。

## 重現結果

### 1. 照 experiment.md 的指令重現 experiment_data.json

- `git worktree add /tmp/rev 506e0bc`（experiment.md 指定的 commit），執行 `python -m research.r001.disc0003.run 100000 > out.json`（輸出放在 scratchpad，不在 repo 內）。
- 環境：Python 3.13.18，Linux-6.18.44-fc-v726-x86_64-with-glibc2.39。耗時 40.5 秒，低於 600 秒上限。
- 輸出的 `git_commit` = `506e0bced1a0fa782f86f77db9366263f0f1bcbf`，沒有 `-dirty`。
- **`results`、`extensions`、`params` 與 `experiment_data.json` 完全相同**（Python `==` 為 True）。
- 同一個 worktree：`python -m pytest -q tests/test_disc0003.py` → 3 passed；`python -m discovery.independence` → `checked 1 research dirs with impl_*.py, 0 problems`。
- 另外在 `4668a62` 重跑第一版：H1～H6 除 `implementations`（2 對 3）外相同，`extensions` 相同，沒有 H7（見 R4-2）。
- 完成後已 `git worktree remove`。`506e0bc..122a190` 之間只改了 records/ 下的文件，沒有改 research/、tests/、discovery/、lean/，所以 HEAD 的程式與重現用的程式相同。

### 2. 新穎性資料

- 主目錄 `data/oeis/raw/stripped.gz` 的 SHA-256 前 12 碼是 `c6d34403102c`，與 `novelty_data.json` 一致。
- 在主目錄執行 `python -m research.r001.disc0003.novelty_run`（輸出到 scratchpad）：14 個序列的 `status`、`matches`、`query`、`sources_checked` 全部與 `novelty_data.json` 相同；線上 OEIS 同樣是 proxy 403。
- 我另外寫了一個與 `discovery.novelty` 無關的掃描（對 stripped.gz 401,773 條做 80 項連續子字串比對）：H1_R1 → A001227、A318874；E1～E12 各自只命中上表的那一條；E13 的 80 項與「從 n = 3 起 20 項」都 0 筆。與 novelty_data.json 一致。
- names.gz 中各 A 號的名稱我也逐一核對過（見 R4-3、R5）。

### 3. Lean

- `git diff 4668a62 HEAD -- lean` 為空；`git log -- lean` 最後一次修改是 `4668a62`。
- 本機 `lake env lean Discovery/Consecutive.lean`（Lean 4.15.0）：12.6 秒，無錯誤、無警告。
- 檔案中沒有 `sorry`、`admit`、`axiom`、`native_decide`。
- 只匯入 `Discovery.Consecutive` 的 scratch 檔 `#print axioms`：`Consecutive.lean` 的 8 個定理（四個主定理加 `two_mul_apSum`、`mem_reps`、`mem_reps_one`、`mem_oddDivisors`）全部只依賴 `[propext, Classical.choice, Quot.sound]`。`#check` 印出的型別與 R2 所列相同。
- 本機無法跑完整的 `AxiomCheck.lean`：它 `import Discovery`，而 `Smoke.lean`、`R001.lean` 需要完整 Mathlib，本機只建了子集。完整的公理全檢與 `lean_decls` 交叉檢查以 CI 結果為準（R4-7）。

### 4. 我自己的獨立檢查

- 用另一種寫法（對每個 k 列舉 a，直接累加 k·a + Dk(k−1)/2，奇因數用直接試除）在 N ≤ 20000 檢查 H1、H3、H7：0 個不符；R_2(4) = 2、R_1(4) = 1。

### 5. 全套測試

- 主目錄 `python -m pytest -q`：37 passed、1 failed。失敗的是 `tests/test_records.py::test_all_committed_records_pass`，原因是 `check_record` 回報「DISC-0003/review.md: no 'STATUS:' line」，也就是本檔原本還是佔位內容。本檔寫好後，還需要把 `record.json` 的 `status` 改成一致才會通過（R4-1）。

## 最終判定

STATUS: PROVEN_KNOWN

逐項狀態：H1、H2a、H2b = `PROVEN_KNOWN`；H3、H4 = `SUPPORTED_KNOWN`；H5、H7 = `SUPPORTED_NOVELTY_UNCHECKED`；H6 = `REFUTED`。新穎性：整份 `MATCH_FOUND`；E13 = `NO_MATCH_IN_SCOPE`（不是新的，不升級）。

整份取 `PROVEN_KNOWN` 的理由：

1. 這份紀錄的主結果是 M1.1 基準 H1（標題、literature.md「研究空白」都寫明目的是檢驗流程能否重現已知結果並判成 `*_KNOWN`）。H1 與它的直接推論 H2a、H2b 在一般 N 上由 Lean 證明，CI 通過、只用三個標準公理，而且是已知結果（A001227、A069283）。
2. 這個狀態**只涵蓋 H1、H2a、H2b**。H3、H4 後半、H5、H7 只有範圍內檢查，不是證明；看本紀錄的人必須同時看上面的逐項狀態。
3. 我沒有像 DISC-0002 那樣取最弱的一項。H5 是定義的改寫，H7 是 critic 事後追加的初等推論，兩者都不是這份紀錄的研究目標。如果拿它們的 `SUPPORTED_NOVELTY_UNCHECKED` 當整份狀態，反而會讓人誤以為這份紀錄可能有沒查完的新東西。這和 DISC-0002 的取法不同，已列為 R4-6，建議明文規定。
4. 前提：CI 通過依據 orchestrator 提供的 run 45003700687（commit `4668a62`），之後沒有改 lean/。如果 HEAD 的 `lean` 工作失敗，這個判定要降為 `SUPPORTED_KNOWN`。

要求修正（不影響判定，但應在合併前處理）：

1. **必要**：`record.json` 的 `status` 從 `INCONCLUSIVE` 改為 `PROVEN_KNOWN`，然後跑 `python -m discovery.check_record` 與 `pytest` 確認通過。
2. **必要**：確認 HEAD（`122a190` 或之後）的 CI `lean` 與 `tests` 都是綠燈。
3. experiment.md「第一版結果除了實作數之外完全相同」改成「H1～H6 與延伸序列除實作數外相同；H7 是第二版新增」（R4-2）。依 §3 用附加說明的方式更正。
4. literature.md 第 3 條／experiment.md E2 列補上 A082647 名稱與「奇數項」的等價說明，並註明「< √(2N)」公式沒有在讀過的來源原文中看到（R4-3）。
5. 選做：experiment.md 補一句「兩套 H5 的右邊是同一個式子，只是列舉 2N 因數的方法不同」（critic A4 附帶建議）；impl_c 補 `holds_h7`；H3 補 Lean（成本低）；有網路時讀 A239140 原文確認母體標準差。

## 給 CEO 的摘要

1. 這次沒有新發現，也沒有宣稱新發現。這是 M1.1 的基準測試：讓整套流程去重現一個教科書結果，看它能不能正確判成「已知」。它判對了。
2. 主結果「把 N 寫成連續正整數之和的方法數 = N 的奇因數個數」（還有兩條推論）已經由 Lean 證明，GitHub 上編譯通過，所以整份紀錄標 `PROVEN_KNOWN`：已證明，但早就知道。
3. 其他幾條延伸說法只在 N ≤ 100000（或 10000）內用電腦檢查成立，不是證明，各自標成 `SUPPORTED_KNOWN` 或 `SUPPORTED_NOVELTY_UNCHECKED`。刻意放進去的一條錯誤說法（H6）被三套程式一致推翻，反例是 N = 4，代表找反例的機制有作用。
4. 我在乾淨環境照紀錄的指令重跑，結果完全一樣；新穎性比對也重跑了，另外用自己的程式掃過 OEIS 快照，結論相同。13 條延伸序列中 12 條在 OEIS 已有，唯一沒查到的（E13）是很平凡的組合，查不到不代表是新的。
5. 合併前要先把 `record.json` 的狀態改成和這份審查一致，並確認最新 commit 的 CI 是綠燈。
