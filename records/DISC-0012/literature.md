# DISC-0012 文獻

## 問題

R2-C10 的最後一段：規則 54（新格 = 中 XOR（左 OR 右））在 w 格環上、只有第 0 格活著出發，w ≡ 1 (mod 4) 時暫態 w − 3、週期恰好 4。DISC-0005 提出、DISC-0006 用 Lean 有限核驗 6 ≤ w ≤ 200；DISC-0010、DISC-0011 已證 w ≡ 0、2、3。

## 已知成果

| 結果 | 出處 | 和我們的關係 |
|---|---|---|
| R2-C10 的四類混合暫態序列在 OEIS 線上查無 | DISC-0006-S005（2026-11-22） | 混合序列沒有出處；單看 w ≡ 1 這段，暫態是 6, 10, 14, …（4k + 2），那次查詢對單段沒有辨別力 |
| OpenAlex「rule 54 transient periodic boundary」前 10 筆沒有環上暫態公式 | DISC-0006-S006 | 同上 |
| 規則 54 的 ether、相位不同的 ether 之間的「牆」、粒子碰撞 | Hanson–Crutchfield 1997（Physica D 103）、Boccara–Nasser–Roger 1991、Martínez 等 2005 | ether、相位牆（domain wall）都是已知的規則 54 粒子語言；**本次沒有重讀原文** |
| 光錐 + ether、對稱軌道對折成線段 | DISC-0010、DISC-0011、DISC-0009 | 本紀錄直接沿用 |

## 研究空白

- 單一種子在環上的暫態公式，在 DISC-0006 查過的範圍內沒有找到出處；這一段單獨看沒被辨別過。
- 論證：光錐填滿線段 → 中心出現一道相位牆，以速度 1 走回種子 → 牆後是相位平移的 ether，兩端各一個每 4 步出現一次的缺陷。全是已知語言，習題程度（只是情形較多）。新穎性不宣稱。
- 本紀錄沒有新增查詢（省 token，沿用 DISC-0006 的存證）；arXiv、MathSciNet 沒查。

## 查詢紀錄

| # | 管道 | 查詢 | 結果 |
|---|---|---|---|
| 1 | （沿用）DISC-0006-S005 OEIS | 2,6,2,2,4,10,4,4,6,14,6,6,8,18 | 查無 |
| 2 | （沿用）DISC-0006-S006 OpenAlex | elementary cellular automaton rule 54 transient periodic boundary | 沒有環上暫態公式 |
