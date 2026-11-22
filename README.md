# Project Discovery

一套用 AI 輔助、但**以證據為準**的研究系統。目標：在數學、物理、AI 與工程問題上，產生**可重現、可驗證、可被獨立反駁**的成果。

研究成果的白話摘要見 [RESEARCH.md](RESEARCH.md)，開發大事見 [DEVLOG.md](DEVLOG.md)。

> 規則第一條：任何 agent（包括 Claude）都不能自己宣布成功。成果必須經過反例搜尋、獨立實作驗證、新穎性檢查，並留下可重跑的紀錄。

## 目前狀態：Phase 0 完成到 P0-07（等待 CEO 驗收 M0.1～M0.3）

| 任務 | 狀態 |
|---|---|
| P0-01 GitHub repo | 完成 |
| P0-02 Python 環境 + pytest | 完成（只用標準函式庫 + pytest） |
| P0-03 Lean 4 + Mathlib | 完成：`lean/`，在 GitHub Actions 編譯，依賴鎖定，自動稽核公理 |
| P0-04 六個 agent | 完成：`.claude/agents/`，分工見 [docs/AGENTS.md](docs/AGENTS.md) |
| P0-05 SQLite 任務庫 | 完成：結果只能新增，中斷可續跑 |
| P0-06 驗證機制 | 完成：雙實作交叉檢查、新穎性檢查、紀錄完整性檢查器 |
| P0-07 首次完整演練 | 完成：`records/DISC-0002/` |

已知限制：
- 開發環境連不到 oeis.org、OpenAlex、Lean 下載站。新穎性的線上查詢尚未實測成功；Lean 只在 CI 上編譯。
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
