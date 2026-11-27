# DISC-0027 Review（獨立審查）

## 審查項目

1. **critic 第二輪的四條必修**：
   - 必修 1（定理 2 的「次數相加 < 60、比 120 項」論證）：**論文已改**。`paper/a308758-four-parts.md` 定理 2 現在寫「numerator1·denominator2 − numerator2·denominator1 is the zero polynomial」，指向 `check_gf_exact`。我讀過 `check_gf_exact`：用整數係數多項式（list）運算，把每個 g.f. 寫成 N/Q0²（Q0 = (1−x)(1−x²)(1−x³)(1−x⁴)），Barker 的分母改寫成 (1−x)^(top−3−k3)(1−x²)(1−x⁴)²(1−x³)^k3，(1−x) 的指數正負都搬到正確的一邊，然後交叉相乘比較，沒有截斷。這個改寫我手算過：(1−x²)(1−x⁴)²(1−x³)^k3 = (1−x)^(3+k3)(1+x)³(1+x²)²(1+x+x²)^k3，所以指數是 2−k3（分拆）或 1−k3（三角形），和程式一致。`check_gf`（前 120 項）留著當額外檢查，註解已寫明「only a sanity check」。
     **但沒有同步改完**：`records/DISC-0027/experiment.md`「實作三」和 `proof.md`「定理對照」第 4 點還寫「比較前 120 個係數（次數和都小於 60，所以相等）」；`check_a308758.py` 開頭說明第 (3) 點和第 132 行註解也還寫「to a degree that makes agreement equivalent / the same degree argument applies」。critic 已算出照字面寫法 A308775 的交叉乘積次數是 140，大於 120，所以這個論證本身不成立。結論沒受影響（精確恆等式成立），但文件互相矛盾。見必修 1。
   - 必修 2（n ≥ 2）：**已改**。論文定理 1 寫「For n >= 2」，並註明 n = 1 時把三條 offset 1 數列不存在的第 0 項當 0，兩邊都是 0。OEIS 草稿 FORMULA 也寫「for n >= 2」。
   - 必修 3（作者行）：**已改**。論文開頭是「Chi Hsia ... (Prepared with the help of an AI assistant (Claude); to be checked by the author before any OEIS submission.)」，不再替人類作者宣稱已核對。
   - 必修 4（高二版說明）：**已補**。`results/A308758/證明方法說明.md`、`程式說明.md` 都存在，內容見第 6 項。
2. **定義與偏移**：用離線 OEIS（`python -m discovery.oeisdb show`）核對。A308758 %S 從 offset 0 起是 0,0,0,0,1,1,2,4,…，所以 a(6) = 2、a(7) = 4；A307966 offset 1 起是 0,0,1,…。定義（第三大部分、最短邊、x+y>z 嚴格）和 critic 第一輪一致。八條 Barker 的 g.f. 原文我逐條讀過，都還標「Conjectures」，和 literature.md 一致。
3. **定理 1 的證明**：我逐步檢查過。a → a+1 的像正好是 a > b 的分拆；(a,a,c,d) ↦ (c, a, a+d−1) 與反函數 (y, y, x, z−y+1) 的條件（d ≥ 1 ⇔ z ≥ y，c ≥ d ⇔ x+y > z，a ≥ c ⇔ y ≥ x）完整，論文也補上了兩邊互逆的一行。四條差分式由 c = x、a = y、d = z−y+1 直接得到；A308760 多出的 A026810(n−1) 來自 a 加 1，正確。
4. **定理 2**：除了專案程式和 critic 的獨立程式，我另外用 PARI/GP 做了第三次檢查（見重現結果）：以論文的參數化建 F、Y1～Y4、D、C、B、A 和三角形的 Tx、Ty、Tz，與 Barker 的 8 個 g.f. 做有理函數相等比較，8 條全部為真。這是有理函數的精確相等，不是取樣。
   遞迴式那句（「hold for every n larger than the numerator degree」）成立的前提是把負索引的項當 0；若不這樣約定，還要 n ≥ 遞迴階數。Barker 寫的範圍（n > 13、n > 15）兩個條件都滿足，所以結論沒錯，只是說法可以更精確（建議）。
5. **研究規範第 1、1b、6、7 節**：
   - 第 1 節：紙上證明完整，但沒有 Lean，所以不能標 `PROVEN_*`。record.json 紀錄層級與 8 個候選都是 `SUPPORTED_NOVELTY_UNCHECKED`，合規。
   - 第 1b、6 節：novelty 是 `NO_MATCH_IN_SCOPE`，寫明了快照 commit 091a90f51479、查證日期、3 筆查詢（S001～S003），也寫明網路、MathSciNet、zbMATH、arXiv 都沒查，並說「很可能是習題級，不宣稱新」。沒有把「沒找到」說成「新的」。
   - 第 7 節：草稿寫明由使用者自己送、留言要用自己的話重寫、一次只送 A308758 一條、保留 Barker 原句、署名 `_Chi Hsia_`、LINKS 註明 LLM 協助。合規。LINKS 指向 GitHub main，要等合併後才有效。
