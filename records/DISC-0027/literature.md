# DISC-0027 文獻與新穎性（只查了離線 OEIS）

## 問題

OEIS 上「n 分成 4 部分的分拆，各部分加總」（A308733/58/59/60/75）和「周長 n 的整數三角形，各邊加總」（A307686/A308096/A307966）有沒有已知關係；兩家族上 Colin Barker 的猜想 g.f. 是否已證。

## 已知成果

查證日期 2026-11-27，OEIS 快照 oeis/oeisdata commit 091a90f51479（402,063 條）。

- 九條條目（A308733、A308758、A308759、A308760、A308775、A307686、A308096、A307966、A026810）全文在離線庫裡逐條讀過。4 部分分拆那五條（Wesley Ivan Hurt 2019）只互相引用；三角形那三條（Hurt 2019）只引用 A005044 和彼此。兩邊之間沒有任何交叉引用、公式或留言。
- 全文搜尋 A307686、A308758 在所有條目的出現處：只有 A308096、A308107、A308733、A308759、A308760、A308775（都是同一家族內部）。
- 計數版已知：A026810 的 Crossrefs 寫「A005044 (first differences)」；A005044 有 Hurt 2021 留言「Number of partitions of n+1 into 4 parts whose largest two parts are equal」。所以 p4(n) − p4(n−1) = A005044(n−1) 不是新的；本紀錄的雙射正是這條留言背後的對應，加權版本沒有人寫。
- 八條 Colin Barker 的 g.f. 仍標「Conjectures」，條目內沒有人說已證（對照：A163723 有 Andrew Howroyd 2025 的「Formulas confirmed using the transfer matrix method」，這家族沒有）。
- **沒查：** 網路、MathSciNet、zbMATH、arXiv。用「部分和 + 雙射」的程度看，很可能是習題級，不宣稱新。

見 search_evidence.jsonl。

## 研究空白

加權版本的差分關係、以及八個 g.f. 的證明，在 OEIS 快照內都沒有。

## 查詢紀錄

DISC-0027-S001～S003（search_evidence.jsonl）。
