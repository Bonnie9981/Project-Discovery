# OEIS A219433：延伸驗證（沒有新例外，沒有草稿）

紀錄 [DISC-0026](../../records/DISC-0026/)。Lei Zhou 2012 猜想「a(n) < prime(n)，只有 n = 522720 例外」，條目驗到 n ≤ 10^6。

`code/a219433_scan.c`：n ≤ 10^8 只有已知的 n = 522720。指令 `gcc -O2 -o a219 code/a219433_scan.c -lm && ./a219 100000000`。只是範圍延伸，暫不送 OEIS。
