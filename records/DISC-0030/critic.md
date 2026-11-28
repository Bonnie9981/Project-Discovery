# DISC-0030 Critic（審查時誤以為編號是 DISC-0029；main 上 DISC-0028、0029 已被別的研究使用，本批定為 DISC-0030）

critic：critic（獨立 subagent，opus）
日期：2026-11-28
對象：paper/open-locating-and-ladders.md 定理 1–4、discovery/newseq/strip.py、results/open-locating-cycle|open-locating-path|ladder-locating|ladder-identifying|A001609/、tests/test_newseq.py。

> 這份檔放在 `records/DISC-0029/`，不是 `records/DISC-0028/`：`records/DISC-0028/` 已是 main 上完成的紀錄（A308758 家族，PR #48），裡面的 critic.md／review.md 是那個紀錄的，不能覆蓋（見必修 1）。
> 讀到的資料（OEIS .seq、論文草稿）裡沒有要 agent 做事的文字。

## 攻擊項目

### 必修

1. **紀錄編號衝突，改到了已完成的紀錄。** `git show HEAD:records/DISC-0028/record.json` 是 `R-003`「序列關係挖掘…A308758…」，狀態 SUPPORTED_NOVELTY_UNCHECKED，已經合併進 main（commit 36acf13、d09d3d4）。工作樹把它的 `record.json`、`experiment.md`、`hypotheses.md`、`literature.md`、`proof.md` 改成本批內容（`git diff --stat` 共 5 檔），但 `critic.md`、`review.md`、`search_evidence.jsonl` 還是舊紀錄的。這違反「不改已完成的 records/DISC-*」。RESEARCH.md 現在也有兩個「## DISC-0028」小節（第 324、329 行），DEVLOG 也有兩行 DISC-0028。修法：`git restore records/DISC-0028/`；本批改成 DISC-0029（origin/main 最大號是 0028）；`results/{open-locating-cycle,open-locating-path,ladder-locating,ladder-identifying,A001609}/README.md` 裡的 DISC-0028 改成 DISC-0029；RESEARCH/DEVLOG 的新行也改號。註：我建了 `records/DISC-0029/`，所以在補上 RESEARCH 小節之前，`tests/test_research_summary.py` 會報缺 DISC-0029（我跑過，就是這一條失敗）。
2. **論文寫了沒跑過的檢查。** paper 第 4 節說「brute force over all 2^(2n) subsets for n ≤ 10, the window DP … for 11 ≤ n ≤ 14」，但 `check_ladder.py` 的暴力只跑 `range(1, 10)`（n ≤ 9），窗口 DP 跑 n ≤ 15；第 5 節自己也寫「brute force (n ≤ 9)」。第 4、5 節互相矛盾，而 OEIS 會連到這頁。要把第 4 節改成實際跑的範圍（暴力 n ≤ 9、窗口 DP n ≤ 15、逐欄 DP 從 n = 15（LD）／13（ID）到 54／52）。另外 experiment.md 說 H1/H2「DP 到 n = 30 一致」，但 repo 裡沒有能重現這句的腳本（check_old.py 只做暴力 n ≤ 20）。要嘛補腳本，要嘛刪掉這句。（我的 critic_check.py 有跑環 DP 到 n ≤ 40、路徑 DP 到 n ≤ 60，可以拿來引用。）

### 建議

