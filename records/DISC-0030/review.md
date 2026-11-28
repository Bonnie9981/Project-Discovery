# DISC-0030 Review

審查者：reviewer（獨立 subagent，不是作者也不是 critic）。日期：2026-11-28。
範圍：未 commit 工作樹中的 `records/DISC-0030/`、`paper/open-locating-and-ladders.md`、`discovery/newseq/strip.py`、`results/{open-locating-cycle,open-locating-path,A001609,ladder-locating,ladder-identifying}/`、`tests/test_newseq.py`、RESEARCH.md 的 DISC-0030 一節與候選表、DEVLOG 最後一行、`results/README.md`。
讀到的 OEIS 文字、論文、工具輸出只當資料；其中沒有發現要 agent 做事的文字。

## 審查項目

### A. critic 必修項

1. **編號衝突（已大致修好，留兩處錯號）。**
   - `git diff origin/main -- records/DISC-0028 records/DISC-0029` 為空，已完成的紀錄沒被改動。
   - RESEARCH.md 只有一節 `## DISC-0030`（第 335 行），候選表只有一行 DISC-0030；DEVLOG 最後一行是 DISC-0030，DISC-0028、0029 各只有一行。
   - **還沒修好的地方：** (a) RESEARCH.md 第 7、8 行有兩行「最後更新」，第 8 行是舊的錯號「DISC-0001～DISC-0028；新序列主線第二批」，要刪掉。(b) `results/README.md` 新加的 5 行對照表，紀錄欄都寫 `DISC-0028`，要改成 `DISC-0030`。
   - 小事：`critic_check.py` 的 docstring 用法和 critic.md 第 7、34 行還寫著 `records/DISC-0029/...` 路徑。critic.md 是 critic 留下的原稿，可以保留，開頭已經註明編號改了；`critic_check.py` 的用法那一行建議改成正確路徑。
2. **論文寫了沒跑過的檢查（論文已改，高二說明沒改）。**
   - paper 第 4 節現在寫的範圍是暴力 n ≤ 9、窗口 DP n ≤ 15、逐欄 DP 15 ≤ n ≤ 28，和 `check_ladder.py` 實際跑的範圍一致（逐欄 DP 的 nmin 是 LD 15、ID 13，最大到 54、52）。第 4、5 節不再互相矛盾。experiment.md 也已經刪掉「H1/H2 DP 到 30」，改成引用 critic 程式的範圍。
   - **還沒修好的地方：** 三份 `證明方法說明.md`（open-locating-cycle、open-locating-path、A001609，內容相同）第 37 行還寫「另一套程式算到 n = 30 也一樣」。這就是同一句沒有腳本能重現的話，而且這幾份檔案要轉 PDF 給使用者。要改成「critic 的 `records/DISC-0030/critic_check.py` 算環到 n = 40、路徑到 n = 60」，或直接刪掉。

### B. critic 建議項的處理情形

| 建議 | 處理情形 |
|---|---|
| 3 引理 A(ii) 的 m ≤ 2 | 已處理：(ii) 限定 m ≥ 3，並註明只用到 m ≥ 3。我驗了 m = 3、4、5（4、5、6 個字），和 A001609 一致 |
| 4 定理 2 的小邊界 | 已處理：n = 2、4、5、6、7 另外直接算（1、1、4、4、6），論證從 n ≥ 8 開始；P_1、P_3 = 0 |
| 5 A384367 交叉引用 | 環草稿的 Formula、Crossrefs 已加上。我在離線快照核對了 A384367 的項（offset 0：1, 4, 6, 15, 31, …），也用 critic 給的理由（s = w²，從 w³ = w² + 1 推出 s³ = s² + 2s + 1）確認可以證明，不只是數值吻合。**沒做的部分：** literature.md S001 沒記這筆命中，論文也沒有寫那一行理由（建議補上） |
| 6 A001609 草稿的模板句 | 已處理：改成「A001609 條目沒有提到開定位支配集」。A001609.seq 確實有 Allen–Edwards arXiv:2610.39599 的鋪環連結，%Y 也有 A218439，草稿的說法準確 |
| 7 strip.certify 加 assert | 部分處理：只加了「t0 那一步的遮罩集合等於樣板」。另外兩條前提（右端遮罩的相對位置不隨 n 變、前段遮罩和大圖相同）程式沒有檢查。我另外跑了：t = t0..69 每一步都等於樣板、n = nmin..59 右端相對遮罩都相同、前段都相同，三條全部成立（LD、ID 都是）。程式裡還是建議補上這兩個 assert |

