# DISC-0014 審查：A071052 的 a(2n) = a(n) + 2n

審查者：reviewer（獨立 subagent，不是作者，也不是 critic）。審查對象：commit c669ba2。

## 審查項目

1. **critic 必修 1（論文 AI-use note）：已改好，但有條件。** 現在寫的是「attacked and reviewed by separate AI agents (critic.md, review.md), and machine-checked by Lean 4 in the repository's CI」。review.md 由本檔補上，所以前半句成立了。後半句的「CI 已通過」在 PR 的 CI 跑綠之前還不是事實。論文要等 PR 合併後才公開，到那時 CI 一定已經跑過，所以本審查接受這個寫法，條件是合併前 CI 必須是綠的。
2. **critic 必修 2（「two independent programs」）：已改好。** 論文 Checks 段改成「Two different algorithms … in `l07_a071052_even.py`」，另外寫明 critic 的第三套程式是分開寫的。experiment.md 也寫明「兩種算法在同一個檔案、共用手抄 DATA」。record.json 的 `candidates.proof` 還寫著「two implementations」，沒寫「independent」，不算錯，但可以順手改得更精確（見建議 1）。
3. **結論有沒有被證據支持：有。** 「對所有 n」這個說法是靠 Lean 定理 `a071052_double` 撐起來的，不是靠有限範圍的計算。數值檢查只拿來核對定義有沒有寫對，沒有被當成證明。
4. **Lean 定理有沒有對應到猜想：有。** 我逐行讀了 `step`、`seed`、`row`、`cnt`、`zeros`：`step` 就是三鄰居 xor（規則 150），種子只在位置 0，視窗是 −n..n 共 2n+1 格，定理對所有 n : Nat 成立（包含 n = 0，和 OEIS 的 offset 0 一致）。我在暫存副本裡加了 `#eval`：zeros(0..12) = [0,0,2,2,6,2,8,4,14,10,12,8,20]，和 DATA 相同；ones(0..12) = [1,3,3,5,3,9,5,11,3,9,9,15,5]，就是 A071053。proof.md 的定理對照表和檔案內容一致。
5. **有沒有空洞：沒有。** 搜不到 sorry、admit、axiom、native_decide、implemented_by、unsafe。`#print axioms a071052_double` = [propext, Quot.sound]。檔案已經加進 `lean/Discovery.lean` 的 import，CI 會編到它。研究規範寫的是「Lean 4 + Mathlib」；這份只用 core，不靠任何額外函式庫，條件只會更嚴，不影響判定。
6. **新穎性：誠實。** literature.md 和 record.json 都寫明關鍵的 A071053(2n) = A071053(n) 已經在 A071053 條目裡（Taylor 2020），而且是 GF(2) 上的標準事實。所以這不是新數學，只是把 OEIS 上的「conjectured」補上證明。arXiv、MathSciNet 沒查，也照實寫了。因為不宣稱新穎，這點不影響判定。
7. **外部資料：** 有兩筆查詢紀錄 S001、S002（claude-in-chrome）。我這次也試著連 oeis.org 抓 b-file 核對手抄的 DATA，被代理擋下（HTTP 403），critic 也遇到一樣的情況。目前只能確定 l07、critic 程式和 Lean `#eval` 三方一致，而且 ones 欄和 A071053 的已知開頭一致。讀到的資料裡沒有任何要我做事的文字。
8. **OEIS 草稿：** 已經補上「see A071053」，也加了「不要寫成大發現」的提醒。critic 建議把「[proved by _Chi Hsia_]」改低調一點，草稿沒有照做。這是署名風格的問題，留給使用者決定，不列為必修。

## 重現結果

所有計算都用 `discovery.limits.run_limited` 跑，都在上限內：

- `python research/r003/l07_a071052_even.py 2000`：輸出「OK: 0 <= n <= 1000: a(2n) = a(n) + 2n; cell-by-cell doubling holds; two methods agree to n = 2000; 67 DATA terms match」，約 0.8 秒。和 experiment.md 預期的開頭一致。
- `python research/r003/critic_c_a071052.py 3000`：輸出「OK N=3000: M1(Lucas)=M2(sim) rows, M3 counts; H1,H3 for n<=1500」，約 2.1 秒。
- `lean Discovery/A071052Even.lean`（Lean 4.15.0）：0 錯誤，約 1 秒。另外用暫存副本加 `#print axioms` 和 `#eval` 檢查，結果見審查項目 4、5，原檔沒動。
- `python -m discovery.independence`：0 problems。
- `python -m discovery.check_record`：寫這份 review.md 之前唯一的問題是「DISC-0014: missing review.md」，寫完後重跑：checked 14 records, 0 problems。

## 最終判定

STATUS: PROVEN_KNOWN

理由：Lean（只用 core，沒有 sorry，也沒有額外公理）證明了對所有 n ≥ 0 都有 a(2n) = a(n) + 2n，定義和 OEIS 對得上。關鍵的一步已經寫在 A071053 條目裡，是已知技巧，不宣稱新。

**必修：** 無。（合併條件：PR 的 Lean CI 必須是綠的，論文 AI-use note 的「machine-checked … in CI」才成立。）

**建議：**
1. record.json 的 `candidates.proof` 把「two implementations」改成「two methods in one script, plus the critic's separate script (n ≤ 3000)」。
2. 送出 OEIS 前，由使用者手動對一次 DATA 和 A071036 的列定義。這次連不上 oeis.org，沒辦法自動核對。
3. OEIS 草稿的「[proved by …]」可以考慮改成較低調的寫法，由使用者決定。

## 給 CEO 的摘要

A071052 這條 2004 年的「猜想」已經用 Lean 證明了，而且對所有 n 都成立。我重跑兩支檢查程式和 Lean 編譯，全部通過。critic 提的兩項必修都已經改好。這是 A071053 條目裡已知事實的一行推論，屬於習題程度，不是新發現。判定 PROVEN_KNOWN。送 OEIS 前請使用者自己看一眼條目原文，並確認 PR 的 CI 是綠的。
