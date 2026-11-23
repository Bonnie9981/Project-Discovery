# DISC-0016 審查：A085588 的週期整除 2^D(2^s−1)

審查者：reviewer（獨立 subagent，不是作者，也不是 critic）。

## 審查項目

1. **critic 必修 1（445 → 455）：已改好。** literature.md 的「更正」段、S001 摘要（註明「sic」）、proof.md、record.json 的 `A085588-fixed-points`、論文最後一段（寫成「appears to be 455」，語氣保守）、OEIS 草稿的「另一個小更正」都已改成 455。我自己重算：無進位乘法 11 ⊗ 445 ≠ 7·445，11 ⊗ 455 = 7·455；A115770 在 1000 以內的項是 7, 14, …, 448, 455, 480, …，455 之前的每一項都在 S003 列出的「a(n) = n」名單裡；逐步模擬 455 格的環得 a(455) = 4095。所以「第一個例外是 455」成立。條目原文到底寫 445 還是 455，我連不到 oeis.org，沒辦法再確認，只能依 S001 的抄錄；草稿已提醒使用者送出前自己看一眼。
2. **critic 必修 2（「足以推出」，不是「等價」）：已改好。** proof.md 寫「足以推出第 2 條（不是等價：A115770 也有非梅森形式的數，如 455、903、910）」，論文寫「would suffice (it is not equivalent: …)」。我的重算也看到 A115770 裡有 911、967 這類奇數部分不是梅森數的項，說法正確。第 2 條本身維持 OPEN，沒有被說成已證。
3. **critic 必修 3（論文 AI 聲明）：有條件接受。** 論文寫「reviewed by separate AI agents (critic.md, review.md), and machine-checked by Lean 4 in the repository's CI」。review.md 由本檔補上，前半句成立。後半句要等 PR 的 CI 跑綠才是事實；論文要等 PR 合併、使用者送出 OEIS 後才會被外人看到，所以和 DISC-0014 一樣處理：**合併前 CI 必須是綠的**，否則這句不能留。
4. **critic 必修 4（草稿 COMMENTS 指向）：已改好。** 現在寫「The n where the two differ are those listed in the comment above」，新留言放在 Khrabrov 那段 (End) 之後，所以「above」指的就是他列 6·2^k、13·2^k… 的那句，指向正確。
5. **結論有沒有被證據支持：有。** 「對所有 n」靠的是 Lean 定理，不是有限計算；計算只拿來對定義、找原句的反例。原句方向寫反的判定靠兩個具體反例（a(4) = 2、a(13) = 21），我重跑兩支程式都得到這兩個值，足以推翻原句。H4 只寫「n ≤ 1000 中」，沒有說成證明。
6. **Lean 敘述是否忠實於 OEIS 定義：是。** 逐行看過：`step` 是 i−1、i、i+1 三格 xor，就是規則 150；以 n 為週期的 `Int → Bool` 和 n 格環一一對應；`seed n i = decide (i % n = 0)` 是環上單一 ON 細胞；`EventualPeriod f p` = 最小 p > 0 使某個 k 起 F^(k+p) f = F^k f，就是條目名稱的 eventual period。`a085588_dvd` 的形式是「若 p 是單點軌道的最終週期，則 p | 2^D(2^s−1)」，條件只要 m | 2^s ∓ 1，不要求 m 奇數或 s 最小，所以套到 m 奇數、s = A309786(n) 一定成立；D = A007814(n)、s = A309786(n) 這層對應在 Lean 外，靠定義直接成立（A309786(2n−1) = A003558(n−1) = 最小 k 使 2^k ≡ ±1 mod 2n−1；critic 程式算出的 A309786(1..20) 與此一致）。我在暫存副本裡加 `#eval`，n = 5 時 seed 走 3 步回到原狀，和 P = 2^0(2^2−1) = 3 一致。docstring 說「前週期最多 2^D 步」沒有獨立寫成定理，但它就是 `iter_identity` 的直接意思，不影響判定。
7. **有沒有空洞：沒有。** 搜不到 sorry、admit、axiom、native_decide、implemented_by、unsafe（只有註解裡一處「no native_decide」）。`#print axioms a085588_dvd` = [propext, Quot.sound]。檔案已加進 `lean/Discovery.lean` 的 import。只用 core，比規範的「Lean 4 + Mathlib」更嚴，不影響判定。
8. **新穎性：誠實。** 寫明是 MOW 1984 規則 90 的同一招（原文沒讀、靠條目轉述）、Tadaki 1993 可能已含此結果（沒讀），不宣稱新。novelty 標 NO_MATCH_IN_SCOPE、狀態 PROVEN_KNOWN，一致。
9. **外部資料：** S001–S003（claude-in-chrome）是唯一的條目來源；b-file 998 項的檢查是在瀏覽器內做的，程式 `results/A085588/code/bfile_check.js` 已放進 repo，論文也註明了。我無法重跑那一段（連不到 oeis.org），自算部分（n ≤ 200）和 DATA 一致。讀到的資料裡沒有任何要我做事的文字。
10. **critic 的建議 5–10：** 論文改成「agree with the n …」、b-file 註明瀏覽器檢查、MOW 改成「the entry attributes to」、FORMULA 寫法改清楚、literature 改成「作者本意無法確定」、「有限體字元和」的預測已刪，都已處理。只剩 record.json 的 `A085588-literal` 還寫「exactly the n the comment lists」（見建議 1）。

