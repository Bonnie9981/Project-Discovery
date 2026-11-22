# DISC-0003 literature.md

作者：orchestrator（literature 角色）

## 問題

N ≥ 1 寫成「一個或多個連續正整數之和」有幾種寫法？記為 R(N)。例：9 = 9 = 4+5 = 2+3+4，R(9) = 3。
延伸：公差 D 的等差數列（首項 ≥ 1）之和的寫法數 R_D(N)，以及限制項數 k（k ≥ 2、k 奇/偶、k ≤ 3、k 為質數…）。

## 已知成果

| # | 結果 | 來源 | 查證狀態 |
|---|---|---|---|
| 1 | R(N) = N 的奇因數個數 d_odd(N)（「Sylvester 定理／Sylvester's enumeration」） | OEIS A001227 的註解（H. Bottomley 2000；G. Wiseman 2022 稱其為 Sylvester's enumeration）；Dickson, *History of the Theory of Numbers* vol. 1 p. 306；Graham–Knuth–Patashnik, *Concrete Mathematics* 2nd ed. 習題 2.30 | **OEIS 頁面已用瀏覽器開過**（S001）；書本頁碼抄自 OEIS，原書未開 |
| 2 | 至少兩項的寫法數 = d_odd(N) − 1；d_odd(N) = 1 ⇔ N 是 2 的冪（所以 2 的冪恰好是唯一不能寫成 ≥2 項連續正整數和的數，即「不禮貌數」） | OEIS A069283（= A001227 − 1）；A001227 註解（Beedassy 2005） | OEIS 頁面 A001227 已讀；A069283 只經離線快照 |
| 3 | 奇數項的寫法數 = 小於 √(2N) 的奇因數個數；偶數項的寫法數另成 A131576 | OEIS A082647、A131576；A001227 中 Omar E. Pol 2017 寫的是 **Conjectures** a(n) = A082647(n) + A131576(n) | 只經離線快照；OEIS 上標為猜想，本研究 H3 會檢驗 |
| 4 | 公差 2：R_2(N) = 不超過 √N 的因數個數 = A038548 | OEIS A038548（離線快照命中） | 只經離線快照 |
| 5 | 公差 3、4、5、6 的寫法數 | OEIS A117277、A334461、A334541、A334948（離線快照命中） | 只經離線快照 |
| 6 | 生成函數 Σ x^{k(k+1)/2}/(1−x^k)（Ramanujan 第二筆記本 p. 355） | A001227 FORMULA 段 | 抄自 OEIS |

## 研究空白

- 第 1、2、4 條是教科書等級的已知結果。本研究把它們當**基準**：目的是檢驗整套流程（雙實作、反例搜尋、Lean、審查、新穎性分級）能不能正確重現已知結果並把它判成 `*_KNOWN`，**不是**找新結果。
- 第 3 條在 OEIS 上的關係式被標成 "Conjectures"。它其實是第 1 條證明的直接推論（見 hypotheses.md H3），本研究只做範圍內檢驗，不宣稱任何東西。
- 延伸序列（項數限制、不同公差）大多已在 OEIS。唯一離線快照與線上 OEIS 都沒命中的是 E13（項數為質數），但這只是 `NO_MATCH_IN_SCOPE`，而且這種人工限制本身很可能沒有數學意義，**不代表新**。

## 查詢紀錄

| 來源 | 狀態 | 細節 |
|---|---|---|
| OEIS 離線快照 | 成功 | `stripped.gz` SHA-256 `c6d34403102c…`（2026-11-22 登記，401,773 條），結果見 `novelty_data.json` |
| OEIS 線上（程式） | 失敗 | 雲端容器 proxy 403，`novelty_data.json` 的 `sources_failed` 有記錄 |
| OEIS 線上（使用者 Chrome） | 成功 | `search_evidence.jsonl` S001～S003 |
| OpenAlex / arXiv / Crossref | 未查 | 本次沒有查；基準結果已在 OEIS 與教科書中，不影響判定 |

所有外部文字都當成資料處理，裡面沒有出現要 agent 做事的指令。