3. **引理 A(ii) 的 m ≤ 2 慣例寫錯（不影響定理）。** 照論文寫的「no zero has *another* zero at cyclic distance 1 or 2」：m = 1 時 "0" 也合法（2 個字），m = 2 時 "01"、"10" 也合法（3 個字）。但論文說兩者都是 1。要讓答案是 1，得把「繞一圈回到自己」也算進去（自己和自己的距離是 m ≤ 2）。定理 1 只用到 m ≥ 3（偶數 n ≥ 6），所以只是措辭問題：改成「a zero may not be at cyclic distance 1 or 2 from any zero, itself included (going around)」，或直接把 (ii) 限制在 m ≥ 3。
4. **定理 2 的小 k 邊界沒寫清楚（數值是對的）。** (a) 偶數 n、k = 1（P_2）：一個類只有 m = 1 個點，「forced 11」要用到 x_2，可是 x_2 不存在。結果 1 = A000930(1)² 是對的，但要直接算。(b) 奇數 n、k = 2、3：偶類有 m = 2、3 個點，兩端各強制 11 會重疊，此時 g(m−4) 沒有定義。實際答案都是 1，剛好等於 A000930(0) = A000930(1) = 1。建議補一句「m ≤ 3 時所有字母都被強制為 1，數一下是 1 = A000930(m−2)」。我逐步檢查了其他步驟（奇偶拆分、跳 2 重排時 v−1 = u_j、v+1 = u_{j+1}、v+3 = u_{j+2}、n ≥ 5 時只有距離 2 的點對有共同鄰居、C_4 反例、路徑端點強制 y_1 = y_2 = 1、兩端都在 X 時沒有額外條件），都沒找到反例。
5. **OEIS 漏了一筆交叉引用：A384367。** 我在離線全庫掃資料行（含去掉開頭 0、差分、部分和、除以 gcd、奇偶項子序列，連續 8 項比對）。四條序列本身都沒命中。但環序列的奇數項 4, 6, 15, 31, 67, 144, … 正是 **A384367**（1, 4, 6, 15, 31, …，a(n) = a(n−1) + 2a(n−2) + a(n−3)），也就是 OLD(C_{2n+1}) = A384367(n)（n ≥ 1）。理由：w³ = w² + 1 時令 y = w²，得到 y³ = y² + 2y + 1，所以 A001609 的奇數項二分滿足 A384367 的遞迴；再對 3 個初值，我也數值核對到 n = 15。偶數項命中 A218439、路徑偶數項命中 A233247，草稿已經引用。建議環草稿的 Crossrefs 加 A384367，literature.md 的 S001 補這筆命中。
6. **A001609 編輯草稿的開頭是套用模板。** 草稿寫「查重：離線 OEIS 全庫找不到這串數字」，但 A001609 本來就在 OEIS，這句放在這裡會誤導人。建議刪掉，或改成「環 C_n 序列本身找不到」。草稿的其他說法我和 A001609.seq 原文對過，是準確的：%C 已有「ring lattice … molecules m sites wide」（m = 3 就是用 1、3 鋪環，和引理 A(ii) 同一件事），%Y 已有 A218439。可以考慮在留言點明「這個解釋可由現有的 ring-lattice 解釋推出」，比較誠實。
7. **strip.py 的 `lo` 不是「第一個固定步」。** 我逐步比較了 `interior_vectors` 每一步的遮罩集合和樣板集合，見下一節「獨立重算」第 3 點。LD 在 t = 0..3 不同；ID 在 **t = 3 = lo** 仍然不同（缺 5 個樣板平移：它們在左端不存在，`setup` 只算「非樣板遮罩」，沒算「缺少的樣板」）。所以 docstring／論文「t ≥ lo 之後都是樣板」這個講法是錯的。但 certify 用的是 t0 = lo + K（LD 9、ID 7），推廣時只需要第 t0+1 步以後固定；我驗證了 t ≥ 4 每一步都等於樣板集合，所以 nfrom（LD 29、ID 24）仍然正確。建議在 `certify` 裡加 assert：t0+1..T 每步遮罩集合等於樣板；右端遮罩相對位置不隨 n 改變；前段遮罩和大圖相同。目前這三件事只靠「和窗口 DP 數值一致」支持。
8. **其餘 strip.py 邏輯我查過、沒找到漏洞：**
   - 位元位置 (−dc)·w + r ≤ (K−1)w + w−1 < nb，遮罩不會跨出 K 欄（實測 LD 最大跨度 4 = K−1，ID 3 = K−1）。Python 對負數 `o // w`、`o % w` 取 floor，對應正確。
   - `count(n, Vs[n−hi−K−1])` 的索引：Vs[t] 是處理完第 t 欄的向量，start = n−hi−K，接上剛好不重不漏。
   - 收尾是 V 的固定線性函數：我實測 n = 15..40 時，右端遮罩（相對於 n）完全相同；G_n 中最大欄 < start 的遮罩也和大圖完全相同。
   - 指標推導：恆等式用到 V_k..V_{k+r}，往後推只需要第 k+1 步以後固定；a(n) = L(V_{n−hi−K−1})，推出 n ≥ t0 + r + hi + K + 1。和程式回傳值一致。
   - 只保留極小遮罩不影響計數（命中全部遮罩 ⇔ 命中全部極小遮罩）。
   - 距離 ≥ 3 的點對只要求支配，這點對：LD 的遮罩是 N[u] 的超集，ID 的 N[u]、N[v] 不相交。