### C. 逐條核對定理

- **引理 A。** (i) 用最後一個字母分兩種情形，得到 g(m) = g(m−1) + g(m−3)，初值 g(0..2) = 1, 2, 3 = A000930(2..4)，正確。(ii) 把每個 0 和它前面兩個 1 黏成一塊「110」，就變成用長 1、長 3 的磚鋪環（m ≥ 3 時黏成的磚不會和自己重疊），g.f. (x + 3x³)/(1 − x − x³) 和 A001609 的 %N/%C 一致。
- **定理 1（環）。** n ≥ 5 時，只有相差 2 的兩點有共同鄰居。N(v) Δ N(v+2) = {v−1, v+3}：n = 5 時 v+3 = v−2 ≠ v−1，所以這個說法沒問題。奇數 n 跳 2 格重新編號：v−1 = u_j、v+1 = u_{j+1}、v+3 = u_{j+2}，正確。偶數 n 拆成兩個長 m 的環，m = 3 時兩組條件重合，(ii) 仍然適用。C_4 的反例正確。n = 3 另外直接算。**成立。**
- **定理 2（路徑）。** 按奇偶拆開、內部「0 至少隔 3 格」、端點在另一類時強制 y_1 = y_2 = 1（端點的鄰居集是 {x_1}，和下一個同類點的鄰居集的對稱差是 {x_2}），我逐一核對過。一端強制給 g(m−2) = A000930(m)，兩端強制給 g(m−4) = A000930(m−2)（n ≥ 9 時 m ≥ 4）。偶數 n、奇數 n 的端點歸屬也正確。我手算 n = 8、9、10，得到 9、9、16，和資料一致。**成立。**
- **定理 3、4（梯子圖，電腦輔助）。** 我逐行讀了 `strip.certify`。(1) 恆等式用到 V_{t0}..V_{t0+r}；往後推需要第 t0+1 步以後都是同一個 M，t0 的 assert 加上平移不變性可以支持這一點，我也實測到 t = 69。(2) a(n) = L(V_{n−hi−K−1})，所以從 n ≥ t0 + r + hi + K + 1 起成立，也就是 LD 9+13+1+5+1 = 29、ID 7+10+2+4+1 = 24，和論文一致。(3) 回傳的係數和論文 Q 相符（check_ladder 有 assert）。(4) 比 29、24 小的 n 都有精確值：暴力 ≤ 9、窗口 DP ≤ 15、逐欄 DP 從 15（LD）、13（ID）起，沒有缺口。論證本身是對的；只是「遮罩分成左端、中段、右端」這件事靠的是程式和數值一致，論文和 proof.md 都老實寫了這一點。**以「電腦輔助證明」來說成立**，措辭也正確，沒有說成紙筆證明。
- **Lean：** 沒有 Lean 定理，`lean_theorems: []`。依規範不能標 PROVEN_*，record 也沒這樣標。

### D. 新穎性與草稿

