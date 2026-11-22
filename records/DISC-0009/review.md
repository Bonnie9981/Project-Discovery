# DISC-0009 審查

審查者：reviewer（獨立 subagent，沒有參與撰寫）。審查日期：2026-11-22。審查的 commit：`b63428c`（工作目錄乾淨）。

## 審查項目

1. **結論有沒有被證據支持？** 有。proof.md 的四個步驟（奇偶、一步對一步、第一步、單射）都有對應的 Lean 定理。主定理 `rule26_even_eventual_period` 對所有 m ≥ 2 和所有 p 證明：環（寬 2m）的軌道「最終以 p 為週期」⇔ 導線（寬 m−1）的軌道「最終以 p 為週期」。`rule26_even_least_period` 再把它推到「最小正最終週期相同」，這就是 OEIS 的定義。這是一般證明，不是「在測試範圍內成立」。
2. **Lean 定理是否真的對應猜想？** 對應。
   - 寬度：m ≥ 2，環寬 2m = 2n+2，導線寬 m−1 = n ≥ 1，正好是 A334504 猜想的範圍（n ≥ 1）。w = 2 不在猜想範圍內，proof.md 也寫明了。
   - 環的 `step`／`iter` 沿用 DISC-0008 的 `Discovery.Rule26`。我核對過 `step` 的三個項目，分別是鄰域 100、011、001，也就是 26 = 0b00011010。這和 DISC-0008 審查過的定義一致。
   - 導線 `nstep n y = ((y<<<1) ^^^ (y>>>1)) &&& (2^n−1)`、種子 1，和 search_evidence S001 記下的 A268754 PROG（`((hare << 1) ^ (hare >> 1)) & wire_mask`，從 1 開始）一致。
   - 「最終週期」用 `EvPer`（∃T ∀t≥T, f(t+p)=f(t)）表示，再加上最小正週期的版本，沒有偷換定義。
   - 「環的暫態 = 導線暫態 + 1」沒有 Lean 定理，proof.md 已經寫明它是紙上推論，加上 n ≤ 40 的數值驗證。這一句不屬於 OEIS 猜想本身，不影響判定。
3. **新穎性主張有沒有來源？** 有，而且寫得保守。敘述本身在 A334504 FORMULA 裡（Zabolotskii 2024，「It seems that」），A268754 的 CROSSREFS 也只寫「Seems to be」，所以 novelty = `PARTIAL_MATCH` 合理。literature.md 誠實寫了沒查 arXiv、OpenAlex、MathSciNet、Math Fun，也寫了反射技巧的出處待查，沒有把 MOW 1984 當成出處（這是 critic 必修 2，已經修好）。紀錄沒有宣稱新穎。
4. **critic 必修項。** 兩項必修都已解決，我自己核對過：暫態那句已在 proof.md 的對照表和〈敘述差異〉註明；MOW 已改成「出處待查」。建議 1（最小週期推論）也採納了。
5. **非阻擋的小疑點。** A268754 的 OEIS 名稱是「B1/S Life-like CA 中 n×1 長方形振盪子的週期」。本紀錄用的是條目裡的 PROG／MATHEMATICA 定義（零邊界規則 90、左端種子），名稱和這個定義等價這件事沒有另外論證。不過 l02_check 把 n ≤ 40 的值逐項和 A268754 的 DATA 比對，全部吻合，而 A334504 猜想引用的就是這串數列。所以我不把它算成阻擋項。另外，A268754 的資料是用瀏覽器抄錄的，critic 建議有網路時重讀全文核對。
6. **外部資料裡的指令。** 審查過程中讀到的 OEIS 摘錄和工具輸出裡，沒有看到要求 agent 做事的文字。

## 重現結果

