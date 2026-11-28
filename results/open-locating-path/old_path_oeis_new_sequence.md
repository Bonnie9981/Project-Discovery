# OEIS 新序列草稿：路徑 P_n 的開定位支配集個數

由使用者本人送出。英文只是參考，**請用自己的話改寫**（OEIS 禁止 AI 寫的留言全文），一次只送一條，等編輯回覆再送下一條。署名 `_Chi Hsia_, Nov 28 2026`（日期改成實際送出那天）。AI 聲明用自己的話寫，例如 "Found and proved with the assistance of an AI system (Claude)."；只有自己讀懂並核對過證明，才加 "the author has checked the proof"。查重：離線 OEIS 全庫（快照 091a90f51479）找不到這串數字；網路粗查只看到「最小大小」的論文，沒看到計數。**不等於新的。**

- 證明連結：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/open-locating-and-ladders.md （第 1、3 節）；b-file：`b_old_path.txt`（n = 1..500）
- 要能自己講的證明：鄰居都在另一個奇偶類，所以問題拆成「奇數位置」「偶數位置」兩個互不相干的小問題，答案相乘。每個小問題是「0/1 字串、任兩個 0 至少隔 3 格」，靠近一端時如果那一端的點不在這一類，最靠近的兩個字母一定是 1。這種字串的個數是 Narayana 牛數 A000930。

**Name**
```
Number of open-locating-dominating sets in the path graph P_n.
```
**Data（offset 1）**
```
0,1,0,1,4,4,6,9,9,16,26,36,57,81,112,169,246,361,540,784,1144,1681,2451,3600,5292,7744,11357,16641,24360,35721,52360,76729,112488,164836,241542,354025,518821,760384,1114470,1633284,2393685,3508129,5141312,7535025,11043198,16184529,23719672,34762816,50947200
```
**Comments**
```
A set S of vertices is open-locating-dominating if the sets N(v) intersect S are nonempty and pairwise distinct (Seo and Slater). Since N(v) lies in the parity class opposite to v, the conditions split into two independent problems, one for each parity class; each is counted by Narayana's cows sequence A000930. See the link.
```
**Formula**
```
a(2*k) = A000930(k)^2 for k >= 1.
a(2*k+1) = A000930(k+3)*A000930(k-2) for k >= 2.
```
**Example**
```
a(2) = 1: in P_2 the only open-locating-dominating set is {1,2}. a(3) = 0: vertices 1 and 3 have the same neighborhood.
```
**Crossrefs**: Cf. A000930, A233247, A?????? (cycles).
**Keywords**: nonn,easy
