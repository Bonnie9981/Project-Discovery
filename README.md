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
| Phase 2 結構性數學發現 | 進行中：DISC-0008、DISC-0009 證明 OEIS A334504 的奇數項與偶數項猜想（規則 26 週期）；DISC-0010～DISC-0012 證明規則 54 暫態公式的四段（寬度除以 4 餘 0、1、2、3）；DISC-0013 證明 OEIS A268754 的奇數項公式 a(2n+1) = 2a(n) |

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

repo 分兩大區：**工具**（將來可能抽成開源工具）和**成果**（每條 OEIS 序列一個資料夾）。

```
── 工具區 ──────────────────────────────────────────
discovery/        核心套件：紀錄檢查、證據獨立性、新穎性查詢、digest/quiet（省 token）、CLI
.claude/agents/   六個研究角色（literature、hypothesis、experiment、critic、proof、reviewer）
research/r001/    通用引擎：整數序列批次搜尋（R-001）
research/r002/    通用引擎：一維細胞自動機模擬，三種獨立實作（R-002）
research/r003/    通用引擎：CA 結果和 OEIS 的算術比對（R-003）
docs/ config/     研究規範、token 預算、資源上限
tests/            自動測試
── 成果區 ──────────────────────────────────────────
results/A334504/          規則 26 環上的週期（DISC-0008、0009）：短文、OEIS 草稿、規格審計、檢查腳本
results/A268754/          a(2n+1) = 2a(n)（DISC-0013）
results/A071052/          a(2n) = a(n) + 2n（DISC-0014）
results/rule54-transient/ 規則 54 暫態，OEIS 新序列草稿（DISC-0010～0012）
paper/            OEIS 連過來的證明頁（網址固定，不搬）
records/          研究流水帳：每次研究一個 DISC-XXXX 資料夾，只增不改
lean/             Lean 4 證明（一個 Lake 專案，CI 綁這個路徑）
```

各序列資料夾的 README 列出對應的 DISC 紀錄和 Lean 檔。舊路徑對照見 [results/README.md](results/README.md)。

詳見 [docs/RESEARCH_STANDARDS.md](docs/RESEARCH_STANDARDS.md)。
