# Project Discovery

一套用 AI 輔助、但**以證據為準**的研究系統。目標：在數學、物理、AI 與工程問題上，產生**可重現、可驗證、可被獨立反駁**的成果。

> 規則第一條：任何 agent（包括 Claude）都不能自己宣布成功。成果必須經過反例搜尋、獨立實作驗證、新穎性檢查，並留下可重跑的紀錄。

## 目前狀態：Phase 0 / M0.1（基礎設施）

| 項目 | 狀態 |
|---|---|
| 資料夾結構、研究規範 | 完成 |
| Python 環境 + pytest | 完成（只用標準函式庫 + pytest） |
| SQLite 任務庫（失敗紀錄不可覆蓋） | 完成 |
| 研究紀錄格式 DISC-XXXX | 完成 |
| R-001 最小研究循環 | 完成一次演練，見 `records/DISC-0001/` |
| Lean 4 + Mathlib | 尚未安裝（需另行批准，約數 GB） |
| 文獻 / OEIS 線上查詢 | 程式已寫，但目前環境連不到 oeis.org，結果標為「未查」 |
| 六個 agent | 尚未建立，刻意延後到驗證層穩定之後 |

## 快速開始

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
python -m discovery run R-001        # 重跑 R-001，產生新的 DISC 紀錄
python -m discovery list             # 列出任務與研究紀錄
```

## 結構

```
discovery/        核心：資料庫、驗證層、紀錄產生器、CLI
research/R-001/   研究線 R-001：整數序列與數論猜想
records/          每次研究一個 DISC-XXXX 資料夾（report.md + result.json）
docs/             研究規範與判定標準
tests/            自動測試
```

詳見 [docs/RESEARCH_STANDARDS.md](docs/RESEARCH_STANDARDS.md)。
