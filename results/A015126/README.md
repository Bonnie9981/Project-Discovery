# OEIS A015126：延伸驗證（沒有反例，沒有草稿）

紀錄 [DISC-0024](../../records/DISC-0024/)。Jianing Song 2022 猜想：n 奇數時 φ(k) = φ(n) 的最小 k 是奇數。

- `code/a015126_scan.c`：所有 φ 值 ≤ 2·10^9 檢查過，沒有反例。指令 `gcc -O2 -o inv code/a015126_scan.c -lm && ./inv 2000000000 6`。

只有範圍延伸，暫不送 OEIS。
