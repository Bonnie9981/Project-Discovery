# OEIS A212339、A212341（以及 A212344、A212345）：132-避免排列的 marked mesh pattern

紀錄 [DISC-0031](../../records/DISC-0031/)。證明頁 [paper/a212339-marked-mesh.md](../../paper/a212339-marked-mesh.md)。序列關係挖掘（`discovery/relmine.py`，嚴篩選）找到的第三個結果。

| 檔案 | 內容 |
|---|---|
| `a212339_oeis_edit_draft.md` | OEIS 編輯草稿（四條，一次送一條），使用者自己送出 |
| `code/check_a212339.py` | 暴力枚舉 n ≤ 11、遞推到 n < 60、精確多項式恆等、比對五條條目的 OEIS 資料 |
| `證明方法說明.md`、`程式說明.md` | 高二版中文說明 |

結果：Q^{(0,0,k,0)} 的 x 係數 g.f. 是 t(1 − P_k + tP_k²)/(1 − tP_k)³，所以 A212339（Barker 的 empirical g.f.、Dale 的遞迴猜想）和 A212341（Barker 的 empirical g.f.）成立。A212344 = 5·C(n−3)、A212345 = 9·C(n−3) 是 Kitaev–Remmel–Tiefenbruck Theorem 13 的特例（已知，只補出處）。紙上證明，沒有 Lean。
