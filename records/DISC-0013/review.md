# DISC-0013 Review

審查者：reviewer（獨立 subagent），2026-11-22。只新增本檔，沒有改其他檔。

## 審查項目

1. **結論有沒有證據支持。** 主結論（n ≥ 1：n+1 不是 2 的次方時 a(2n+1) = 2a(n)；n+1 = 2^k 時 a(n) = a(2n+1) = 1；死光 ⇔ n+1 = 2^k）由 Lean 定理支持，對所有 n 成立，不是有限範圍的檢查。數值（n ≤ 40、死亡 n ≤ 2000、54 項 DATA）只當作交叉檢查，文件沒有把數值範圍說成證明。
2. **Lean 敘述和 OEIS 定義對不對得上。** 我親自 `#check`／`#print`：
   - `nstep n y = ((y <<< 1) ^^^ (y >>> 1)) &&& (2^n − 1)`、`niter` 從種子 1 出發：零邊界規則 90，左端單一種子，和條目的 PROG 一致（DISC-0009 已核對）。
   - `EvPer f p := ∃ T, ∀ t ≥ T, f (t+p) = f t`；`LeastPer f p := 0 < p ∧ EvPer f p ∧ 沒有更小的正最終週期` = 最小正最終週期，就是 a(n)。
   - `a268754_odd : 1 ≤ n → ¬∃k, n+1 = 2^k → LeastPer(n 格) p → LeastPer(2n+1 格) (2p)`；`a268754_odd_iff` 是雙向版；`a268754_odd_exception` 兩邊都 LeastPer 1；`dies_iff : 1 ≤ n → (Dies n ↔ ∃k, n+1 = 2^k)`，`Dies n := ∃t, niter n t 1 = 0`。和猜想 H1–H3 一一對應。
   - 剩下的缺口（非阻擋）：「最小正最終週期存在」沒有在 Lean 證（有限狀態的鴿籠原理，數學上顯然，OEIS 定義本身預設它）。`exists_leastPer_iff` 證了兩邊同時存在或同時不存在，所以只差這一個一般引理。proof.md「敘述差異」已誠實寫明。
3. **公理與 sorry。** grep `sorry|admit|axiom |implemented_by|extern`（A268754Odd、Rule26、Rule26Even）沒有結果。五個主要定理的 `#print axioms` 都只有 [propext, Classical.choice, Quot.sound]。檔案有被 `lean/Discovery.lean` import，所以 CI 的 AxiomCheck 會檢查到。
4. **證明論證。** 逐步讀了 proof.md 和 paper/a268754-odd.md：奇偶、間隔展開（右端 y_n = 0 的處理）、奇數週期矛盾（需要「永不死」，由 dies_iff 提供，沒有循環論證）、偶數寬度核只有 0（奇數位從左往右、偶數位從右往左，n 偶數時 n−2 是偶數，推得通）、強歸納。沒找到漏洞。
5. **新穎性。** 狀態 PROVEN_KNOWN，novelty = NO_MATCH_IN_SCOPE，沒有宣稱新。沒查的來源（arXiv、MathSciNet、Math Fun、條目連到的 SE 聊天記錄）在 literature.md 和 record.json 都有寫。critic 建議 9（和 MOW 1984「Π_{2N} = 2Π_N」的關係更近）已經寫進 literature.md。
6. **paper/a268754-odd.md 的英文敘述。** 定理敘述準確，n ≥ 1、例外句寫成 a(n) = a(2n+1) = 1，沒有誇大（沒有說 new，有 LLM 致謝）。建議（非阻擋）：
   - 「Formal verification」段落補一句：Lean 定理的形式是「若 p 是 n 格的最小最終週期，則 2p 是 2n+1 格的最小最終週期」（另有雙向版 `a268754_odd_iff`），最小週期存在（鴿籠原理）沒有形式化。現在這段只列三個定理，讀者可能以為函數等式已經完整形式化。
   - 「Numerical cross-check by two independent implementations」：兩個實作放在同一個檔案（critic 第 7 點），說 "two implementations" 比 "independent" 精確；critic 另有第三套閉式重算（`research/r003/critic_c_a268754.py`）可以一起列出。
7. **paper/a268754_oeis_edit_draft.md。** FORMULA 新增句和 Lean 一致。COMMENTS 句寫「put the n-wire on the even cells」：用 1 起算的格子編號是對的（第 i 位 → 第 2i+1 位 = 第 2i+2 格），但 paper 用的是 0 起算的位元，說「odd bits」，兩邊讀起來會打架。建議改成「cells 2, 4, ..., 2n」。草稿明確寫由使用者本人送出、Claude 不代送，符合安全規則。
8. **條目名稱等價。** A268754 名稱是 B1/S 規則的 n×1 長方形振盪子，和零邊界規則 90 等價沒有另外論證（沿用 DISC-0009 的非阻擋項），54 項數值一致。
9. **嵌入指令。** 讀過的 literature、paper、critic、腳本輸出裡沒有要 agent 做事的文字。

## 重現結果

- `python -m discovery.quiet -- python research/r003/l06_a268754_odd.py 40 2000`：exit 0，輸出 `OK: 1 <= n <= 40: a(2n+1) = 2a(n) unless n = 2^k-1 (then both 1); way1 == way2; matches 54 OEIS terms; spread lemma n <= 30; dies iff n+1 = 2^k for n <= 2000`，和 experiment.md 的預期一致。完整紀錄：`logs/python_research_r003_l06_a268754_odd.py_40_2000.log`。
- `cd lean && LEAN_PATH=/tmp/claude-0/lb lean Discovery/A268754Odd.lean`（Lean 4.15.0）：exit 0，沒有錯誤也沒有警告，約 3.5 秒。scratch 副本加上 `#check`、`#print axioms` 的結果見審查項目 2、3。
- `python -m discovery.independence`：3 個 dirs，0 個問題。
- `pytest tests`：65 個通過，只有 `test_records` 因為「DISC-0013: missing review.md」失敗；本檔就是要補這一項。

## 最終判定

STATUS: PROVEN_KNOWN

和 record.json 一致，不用改。理由：主定理對所有 n ≥ 1 在 Lean（只用 core、標準公理）裡證完，敘述對得上 OEIS 的定義；重現通過。用的是已知技巧，也沒有完整查過文獻，所以不宣稱新。沒有必修項。審查項目 2、6、7 的建議（補鴿籠存在引理、paper 註明形式化的確切形式、COMMENTS 的格子編號寫法）在送 OEIS 前處理比較好，但不影響判定。

## 給 CEO 的摘要

A268754 條目裡「奇數項 a(2n+1) = 2a(n)，n = 2^k − 1 時例外」和「n+1 是 2 的次方時格子會死光」這兩句，現在都有對所有 n 成立的 Lean 證明，我自己重新編譯過，也重跑了數值檢查，都通過。判定 PROVEN_KNOWN：證明是對的，但技巧是已知的，不宣稱新。OEIS 草稿可以用，送出前建議改兩個小地方：(1) paper 註明 Lean 沒有證「最小週期存在」（這是顯然的鴿籠原理）；(2) COMMENTS 那句的「even cells」改成「cells 2, 4, ..., 2n」，避免和 paper 的位元編號混淆。草稿要由使用者本人登入送出。
