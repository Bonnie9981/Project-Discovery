# DISC-0026 審查

審查者：reviewer（獨立 subagent，不是做這份研究或 critic 的 agent）。日期：2026-11-27。

**結論：通過，沒有必修項目。** A372430 的猜想確實被 k = 2^87 + 2^49 推翻；A219433 維持 `INCONCLUSIVE`（只延伸驗證，沒有反例）。下面「建議」是可改可不改的小地方，不影響結論。

外部資料（`data/cx/entries/A372430.txt`、`A219433.txt` 的 OEIS 原文、程式輸出）裡沒有要 agent 做事的文字。

## 審查項目

1. **猜想讀得對不對（只看條目原文）。** A372430 %C 寫：「Conjecture: The only number whose binary indices are a subset of its prime indices is 4100 ... Verified up to 10,000,000.」二進位指標從 1 算（A048793），質數指標 m 指 prime(m) | k。紀錄用的方向是「二進位指標 ⊆ 質數指標」，跟條目數列本身（反方向）分開，沒搞混。4100 → 二進位指標 {3, 13}、5 和 41 整除，跟原文一致，所以從 1 算的讀法正確。A219433 %C：「a(n) < prime(n) except for a(522720)」「tested up to a(1000000)」，紀錄引用正確。
2. **反例成立嗎？** 成立。我自己從頭算：bin(k) 反轉後 1 在第 50、88 位；自己生成質數表得 prime(50) = 229、prime(88) = 457，k mod 229 = k mod 457 = 0。
3. **REFUTED 要兩個獨立實作確認（RESEARCH_STANDARDS 第 1 節）。** 有：C 的 DFS（`a372430_dfs.c`）、`results/A372430/code/check372430.py`（只列至多 4 個 1 位元的數，演算法不同）、critic 自寫的 `critic_a372430_search.py`（全域搜尋，到 2^88 也重新找到同一個數）、Lean kernel 計算，加上我這次的手算。符合。
4. **「最小」的說法。** 「4100 之後最小」只需要到 2^88 沒有其他解：C 的 DFS 和 critic 的 Python 搜尋兩套各自確認，成立。「2^120 以內只有這兩個」只有 C 的 DFS 一套跑完（critic.md 有誠實寫出來）；我讀過 DFS 程式：模數是不同質數的乘積（= lcm），葉節點列出所有 M 的倍數再完整檢查，u128 不會溢位，邏輯沒問題。這是「範圍內窮舉」的電腦結果，沒有被說成證明；proof.md 也寫明最小性沒有形式化。
5. **Lean 定理對不對得上猜想（`lean/Discovery/A372430Counter.lean`）。** 讀過全文。`IsPrime` 是一般定義，`isPrimeB_iff` 證明試除法跟它等價；`primesBelow p = j−1` 加上 p 是質數，就是「p 是第 j 個質數」；`testBit i` 對應二進位指標 i+1（49 → 50、87 → 88），沒有差一。總定理 `a372430_counterexample` 寫的是 k ≠ 4100、k < 2^88、i < 88 的 1 位元只有 49 和 87、兩個質數都整除 k。高位全 0 要由 k < 2^88 推出，沒直接寫成一句「∀ i, testBit → prime(i+1) ∣ k」，但內容等價、忠實。沒有 `sorry`、`native_decide`；檔案被 `lean/Discovery.lean` 第 26 行 import。CI 綠燈、公理只有 propext / Quot.sound 是交付訊息說的，本機沒有 Lean，**我沒有重驗**。record.json 的 11 個 Lean 定理名稱都在檔案裡（check_record 也會檢查）。
6. **新穎性。** 沒有宣稱新。`search_evidence.jsonl` 兩筆（S001 選題、S002 搜這個數字和關鍵字）都只查 OEIS，`coverage_limits` 和 record.json 的 note 都寫明網路、MathSciNet、zbMATH 沒查。`novelty.status = NO_MATCH_IN_SCOPE` 合乎「沒查到 ≠ 新」的規則。RESEARCH.md 的寫法是「OEIS 上沒有人提過」「不宣稱新」，沒有超出證據。
7. **A219433 掃描（`a219433_scan.c`）。** 3-smooth 表完整且排序；12 個質數底的 Miller–Rabin 對 < 2^64 是確定性的；質數上界 n(ln n + ln ln n) 足夠。到 n = 10^8 只有 C 一套跑過（critic 用 C 重跑到 10^7、用自寫 Python 到 6·10^5，都只有 522720）。
8. **record.json。** `status = REFUTED`（合法，取研究目標 A372430 的狀態，符合 1c 節）；候選 A372430 = REFUTED、A219433 = INCONCLUSIVE，都是合法狀態；`critic_model = "opus"`；reviewer 不在 authors 裡。
9. **結果檔一致性。** `results/A372430/code/a372430_dfs.c`、`results/A219433/code/a219433_scan.c` 和紀錄資料夾裡的版本逐字相同（diff 無差異）。OEIS 草稿的數字（154742504911235484315811840、{50, 88}、229、457、5·229·457·525313、2^120）都對過；原 Conjecture 行保留、註明 LLM 輔助、由使用者送出。