- `python -m discovery.quiet -- python research/r003/l02_check.py 40`：exit 0，約 1.9 秒。最後一行是 `OK: 1 <= n <= 40: period_26(2n+2) = period_90null(n) = A268754(n), transient_26 = transient_90null + 1; structure lemma n <= 20`，和 experiment.md 預期的一樣。完整輸出在 `logs/python_research_r003_l02_check.py_40.log`。
- Lean 4.15.0（`/opt/lean/lean-4.15.0-linux/bin`）：先編譯 `Discovery/Rule26.lean`，再編譯 `Discovery/Rule26Even.lean`，rc = 0，沒有錯誤也沒有警告。兩個檔案都沒有 `sorry`、`admit`、`axiom`、`native_decide`、`implemented_by`、`extern`、`unsafe`（`native_decide` 只出現在註解的「不使用」說明裡）。
- `#print axioms`（scratch 檔，放在 repo 外）：`rule26_even_eventual_period`、`rule26_even_least_period`、`iter_succ_testBit`、`iter_succ_eq_iff`、`iter_succ_ne_one` 都只用 [propext, Classical.choice, Quot.sound]；`check_small` 只用 [propext]。這些都是標準公理。
- `lean/Discovery.lean` 有 import `Discovery.Rule26Even`，所以 CI 的 lean 工作和公理稽核都會涵蓋它。
- CI：PR #17 在 head `b63428c` 的 check（build、test）審查時還在跑（in_progress）。依規範，CI 的 lean 公理稽核才是權威結果。

## 最終判定

STATUS: PROVEN_KNOWN

理由：
- R3-L02 對所有 n ≥ 1 都有完整的一般證明，而且用 Lean 形式化，只用標準公理。我在本機重現了編譯和數值檢查。這符合 `PROVEN_*` 的條件。
- 敘述本身已經以猜想形式記載在 OEIS（A334504 FORMULA），novelty 是 `PARTIAL_MATCH`。和 DISC-0008 的判定一致：`PROVEN_POSSIBLY_NEW` 需要人把 novelty 確認到 `PENDING_REVIEW`，目前沒有。所以合法而且保守的選擇是 `PROVEN_KNOWN`。
- `PROVEN_KNOWN` 在這裡的意思是「這個敘述不是我們先提出的」，**不**代表已經有既有的證明。「證明可能是新的」這個問題保留在 `novelty.open`（R3-L02）。

**條件：** 這個判定的前提是 PR #17 的 CI lean 工作（含公理稽核）通過。如果 CI 失敗，這份判定要撤回，改回 `INCONCLUSIVE`，並附加新的審查項目。

**建議（非必修）：**
- 有網路時重讀 A268754、A334504 全文，核對 offset 和抄錄的資料，並確認 B1/S 名稱和 PROG 定義等價。
- 查 arXiv、MathSciNet、zbMATH、Math Fun，找反射技巧和「規則 26 單一種子 = 規則 90」的出處。
- 把 critic 的 impl_c 收進 repo，再跑 `python -m discovery.independence`。

## 給 CEO 的摘要

- **結論：** OEIS A334504 裡有一條沒人證明過的觀察：「偶數寬度的規則 26 環，週期等於另一個數列 A268754」。這次我們對所有寬度都證明了，而且 Lean 電腦證明在本機編譯通過，只用標準公理。
- **狀態：PROVEN_KNOWN。** 因為這個敘述是別人先在 OEIS 寫下的猜想，所以算「已知」。這不表示別人已經證明過；我們只查了 OEIS，沒查論文資料庫，所以不宣稱證明是新的。
- **重現：** 數值檢查（n = 1 到 40，和 OEIS 的資料逐項比對）我自己跑過，全部通過，約 2 秒。Lean 也自己編過一次，沒有錯誤。
- **還要等：** GitHub 上的 CI 還在跑，要它通過這個判定才算數。
- **小提醒：** 「暫態多 1 步」只有紙上推論加數值驗證，沒有電腦證明，不過它不在 OEIS 的猜想裡。A268754 的資料是用瀏覽器抄的，之後有網路要再核對一次。
