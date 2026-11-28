# DISC-0031 審查

Reviewer：獨立 subagent，2026-11-28。讀了 `records/DISC-0031/` 全部七份檔（含 critic.md）、`paper/a212339-marked-mesh.md`、`results/A212339/` 全部檔案、`docs/RESEARCH_STANDARDS.md`，以及離線 OEIS 的 A212339、A212341、A212344、A212345 `.seq` 檔。讀到的資料（OEIS 文字、論文轉述、程式輸出）裡沒有要 agent 做事的文字。

## 審查項目

### 1. 證明本身

- 分解 σ = α n β、左下方點數的三種情況、函數方程 (*)、取 x⁰ 和 x¹ 的係數、化簡 F − P_k：我逐步重推了一遍，都對。critic 第 1 項的結論我同意。
- 反方向（任給 α、β，α n β 一定避開 132）：證明頁已經補上。小缺口是沒寫「1 在 β 裡」的情形（這時 2 和 3 在它後面，也都在 β 裡，所以整組在同一段裡，不可能），不過這已經包含在「不可能整組在同一段」那句裡。可以順手補半句，不是必修。
- **(*) 和 KRT 的閉式等價，我另外查到了證據**：A212339、A212341 的 `%t`（Robert Price 的 Mathematica 程式）印了 Q^(0,0,k,0)(t,x) = 2/(A + sqrt(A² − 4tx))，其中 A = 1 + (tx − t)P_k。把 (*) 整理成 txQ² − AQ + 1 = 0，解出來剛好就是這個式子。所以 (*) 等於 OEIS 條目裡已經印出來的閉式。critic 第 4 項提的疑點，到這裡在數學上已經解決。證明頁現在寫「KRT 由同一個分解推出 g.f.」，這句沒有超出證據。
- **反過來說，這正是新穎性的問題（見第 4 項）**：直接對這個閉式取 ∂/∂x 再代 x = 0，三行就得到 t(1 − P_k + tP_k²)/(1 − tP_k)³。我用 PARI 對 k = 3、4 驗算：導數和定理的 g.f. 到 t²⁹ 都一樣（`rev2.gp`，見重現結果）。

### 2. critic 的必修項目有沒有真的改

| # | critic 要求 | 現況 | 判斷 |
|---|---|---|---|
| 1 | 證明頁補上分解的反方向 | 已補（Proof 第一段的 "Conversely, ..."） | 已修 |
| 2 | Dale 遞迴的成立範圍：分子 6 次；補 0 時 n ≥ 7，只用條目存的項時 n ≥ 13 | 證明頁已改。proof.md 用附加的「更正」段處理，原文沒動，符合不能覆蓋的規定 | 已修 |
| 3 | Gladkovskii 的連分數不要算成已解決 | 證明頁改成「the closed form 5*(1-sqrt(1-4*x))/(2*x) up to the offset; Gladkovskii's continued fractions are not checked here」；草稿第三條只提 Bala 和 Mathar，送出前注意事項也提醒不要寫已證 | 已修 |
| 4 | KRT (21) 的原文，或者把說法改弱 | 選了改弱：「KRT derive ... from the same decomposition」。原文還是沒有逐字比對（我連 arxiv.org 也被 proxy 擋，回 403），但第 1 項的 OEIS `%t` 閉式已經在數學上確認等價 | 已修 |
| 5 | 補齊 `results/A212339/` 的 README、草稿、兩份中文說明 | 四份都有了 | 已修 |

### 3. 程式和數據

- 程式真的有驗證定理說的東西：暴力法（n ≤ 11）和 OEIS 資料是獨立的；DP 用的是同一個分解，紀錄自己也有說明。critic 的第三套（自己寫產生器，k = 1～5，n ≤ 12，比了完整分布）已經補上這部分的獨立性。
- 研究規範 2b 要的 `research/r003/impl_c.py` 還沒放：critic 的 `crit.py` 還在 scratchpad，沒有進 repo。這不影響數學，但第三套實作沒有長期保存（見必修 4）。
- 第三象限的定義：只有第三象限的 x 係數和 OEIS 資料吻合（critic 的檢查，我重跑後同樣只得到 III），和 `%N` 的寫法一致。

### 4. 新穎性：判 `SUPPORTED_KNOWN`，不判 `SUPPORTED_NOVELTY_UNCHECKED`

record.json 把 A212339、A212341 標成 `SUPPORTED_NOVELTY_UNCHECKED`。我判 `SUPPORTED_KNOWN`，理由：