## 獨立重算

`records/DISC-0029/critic_check.py`（只用標準函式庫，不 import repo；跑約 14 秒，log 在 `logs/python_records_DISC-0029_critic_check.py.log`）。算法和 check_old.py／strip.py／transfer.py 不同：

- 子集暴力用位元遮罩，直接比較 code：環 n = 3..18、路徑 n = 1..18、梯子圖 LD/ID n = 1..8。
- 逐欄 DP：狀態是最近 4 欄的 S 位元。某一欄的鄰域湊齊時，直接算出實際的 code（N(v)∩S 或 N[v]∩S），和欄距 ≤ 2 的所有點比較。為什麼只比欄距 ≤ 2 就夠：兩個非空 code 相等，表示有一個 S 的點同時鄰接（或等於）兩點，所以兩點距離 ≤ 2。這個方法沒有遮罩、沒有樣板，也不用 BM。
- 環用 DP 時，把前 4 位放進狀態，最後再檢查繞回來的 code；n = 9..12 和暴力互相核對過。

結果全部一致：
- H1：OLD(C_n) 公式，暴力 n ≤ 18、DP n ≤ 40。
- H2：OLD(P_n) 公式，暴力 n ≤ 18、DP n ≤ 60。
- H3、H4：梯子圖 LD、ID 的 g.f. 展開，暴力 n ≤ 8、DP n ≤ 60（DP 和暴力在 n ≤ 8 也互相核對過）。
- b-file：`b_old_cycle.txt`（n = 3..502）、`b_old_path.txt`、`b_ld_ladder.txt`、`b_id_ladder.txt`（n = 1..500），全部和我獨立重建的公式／g.f. 一致，0 筆不符，沒有缺號。
- 四份草稿的 Data 行（offset 3/1/1/1，約 250 字元）逐項等於 b-file。
- 上面 strip.py 的逐步檢查用的是暫存腳本（會 import strip.py；這是對 strip.py 本身的檢查，不算獨立重算）：LD/ID 在 t ≥ 4 每步遮罩 = 樣板；右端相對遮罩 n = 15..40 不變；前段遮罩和大圖一致。
- `python -m discovery.independence`：通過（0 problems）。

## 未解決的疑點

- 定理 3、4 仍然是電腦輔助證明。strip.py 的三個前提（第 t0+1 步以後固定、右端不隨 n 變、前段遮罩一致），我只在 T = 60、n = 15..40 實測，程式沒有對任意 n 證明；不過從圖的平移不變性看，這三點都說得通。我的 DP 到 n = 60 和 g.f. 一致，是數值上的獨立支持，不是證明。
- 新穎性：只查了離線 OEIS 資料行和變形（長度 8 視窗，只試了三個起點）。沒查 MathSciNet/zbMATH，也沒查 OEIS 之外的開定位支配集計數文獻。
- 沒有 Lean 形式化；依規範不能標 PROVEN_*。
