# DISC-0006 實驗

## 方法

- **H1、H2：**
  - DISC-0004 時已由 impl_c（線性篩）檢查到 10⁶。
  - 這次再用 impl_a（逐數試除）和 impl_b（篩表）各自檢查到 10⁶：`research/r001/m13/extend_ab.py`。
  - critic 另外寫了一支不 import repo 的獨立程式，檢查到 2×10⁶。
- **H3：**
  - 三套獨立實作 impl_a、impl_b、impl_c 檢查 6 ≤ w ≤ 300：`research/r002/m13_rule54.py`。
  - critic 的獨立模擬檢查到 w = 1200。
  - Lean `decide` 在 6 ≤ w ≤ 200 的範圍內做核驗（見 proof.md）。

## 結果

- `extend_ab_1e6.json`：
  - C01 用 impl_a、impl_b 檢查，各 0 個失敗。
  - C02 兩套實作的解集完全相同，共 39,234 個解，0 個違反 H2。
- `rule54_abc_300.json`：三套實作在 6 ≤ w ≤ 300 完全一致，暫態全部等於公式，週期只出現 4。
- critic.md：
  - H1 到 2×10⁶ 成立。
  - H2′ 在 30,913 個 2^a·p 的情形上和直接計算一致。critic 另外找到 a = 9、11、13、15 的解，例如 5935616 = 2⁹·11593，所以 DISC-0004 報告裡「額外解只有 2³p、2⁵p、2⁷p」只是檢查範圍造成的現象。
  - H3 到 w = 1200 成立。
- **重要的負面發現（critic）：** H1 的偶數反例如果存在，最小也要大約 5.5×10⁶。所以「檢查到 10⁶ 沒有反例」對 H1 的偶數情形其實沒有證據力，H1 的證據要靠證明。

## 重現方式

```
python -m research.r001.m13.extend_ab 1000000     # 約 1 分鐘
python -m research.r002.m13_rule54 300            # 約 5 秒
```
