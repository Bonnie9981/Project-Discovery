# DISC-0031 實驗

## 方法

Python 3；`python results/A212339/code/check_a212339.py 11`，約 5 秒。
- 實作一：暴力列出所有 132-避免排列（n ≤ 11，先檢查個數是 Catalan 數），直接算每個元素左下方、左上方的點數，對 k = 2、3、4 驗 H1，對 (0,3,0,0) 驗 H2。
- 實作二：證明裡的分解式遞推（不完全獨立，用了同一個分解），算完整多項式 Q_n(x) 到 n < 60，和 H1 的 g.f. 展開比。
- 實作三：精確多項式交叉相乘，比 H1 與 A212338（Mathar）、A212339、A212341（Barker）的 g.f.，以及 (1 − t − t² − 2t³)³ 與 Dale 的 signature。
- OEIS 資料：A212338 33 項、A212339 29 項、A212341 26 項、A212344 27 項、A212345 26 項全部吻合。

## 結果

全部通過。

## 重現方式

`python results/A212339/code/check_a212339.py 11`（需要離線 OEIS 與 data/relmine/terms.pkl 才比對條目資料，否則顯示 skipped）。

## 補記（critic、reviewer）

- critic 另寫獨立程式 `results/A212339/code/independent_check.py`（不 import 專案模組；n ≤ 12、k = 1～5、四個象限都算，只有第三象限對上 A212338/39/41），全部吻合；另一支 n ≤ 9 比對整個分布 Q_n(x)。
- reviewer 用 PARI 2.15.4 把 KRT 閉式解（條目 Mathematica 程式裡也有）對 x 微分，k = 3、4 與我們的 g.f. 一致到 O(t³⁰)。