1. **公式本身 OEIS 已經有記載**：Barker 在 2013 年就把這兩條 g.f. 寫在 A212339、A212341 的 `%F`，只是標成 empirical。我們做的是把它證出來，不是找到新公式。
2. **證明只差一步**：完整閉式 Q^(0,0,k,0)(t,x) 在 KRT 的 (17) 裡，也印在這兩條條目的 `%t`。對 x 微分一次、代 x = 0 就得到結果（第 1 項，PARI 驗過）。研究規範 1c 的 L1 條件明文排除「已知公式一步就能推出」的東西，紀錄自己也寫了「習題程度、不宣稱新」。
3. **前例一致**：DISC-0029 也是「由已知 g.f. 求導一步推出」，審查判 `SUPPORTED_KNOWN`，novelty 維持 `NO_MATCH_IN_SCOPE`。
4. critic 說「KRT 寫了沒有簡單辦法，所以不算已知」。我不同意這樣推論：KRT 那句話只是說他們沒有去做，不代表這件事有難度。`SUPPORTED_NOVELTY_UNCHECKED` 的意思是「也許是新的，只是還沒查」，用在這裡會讓人以為還有新發現的可能。照實寫，應該是「公式已知，閉式已知，證明是例行的一步」。

`novelty.status` 維持 `NO_MATCH_IN_SCOPE`：在查過的範圍內，沒找到有人把 x 係數的證明寫出來。這只是在說證明有沒有人寫過，不代表結果是新的。

A212344、A212345 是 KRT Theorem 13 的特例，維持 `SUPPORTED_KNOWN`。限制：Theorem 13 的原文和編號只來自 literature.md 的轉述，critic 和我都沒能重新讀原文（403）。不過暴力法驗了 k = 1～5、n ≤ 12，Theorem 13 的兩部分都成立。

### 5. 有沒有把「範圍內成立」說成「證明」

- 證明頁、README、兩份說明都寫了「紙上證明，沒有 Lean」，狀態也沒有寫 PROVEN，這部分沒問題。
- 紀錄標題用了「證明 A212339……的猜想」。紙上證明確實存在，但讀起來容易以為是 PROVEN。建議以後寫「紙上證明」，已經完成的標題不必改。

### 6. OEIS 草稿

- 沒有宣稱新穎；A212344、A212345 都標明只是補出處；Gladkovskii 的連分數沒有寫成已證；也提醒了要用自己的話重寫、一次送一條。這些都符合研究規範第 7 節。
- 草稿列的 PARI 指令我用 PARI 2.15.4 跑過：得到 [5, 19, 61, 188, 523, 1387] 和 0，和草稿說的一樣。另外驗了 k = 4 和 Barker 的式子相減也是 0。
- 要修的地方：
  - (a) 第一條寫「so is the conjectured signature」，沒有寫成立範圍。要加上「(for n >= 13)」，和證明頁一致。
  - (b) 可選 COMMENTS 的「532 是 523 的筆誤」，以及第三、四條的「Theorem 13(1)/(2)」，都只根據 literature.md 的轉述，原文沒有第二個人讀過。使用者送出前要自己打開 arXiv:1201.6243 的 PDF，確認定理編號和那串數字。草稿的「送出前」清單要加這一條。

### 7. 兩份高二版說明

- 內容都有檔案或輸出支持：小例子（n = 4 時是 5 個；2 3 4 5 1 的 mmp = 1；2 4 1 3 含 132）我逐一手算過，都對；程式輸出和我重跑的一字不差；PARI 那段我也重跑確認了。
- 要修：`證明方法說明.md` 的「判定與限制」寫 A212339、A212341「暫定 `SUPPORTED_NOVELTY_UNCHECKED`」，要改成 `SUPPORTED_KNOWN`，並加一句理由：「Barker 的式子已經在 OEIS 上，KRT 的閉式（也印在條目的 Mathematica 程式裡）對 x 微分一次就得到，所以只是補證明，不算新發現」。
- 可以補（不是必修）：Dale 遞迴的成立範圍（n ≥ 13）。

## 重現結果

