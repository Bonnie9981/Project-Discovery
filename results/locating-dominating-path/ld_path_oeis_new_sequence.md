# OEIS 新序列草稿：路徑圖 P_n 的定位支配集個數

由使用者本人登入 OEIS 送出（New sequence 表單）。以下英文只是參考，**請用自己的話改寫**（OEIS 規定不能用 AI 寫的留言全文），一次只送一條，等編輯回覆再送下一條。

## 送出前要知道的事

- **查重（2026-11-27，離線 OEIS 全庫，快照 091a90f51479）：** 1,3,4,9,15,28,50,91,165,299 不在任何條目裡；整個 OEIS 沒有一條提到 "locating-dominating" 或 "identifying code"。網路粗查只找到「最小的定位支配集多大」（Slater：⌈2n/5⌉），沒看到有人算過個數。**這不等於「新」**，只是我們查的範圍內沒有。
- **證明連結（PR 合併後有效）：** https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/locating-dominating-paths.md
- **b-file：** `results/locating-dominating-path/b_ld_path.txt`（n = 1..500，用已證明的遞迴算，前 60 項另用轉移矩陣程式逐一核對）。
- **要能用自己的話說出證明：** 把集合寫成 0/1 字串，看相鄰兩個 1 之間有幾個 0（空隙）。「每個 0 都碰到 1」⇔ 中間空隙 ≤ 2、兩端空隙 ≤ 1；「兩個 0 看到的 1 不一樣」⇔ 不能有一個 1 左右兩邊都是「長空隙」（中間的 2 或兩端的 1）。再用兩個狀態（上一個空隙長不長）數字串，得到生成函數。
- 署名格式：`_Chi Hsia_, Nov 27 2026`（日期改成實際送出那天）。

---

## 表單各欄

**Name**
```
Number of locating-dominating sets in the path graph P_n.
```

**Data（offset 1）**
```
1,3,4,9,15,28,50,91,165,299,542,982,1780,3226,5847,10597,19206,34809,63088,114341,207232,375588,680717,1233734,2236024,4052578,7344907,13311936,24126601,43727139,79251225,143635207,260324969,471813916,855117249,1549817597,2808895022,5090851504,9226677691
```

**Comments**
```
A set S of vertices is locating-dominating if every vertex outside S has a neighbor in S and no two vertices outside S have the same set of neighbors in S (Slater).
Writing S as a binary word, S is locating-dominating if and only if every gap of zeros between two ones has length at most 2, the gaps at both ends have length at most 1, and no one is flanked on both sides by a "long" gap (an inner gap of length 2 or an end gap of length 1). See the link for a proof.
The minimum size of such a set is ceiling(2*n/5) (Slater).
For the cycle graph C_n the corresponding counts are A001642(n) for n >= 5.
```

**Formula**
```
G.f.: x*(1 + 2*x + 2*x^3 + x^4)/(1 - x - x^2 - x^4 - x^5).
a(n) = a(n-1) + a(n-2) + a(n-4) + a(n-5) for n >= 6.
a(n) ~ c*r^n where r = 1.8124036... is the largest root of x^5 - x^4 - x^3 - x - 1.
```

**Example**
```
For n = 3 the locating-dominating sets are {1,2}, {2,3}, {1,3}, {1,2,3}, so a(3) = 4. The set {2} is dominating but vertices 1 and 3 both see only vertex 2.
```

**Links**
```
Chi Hsia, Counting locating-dominating sets and identifying codes in paths and cycles, 2026.
```
（網址填上面「證明連結」）

**Program（PARI，請自己跑過、看懂再貼）**
```
a(n) = polcoef(x*(1+2*x+2*x^3+x^4)/(1-x-x^2-x^4-x^5) + O(x^(n+1)), n)
```

**Crossrefs**
```
Cf. A001642 (cycles), A000213 (dominating sets in paths).
```

**Keywords:** nonn,easy

**Author / AI 聲明（放 Comments 最後一行，用自己的話）：** 例如 "Found and proved with the assistance of an AI system (Claude)."；只有你自己讀懂並核對過證明，才加 "the author has checked the proof"。
