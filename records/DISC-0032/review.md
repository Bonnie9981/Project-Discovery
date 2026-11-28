# DISC-0032 審查（Reviewer）

審查者：reviewer（獨立 subagent，不是作者）。讀了 `records/DISC-0032/` 全部檔案、`docs/RESEARCH_STANDARDS.md`、`paper/a336662-manhattan.md`、`results/A336662/` 全部檔案（README、OEIS 草稿、兩份高二版說明、`code/check_a336662.py`）。
OEIS 文字、論文、程式輸出都當資料看；裡面沒有要求 agent 做事的文字。

## 審查項目

1. **結論有沒有被說成「證明」。** 紙上證明加 n ≤ 16 暴力和中點對應逐條檢查；沒有 Lean。proof.md、論文、兩份說明都寫明「沒有 Lean」，沒有標 PROVEN。合格。
2. **critic 必修 1（Step 1 二部圖論證、b ≥ a+4）——已改。** 論文 Step 1 現在寫：同種的兩步，兩倍中點相差兩個座標都是偶數，經 A 後不會距離 1（並舉東北西南西的第 1、5 步）；反方向用「b − a 偶數（二部圖）、b − a ≥ 4、第 a+1 步和第 b 步一橫一直」。我手算核對：一橫一直兩步的兩倍中點相差 (±1,±1) ⇔ 共用端點；A(a,b) 在 a、b 都奇數時 L1 長度 = max(|a|,|b|)，所以距離 1 ⇔ 差 (±1,±1)。論證正確、完整。
3. **critic 必修 2（A337353 範圍 n ≥ 1、原式每項都不成立）——已改。** 論文定理寫 4·A336662(n−1)（n ≥ 1），並寫原式「fails for every n >= 1」。程式 H2 迴圈從 n = 1 開始，也檢查 `nr[n] != 4*mh[n]`。我在 terms.pkl 上重驗：原式在已存的 39 個 n（含 n = 0）**全部**不成立。論文寫「every n >= 1」是對的（只是沒提 n = 0 也不成立，屬保守，不算錯）。
   - 還沒改乾淨的地方：`results/A336662/README.md` 仍寫「= 4·A336662(n−1)（n ≥ 2）」；`literature.md` 和 `search_evidence.jsonl` S001 仍寫「n ≥ 2」「n = 1 就不成立」。proof.md 的「更正」段已說明，記錄檔不必改，但 README 要改（見最終判定）。
4. **critic 建議 4（offset 從資料讀）——已改。** `check_a336662.py` 現在用 `oeis_terms` 讀進來的 offset（om、ob、oc）算關係的範圍，沒有寫死。
5. **critic 建議 3（A322419 推論）——論文已加，草稿沒加。** 論文定理下方加了 A336662(n) = A322419(n+1)/2、A337353(n) = 2·A322419(n)（n ≥ 1）。我在 terms.pkl 上重驗：A322419 offset 0、41 項；第一條對所有重疊的 n ≥ 0 成立，第二條對所有 n ≥ 1 成立（n = 0 時 1 ≠ 2，所以 n ≥ 1 是對的），A322419(n) = 4·A189722(n)（n ≥ 2）也成立。這兩條程式沒有檢查，只有我和 critic 在已存項上驗過；它們是由 H1、H2 加 OEIS 現有的 A322419 公式直接推出，沒問題。OEIS 草稿和高二說明都沒用上 A322419（非必要）。
6. **Step 2、Step 3、鏡射、一一對應。** critic 已逐案手算；我抽查 Step 2 的 e_i=(1,0)、e_{i+1}=(0,1) 例和 Step 3 向東偶數列的情況，結論相同。一一對應是「直走／轉彎」字串的雙射，兩邊都是 2^(m−2)，論證完整。
7. **offset。** 從 sqlite 和 terms.pkl 讀：A189722 offset 2、A336662 offset 0、A337353 offset 0、A322419 offset 0。和 proof.md「敘述差異」一致。
8. **程式獨立性。** experiment.md 說三種列舉是「彼此獨立的程式路徑」：三個計數函式確實各寫各的，但 `midpoint_check` 和 `manhattan_nocontact` 共用 `manhattan_ok`（critic 第 10 點）。critic 的 `critic_0032.py`（不 import 專案模組、換了方向約定、直接比對集合）補上了獨立性；但它放在 scratchpad，不在 repo 裡（見待修）。
9. **新穎性——比紀錄寫的更接近「已知」。** 我在 OEIS 離線庫重查 A337353、A336662、A189722、A322419 的 N/C/F/Y 行：
   - A337353 的 F 行「a(n) = 4*A336662(n)」本身就是 A337353 和 A336662 的關係，只是下標差一格（把整串往右移一格就全部吻合），屬於打字等級的錯誤。
   - A337353(n) = 8·A189722(n) 是定義層級的對稱（不能連續同向又不能回頭 ⇒ 每步都轉；4 個起始方向 × 2 個第一轉向）；A322419 已有 a(n) = 4·A189722(n)。
   - 所以 H1「A336662(k) = 2·A189722(k+1)」= 「A337353 那行公式改正下標」再除以 8·A189722 的對稱，**OEIS 上已經記載（下標寫錯）**，只是沒有證明。研究規範的 `SUPPORTED_KNOWN` 是「文獻、OEIS 有記載」；照 DISC-0031 的先例（OEIS 上有無證明的經驗式即算已知），這裡也應算已知。
   - 證明方法本身是 Watson 1970 覆蓋格子對應的特例（S002 逐字讀過）；「覆蓋路徑剛好是 Manhattan 格子」這一步沒找到明文出處，但它只是證明手法，不是新的計數結果。
   - 結論：本紀錄的實際貢獻是「更正 A337353 的下標」加上「給一個簡短證明、補交叉引用」。不是新發現。
