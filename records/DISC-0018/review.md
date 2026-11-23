# DISC-0018 審查

審查者：獨立 reviewer subagent（不是作者，也不是 critic）。讀到的檔案、OEIS 摘錄和工具輸出裡沒有出現要 agent 做事的文字。

## 審查項目

1. **Lean 和猜想對得上**：對得上。`a231897_exists` 是 ∀n ∃m ≤ 2^n−1, wt(m·m)=n，正是「永遠不是 −1」。`a215462_pos`（n>19）、`a215461_pos`（n>5）要求奇數、`NonPrime` 含 1、`IsPrime` 是一般定義，和條目定義一致；證的是「至少一種拆法」，即 a(n) ≠ 0。敘述不空洞（存在量詞有具體見證）。
2. **公理**：自己加 `#print axioms`，三個主定理只用 `propext`、`Quot.sound`；檔內沒有 `sorry`、`native_decide`。
3. **紙上證明**：H1 的 a=0 情形已補（critic 建議已處理）；H2 依 2n mod 6 取 9/25/35，2n≡2 時 2n≥44，餘數 ≥9；H3 依 2n mod 3 取 3/7/5。都正確。
4. **不誇大**：全文寫「習題程度、不宣稱新」，A215462 標明是 AIME 1984 #14；邊界 a(5)=0、a(19)=0 明說只靠實驗，不在 Lean 裡。`novelty` 是 `NO_MATCH_IN_SCOPE`，沒有說成新結果。
5. **文獻**：S004 已補上網頁搜尋和 AIME 查詢（critic 建議已處理）。AIME 原文、Lindström 原文沒讀，literature.md 有誠實標示。
6. **OEIS 草稿**：署名格式 `- _Chi Hsia_, Nov 23 2026` 正確；兩份都寫明保留原 Conjecture 句、另加一行；乘號都寫 `*`；A215462 的 mod 6 對應（0→9、4→25、2→35）正確；例子 13^2=169=10101001₂ 確實 4 個 1。語氣平實。
7. **RESEARCH.md／DEVLOG.md**：DISC-0018 一節、候選清單、最後更新日期都有，內容和紀錄一致；DEVLOG 一行，新的在下。

## 必修

- **critic.md 缺 `## 獨立重算`、`## 未解決的疑點` 兩段**，`check_record` 會 FAIL（CI 會擋）。請在 critic.md 末尾附加這兩段（內容可從現有「攻擊項目」「建議」搬：獨立 C 程式重算 n < 2×10^6；未解決疑點＝沒親自連上 OEIS 核對條目現版）。這是格式問題，不影響判定。

建議（不擋）：
- A231897 草稿的 `(2^(n-1)-1)*2^(n+1)` 在 n=0 沒意義，可改寫成 `(2^n-1)^2 = 2^(2*n) - 2^(n+1) + 1 has binary weight n for n >= 1`，或加「for n >= 1」。
- critic 提醒「送出前核對條目目前版本」沒寫進草稿的送出前清單，建議加一條。
- `PROVEN_KNOWN` 定義寫「Lean 4 + Mathlib」，本紀錄只用 core；建議日後把標準改成「Lean 4（core 或 Mathlib）」。

## 重現結果

- `lean lean/Discovery/NeverEasy.lean`（Lean 4.15.0）：約 2.5 秒，exit 0，無警告。
- `python3 results/A231897/code/verify.py`：0.7 秒，輸出和 experiment.md 完全一致（a≤3000 成立、前 25 項吻合、兩套實作 n<600 一致、零點 n<200000 只有 [0,1,5] 與 [0,2,3,4,6,7,10,16,19]、Lean 見證 n<500000 成立）。
- 沒有碰到 `config/limits.json` 上限。

## 最終判定

STATUS: PROVEN_KNOWN

三條猜想都有對得上定義、只用標準公理的 Lean 證明，數值可重現，結果是習題程度且已知（A215462 即 AIME 1984 #14），所以是 PROVEN_KNOWN，不是新穎。

## 給 CEO 的摘要

三條 OEIS「永遠不會」猜想確實被證了，Lean 和數值我都重跑過。OEIS 草稿準確、署名和格式對。唯一必修是 critic.md 少兩個段落標題，補上 CI 才會過；草稿 A231897 的 n=0 寫法可順手修。