- `python -m discovery.quiet -- python results/A212339/code/check_a212339.py 11`：exit 0，5.1 秒，輸出 `brute n <= 11, DP n < 60, exact g.f. identities (A212338/39/41, Dale signature) OK; OEIS terms: A212338:33 A212339:29 A212341:26 A212344:27 A212345:26`。和 experiment.md、程式說明.md 寫的完全相同。log 在 `logs/python_results_A212339_code_check_a212339.py_11.log`。
- critic 的獨立實作 `python -I .../scratchpad/crit.py 11`：H1 在 k = 1～5 都和暴力法相等；三條 OEIS 條目只有第三象限吻合；Theorem 13 在 k = 1～5 沒有失敗；A212344、A212345 分別等於 5C(n−3)、9C(n−3)；Dale 遞迴在補 0 時只有 n = 4、5、6 不成立。
- 草稿的 PARI 指令（我自己的檔案 `scratchpad/rev_pari.gp`，PARI 2.15.4）：`[5, 19, 61, 188, 523, 1387]`、`0`；k = 4 和 Barker 的式子相減也是 `0`。
- OEIS 閉式取 x 係數（`scratchpad/rev2.gp`）：k = 3、4 時，Price `%t` 的閉式對 y 微分後代 y = 0，和定理的 g.f. 相減是 O(t³⁰)。也就是說，從 OEIS 已有的式子一步就能得到結果。
- 沒有 Lean，所以沒有東西要編譯。
- 外部來源：arxiv.org 被 proxy 擋（CONNECT 403），KRT 原文沒有讀到。

## 最終判定

STATUS: SUPPORTED_KNOWN

| 候選 | 判定 | 和 record.json 比 |
|---|---|---|
| A212339 | `SUPPORTED_KNOWN` | 不同（record 寫 `SUPPORTED_NOVELTY_UNCHECKED`） |
| A212341 | `SUPPORTED_KNOWN` | 不同（record 寫 `SUPPORTED_NOVELTY_UNCHECKED`） |
| A212344 | `SUPPORTED_KNOWN` | 相同 |
| A212345 | `SUPPORTED_KNOWN` | 相同 |
| 整份紀錄 | `SUPPORTED_KNOWN`（取研究目標 A212339 的狀態） | 不同 |

數學上沒有錯：紙上證明正確，程式重現成功，critic 的五項必修都改了。降級只因為新穎性：公式 OEIS 早就有，證明是從已知閉式取一次導數。沒有 Lean，所以不能標 PROVEN。

**record.json 要改的地方**（我沒有動其他檔案）：
1. 最上層 `"status"` 改成 `"SUPPORTED_KNOWN"`（不改的話 `check_record` 會因為和本檔的 STATUS 不一致而失敗）。
2. `candidates.A212339.status`、`candidates.A212341.status` 改成 `"SUPPORTED_KNOWN"`。
3. `novelty.status` 維持 `"NO_MATCH_IN_SCOPE"`。`novelty.note` 補一句：`"The g.f.s are recorded in OEIS (Barker, empirical) and the closed form of Q^(0,0,k,0)(t,x) is in KRT (17) and in the %t of A212339/A212341; the x-coefficient follows by one differentiation, so the result is SUPPORTED_KNOWN (proof supplied, not a new formula)."`
4. `novelty.open` 加一條：`"KRT arXiv:1201.6243 not re-read independently (proxy 403): Theorem 13 numbering and the '532' typo rely on literature.md"`。

**其他還要修的項目**：
1. `results/A212339/證明方法說明.md`：狀態改成 `SUPPORTED_KNOWN`，加上理由（見審查項目 7）。如果有轉成 PDF，要重新轉。
2. `results/A212339/a212339_oeis_edit_draft.md`：第一條加上「(for n >= 13)」；「送出前」清單加一條「自己打開 KRT PDF，核對 Theorem 13 的編號和 Section 4 的 532」。
3. `RESEARCH.md`：DISC-0031 那一節和候選清單的狀態要跟著改。
4. 把 critic 的 `crit.py` 放到 `research/r003/impl_c.py`，再跑 `python -m discovery.independence`（研究規範 2b）。
5. （建議）證明頁反方向那段補「若 1 在 β 中，三個數都在 β 中」半句。

## 給 CEO 的摘要

- 數學是對的：Barker 對 A212339、A212341 猜的 g.f. 和 Dale 猜的遞迴，紙上證明都成立；程式重跑結果一致；critic 要求的五項都改了。
- 但這不算新發現。公式 2013 年就寫在 OEIS 上，完整的閉式也在 KRT 論文和 OEIS 條目的 Mathematica 程式裡，對 x 微分一次就得到。所以 A212339、A212341 從 `SUPPORTED_NOVELTY_UNCHECKED` 降成 `SUPPORTED_KNOWN`；A212344、A212345 本來就是 KRT 的定理，維持 `SUPPORTED_KNOWN`。
- 送到 OEIS 仍然有價值（把「猜想」變成「有證明」），只是不能說是新結果。送出前使用者要自己讀 KRT 原文，核對定理編號；AI 這邊連不到 arXiv。
- 還要做的：改 record.json 和 RESEARCH.md 的狀態、修高二說明裡的狀態、在草稿補遞迴的成立範圍、把第三套實作存進 repo。
