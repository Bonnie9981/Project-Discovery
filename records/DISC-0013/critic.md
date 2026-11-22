# DISC-0013 Critic

結論：沒找到反例，也沒有必修項。Lean 敘述對得上 OEIS 的定義（最小正最終週期、offset 1、例外句兩種讀法都有證到）；第三套實作重算的數字全部一致。下面「建議」各項都不擋判定。

## 攻擊項目

1. **Lean 有沒有偷用公理或 sorry。** 把 `lean/Discovery/A268754Odd.lean` 複製到 scratch，在檔尾加 `#print axioms`，用本機 Lean 4.15.0 編譯（LEAN_PATH=/tmp/claude-0/lb，olean 比 Rule26*.lean 新）。結果：`a268754_odd`、`a268754_odd_exception`、`dies_iff` 都只用 [propext, Classical.choice, Quot.sound]，約 3 秒，沒有錯誤。原檔和 Rule26/Rule26Even 都 grep 不到 `sorry/admit/axiom/extern/implemented_by`。原檔沒有改。
2. **敘述是不是 OEIS 的 a(n)。** `#check` 結果：`1 ≤ n → ¬∃k, n+1 = 2^k → LeastPer (niter n · 1) p → LeastPer (niter (2n+1) · 1) (2p)`。`LeastPer` = 0<p ∧ 最終以 p 為週期 ∧ 沒有更小的正最終週期，就是「最小正最終週期」；`EvPer` 是 ∃T ∀t≥T，最終週期的意思沒錯；`nstep` 和條目的 Python 一樣。Offset：n≥1 涵蓋 a(3)、a(5)…，n=0 本來就不在定義域。例外句：照字面讀是「a(n)=1」，自然讀法是「a(n)=a(2n+1)=1」，`a268754_odd_exception` 兩邊都證了，兩種讀法都成立。
3. **缺口（建議，不擋）：最小週期存在沒有證。** `a268754_odd` 的前提是 `LeastPer … p`；如果 p 不存在，定理就是空的。數學上有限狀態必然存在，proof.md「敘述差異」也已經寫明。要做成可以給 OEIS 的版本，建議補一個鴿籠引理 `∃ p, LeastPer (niter n · 1) p`（n ≥ 1），這樣「a(2n+1) = 2a(n)」就是完整的函數等式。
4. **證明論證逐步核對。** 第 2 步右端：短導線的 y_n 是第 n 位，因為 y < 2^n 一定是 0；長導線有第 0..2n 位，2i+1 ≤ 2n−1，沒有越界。第 3 步：週期是奇數時，x_{s+p} 和 x_s 的奇偶相反，所以 x_s = 0，而 x_s = S(y) ≠ 0，矛盾；這裡要「永不死」，由 `dies_iff` 提供，沒有循環論證。第 4 步歸納：n+1 = 2^0 只對應 n=0，已經排除；n=1 另外處理。沒找到漏洞。
5. **死亡檢查的範圍是否足夠。** l06 只看 n+1 步內有沒有死。我補的論證：線性映射在 n 位元上的暫態 ≤ n，0 又是不動點，所以「曾經死過 ⇔ x_n = 0」。l06 的 `range(n+1)` 會檢查到 t = n，判定是精確的，不是抽樣；第三套實作也用 x_n 檢查（見下）。
6. **反向控制（確認檢查器會抓錯）。** 我的 `is_least_period`：w=4 時 p=3、12 為假，6 為真；w=9 時 6、24 為假，12 為真；w=7 時 p=2 為假（死光的導線週期是 1，不是 2）。檢查器確實會把錯的值擋下來。
7. **獨立性與研究標準。** l06 的 way1/way2 放在同一個檔案，不是標準 2b 規定的 `impl_a.py`/`impl_b.py`。不過兩者的編碼（遮罩 vs 2n+2 格環）和找週期的方法（Brent vs 字典）都不同，也沒有共用的輔助函式，只有 DATA 比對只用了 way1。總控要的檔名 `impl_c_a268754.py` 我試過：放進去之後 `python -m discovery.independence` 會失敗（"research/r003: only one impl_*.py; need at least impl_a and impl_b"），因為 r003 沒有 impl_a/b。所以照 r003 既有慣例（`critic_c_mod1.py`）改名為 `research/r003/critic_c_a268754.py`，independence 通過（3 dirs, 0 problems）。這支檔案只 import random 和 sys。
8. **Lean 的 `check_small` 只驗了週期 6、12 會重複，沒驗最小性**（例如沒驗 niter 4 3 ≠ niter 4 0）。只是抽查，不影響主定理。建議，不擋。
9. **文獻（建議，不擋）。** n 格導線 ↔ 2n+2 格環，所以 2n+1 格導線 ↔ 4n+4 = 2·(2n+2) 格環。這個公式其實就是 MOW 1984「Π_{2N} = 2Π_N」的論證套用在這條對稱軌道上，和那篇的關係比 literature.md 寫的「不同的量」更近。建議在 literature/novelty note 補這一句，PROVEN_KNOWN 不用改。

## 獨立重算

`python research/r003/critic_c_a268754.py 40 1000`（約 103 秒，在 limits 600 秒內，exit 0）。方法完全不迭代、不做循環偵測：用鏡像法加 Lucas 定理寫出閉式，x_t 的第 j 格 = Σ_{s=±1} Σ_m C(t, (t+j−s+m(2n+2))/2) mod 2，任何時刻的狀態都能直接算。週期是「驗證」出來的，不是「搜尋」出來的：取 T = 寬度，p 是最小週期 ⇔ x_{T+p} = x_T，而且對 p 的每個質因數 q，x_{T+p/q} ≠ x_T。

- [1] 條目 DATA 1..54（含 a(46) = 16777214、a(52) = 134217726）都是最小正最終週期：OK。
- [2] 1 ≤ n ≤ 40：寬度 2n+1 的最小週期 = 2a(n)（例外時 = 1，且 a(n) = 1）：OK，最大 349524（與 experiment.md 相同）。
- [3] 1 ≤ n ≤ 1000：x_n = 0 ⇔ n+1 = 2^k：OK（精確判定，理由見攻擊項目 5）。
- [4] 間隔展開：隨機 40 組，n ≤ 60、t ≤ 10^6，x^(2n+1)_{2t+1} = S(x^(n)_t)：OK。這是 l06 涵蓋不到的大 t。
- 另外重跑 l06（40 2000）：OK，6.6 秒。

## 未解決的疑點

- **DATA 抄錄無法對照原文。** 連 oeis.org 被代理擋下（HTTP 403），54 項 DATA 和 FORMULA／COMMENTS 的原文我都沒能親自重讀，只能確認抄錄值內部一致，而且和兩套重算相符。條目名稱（B1/S 規則的 n×1 長方形振盪子）和零邊界規則 90 等價，這點仍然沿用 DISC-0009 的非阻擋項。
- 最小週期存在沒有在 Lean 證（攻擊項目 3）。
- 研究資料（l06 docstring、literature.md）裡沒有看到要 agent 做事的嵌入文字。
