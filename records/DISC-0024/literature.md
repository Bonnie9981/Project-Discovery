# DISC-0024 文獻與選題

## 問題

OEIS 上其他作者早年只驗到小範圍、沒人回覆的「never / no other / always」型數論猜想，哪些能證明、哪些有反例？

第五批反例搜尋（使用者 2026-11-23 要求主線繼續）。Ratajczak、Sun、Cloitre、Ordowski、Coman 大多已掃過（`data/cx/triage.json`），這批換其他作者。

## 查詢紀錄

見 `search_evidence.jsonl`（DISC-0024-S001、S002）。

## 選題方式（DISC-0024-S001）

在 OEIS 用 `fmt=text` 批次搜「Conjecture: a(n) is never」「is never prime」「has no solutions」「no other solutions … checked」「Conjecture: there are no other terms」「checked up to」「Conjecture: all terms are」「Conjecture: a(n) is always」「never divisible」「squarefree」「only solutions」等（約 15 組、每組 2～3 頁），程式先濾掉含 counterexample / proof / proved / is true / incorrect 的條目、濾掉細胞自動機，剩約 150 條人工看。

## 挑出來的

| 條目 | 作者 | 原句（逐字存檔 `data/cx/entries/`） | 處理 |
|---|---|---|---|
| A084189 | Jason Earls 2003 | Conjecture: a(n) is never greater than 3.（A046376 回文數 p·q，p、q 是回文質數，兩因數的最小數字） | 證明 |
| A084352 | Jason Earls 2003 | 同上，回文的 brilliant 數（p、q 位數相同） | 證明 |
| A225004 | J. Lowell 2013 | Conjecture: a(n) is always a divisor of n^2. | 證明 |
| A276674 | Thomas Ordowski 2016 | Conjecture: if x - lambda(x) = 2*m > 0, then x <= 4*m. | 證明 |
| A340896 | J. Lowell 2021 | Conjecture: row n includes n^2 if and only if n is a power of a prime number. | 證明 |
| A015126 | Jianing Song 2022（在 Jovovic 條目） | Conjecture: a(n) is always odd for odd n. | 重算 |
| A058383 | Cloitre 2018 | Conjecture: these are the only solutions >=7 to phi(x) + phi(x-1) = floor((4x-3)/3). | 重算 |

## 已知成果（DISC-0024-S002）

- 四條證明的條目全文（含所有 %C）都沒有證明或反例；用 OEIS 搜 `A084189`、`A084352`、`A225004` 只出現本身和 A340896（A340896 只說 A225004 是各列最後一項）。
- A084189 註解提到的 JRM 題目「找大於 343 的合數回文，質因數都是只用 >3 數字的回文」允許三個以上因數（343 = 7³），和兩因數的猜想不同。
- 跳過：A111441（Bamberger 2020 猜想條目已有 Munch-Andersen 證明）、A110700、A162657、A353008 類（要無界搜尋）、A257230/A257231（等價於質數間隔上界，2^64 內已知）。
- 網路、MathSciNet、zbMATH 沒查。

## 研究空白

七條猜想的條目都沒有證明或反例；用到的工具（偶數位回文被 11 整除、除數個數公式、Carmichael 函數性質）都是古典的。
