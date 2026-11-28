> 注意：兩條都可以由條目裡已有的生成函數一步推出（審查判 `SUPPORTED_KNOWN`），屬於「把沒寫出的關係補上」的小編輯，不是新發現。

# OEIS 編輯草稿：A336482 與 A102712 的差分關係；A119706 的 Mathar 猜想（證明）

由使用者本人登入 OEIS 後送出。Claude 只準備內容清單，不代為送出。

送出前：
- **先讀** OEIS 對 AI 輔助內容的規定（docs/RESEARCH_STANDARDS.md 第 7 節）：英文只是參考，**留言用自己的話重寫**。
- **兩條分開送，一次一條。** 建議先送 A119706（一行雙射，最簡單），等編輯處理完再送 A336482。
- **原句不要刪：** Mathar 的 Conjecture 那行保留，在後面另加一行。
- **署名：** `- _Chi Hsia_, Nov 28 2026`（改成實際送出那天）。
- **自己驗一次（PARI，分行輸入）：**
  ```
  L(n)=my(t=0);forstep(m=0,2^(n-1)-1,1,my(c=1,b=0);for(i=0,n-2,if(bittest(m,i),b=max(b,c);c=1,c++));t+=max(b,c));t
  R(n)=my(t=0);for(m=0,2^(n-1)-1,my(c=1,v=[]);for(i=0,n-2,if(bittest(m,i),v=concat(v,c);c=1,c++));v=concat(v,c);my(r=0,M=0);for(k=1,#v,if(v[k]>M,r++;M=v[k]));t+=r);t
  vector(15,n,R(n+1)-L(n+1)+L(n))
  ```
  應該是 15 個 0（L 是 A102712、R 是 A336482；已在 PARI 2.15.4 跑過）。

## 第一條：A119706

**FORMULA**（在 Mathar 的 Conjecture 那行後面加）：

```
The conjecture a(n) = A102712(n+1) - 2^n is true: joining the i-th and (i+1)-th of n+1 ones whenever the i-th bit is 1 maps binary words of length n bijectively onto compositions of n+1, and a maximal run of k ones becomes a part k+1, so the largest part is the longest run plus 1. (It also follows by subtracting the g.f.s of A102712 and of this sequence.) - _Chi Hsia_, Nov 28 2026
```

**Reason for edit**：`Proof of the conjectured formula (bijection between binary words and compositions).`

## 第二條：A336482

**FORMULA**：

```
a(n) = A102712(n) - A102712(n-1) for n >= 2. More precisely, for each j >= 1 the number of compositions of n whose first part >= j equals j (i.e., that have a left-to-right maximum equal to j) is the number of compositions of n with largest part >= j minus the same number for n-1. - _Chi Hsia_, Nov 28 2026
G.f.: (1-x)^2/(1-2*x) * Sum_{i>=1} x^i/(1-2*x+x^i) (differentiate the g.f. of A382312 with respect to y at y = 1). - _Chi Hsia_, Nov 28 2026
```

**CROSSREFS**：加 `Cf. A079500, A102712, A119706, A382312.`（A079500 是只有一次破紀錄的組合數；critic 驗過 A336482 的 g.f. = x(1−x)/(1−2x) × A079500 的 g.f.，可選擇不提）

**LINKS**（可選，等 GitHub 合併後才有效）：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a336482-records.md">Compositions: left-to-right maxima, largest parts and longest runs</a>, 2026. Written with the help of an LLM (Claude).
```

**Reason for edit**：`Added a(n) = A102712(n) - A102712(n-1) with proof, and a g.f.`
