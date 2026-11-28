# OEIS 新序列草稿：梯子圖 P_2 × P_n 的locating-dominating sets個數

由使用者本人送出。英文只是參考，**請用自己的話改寫**（OEIS 禁止 AI 寫的留言全文），一次只送一條，等編輯回覆再送下一條。署名 `_Chi Hsia_, Nov 28 2026`（日期改成實際送出那天）。AI 聲明用自己的話寫，例如 "Found and proved with the assistance of an AI system (Claude)."；只有自己讀懂並核對過證明，才加 "the author has checked the proof"。查重：離線 OEIS 全庫（快照 091a90f51479）找不到這串數字；網路粗查只看到「最小大小」的論文，沒看到計數。**不等於新的。**

- 證明連結：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/open-locating-and-ladders.md （第 4 節，電腦輔助證明）；b-file：`b_ld_ladder.txt`（n = 1..500）；檢查程式：`results/ladder-locating/code/check_ladder.py`
- 要能自己講的證明：條件只牽涉相鄰幾欄，所以一欄一欄往右加，只記最後幾欄的狀態；中段每一步都是同一個矩陣。電腦算出狀態向量，驗證「某一步的向量恰好等於前幾步向量的固定組合」，之後每一步都乘同一個矩陣，所以這條關係永遠成立，數列就滿足那條遞迴。這是電腦輔助證明，不是紙筆推出的遞迴。

**Name**
```
Number of locating-dominating sets in the ladder graph P_2 X P_n.
```
**Data（offset 1）**
```
3,9,34,117,403,1396,4872,16969,59035,205417,714944,2488286,8659796,30138018,104887971,365037141,1270421124,4421383927,15387528698,53552476389,186376100062,648635737394,2257415639163,7856374688776,27342161590058,95157605048872,331172419198363,1152563383674050
```
**Formula**
```
G.f.: x*(3 + 7*x^2 + 3*x^3 - 5*x^4 - 6*x^5 + 2*x^6 - x^7 + x^8 + 2*x^9 - 3*x^10 + x^12)/(1 - 3*x - 4*x^3 - 7*x^4 + 2*x^5 + 2*x^6 - 3*x^7 + x^8 + x^9 - 2*x^10 + 3*x^11 + x^12 - x^13).
```
**Comments**
```
The g.f. was obtained from a column-by-column transfer matrix; the linear recurrence was certified by checking one vector identity for the state vectors, which then propagates to all n. See the link.
```
**Crossrefs**: Cf. A?????? (locating-dominating sets / identifying codes in P_n, the first-batch sequences).
**Keywords**: nonn
