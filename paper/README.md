# paper/：A334504 證明短文（草稿）

- `a334504.tex`：英文短文草稿，人看得懂的證明，不需要讀 Lean。奇數寬度（DISC-0008）和偶數寬度（DISC-0009）兩節。
- `a268754-odd.md`：OEIS A268754 奇數項公式 a(2n+1) = 2a(n) 的英文短證明（DISC-0013），OEIS LINKS 要連的頁面。
- `a268754_oeis_edit_draft.md`：A268754 的 OEIS 編輯草稿（中文說明＋英文文字），使用者自己送出。
- `spec_audit.md`：Lean 敘述和 OEIS 定義的逐項對照；標「待辦」的項目做完前不對外。

狀態：**內部草稿，沒有投稿、沒有上 arXiv、沒有改 OEIS。** 對外的每一步（找教授、arXiv、OEIS、期刊）都要使用者決定。

作者欄先留空，由使用者決定署名；論文 Discussion 有「AI 使用」一段，作者要自己補上本人貢獻。

編譯：`pdflatex a334504.tex`（只用 amsmath、amsthm、hyperref、geometry）。

定位（Gemini 與 ChatGPT 的共識，2026-11-22）：短篇研究筆記等級。新意只主張規則 26 環上的具體軌道結構和週期，不主張 Rule 90、Pascal 三角形或奇偶化約這些方法本身。

## 規則 54 暫態（R2-C10）→ OEIS 新序列

- `rule54_oeis_new_sequence.md`：OEIS 新序列投稿草稿（查重結果、表單各欄、核對清單）。由使用者本人送出。
- `rule54_transient.html` → `rule54_transient.pdf`：人看得懂的短證明（3 頁），四個餘數類都講。PDF 用 Chromium 從 HTML 印出（容器裡沒有 LaTeX，tectonic 下載字型包被擋）。
- `b_rule54_transient.txt`：OEIS b-file，n = 1..1000，用 `research/r002/impl_b.py` 的位元模擬逐一算出。
