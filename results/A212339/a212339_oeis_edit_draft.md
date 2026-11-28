> 注意：審查判四條都是 `SUPPORTED_KNOWN`：Barker 的 g.f. 已在條目上，KRT 的閉式解微分一次就得到；A212344、A212345 是 KRT Theorem 13 的特例。屬於「補上證明或出處」的小編輯，不是新發現。

# OEIS 編輯草稿：132-避免排列 marked mesh pattern 的 x 係數（A212339、A212341），以及 A212344、A212345

由使用者本人登入 OEIS 後送出。Claude 只準備內容清單，不代為送出。

送出前：
- **先讀** OEIS 對 AI 輔助內容的規定（docs/RESEARCH_STANDARDS.md 第 7 節）：下面英文只是參考，**留言用自己的話重寫**。
- **一次只送一條。** 建議順序：A212339 → A212341 → A212344 → A212345，每條等編輯處理完再送下一條。
- **原句不要刪：** Barker 的 Empirical g.f.、Dale 的 Conjecture、Mathar/Bala/Gladkovskii 的猜想都保留（Gladkovskii 的連分數我們沒證，不要寫已證），只在後面註明已證。
- **送出前自己核對論文：** 打開 KRT 論文 PDF（https://arxiv.org/pdf/1201.6243），確認 Theorem 13 的編號與內容、Section 4 那串數字裡寫的是 532。我們是透過網頁讀取工具看的，沒有親自開 PDF。
- **署名：** `- _Chi Hsia_, Nov 28 2026`（改成實際送出那天）。
- **自己驗一次（PARI，每行分開輸入）：**
  ```
  av(p)=my(n=#p);for(i=1,n,for(j=i+1,n,for(k=j+1,n,if(p[i]<p[k]&&p[k]<p[j],return(0)))));1
  m(p,k)=sum(i=1,#p,sum(j=1,i-1,p[j]<p[i])>=k)
  b(n,k)=my(t=0);forperm(n,p,if(av(p)&&m(p,k)==1,t++));t
  vector(6,n,b(n+3,3))
  P=1+x+2*x^2;G=x*(1-P+x*P^2)/(1-x*P)^3;
  G-x^4*(5+4*x+4*x^2)/((1-2*x)^3*(1+x+x^2)^3)
  ```
  第 4 行應得 [5, 19, 61, 188, 523, 1387]（直接數 132-避免排列，等於 A212339 開頭），最後一行應得 0（我們的 g.f. 等於 Barker 的）。已在 PARI 2.15.4 跑過。
- 要能用自己的話說出大意：「132-避免排列寫成 α n β，α 全部比 β 大。左下方的點只會在自己那一段裡，n 左下方有 |α| 個點。所以生成函數滿足 Q = 1 + t(P + x(Q − P))Q，取 x 的一次項就是答案。」

## 第一條：A212339

**FORMULA**（在 Barker 的 Empirical g.f. 那行後面加）：

```
The empirical g.f. is correct, and so is the conjectured signature (for n >= 13). Write a 132-avoiding permutation as alpha n beta; every entry of alpha exceeds every entry of beta, so entries of alpha and beta have their south-west points inside their own block and n has |alpha| of them. Hence, with Q(x,y) = Sum_n Q_{n,132}^(0,0,3,0)(y)*x^n and P = 1 + x + 2*x^2, Q = 1 + x*(P + y*(Q - P))*Q. Taking the coefficient of y gives x*(1 - P + x*P^2)/(1 - x*P)^3 = x^4*(5+4*x+4*x^2)/((1-2*x)^3*(1+x+x^2)^3). - _Chi Hsia_, Nov 28 2026
```

**COMMENTS**（可選）：`The terms 5, 19, 61, 188, 532, 1387 listed in Kitaev-Remmel-Tiefenbruck, Section 4, contain a typo: the fifth term is 523, as in their expansion of Q^(0,0,3,0)(t,x).`

**Reason for edit**：`Proof of the empirical g.f. and of the conjectured recurrence.`

## 第二條：A212341

**FORMULA**：

```
The empirical g.f. is correct: the same argument as in A212339 with P = 1 + x + 2*x^2 + 5*x^3 gives x*(1 - P + x*P^2)/(1 - x*P)^3. In general, the coefficient of y in Q_{n,132}^(0,0,k,0)(y) has g.f. x*(1 - P_k + x*P_k^2)/(1 - x*P_k)^3 with P_k = Sum_{i=0..k-1} A000108(i)*x^i (k = 2: A212338, k = 3: A212339). - _Chi Hsia_, Nov 28 2026
```

**Reason for edit**：`Proof of the empirical g.f.`

## 第三條：A212344（只是補出處，不是我們的定理）

**FORMULA**（在 Mathar 的 Conjecture 後面加）：

```
a(n) = 5*A000108(n-3): this is the case k = 3 of Theorem 13(1) of Kitaev, Remmel and Tiefenbruck (the highest coefficient of Q_{n,132}^(0,k,0,0)(x) is C_k*C_{n-k}), which proves the conjecture of Peter Bala and the recurrence conjectured by R. J. Mathar. - _Chi Hsia_, Nov 28 2026
```

**Reason for edit**：`The conjectures follow from Theorem 13 of the linked paper.`

## 第四條：A212345（同上，補公式與出處）

**FORMULA**：

```
a(n) = 9*A000108(n-3) for n >= 4, by Theorem 13(2) of Kitaev, Remmel and Tiefenbruck with k = 3 (a_3 = 9). - _Chi Hsia_, Nov 28 2026
```

**Reason for edit**：`Added formula from Theorem 13 of the linked paper.`

**LINKS**（可選，只加在 A212339，等 GitHub 合併後才有效）：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a212339-marked-mesh.md">Quadrant marked mesh patterns in 132-avoiding permutations: the coefficient of x</a>, 2026. Written with the help of an LLM (Claude).
```
