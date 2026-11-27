# DISC-0026 文獻與選題

## 問題

OEIS 上「只驗到小範圍」的早年猜想，重算到大範圍能不能找到反例？（使用者 2026-11-24 同意：這批專找反例。）

## 選題（DISC-0026-S001）

在 OEIS 用 10 組句型（`conjecture "verified for n <"`、`"checked for n <"`、`"tested up to"`、`"verified up to" prime`、`"checked up to" never`、`"for n <= 1000"`、`"verified for n up to"`、`"no other solutions" "checked"`、`"searched up to"` 等）各抓 3 頁 `fmt=text`，程式濾掉含 proof / counterexample / is true 等字的條目、已在 `data/cx/triage.json` 的條目、細胞自動機、Goldbach/Collatz 類，剩約 60 條人工看。

挑出來重算（逐字存檔在 `data/cx/entries/`）：

| 條目 | 作者 | 原句 | 條目自稱範圍 |
|---|---|---|---|
| A372430 | Gus Wiseman 2024 | Conjecture: The only number whose binary indices are a subset of its prime indices is 4100 ... | 10^7 |
| A219433 | Lei Zhou 2012 | Conjecture: a(n) < prime(n) except for a(522720). | n ≤ 10^6 |

看過但這批不做（記在 triage）：A037301 / A330904 / A334765（不會有 5／5／4 個連續項，已窮舉到 3^29、3^30、3^26，再往上要更聰明的搜法）、A134003（Layman：加上「a, b 為正整數」後可直接證明，平凡解 a = 0 永遠存在）、A272170（Fibonacci 第二高位不會連三個相同，用 log2 φ 的等分布可證）。

## 已知成果（DISC-0026-S002）

- A372430：用 OEIS 搜 154742504911235484315811840、「binary indices」「prime indices」4100，只出現條目本身和無關的 A333492（4100 只是其中一個數值）。沒有人回報第二個數。
- A219433：條目只有作者的例外 a(522720)。

## 研究空白

A372430 的反向猜想只驗到 10^7，而反例要到 1.5·10^26 才出現，暴力不可能碰到；需要用「每個 1 位元都逼一個質數整除」的結構剪枝。網路、MathSciNet 沒查。

## 查詢紀錄

見 `search_evidence.jsonl`（DISC-0026-S001、S002）。
