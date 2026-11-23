# DISC-0017 審查

審查者：獨立 reviewer subagent（不是作者，也不是 critic）。只複查 critic 的必修項和關鍵主張，沒有全面重做。
讀到的檔案和工具輸出裡沒有出現要 agent 做事的文字。重跑的原始輸出放在 scratchpad 的 `rev/` 子目錄，不進 repo。

## 審查項目

1. **critic 必修 1（說法範圍）：已改好。**
   - paper 開頭改成：第 1、2 節是紙本證明；反例由 Lean kernel 檢查；最小性靠三支獨立程式的搜尋。
   - paper 第 3 節逐一寫出每支程式的範圍：scan.c 到 6.1·10^10，brute.c 到 1.964·10^10，critic_search.go 的結構搜尋到 6.1·10^10、一般搜尋到 10^10、窮舉到 2·10^8。
   - proof.md「敘述差異」也同步改了，並寫明最小性不在 Lean 裡。
2. **critic 必修 2（critic 程式留存）：已改好。**
   - `results/A294646/code/critic_search.go` 已在 repo 裡，有 148 行，不 import 專案程式，可以編譯也可以重跑（見下節）。
3. **critic 建議：都處理了。**
   - OEIS 草稿已加「(exhaustive search, see link)」和「(classical; proofs in link)」。
   - paper 第 2 節加了「with multiplicity」，第 3 節加了「r ≡ 0 mod gcd(ord_p(2), 6)」。
   - scan.c 改成 `if(!k0) continue;`。
4. **結論有沒有被證據支持：有。**
   - 反例是一個明確數值，有 Lean kernel、Python 大整數、Go 兩條路徑（math/big 和 uint64）三方確認。符合 REFUTED「兩個獨立實作確認」的要求。
   - 「最小反例」寫成搜尋結果，沒有說成是證明出來的。paper、OEIS 草稿和 record.json 都標了 6.1·10^10 這個範圍，以及範圍內的完整性理由（最小質因數 ≤ √m，最小可用質數是 61，所以 k ≤ 10^9）。
   - 另外兩半是古典結果，標為 SUPPORTED_KNOWN，也寫明只有紙本證明。critic 已逐步檢查過，這裡不重做。
5. **Lean 定理有沒有對應到猜想：有。**
   - `IsA294646 n k` 的定義是「最小的 k > 0，使 k·2^(2n) ≡ 1 (mod 2n+1)」，和條目留言的刻畫一致。
   - `a294646_counterexample : IsA294646 N (2*N−2)` 直接說 a(N) = 2N−2。
   - `#print axioms` 只列出 propext 和 Quot.sound，沒有 sorry，也沒有 native_decide。
6. **新穎性用語：恰當。**
   - record.json 標 NO_MATCH_IN_SCOPE，列了 S001 到 S003 三次查詢，也寫明沒查 MathSciNet 和 zbMATH，並說「Not claimed as a new theorem」。
   - RESEARCH.md 寫「查過的範圍內沒有人回報過，但不宣稱新定理」。
   - OEIS 草稿只陳述事實，沒有使用「new」「first」這類字眼。
   - 合乎規則，不需要修改。
7. **小的不一致（非必修，不影響判定）。**
   - experiment.md「結果」寫「H1、H2：brute 到 10^10」，record.json 的三個候選也都寫「brute force m < 1e10」。
   - 但 experiment.md「方法」和 paper 都寫 brute 跑到 1.964·10^10（brute.c 同時檢查三種情形）。
   - 兩個數字都沒有錯，只是寫法不統一：較小的數字只是說得保守。之後如果有更正，可以順手統一。這份紀錄已完成，本審查不去改。
   - 另外，critic.md 第 4 行說程式「沒有存進 repo」，那是寫報告當時的狀態，後來已經補進 repo（見第 2 項）。
8. **外部資料限制（照實轉述）。**
   - critic 那次執行連不到 oeis.org。本次 reviewer 也沒有重新上網查。
   - DATA 前 20 項只和 verify.py 的抄本比對過。我自己重跑 critic_search.go，得到的 a(1..30) 和 critic 報告相同。
   - OEIS 草稿已經提醒使用者送出前用 PARI 自己驗一次。

## 重現結果

| 項目 | 指令 | 結果 | 時間 |
|---|---|---|---|
| Python 驗證 | `python3 results/A294646/code/verify.py` | a(n) = 19628894806 = 2n−2；(3·2^(2n)+1) mod (2n+1) = 0；前 20 項 DATA 一致 | 0.02 秒 |
| Lean | `lean lean/Discovery/A294646Counter.lean`（4.15.0，只用 core） | 通過；axioms 只有 [propext, Quot.sound] | 0.43 秒 |
| scan 重跑 | `gen_primes.py 2000000` 加 `scan 1000000000 0 1` | 只印出 `HIT m=19628894809 p=367 k=53484727` | 8 秒加 64 秒 |
| critic_search.go | `verify` | 兩條路徑都得到 3·2^(m−1)+1 ≡ 0，367·53484727 = m | 瞬間 |
| critic_search.go | `scan 61000000000 3 mod6` | hits 只有 [19628894809] | 13 秒 |

說明：
- brute.c 沒有重跑。總控說作者已經跑到 1.964·10^10，而且這次的時間預算不夠。
- scan.c 和 critic_search.go 這兩套程式都對 m ≤ 6.1·10^10 給出同一個唯一解。

## 最終判定

STATUS: REFUTED

- 條目猜想裡「a(n) 不會是 2n−2」的部分被明確反例 n = 9814447404 推翻。
- 反例由 Lean kernel 和多個獨立實作確認。
- 「最小反例」只在 2n+1 ≤ 6.1·10^10 的完整搜尋範圍內成立，文件也是這樣寫的。
- 另外兩半屬於古典結果，標 SUPPORTED_KNOWN，只有紙本證明。
- 沒有必修項。

## 給 CEO 的摘要

- OEIS A294646 猜想「a(n) 不會是 2n−2」是錯的：n = 9814447404 就是反例。
- 這個反例已經用 Lean 和三支程式驗過，我自己也重跑確認了。
- 在 2n+1 ≤ 6.1×10^10 的範圍內，它是唯一、也是最小的反例。這是搜尋結果，不是定理。
- 「不會是 2」和「不會是 2n」這兩半是古典習題，有紙本證明。
- 查過的範圍內沒人回報過這個反例，但我們不宣稱新定理。
- OEIS 草稿措辭恰當，可以交給使用者。送出前請用 PARI 自己驗一次。
