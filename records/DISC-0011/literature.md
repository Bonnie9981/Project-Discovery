# DISC-0011 文獻

## 問題

R2-C10 的第二、三段：規則 54（新格 = 中 XOR（左 OR 右））在 w 格環上、只有第 0 格活著出發。w ≡ 2 (mod 4) 時暫態 (w − 6)/2、w ≡ 3 (mod 4) 時暫態 (w − 7)/2，週期都恰好是 4。DISC-0005 提出、DISC-0006 用 Lean 有限核驗 6 ≤ w ≤ 200；DISC-0010 證了 w ≡ 0 段。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| R2-C10 的四類混合暫態序列在 OEIS 線上查無 | DISC-0006-S005（2026-11-22） | 混合序列沒有出處；單看 w ≡ 2 或 w ≡ 3 這兩段，暫態只是偶數列 0, 2, 4, …，那次查詢對單段沒有辨別力 |
| OpenAlex「rule 54 transient periodic boundary」前 10 筆沒有環上暫態公式 | DISC-0006-S006 | 同上 |
| 規則 54 的 ether（空間、時間週期都是 4）與缺陷／粒子分析 | Hanson–Crutchfield 1997（Physica D 103）、Boccara–Nasser–Roger 1991、Martínez 等 2005 | ether 與「兩塊 ether 相接處的靜止缺陷」都屬已知的規則 54 粒子語言；**本次沒有重讀原文** |
| 單種子規則 54 在 w ≡ 0 (mod 4) 的證明（光錐 + ether） | DISC-0010（`Discovery.Rule54Mod4.rule54_mod4_zero`） | 本紀錄沿用 ether 與它的餘數表，改用「對折」把環變成線段 |
| 對稱軌道對折成有反射邊界的線段 | DISC-0009（規則 90，偶數環＝零邊界導線） | 同一種技巧，已知 |

## 研究空白

- 單一種子在環上的暫態公式，在 DISC-0006 查過的範圍內沒有找到出處；但如上所述，這兩段單獨看沒有被那次查詢辨別過。
- 論證只用三個基本事實（軌道左右對稱 → 對折成線段；光錐內是 ether；兩塊 ether 在中心相接成一個靜止缺陷（每 4 步中有一步比 ether 少亮）），習題程度。新穎性不宣稱。
- 本紀錄沒有新增查詢（省 token，沿用 DISC-0006 的存證）；arXiv、MathSciNet 沒查。

## 查詢紀錄

| # | 管道 | 查詢 | 結果 |
|---|---|---|---|
| 1 | （沿用）DISC-0006-S005 OEIS | 2,6,2,2,4,10,4,4,6,14,6,6,8,18 | 查無 |
| 2 | （沿用）DISC-0006-S006 OpenAlex | elementary cellular automaton rule 54 transient periodic boundary | 沒有環上暫態公式 |
