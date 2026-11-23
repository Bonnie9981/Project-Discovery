# DISC-0019 實驗

## 方法

1. 目錄：`discovery/cxsearch/psp2.c`（分段篩去質數 + Montgomery 算 2^(n−1) mod n，n < 2^63 精確）列出 10^10 以下所有 psp2，4 核約 15 分鐘（超過 `config/limits.json` 的 600 秒上限，這次是例外；平常直接用存好的目錄，`catalog` 只重驗不重建），存成 `data/cx/psp2_1e10.txt.gz`（sha256 28a9b306…）。`catalog.check` 用 Python 大整數逐一重驗每一項，並和 OEIS A055550、A055553 的 10^3～10^10 計數比對；另用純 Python 篩法重算 10^5 以下（測試）。
2. 對齊：A215944 的定義（三個質因數含重數、被較小 psp2 整除）在 10^7、10^8、10^9、10^10 以下的項數與總和，和 OEIS b-file 完全一致（S003）。
3. 自我測試：A218010（已知反例）跑出來必須剛好是 3380740301。
4. 每條猜想一個判定函式（`discovery/cxsearch/conjectures.py`），掃整個目錄；A058128 直接對 n 算大整數。
5. A321790 另做結構搜尋（`results/A321790/code/struct.py`）：反例 k = pq 必須 p−1 | q−1 且 q 整除所有 a^(p−1) − 1（a < p 的質數），所以對每個 p 算 gcd，不限 q 大小。

## 結果

- 目錄：10^10 以下 psp2 14884 個、Carmichael 1547 個，十個計數全對。
- 自我測試：A218010 只找到 3380740301，和 Greathouse 2014 一致。
- H1 推翻：798 個 A215944 項（< 10^10）裡 211 個是反例（critic 抓到原本漏算有平方因數的 5654273717 = 1093²·4733，判定函式已修），最小 3048841 = 61·151·331（被 psp2 49981 = 151·331 整除，60 ∤ 150）。允許 p、因數不是質數、n 有四個以上質因數的寬讀法，4·10^6 以下最小的反例仍是 3048841。
- H2：n < 400 的偶數全部成立（測試也跑到 400）；有一般證明（proof.md）。
- H3：目錄內 0 個；有一般證明（5 | n 需要 4 | n−1，但 n−1 ≡ 14 (mod 40)）。但條目已有 Greathouse 2014 的留言說三條都對，所以不算成果。
- H4：10^10 以下 6504 個半質數 psp2 都成立；結構搜尋 p ≤ 10^5（任何 q）沒有反例。順便填上條目的「?」：最小的「a(n) = 7」半質數 psp2 是 873181 = 661·1321。

## 重現方式

```
python -m discovery.cxsearch catalog            # 重驗目錄與計數
python -m discovery.cxsearch scan               # 全部猜想
python -m discovery.cxsearch catalog --build 1e10 --path /tmp/psp2_1e10.txt.gz   # 從頭建（約 15 分鐘）
python results/A321790/code/struct.py 100000
python -m pytest -q tests/test_cxsearch.py
```