6. **高二版說明**：
   - 例子我逐一驗過：n = 7 的三個分拆與 c 總和 4、n = 6 的 c 總和 2、周長 6 只有 (2,2,2)，A307686(6) = 2，差 4 − 2 = 2。都和 OEIS %S 及 PARI 輸出一致。
   - 證明步驟和論文一致，生成函數一節標明「超出高二」。「兩個不同的程式都算過」有依據（專案程式與 critic 第二輪的獨立程式）。
   - `程式說明.md` 貼的輸出和我重跑的輸出逐字相同；PARI 指令我也跑過，結果相同。「forpart 由小到大排，p[2] 是第三大」正確。
   - 沒有寫超出檔案依據的內容。
7. **輸入安全**：OEIS 條目文字和工具輸出裡沒有要 agent 做事的指令。

## 重現結果

| 項目 | 指令 | 結果 | 是否一致 |
|---|---|---|---|
| 主檢查 | `python results/A308758/code/check_a308758.py 200` | 約 7.1 秒，exit 0：n ≤ 200 四條差分與雙射 OK；8 個 g.f. 精確多項式恆等成立；OEIS 項 A308760:49 A308759:51 A308758:53 A308733:55 A026810:58 A307686:59 A308096:56 A307966:56 A005044:74 全部一致 | 與 experiment.md、程式說明.md 一致 |
| PARI 自驗（草稿的指令） | `vector(40,n,s(n+1)-s(n)-u(n))` | 40 個 0；s(6) = 2、s(7) = 4、u(6) = 2 | 一致 |
| 8 個 g.f.（我自寫，PARI 有理函數比較） | scratchpad 的 `rev27.gp`（暫存，不進 repo） | 8 條全部相等 | 與 `check_gf_exact`、critic 第二輪一致 |

完整輸出在 `logs/python_results_A308758_code_check_a308758.py_200.log`。

## 最終判定

STATUS: SUPPORTED_NOVELTY_UNCHECKED

- 數學：定理 1（四條加權差分關係）有完整的雙射證明；定理 2（Barker 的 8 個猜想 g.f.）由精確多項式恆等式證明，三個獨立程式（專案程式、critic、本審查的 PARI）都確認。
- 為什麼不是 PROVEN：沒有 Lean，依第 1 節只能停在 SUPPORTED。
- 新穎性：`NO_MATCH_IN_SCOPE`，只查了離線 OEIS 快照。不可宣稱新。
- 8 個候選維持 `SUPPORTED_NOVELTY_UNCHECKED`。

必修（只涉及文件，不影響判定與數學）：
1. 把舊的「前 120 項、次數和 < 60」論證改成「交叉相乘為零多項式（`check_gf_exact`）」，或註明 120 項只是額外檢查。要改的地方：`records/DISC-0027/experiment.md`「實作三」、`proof.md`「定理對照」第 4 點、`results/A308758/code/check_a308758.py` 開頭說明第 (3) 點和第 132 行註解。這個論證對 A308775 不成立（交叉乘積次數 140 > 120），不能留在紀錄裡。依第 3 節，紀錄完成後要用附加的方式更正（例如在 experiment.md 末尾加「更正」一節）。

建議：
- 論文遞迴式那句補上「把負索引的項當 0」，或改成「n ≥ max(分子次數+1, 階數)」。
- literature.md 的查詢只有 3 筆；之後若要往 `PENDING_REVIEW` 走，要補網路、arXiv、MathSciNet 的查詢。

## 給 CEO 的摘要

- 結果：4 部分分拆的部分和，與周長少 1 的整數三角形邊長和，有四條差分關係；並因此證明了 Colin Barker 2019 年在 8 條 OEIS 條目上的猜想生成函數。
- 證明我逐步看過，是對的；生成函數有三個獨立程式做精確比較，都相等。重跑 7 秒，結果和紀錄一致。
- 判定 SUPPORTED_NOVELTY_UNCHECKED：沒有 Lean，所以不能標 PROVEN；只查了離線 OEIS，不宣稱新。
- critic 的四條必修都改了；剩一條文件同步（experiment.md、proof.md、程式註解還留著已經不成立的「120 項」舊論證），改完就可以。
- A308758 的 OEIS 草稿和兩份高二版說明正確，可以照草稿流程由使用者自己重寫後送出（一次一條）。