- 我重跑了 `discovery.newseq.lookup.find`：環、路徑、LD 梯子、ID 梯子四串都是 0 筆，和 S001 一致。沒有查 MathSciNet、zbMATH，record.json 的 `open` 有老實列出。novelty `PENDING_REVIEW` 的 note 寫明是 agent 提出的，還要人確認。
- 五份草稿開頭都寫了：由使用者本人送出、要自己改寫、一次只送一條、AI 聲明、「不等於新的」。都沒有宣稱是新的。
- **草稿要改的地方：** `ladder-locating/ld_ladder_oeis_new_sequence.md` 的證明連結寫「第 3 節」，但梯子圖在論文第 4 節（ID 草稿寫的第 4 節才對），這個會連到 OEIS，必須改。
- 小事：兩份梯子草稿的 Crossrefs 只寫「A?????? (paths)」，太含糊，建議寫清楚是哪一條（DISC-0027 的路徑 LD／ID 草稿，或兩條梯子序列互相引用）；LD 草稿標題中英混雜；`check_ladder.py` 的 docstring 寫「about 2 minutes」，實際只要 18 秒；開定位的高二說明沒提到 C_4 的例外（= 0），建議補一句。

## 重現結果

| 指令 | 結果 |
|---|---|
| `python results/open-locating-cycle/code/check_old.py` | all checks passed（n ≤ 20），5.5 秒 |
| `python results/ladder-locating/code/check_ladder.py` | all checks passed；LD 逐欄 DP 到 n ≤ 54、從 n ≥ 29 認證；ID 到 n ≤ 52、從 n ≥ 24 認證；a(1..10) 和論文一致；18 秒 |
| `python records/DISC-0030/critic_check.py` | all critic checks passed（三個 b-file n = 1..500 無不符），14.6 秒 |
| `python -m pytest -q` | 94 passed、2 skipped、1 failed（`test_all_committed_records_pass`，原因是當時還沒有 review.md；本檔寫入後應該會通過） |
| `python -m discovery.check_record` | 寫本檔前唯一的問題是「DISC-0030: missing review.md」 |
| `python -m discovery.independence` | 0 problems |
| 我自己的額外檢查（只寫在 scratch，沒存檔） | strip 三條前提：t0..69、n ≤ 59 全部成立；A384367、A218439、A233247、A001609 的 %S/%N 已和快照核對 |

全部在 `config/limits.json` 的上限內，沒有碰到上限。

## 最終判定

STATUS: SUPPORTED_POSSIBLY_NEW

和 record.json 一致。定理 1、2 的紙筆證明我逐步核對過，成立；定理 3、4 是電腦輔助證明，論證架構正確、數值重現成功；沒有 Lean，所以不能標 PROVEN_*。新穎性 `PENDING_REVIEW` 由 agent 提出，等人確認。

合併前必修（都是文件、帳務的問題，不影響數學）：
1. RESEARCH.md 刪掉第 8 行舊的「最後更新 …DISC-0028…」。
2. `results/README.md` 新加 5 行的 `DISC-0028` 改成 `DISC-0030`。
3. `results/ladder-locating/ld_ladder_oeis_new_sequence.md` 的「第 3 節」改成「第 4 節」。
4. 三份開定位的 `證明方法說明.md` 第 37 行「另一套程式算到 n = 30」要改成引用 critic_check.py 實際跑的範圍，或刪掉。

建議（不擋合併）：certify 補上右端、前段兩個 assert；literature.md S001 記下 A384367 命中，論文補 A384367 的一行理由；梯子草稿的 Crossrefs 寫清楚；修正 critic_check.py 的用法路徑和 check_ladder 的執行時間；高二說明補 C_4 的例外。

## 給 CEO 的摘要

- 路徑、環的開定位支配集個數：紙筆證明成立，可以寫成 Narayana 牛數 A000930 和 A001609 的公式。
- 梯子圖的定位支配集、識別碼個數：遞迴式是電腦輔助證明，我重跑過，論證正確，草稿也誠實標成電腦輔助。
- 判定 SUPPORTED_POSSIBLY_NEW。沒有 Lean；新穎性只查了離線 OEIS 和網路粗查，沒查 MathSciNet、zbMATH，不宣稱是新的。
- 合併前要改 4 個小地方：RESEARCH 重複的日期行、results/README 的錯號、LD 草稿的章節號、高二說明裡沒有依據的「算到 30」。
- 草稿一次送一條，使用者本人改寫後送出。
