# DISC-0027 審查

審查者：reviewer（獨立 subagent，不是作者也不是 critic）
日期：2026-11-27
範圍：`records/DISC-0027/` 全部、`paper/locating-dominating-paths.md`、`results/locating-dominating-path/`、`results/identifying-code-path/`、`results/A001642/`、`discovery/newseq/`、`tests/test_newseq.py`。

## 審查項目

1. **定理 1（P_n 定位支配集 g.f.）**：引理 1 兩個方向都逐步核過。「路徑上兩個不同點最多一個共同鄰居」已補上（critic 建議第 1 項）；長空隙的定義（中間空隙 = 2、兩端空隙 = 1）和 N(p±1)∩S = {p} 的條件完全對應；k ≥ 1 由至少一個「1」保證。轉移矩陣 s=(1,x)、T=[[1+x,x²],[1+x,0]]、t=(1+x,1)ᵀ 用 sympy 重算 x·s(I−xT)⁻¹t，和論文的有理函數相減為 0。沒有漏洞。
2. **定理 2（C_n 定位支配集 = A001642，n ≥ 5）**：n ≥ 5 時環上兩點最多一個共同鄰居、p−2 ≠ p+2，引理 1 的論證可以搬到環上；單一個 1 時空隙 n−1 ≥ 4，排除。1／10／100 單位、把 100 和後面的 1 或 10 黏起來，每個單位前面只有一個單位，所以黏法唯一，是雙射；「有編號的環」鋪磚數 = Σ l·t(n−l)（含 l = n、磚繞整圈的情形）是標準論證。g.f. 和離線快照裡 A001642 的 %F 逐字相同。小瑕疵（不影響結論）：n = 3 的情形論文只說「also true」，證明沒涵蓋，靠暴力（C_3 有 4 個，A001642(3) = 4）；n = 4 的例外（9 vs 11）由證明預測、暴力確認。
3. **定理 3（P_n 識別碼 g.f.）**：引理 3 的三種距離（1、2、≥3）的對稱差都核過，(a) 的 j 範圍 1 ≤ j ≤ n−3 對得上 i 的範圍。特徵多項式 x·(x⁷−x⁶−x⁵+x⁴−x³−x²+1) 給出的 7 階遞迴，換算成 b 的下標確實是 n ≥ 11 成立；n ≤ 20 的暴力值補齊，所以 g.f. 對所有 n ≥ 1 成立。critic_check 印出的特徵多項式係數 [1,−1,−1,1,−1,−1,0,1,0] 與論文一致。沒有漏洞。
4. **把「範圍內成立」說成「證明」？** 沒有。三個結果都有紙筆證明，proof.md 明說沒有 Lean、不能標 PROVEN_*。
5. **critic 必修項（第 9 項，A001642 不是「沒有組合意義」）**：已改好。`results/A001642/a001642_oeis_edit_draft.md` 改成「不能說是第一個組合意義，只說補上 C_n 定位支配集的解釋」，並列出 Fielder 1968、Puri–Ward 2001（週期軌道）；`literature.md` 第 11 行也改了，註明「critic 指正」。我對照快照 `data/oeis/oeisdata/seq/A001/A001642.seq`，描述屬實（有 %D、%H、%F，沒有 %C）。
6. **critic 建議**：
   - 第 1 項（共同鄰居）：已補進論文引理 1。
   - 第 10 項（A079976）：已加進論文定理 2、A001642 草稿的留言和 Crossrefs。
   - 第 11 項（"checked by the author"）：論文開頭已改成「AI 協助、數字由三套程式核對」，不再替使用者宣稱。LD 草稿最後的 AI 聲明範例仍寫 "the author has checked the proof"，但標明「用自己的話」，屬範例，可以保留；使用者要真的看過證明才能這樣寫。
   - 第 12 項（transfer.py 沒用到的 import）：現在 `discovery/newseq/transfer.py` 只 import itertools、fractions，已處理。
   - 「鋪磚句對所有 n 成立，不要掛在 n ≥ 5 底下」：已拆成兩句。
