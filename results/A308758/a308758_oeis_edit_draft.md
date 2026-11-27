# OEIS 編輯草稿：A308758 與 A307686 的差分關係（並證明 Barker 的 g.f.）

由使用者本人登入 OEIS 後送出。Claude 只準備內容清單，不代為送出。

送出前：
- **先讀** OEIS 對 AI 輔助內容的規定（docs/RESEARCH_STANDARDS.md 第 7 節）：下面英文只是參考，**留言要用自己的話重寫**。
- **一次只送一條**：先送 A308758，等編輯處理完再考慮其他七條（A308759、A308733、A308760、A308775、A307686、A308096、A307966，內容見 `paper/a308758-four-parts.md`）。
- **原句不要刪**：Colin Barker 的 Conjectures 那幾行保留，只在後面註明已證。
- **署名格式：** `- _Chi Hsia_, Nov 27 2026`（日期改成實際送出那天）。
- **自己驗一次（PARI）：**
  `s(n)=my(t=0);forpart(p=n,t+=p[2],,[4,4]);t` 是 A308758（forpart 由小到大排，p[2] 是第三大）；
  `u(m)=my(t=0);for(x=1,m\3,for(y=x,(m-x)\2,if(x+y>m-x-y,t+=x)));t` 是 A307686；
  `vector(40,n,s(n+1)-s(n)-u(n))` 應該全是 0（已在 PARI 2.15 跑過）。兩個函式要分兩行輸入。
- 要能用自己的話說出大意：「把 n−1 的分拆最大部分加 1，就得到 n 裡最大部分嚴格大於第二大的那些分拆；剩下的是 (a,a,c,d)，它和周長 n−1 的三角形 (c, a, a+d−1) 一一對應，c 就是最短邊。」

**FORMULA**（加在最後）：

```
a(n) - a(n-1) = A307686(n-1) for n >= 2: the partitions of n into 4 parts a >= b >= c >= d with a > b come from those of n-1 by adding 1 to the largest part, and (a,a,c,d) -> (c, a, a+d-1) is a bijection onto the integer triangles of perimeter n-1, with c the smallest side. - _Chi Hsia_, Nov 27 2026
```

**COMMENTS 或 FORMULA**（Barker 那段 Conjectures 之後加一行）：

```
The conjectured g.f. is correct: with d = y4, c = y4+y3, b = y4+y3+y2, a = y4+y3+y2+y1 (y4 >= 1, y1, y2, y3 >= 0, n = y1+2*y2+3*y3+4*y4), the g.f. of this sequence is x^4/((1-x)(1-x^2)(1-x^3)(1-x^4)) * (x^3/(1-x^3) + 1/(1-x^4)), which equals the conjectured one (cross-multiplying gives a polynomial identity). - _Chi Hsia_, Nov 27 2026
```

**CROSSREFS**：加 `Cf. A005044, A307686.`

**LINKS**（可選，等 GitHub 合併後才有效）：

```
Chi Hsia, <a href="https://github.com/Bonnie9981/Project-Discovery/blob/main/paper/a308758-four-parts.md">Partitions into 4 parts and integer triangles</a>, 2026. Written with the help of an LLM (Claude).
```

**Reason for edit**：

```
Added a(n) - a(n-1) = A307686(n-1) with a bijective proof, and a proof of the conjectured g.f.
```
