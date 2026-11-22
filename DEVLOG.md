# 開發日誌

只記大事件，新的在下。時間為台北時間。

## 2026-11-22

- **建立專案**：依 ChatGPT 規劃的 Project Discovery 建立 repo，第一條研究線是 R-001 整數序列。
- **M0.1 骨架完成（PR #1，15:24）**：只增不改的 SQLite 紀錄庫、雙實作驗證、新穎性檢查。首份紀錄 DISC-0001 找到的序列被正確判定為已知結果（Euler lucky numbers），沒有誤報成新發現。
- **Phase 0 七項完成（PR #2 15:29、PR #3 15:54）**：Lean 4 + Mathlib 在 GitHub Actions 編譯並做公理檢查；定義六個 agent（Literature、Hypothesis、Experiment、Critic、Proof、Reviewer）；紀錄檢查器。DISC-0002 走完整套流程，獨立 critic 找出七個問題（含 Miller–Rabin 上界寫錯、文獻敘述有反例），全部修正或記為已知限制。
- **Phase 0.5 研究完整性升級（PR #4 16:12）**：與 ChatGPT 審查後修正三個漏洞：Lean 公理檢查寫死定理數、雙實作共用程式而不獨立、OEIS 查無結果就判為新穎。新增九級新穎性狀態（未命中不會自動升級）、agent 權限與資源上限、版本鎖定。
- **OEIS 離線快照（PR #5 16:20）**：下載 OEIS 全庫（401,773 條）到本機，只把 SHA-256 清單放進 git，並用真實資料校正比對門檻。
- **DISC-0003 開始**：連續正整數表示法，以已知定理 R(N) = N 的奇因數個數（OEIS A001227）當基準。
- **DISC-0003 完成，M1.1 基準重現（PR #8）**：三套獨立實作在 N ≤ 100000 確認「連續正整數表示數 = 奇因數個數」，Lean 在 CI 證明一般情形（另證 2 的冪恰為唯一不能寫成 ≥2 項之和的數、公差 2 版本）。刻意放入的錯誤猜想在 N = 4 被推翻。獨立 reviewer 判定 `PROVEN_KNOWN`（已知結果，不是新發現）。13 條延伸序列 12 條 OEIS 已有，1 條查無但只標 `NO_MATCH_IN_SCOPE`。
