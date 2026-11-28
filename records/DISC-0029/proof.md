# DISC-0029 證明

## 定理對照

完整證明見 `paper/a336482-records.md`。
1. H1：record 等於 j ⇔ 第一個 ≥ j 的部分是 j；max = #{j : max ≥ j}。對每個 j，B_j 的 g.f. 是 N_j·x^j·K，A_j 的是 K − N_j，用 (1−2x+x^j)N_j = 1−x 與 (1−2x)K = 1−x 推出 (1−x)(K−N_j) = x^j N_j K。
2. H2：長度 n 的字串 ↔ n+1 的組合（位元 1 表示黏合），連續 k 個 1 ↔ 部分 k+1。

## 編譯結果

沒有 Lean 檔。紙上證明加程式驗算；依研究規範第 1 節不能標 PROVEN。

## 敘述差異

- A102712 的 offset 是 1，證明約定 A102712(0) = 0；A336482 offset 0（a(0) = 0）。OEIS 草稿寫 n ≥ 2，避免用到 A102712(0)。
- H2 用 A119706 的 offset 1。