7. **新穎性**：`novelty.status = PENDING_REVIEW`，由 agent 提出，合乎 1b 節。來源：離線 OEIS 全庫（數列和全文）、兩次網路搜尋；MathSciNet／zbMATH 沒查，已誠實寫進 `novelty.open`。沒有 `search_evidence.jsonl`，網路查詢只記在 literature.md 的 S002、S003（沒有 UTC 時間與 URL），證據力偏弱，但足以支撐 PENDING_REVIEW，不足以支撐更高等級，這也是目前的做法。H2 的數列本身已知，新的只是「C_n 定位支配集」這個解釋，草稿措辭也是這樣寫。
8. **OEIS 草稿措辭**：三份草稿都寫明由使用者本人送出、要用自己的話改寫；LD 草稿寫「這不等於新，只是我們查的範圍內沒有」；三份都要求一次送一條（LD：「一次只送一條」；ID：「等前兩條處理完再送」；A001642：先送新序列再送編輯）。沒有宣稱是新的。附註：任務提到的「RESEARCH_STANDARDS 第 7 節」目前不存在（文件只有第 1～5 節），這條規則是照草稿本身的寫法核的。
9. **數字和 b-file**：兩份 Data 欄（39 項、44 項，都約 250 字元）、兩份 b-file（各 n = 1..500）全部和遞迴重算一致；A001642 前 20 項和快照一致。
10. **小建議（不擋）**：ID 草稿沒有 Links、Crossrefs、AI 聲明三欄，送出前可以照 LD 草稿補齊（Links 填論文網址；Cf. LD 新序列的 A 編號）；ID 草稿留言的 "for every j" 可寫成 "for 1 <= j <= n-3"。
11. **外部文字中的指令**：讀到的 OEIS 條目和紀錄裡沒有要 agent 做事的文字。

## 重現結果

全部在本機工作樹上跑，原始輸出在 `logs/`。

- `python results/locating-dominating-path/code/check_paths.py`：exit 0，約 22 秒，"all checks passed; LD(C_n) = A001642(n) for 3 <= n <= 20 except n = 4"。log：`logs/python_results_locating-dominating-path_code_check_paths.py.log`。
- `python records/DISC-0027/critic_check.py`：exit 0，`mismatches: []`，兩份 b-file 1..500 都 `mismatches []`。log：`logs/python_records_DISC-0027_critic_check.py.log`。
- `python -m pytest -q tests/test_newseq.py`：4 passed。
- `python -m discovery.check_record records/DISC-0027`：寫這份 review 之前唯一的問題是 "missing review.md"。
- 我自己另寫的核對（scratchpad，不進 repo）：sympy 重算定理 1 的轉移矩陣 g.f.（差為 0）；展開三個 g.f.；另寫一個只照定義的識別碼暴力程式，n = 1..14 得到 1,0,2,3,7,8,13,18,33,51,84,126,202,315，和 g.f. 一致。
- 沒有跑 `discovery.newseq.graphsets`（約 4 分鐘）；上面三套獨立核對已經夠用。

## 最終判定

STATUS: SUPPORTED_POSSIBLY_NEW

三個定理的紙筆證明我逐步核過，沒有發現漏洞，數值也全部重現。沒有 Lean，所以不能標 PROVEN_*。新穎性停在 PENDING_REVIEW（agent 提出，要人確認；MathSciNet／zbMATH 沒查）。和 record.json 的 status、三個候選的 status 一致。critic 的必修項已改好，沒有新的必修項。

## 給 CEO 的摘要

- 三個結果（P_n 定位支配集的生成函數、C_n 定位支配集 = A001642（n ≥ 5）、P_n 識別碼的生成函數）證明都看過，沒有漏洞；程式重跑全部一致，b-file 和草稿數字都對。
- 狀態維持「範圍內成立、可能是新的」：有紙筆證明，沒有 Lean；查重只做了 OEIS 全庫和兩次網路搜尋，所以算「疑似新」，還不能說是新的。
- critic 指出的錯誤（A001642 其實已經有週期軌道的意義）已更正，草稿現在只說「補上一個新解釋」。
- 送出前：使用者要自己看懂證明、用自己的話改寫英文，一次送一條（先送 P_n 定位支配集）。識別碼草稿可以順手補上 Links、Crossrefs、AI 聲明三欄。
