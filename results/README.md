# results/：研究成果，一條 OEIS 序列一個資料夾

| 資料夾 | 結果 | 紀錄 |
|---|---|---|
| [A334504/](A334504/) | 規則 26 環上的週期（奇數、偶數寬度） | DISC-0008、0009 |
| [A268754/](A268754/) | a(2n+1) = 2a(n) | DISC-0013 |
| [A071052/](A071052/) | a(2n) = a(n) + 2n | DISC-0014 |
| [A118109/](A118109/) | 規則 54 單細胞各列：遞迴、下取整公式 | DISC-0015 |
| [A265225/](A265225/) | 規則 54 前 n 列 ON 總數：封閉式、遞迴；Ianakiev 註解差一個索引 | DISC-0015 |
| [A085588/](A085588/) | 規則 150 環的最終週期整除 2^D(2^s−1)；條目留言的整除方向寫反 | DISC-0016 |
| [A294646/](A294646/) | 猜想「a(n) 不會是 2n−2」的反例 n = 9814447404 | DISC-0017 |
| [A231897/](A231897/) | 猜想「a(n) 不會是 −1」：(2^n−1)^2 有 n 個 1 | DISC-0018 |
| [A215461/](A215461/)、[A215462/](A215462/) | 猜想「n 夠大時 a(n) 不是 0」：一行證明 | DISC-0018 |
| [A215944/](A215944/) | Coman 猜想的反例 3048841 = 61·151·331 | DISC-0019 |
| [A058128/](A058128/) | Rotondo 2024 猜想：偶數 n 時 a(n) 是質數或弱偽質數（證明） | DISC-0019 |
| [A218483/](A218483/) | 沒有 40n+15 型的 2 底偽質數等三條（證明） | DISC-0019 |
| [A321790/](A321790/) | 補上「?」= 873181，搜尋範圍 | DISC-0019 |
| [rule54-transient/](rule54-transient/) | 規則 54 暫態，新序列草稿 | DISC-0010～0012 |

狀態：**全部是內部草稿。** 對外（OEIS 送出）由使用者本人決定、本人送出。署名 Chi Hsia，附 AI 使用聲明。

## 新增一條序列時

1. 開 `results/A??????/`，放 `README.md`（列出 DISC 紀錄和 Lean 檔）、短證明、OEIS 草稿，檢查腳本放 `code/`。
2. `code/` 裡的腳本要用 repo 的模組時，用 `sys.path.insert(0, str(Path(__file__).resolve().parents[3]))`。
3. OEIS 要連的證明頁放 `paper/`（網址一旦送出就不能動），其餘放這裡。
4. 研究過程照舊寫在 `records/DISC-XXXX/`（流水帳，只增不改），Lean 照舊放 `lean/Discovery/`。

## 舊路徑對照（2026-11-22 整理前）

舊紀錄（records/ 裡）提到的路徑沒有改，照這張表找：

| 舊路徑 | 新路徑 |
|---|---|
| `paper/a334504.tex`、`oeis_edit_draft.md`、`spec_audit.md`、`literature_check.md` | `results/A334504/` |
| `paper/a268754_oeis_edit_draft.md` | `results/A268754/` |
| `paper/a071052_oeis_edit_draft.md` | `results/A071052/` |
| `paper/rule54_oeis_new_sequence.md`、`rule54_transient.html`、`paper/b_rule54_transient.txt` | `results/rule54-transient/` |
| `research/r003/l01_check.py`、`l02_check.py` | `results/A334504/code/` |
| `research/r003/l06_*`、`critic_c_a268754.py` | `results/A268754/code/` |
| `research/r003/l07_*`、`critic_c_a071052.py` | `results/A071052/code/` |
| `research/r003/l03_*`、`l04_*`、`l05_*`、`critic_c_mod1.py` | `results/rule54-transient/code/` |
| 證明頁 `a334504.pdf`、`a268754-odd.md`、`a071052-even.md`、`rule54_transient.pdf` | 沒動，還在 `paper/`（OEIS 連結） |