### 建議（不必修）

- A219433 的 C 程式在 p·a + 1 超過 2^64 還沒找到質數時印 `NONE`，但**不算進 exceptions**。這種情況其實就是例外（a 已經遠大於 p）。因為 NONE 會印到輸出、紀錄說輸出只有 522720，不影響這次結論；之後重用最好把 NONE 也算成例外。
- A219433 n ≤ 10^8 那次「約 10 分鐘」剛好貼著 `max_seconds = 600`，記憶體約 2034 MiB 也貼著 2048 MB。experiment.md 沒寫是否經 `run_limited` 跑、確切秒數；之後再延伸要先估，超過就報 INCONCLUSIVE。
- A219433 的 10^8 只有單一實作；目前標 `INCONCLUSIVE` 是保守而合理的寫法（跟 DISC-0025 等前例一致），RESEARCH.md 那句可以補一句「單一程式」。
- RESEARCH.md 候選清單「2^120 以下除 4100 外只有它」這句「2^120」那段只有單一實作，可加註；「最小」本身有兩套支持。

## 重現結果

全部在本機跑，二進位檔放 scratchpad，不寫進 repo。

| 指令 | 結果 | 時間 |
|---|---|---|
| `gcc -O2 a372430_dfs.c && ./dfs 30` | 只輸出 4100（自我檢查） | < 0.01 s |
| `./dfs 100` | 4100、154742504911235484315811840；nodes = 264561966，hits = 2，跟 critic 記錄一致 | 7.9 s |
| `python3 results/A372430/code/check372430.py 120` | 暴力 k ≤ 10^6 只有 4100；≤ 4 個 1 位元、k < 2^120 只有 4100 和 k；反例 OK | 6.9 s |
| `python3 records/DISC-0026/critic_a372430_search.py 64` | k < 2^64 只有 4100；因數分解 2^38+1 = [5, 229, 457, 525313] | 2.0 s |
| 自寫 5 行 Python（反轉 bin、自建質數表、取餘數） | 指標 [50, 88]，229、457 都整除 k | 瞬間 |
| `gcc -O2 a219433_scan.c -lm && ./a219 1000000` | 只有 n = 522720, p = 7728803, a = 12582912，跟條目 %C 一致 | 4.0 s |

沒有重跑：`./dfs 120`（3 分 20 秒）、`./a219 100000000`（約 10 分鐘、2 GB）——依交付要求只做小規模重現。

檢查工具：
- `python3 -m discovery.check_record records/DISC-0026`：寫 review.md 之前唯一的錯誤是「DISC-0026: missing review.md」；寫完後重跑結果見下方「最終判定」。
- `python3 -m pytest -q tests`：寫 review.md 之前 77 passed、2 skipped、1 failed，失敗的就是 `test_records.py::test_all_committed_records_pass`，原因同樣是缺 review.md。寫完後重跑結果見下方。

## 最終判定

STATUS: REFUTED

- A372430（研究目標）：`REFUTED`。反例 k = 2^87 + 2^49 有多套獨立實作與 Lean kernel 計算確認；它是 4100 之後最小的這種數（到 2^88 兩套實作都確認）。
- A219433：`INCONCLUSIVE`。n ≤ 10^8 沒有新例外（單一實作；兩套實作一致的範圍到 10^7 / 6·10^5）。這只是「範圍內沒找到」，不是證明。
- 新穎性：`NO_MATCH_IN_SCOPE`，只查了 OEIS，不宣稱新。
- 寫完 review.md 後：`python3 -m discovery.check_record records/DISC-0026` → checked 26 records, 0 problems；`python3 -m pytest -q tests` → 78 passed, 2 skipped。

## 給 CEO 的摘要

Wiseman 在 A372430 猜「二進位指標全都是質數指標的數只有 4100」，我們找到第二個：2^87 + 2^49（約 1.5·10^26），第 50 個質數 229 和第 88 個質數 457 都整除它。這件事很好驗，我自己重算過，Lean 也讓 kernel 直接驗了。它是 4100 之後最小的，到 2^88 有兩套程式各自確認。A219433 延伸到 10^8 沒有新例外，只是延伸驗證。只查過 OEIS，不宣稱新；OEIS 草稿等使用者自己送出。沒有必修項目。
