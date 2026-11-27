# OEIS 編輯草稿：A001642 的組合意義（環 C_n 的定位支配集個數）

由使用者本人送出；英文請用自己的話改寫。建議順序：先送「路徑圖 P_n 定位支配集」新序列（拿到 A 編號），再送這條編輯，讓兩條互相引用。

## 送出前要知道的事

- **A001642 原文（離線快照 091a90f51479）：** %N "A Fielder sequence."、%F 生成函數，連結有 Fielder 1968、Puri–Ward 2001（週期軌道）等，沒有任何 %C 留言。Fielder 數列本身就是特徵根的 n 次方和，已有「週期點個數」一類意義，所以**不能說是第一個組合意義**，只說「補上 C_n 定位支配集的解釋」。
- **我們證明的：** n ≥ 5（以及 n = 3）時，A001642(n) = 環 C_n 的定位支配集個數。n = 4 不成立（C_4 有 9 個，A001642(4) = 11），原因是 C_4 裡「隔兩格」的兩個點是同一個點。
- **證明大意：** 把定位支配集的 0/1 字串切成「1、10、1001、10010」四種磚，就是用長度 1、2、4、5 的磚鋪一圈有編號的環；鋪環的方法數 = Σ 磚長 × 鋪剩下那段路的方法數，生成函數正好是 A001642 的。
- **證明連結（PR 合併後有效）：** https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/locating-dominating-paths.md （第 2 節）

## 要加的內容

**Comments**
```
a(n) is the number of tilings of a labeled n-cycle by tiles of lengths 1, 2, 4, 5 (equivalently, Sum_{l in {1,2,4,5}} l*A079976(n-l)).
For n >= 5 (and n = 3), a(n) is the number of locating-dominating sets in the cycle graph C_n. See the link. - _Chi Hsia_, Nov 27 2026
```

**Links**
```
Chi Hsia, Counting locating-dominating sets and identifying codes in paths and cycles, 2026.
```

**Crossrefs**（拿到新序列 A 編號後再加）
```
Cf. A079976, A?????? (paths).
```
