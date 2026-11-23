# Tuza 猜想小範圍 SAT 驗證（`discovery/tuzasat/`）

問題（Tuza 1981）：任何圖 G 都有 τ(G) ≤ 2ν(G)。ν 是最多能挑出幾個「兩兩沒有共用邊」的三角形，τ 是最少要刪幾條邊才能把所有三角形拆光。K4、K5 剛好等號成立。這裡對小 n 找反例（DISC-0024），附證書。

## 用法

```
python -m discovery.tuzasat.search 9 --out OUT        # 跑 k = 1..kmax(9)，UNSAT 時寫 CNF＋DRAT＋見證
python -m discovery.tuzasat.search 10 4 --out OUT     # 只跑 k = 4
python -m discovery.tuzasat.check OUT 9 1 2 3         # 獨立檢查
```

## 要排除的東西

對固定 n、k：n 點圖 G，ν(G) ≤ k 而且 τ(G) ≥ 2k+1。對所有 1 ≤ k ≤ kmax(n) 都 UNSAT，就表示 n 點以內沒有反例：

- 點數少於 n 的反例補孤立點就變成 n 點反例，所以 n 點涵蓋所有 ≤ n 點。
- k = 0：沒有三角形時 τ = 0，不可能是反例。
- kmax(n) = ⌊(⌊n(n−1)/4⌋ − 1)/2⌋：任何圖都有至少 m/2 條邊的二部子圖，刪掉其餘邊就沒有三角形，所以 τ ≤ ⌊m/2⌋ ≤ ⌊n(n−1)/4⌋，反例要 2k+1 ≤ 這個數。

## 編碼（變數編號規格，`check.py` 照這裡獨立重建）

- `x(a,b)`（a<b）：`itertools.combinations(range(n), 2)` 的順序 + 1，共 E 個。
- `t(a,b,c)`（a<b<c）：E + 1 + `combinations(range(n), 3)` 的順序，共 T 個。
- 字典序輔助變數從 E + T + 1 起，構造和 `docs/EGSAT.md` 的 LEX 完全相同。

| 家族 | 內容 | 為什麼不會漏掉反例 |
|---|---|---|
| TRI | t(a,b,c) ↔ 三條邊都在 | 定義 |
| INT | 每條邊 x(a,b) → 某個 t(a,b,c) | 不在任何三角形裡的邊刪掉後 τ、ν 都不變，所以可以假設每條邊都在三角形裡 |
| LEX | 相鄰對換 (i,i+1)：上三角向量 ≥lex 對換後的向量 | 取同構類裡字典序最大的標號；INT 在重新標號下不變 |
| P | 找到 k+1 個兩兩沒有共用邊的三角形 → 這些邊不能全有 | 含這些邊的圖 ν ≥ k+1 |
| C | 找到 ≤ 2k 條邊的集合 C 拆光候選圖的三角形 → 至少一個不碰 C 的三角形要存在 | 若所有不碰 C 的三角形都不存在，C 就是覆蓋，τ ≤ 2k |

P、C 是 CEGAR 時加的：外層 SAT 出候選圖，先用內層 SAT 找 k+1 個邊互斥三角形，找不到再找 ≤ 2k 的覆蓋；兩個都找不到就是反例。每條擋子句的見證（三角形或覆蓋邊）依序存在 JSON 裡。

## 證書

UNSAT 時把「基本子句 ＋ 擋子句」寫成 CNF，用 CaDiCaL（PySAT `Cadical195`）重新求解輸出 DRAT。`check.py` 不 import 搜尋程式：

1. 自己重建 TRI、INT、LEX，逐條比對 CNF 開頭；其餘每條子句都要和 JSON 的見證對得上（P：k+1 個三角形兩兩沒有共用邊，子句剛好是這些邊的負字面；C：|C| ≤ 2k，子句剛好是所有不碰 C 的三角形）。
2. 用 `discovery/egsat/check.py` 的自寫 RUP 檢查器驗 DRAT，必須推出空子句。
3. SAT 時暴力算 ν、τ。

`tests/test_tuzasat.py`：n ≤ 6 時基本子句的解涵蓋每個「每條邊都在三角形裡」的同構類（對 networkx 圖譜）；放寬成 τ > 2k−1 時找得到 K4 型緊例；竄改見證會被擋下；另外用暴力法（第二個實作）確認 networkx 圖譜裡所有 ≤ 7 點的圖都滿足 τ ≤ 2ν。
