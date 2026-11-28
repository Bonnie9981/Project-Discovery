# OEIS 新序列草稿：環 C_n 的開定位支配集個數

由使用者本人送出。英文只是參考，**請用自己的話改寫**（OEIS 禁止 AI 寫的留言全文），一次只送一條，等編輯回覆再送下一條。署名 `_Chi Hsia_, Nov 28 2026`（日期改成實際送出那天）。AI 聲明用自己的話寫，例如 "Found and proved with the assistance of an AI system (Claude)."；只有自己讀懂並核對過證明，才加 "the author has checked the proof"。查重：離線 OEIS 全庫（快照 091a90f51479）找不到這串數字；網路粗查只看到「最小大小」的論文，沒看到計數。**不等於新的。**

- 證明連結（PR 合併後有效）：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/open-locating-and-ladders.md （第 1、2 節）
- b-file：`b_old_cycle.txt`（n = 3..502，用已證明的公式算，n ≤ 20 另有暴力核對）
- 要能自己講的證明：每個點的鄰居都在另一個奇偶類；把頂點每次跳 2 格重新排，條件變成「環狀 0/1 字串裡任兩個 0 至少隔 3 格」，那就是用長度 1 和 3 的磚鋪環，個數是 A001609。偶數 n 時兩個奇偶類各自是一個長 n/2 的環，所以是平方。

**Name**
```
Number of open-locating-dominating sets in the cycle graph C_n.
```
**Data（offset 3）**
```
4,0,6,16,15,25,31,36,67,100,144,225,309,441,664,961,1426,2116,3063,4489,6579,9604,14131,20736,30352,44521,65193,95481,140028,205209,300766,440896,646015,946729,1387575,2033476,2980371,4368100,6401536,9381969,13749853,20151121,29533296,43283241,63434538
```
**Comments**
```
A set S of vertices is open-locating-dominating if the sets N(v) intersect S, where N(v) is the set of neighbors of v, are nonempty and pairwise distinct (Seo and Slater).
For odd n, stepping around the cycle by 2 turns S into a cyclic binary word of length n in which any two zeros are at cyclic distance at least 3; for even n the two parity classes give two independent such words of length n/2. See the link.
```
**Formula**
```
a(n) = A001609(n) = A384367((n-1)/2) for odd n >= 3.
a(n) = A001609(n/2)^2 = A218439(n/2) for even n >= 6.
```
**Example**
```
a(4) = 0: in C_4 opposite vertices have the same neighborhood.
a(5) = 6: the sets of 4 vertices (5 of them) and all 5 vertices.
```
**Crossrefs**: Cf. A001609, A218439, A384367, A000930.
**Keywords**: nonn,easy