10. **OEIS 草稿有沒有誇大。** 沒有宣稱新穎；A337353 那條是更正，說法「does not match the data for any n >= 1」正確；A336662 那條附了一句證明並標明是 Watson 對應。可以送，但建議（非必要）在 A336662 那條註明「這等於 A337353 現有公式改正下標後的形式」並加 `Cf. A322419`，讓編輯一眼看出不是新關係。連結的 GitHub 頁要等合併後才有效，草稿已寫明。
11. **兩份高二說明是否只寫檔案支持的內容。**
    - `程式說明.md`：函式名、輸出字串、32767 條、k ≤ 38、n ≤ 39 都和程式與我跑出的輸出一致。寫「確認原公式 A337353(1) = 4·A336662(1) 不成立」比程式實際做的少（程式檢查每個 n ≥ 1），保守，不算錯。「三個函式各寫各的」對三個計數函式是對的。
    - `證明方法說明.md`：內容和論文一致（含東北西南西反例、b − a ≥ 4、n = 1 也成立）。兩個問題：(a) 判定那段寫「暫定 SUPPORTED_NOVELTY_UNCHECKED」，要改成本審查的判定和理由；(b) CLAUDE.md 規定要標明超出高二的地方，目前沒有明標（「轉 45 度、放大」其實是線性變換 A；「西洋棋盤黑白交錯」是二部圖；Watson 覆蓋格子），要加註。

## 重現結果

- `python -m discovery.quiet -- python results/A336662/code/check_a336662.py 16`：exit 0，輸出
  `brute n <= 16 OK; midpoint map checked on 32767 walks; OEIS A189722:16 A336662:17 A337353:17 relations on stored terms: k<=38, n<=39`，和 experiment.md、程式說明.md 寫的完全一樣。完整紀錄在 `logs/python_results_A336662_code_check_a336662.py_16.log`。
- critic 的獨立程式 `python -I critic_0032.py`（scratchpad）重跑：三條序列 n ≤ 14 的值和 terms.pkl 相同；原式 4·A336662(n) 在 0…14 全部不成立；中點對應加鏡射在 m ≤ 13 直接比對集合成立。
- 我另外在 terms.pkl 上驗：A336662(n) = A322419(n+1)/2（全部重疊 n ≥ 0）、A337353(n) = 2·A322419(n)（n ≥ 1）、A322419(n) = 4·A189722(n)（n ≥ 2）、A337353(n) ≠ 4·A336662(n)（全部 39 個 n）。都成立。
- 全部在 `config/limits.json` 上限內（主程式約 7 秒）。

## 最終判定

STATUS: SUPPORTED_KNOWN