## 重現結果

所有計算都用 `discovery.limits.run_limited` 跑，都在上限內：

- `python results/A085588/code/l08_a085588_period.py`：約 10 秒，輸出「identity … ok for n <= 400」「a(n) | 2^D(2^s-1) for 3 <= n <= 200; brute force agrees on 121 n; DATA (n<=66) matches」「literal comment fails at [4, 6, 8, 12, 13, …] … 36 of 198」，最後一行「a(4) = 2  a(13) = 21」，和 experiment.md 一致。
- `python results/A085588/code/critic_c_a085588.py`：約 1.6 秒，a(n) 不整除 P 的 n：無；恆等式反例：無；前週期 > 2^D：無；原句失敗 36 個；a(n) = n 的 n 全在 A115770。
- 我自己的小程式（暫存區，不進 repo）：11 ⊗ 445 ≠ 7·445、11 ⊗ 455 = 7·455，a(455) = 4095（逐步模擬）。
- `lean Discovery/A085588Period.lean`（Lean 4.15.0）：0 錯誤，約 0.9 秒。暫存副本加 `#print axioms`、`#eval` 的結果見審查項目 6、7，原檔沒動。
- `python -m discovery.independence`：0 problems。
- `python -m discovery.check_record`：寫本檔前唯一的問題是「DISC-0016: missing review.md」。

## 最終判定

STATUS: PROVEN_KNOWN

理由：Lean（只用 core，無 sorry、無額外公理）對所有 n 證明了 A085588(n) 整除 2^A007814(n)·(2^A309786(n) − 1)，而且任何起始狀態都成立；定義和 OEIS 對得上。用的是 MOW 1984 的標準 Frobenius 技巧，不宣稱新。條目留言的原句（反方向）被 a(4)、a(13) 推翻（子項 REFUTED）；第二條留言維持 OPEN；「445」應為 455 已重算確認。

**必修：** 無。（合併條件：PR 的 Lean CI 必須是綠的，論文 AI 聲明的「machine-checked … in CI」才成立。）

**建議：**
1. record.json 的 `A085588-literal` 把「exactly the n the comment lists」改成「agree with the n the comment lists」，和論文一致。
2. 送出 OEIS 前，使用者自己在條目上確認第二條留言寫的是 445，並在 A115770 確認 455 在、445 不在（草稿已列）。

## 給 CEO 的摘要

A085588 那條 2024 年的留言把整除方向寫反了：a(13) = 21 不是 63 的倍數。正確方向「a(n) 整除 2^D(2^s−1)」已經用 Lean 對所有 n 證完，我重跑兩支程式和 Lean 編譯，全部通過，Lean 的定義也和條目對得上。critic 的 4 條必修都改好了，另一處更正（445 應為 455）我也自己重算確認過。這是已知技巧的習題程度結果，不是新發現。判定 PROVEN_KNOWN。合併前要確認 CI 是綠的；送 OEIS 前請使用者自己看一眼條目原文。
