# OEIS A058383：延伸驗證（沒有反例，沒有草稿）

紀錄 [DISC-0024](../../records/DISC-0024/)。Cloitre 2018 猜想：φ(x) + φ(x−1) = ⌊(4x−3)/3⌋、x ≥ 7 的解只有 Pierpont 質數 1 + 2^a·3^b（a, b > 0）。

- `code/a058383_scan.c`：x ≤ 10^10 有 66 個解，正好是這範圍內全部 Pierpont 質數；沒有反例。指令 `gcc -O2 -o a58 code/a058383_scan.c -lm && ./a58 1e10`。
- 反方向（Pierpont 質數都是解）紙上一行可證，見紀錄 proof.md。

只有範圍延伸，暫不送 OEIS。
