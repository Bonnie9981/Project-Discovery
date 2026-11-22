# DISC-0010 文獻

## 問題

R2-C10 的第一段：規則 54（新格 = 中 XOR（左 OR 右））在 w 格環上、只有第 0 格活著出發。w ≡ 0 (mod 4)、w ≥ 4 時，暫態是 T = (w − 4)/2，週期恰好是 4。DISC-0005 提出、DISC-0006 用 Lean 有限核驗 6 ≤ w ≤ 200，沒有一般證明。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| R2-C10 的暫態序列在 OEIS 線上查無 | DISC-0006-S005（OEIS 搜尋，2026-11-22） | 公式本身在查過的範圍內沒有出處 |
| OpenAlex「rule 54 transient periodic boundary」前 10 筆沒有環上暫態公式 | DISC-0006-S006 | 同上 |
| 規則 54 的背景圖樣（空間、時間週期都是 4 的「ether」）與粒子分析 | Hanson–Crutchfield 1997（Physica D 103）、Boccara–Nasser–Roger 1991、Martínez 等 2005 的規則 54 滑翔機研究 | ether 是規則 54 的已知 domain；**本次沒有重讀原文**，對應關係憑 DISC-0006 critic 的記憶，待核對 |
| 光錐 + ether 的證明草稿（w ≡ 0, 2, 3） | DISC-0006 critic.md 第 3、4 點 | 本紀錄把 w ≡ 0 的部分寫完整並形式化 |

## 研究空白

- 單一種子在環上的暫態公式，在 DISC-0006 查過的範圍（OEIS 線上、OpenAlex 前 10 筆）沒有找到。但那次 OEIS 查詢用的是四個剩餘類混在一起的數列；w ≡ 0 這段單獨看只是偶數列 0, 2, 4, 6, …，那次查詢對它沒有辨別力，**不能算是對這一段的查證**。
- 本紀錄的論證只用兩個基本事實（光錐內是 ether、w ≡ 0 時錐外剩下的 3 格剛好是 ether 的死格），屬於習題程度；ether 本身是已知結構。新穎性不宣稱。
- 本紀錄沒有新增查詢（省 token，沿用 DISC-0006 的存證）；arXiv、MathSciNet 沒查。

## 查詢紀錄

| # | 管道 | 查詢 | 結果 |
|---|---|---|---|
| 1 | （沿用）DISC-0006-S005 OEIS | 2,6,2,2,4,10,4,4,6,14,6,6,8,18 | 查無 |
| 2 | （沿用）DISC-0006-S006 OpenAlex | elementary cellular automaton rule 54 transient periodic boundary | 沒有環上暫態公式 |
