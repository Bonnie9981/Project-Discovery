# DISC-0031 假設

## 猜想

來源：嚴篩選（兩邊沒有 g.f.、至少一邊只有猜想）後的 relmine 候選 A212344 ↔ A103872（逆二項變換），讀全文時發現整個 marked mesh pattern 家族（Kitaev–Remmel–Tiefenbruck，KRT）有多條猜想或「Empirical」g.f.。

- H1 對每個 k ≥ 1，Q_{132}^{(0,0,k,0)}(t,x) 的 x 係數 g.f. 是 t(1 − P_k + tP_k²)/(1 − tP_k)³，P_k = C_0 + … + C_{k−1}t^{k−1}。
- H1a（k = 3，A212339）：Barker 的 empirical g.f. 與 Dale 猜想的線性遞迴 signature (3,0,1,−12,−3,1,18,12,8) 成立。
- H1b（k = 4，A212341）：Barker 的 empirical g.f. 成立。
- H2 A212344(n) = 5·C(n−3)（Bala、Mathar、Gladkovskii 的猜想）；A212345(n) = 9·C(n−3)。預期是 KRT Theorem 13 的特例。

## 推翻條件

任何 n 使上式不相等；或 KRT 已經寫出 H1。
