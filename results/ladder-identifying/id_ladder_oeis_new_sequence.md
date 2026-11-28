# OEIS 新序列草稿：梯子圖 P_2 × P_n 的identifying codes個數

由使用者本人送出。英文只是參考，**請用自己的話改寫**（OEIS 禁止 AI 寫的留言全文），一次只送一條，等編輯回覆再送下一條。署名 `_Chi Hsia_, Nov 28 2026`（日期改成實際送出那天）。AI 聲明用自己的話寫，例如 "Found and proved with the assistance of an AI system (Claude)."；只有自己讀懂並核對過證明，才加 "the author has checked the proof"。查重：離線 OEIS 全庫（快照 091a90f51479）找不到這串數字；網路粗查只看到「最小大小」的論文，沒看到計數。**不等於新的。**

- 證明連結：https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/open-locating-and-ladders.md （第 4 節，電腦輔助證明）；b-file：`b_id_ladder.txt`（n = 1..500）；檢查程式：`results/ladder-locating/code/check_ladder.py`
- 要能自己講的證明：條件只牽涉相鄰幾欄，所以一欄一欄往右加，只記最後幾欄的狀態；中段每一步都是同一個矩陣。電腦算出狀態向量，驗證「某一步的向量恰好等於前幾步向量的固定組合」，之後每一步都乘同一個矩陣，所以這條關係永遠成立，數列就滿足那條遞迴。這是電腦輔助證明，不是紙筆推出的遞迴。

**Name**
```
Number of identifying codes in the ladder graph P_2 X P_n.
```
**Data（offset 1）**
```
0,5,29,80,251,881,2992,9921,33249,111812,375071,1257457,4218520,14152721,47474221,159249680,534211659,1792031625,6011394512,20165343001,67645129593,226917087716,761198250455,2553456280169,8565625528344,28733579089593,96387422356901,323333728717616
```
**Formula**
```
G.f.: x^2*(5 + 19*x + 12*x^2 + 3*x^3 - 5*x^4 - 22*x^5 - 10*x^6 + 6*x^7 + 8*x^8)/(1 - 2*x - 2*x^2 - 6*x^3 - 10*x^4 + 4*x^5 + x^6 + 6*x^7 + 8*x^8 + 2*x^9 - 8*x^10).
```
**Comments**
```
The g.f. was obtained from a column-by-column transfer matrix; the linear recurrence was certified by checking one vector identity for the state vectors, which then propagates to all n. See the link.
```
**Crossrefs**: Cf. A?????? (locating-dominating sets / identifying codes in P_n, the first-batch sequences).
**Keywords**: nonn
