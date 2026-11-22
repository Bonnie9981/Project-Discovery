# DISC-0014 猜想

## 猜想

記號：r_n = 規則 150（新(i) = 舊(i−1) xor 舊(i) xor 舊(i+1)）從位置 0 單一 ON 細胞走 n 步；ones(n)、zeros(n) = r_n 在位置 −n..n 的 1、0 個數（A071053、A071052）。

- **H1（加倍）：** r_{2n}(2i) = r_n(i)，r_{2n}(2i+1) = 0。
- **H2（A071053）：** ones(2n) = ones(n)。
- **H3（A071052 FORMULA）：** 對所有 n ≥ 0，zeros(2n) = zeros(n) + 2n。

## 推翻條件

- 某個 n：H1 某格不相等，或 zeros(2n) ≠ zeros(n) + 2n，或兩種算法和條目 DATA 不一致。
