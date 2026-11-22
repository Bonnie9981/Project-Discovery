# Project Discovery

一套用 AI 輔助、但**以證據為準**的研究系統。目標：在數學、物理、AI 與工程問題上，產生**可重現、可驗證、可被獨立反駁**的成果。

研究成果的白話摘要見 [RESEARCH.md](RESEARCH.md)，開發大事見 [DEVLOG.md](DEVLOG.md)。

> 規則第一條：任何 agent（包括 Claude）都不能自己宣布成功。成果必須經過反例搜尋、獨立實作驗證、新穎性檢查，並留下可重跑的紀錄。

## 目前狀態：Phase 2 進行中（2026-11-22）

| 階段 | 狀態 |
|---|---|
| Phase 0 研究基礎建設 | 完成：repo、Python + pytest、Lean 4 + Mathlib（CI 編譯並自動稽核公理）、六個 agent、SQLite 任務庫、驗證機制 |
| Phase 0.5 研究完整性 | 完成：雙實作真正獨立、九級新穎性狀態、OEIS 離線快照、查詢存證 |
| Phase 1 研究流程驗證 | 完成：M1.1 重現已知定理（DISC-0003）、M1.2 10 條 L1 候選（DISC-0004、0005）、M1.3 3 條過初篩（DISC-0006）、M1.4 第一條完整 Lean 證明（DISC-0007，C02） |
| Phase 2 結構性數學發現 | 進行中：DISC-0008、DISC-0009 證明 OEIS A334504 的奇數項與偶數項猜想（規則 26 週期）；DISC-0010、DISC-0011 證明規則 54 暫態公式在寬度除以 4 餘 0、2、3 時成立 |

各項研究的白話說明見 [RESEARCH.md](RESEARCH.md)。目前沒有任何結果被宣稱為新發現。

已知限制：
- 程式端連不到 oeis.org、OpenAlex；線上查詢透過使用者的瀏覽器進行並存證。Lean 的正式結果以 GitHub CI 為準。
- MathSciNet、Google Scholar 尚未查詢。
- Orchestrator 目前是 Claude Code 主執行緒，不是背景常駐程式。

## 快速開始

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
python -m discovery run R-001        # 重跑 R-001，產生新的 DISC 紀錄
python -m discovery list             # 列出任務與研究紀錄
python -m discovery new R-001 "題目"  # 建立空白完整紀錄給六個 agent 填
python -m discovery.check_record     # 檢查所有紀錄是否完整
python -m discovery.digest           # 每份紀錄一行摘要（省 token，見 docs/TOKEN_BUDGET.md）
python -m discovery.quiet -- <指令>   # 長輸出存到 logs/，只印摘要
cd lean && lake build                # 編譯 Lean（需先安裝 elan）
```

## 結構

```
discovery/        核心：資料庫、驗證層、紀錄產生器、紀錄檢查器、CLI
lean/             Lean 4 + Mathlib 形式化證明
.claude/agents/   六個研究角色
research/R-001/   研究線 R-001：整數序列與數論猜想
records/          每次研究一個 DISC-XXXX 資料夾（report.md + result.json）
docs/             研究規範與判定標準
tests/            自動測試
```

詳見 [docs/RESEARCH_STANDARDS.md](docs/RESEARCH_STANDARDS.md)。