| 候選 | 判定 | 和 record.json 比 |
|---|---|---|
| A336662（= 2·A189722(k+1)，k ≥ 1） | `SUPPORTED_KNOWN` | 不同（record 寫 `SUPPORTED_NOVELTY_UNCHECKED`） |
| A337353（= 4·A336662(n−1)，n ≥ 1；= 8·A189722(n)，n ≥ 2；原式下標錯） | `SUPPORTED_KNOWN` | 不同（record 寫 `SUPPORTED_NOVELTY_UNCHECKED`） |
| 整份紀錄 | `SUPPORTED_KNOWN`（取研究目標 A336662 的狀態） | 不同 |

數學上沒有錯：紙上證明正確，程式重現成功，critic 的兩項必修都改了，兩項建議論文都做了。降級只因為新穎性：A336662 與 A337353 的關係 OEIS 早就寫在 A337353 的 F 行（下標錯一格、沒有證明），A337353 = 8·A189722 是定義層級的對稱，A322419 = 4·A189722 也已在 OEIS；所以這是「更正下標加補證明」，不是新公式。沒有 Lean，所以不能標 PROVEN。

**record.json 要改的地方**（我沒有動其他檔案）：
1. 最上層 `"status"` 改成 `"SUPPORTED_KNOWN"`（不改的話 `check_record` 會因為和本檔 STATUS 不一致而失敗）。
2. `candidates.A336662.status`、`candidates.A337353.status` 都改成 `"SUPPORTED_KNOWN"`。
3. `novelty.status` 維持 `"NO_MATCH_IN_SCOPE"`（`PARTIAL_MATCH` 只能由程式給）。`novelty.note` 改成／補上：`"The relation is recorded in OEIS: A337353 has the (unproved) formula a(n) = 4*A336662(n), which is off by one index; A337353(n) = 8*A189722(n) is an elementary symmetry and A322419 already has 4*A189722(n). So A336662(k) = 2*A189722(k+1) is the index-corrected form of an existing OEIS formula: SUPPORTED_KNOWN. Contribution: index correction of A337353 plus a short proof (Watson 1970 covering-lattice bijection made explicit; the Manhattan identification was not found stated in the sources read). Not claimed as new."`

**其他還要修的項目**：
1. `results/A336662/README.md`：「A337353(n) = 8·A189722(n) = 4·A336662(n−1)（n ≥ 2）」改成「= 8·A189722(n)（n ≥ 2），= 4·A336662(n−1)（n ≥ 1）」；並註明狀態 `SUPPORTED_KNOWN`（下標更正 + 證明）。
2. `results/A336662/證明方法說明.md`：「判定與限制」改成 `SUPPORTED_KNOWN` 並寫理由（A337353 的 F 行早已寫了這個關係，只是下標錯）；把超出高二的地方標出來（45° 轉放大＝線性變換、二部圖、Watson 覆蓋格子）。若已轉 PDF 要重轉。
3. `RESEARCH.md`：新增 DISC-0032 一節和候選清單，狀態寫 `SUPPORTED_KNOWN`（目前 `RESEARCH.md` 沒有 DISC-0032，`tests/test_research_summary.py` 會擋）。
4. 把 critic 的 `critic_0032.py` 放進 repo（例如 `research/r003/` 下），再跑 `python -m discovery.independence`；不然獨立實作只存在暫存區，研究規範第 2 節第 3 項的「兩個獨立實作」在 repo 內只有部分成立。
5. （建議）OEIS 草稿 A336662 那條註明「這是 A337353 現有公式改正下標後的形式」，並加 `Cf. A322419`；`experiment.md` 附加一句「計數函式彼此獨立，但中點檢查與 Manhattan 計數共用 `manhattan_ok`」。

## 給 CEO 的摘要

- 數學是對的：一直轉彎的蛇（A189722）乘 2 等於 Manhattan 格子上沒有接觸的路徑（A336662），A337353 現有公式下標錯一格，正確是 4·A336662(n−1)（n ≥ 1）。程式重跑全部通過，critic 指出的 Step 1 漏洞已補好。
- 但不是新發現：這個關係 OEIS 在 A337353 早就寫了（只是下標打錯、沒證明），所以兩個候選和整份紀錄都改判 `SUPPORTED_KNOWN`。值得做的是送 OEIS 更正 A337353 的下標，附上簡短證明。
- 沒有 Lean，不能標 PROVEN。合併前要改 record.json 的三個狀態、README 的 n ≥ 2、高二說明的狀態和超出高二的標註、補 RESEARCH.md，並把 critic 的獨立程式放進 repo。
