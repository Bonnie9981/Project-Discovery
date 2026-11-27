# DISC-0027 文獻

## 問題

主線換成「從既有數學模型推出 OEIS 沒有的新序列」（使用者 2026-11-27）。這份紀錄：圖論裡的定位支配集（locating-dominating set，Slater 1987）和識別碼（identifying code，Karpovsky–Chakrabarty–Levitin 1998）在路徑 P_n、環 C_n 上的**個數**。

## 已知成果

- 最小大小是經典結果：P_n 的定位支配集最小 ⌈2n/5⌉（Slater）；P_n 的識別碼最小 ⌈(n+1)/2⌉（n ≥ 3，Bertrand–Charon–Hudry–Lobstein 2004）；環的情形見 arXiv:0908.2750、Junnila 的論文。
- 支配集的個數（domination polynomial）在路徑、環上有很多結果（例如 arXiv:1601.01268；OEIS A000213 等）。
- A001642（Fielder 數列）在 OEIS 有名稱、生成函數和 Fielder 1968、Puri–Ward 2001（週期軌道）等連結，沒有 %C；它是特徵根的 n 次方和，已有週期點一類的意義（critic 指正）。A079976 = 1/(1−x−x²−x⁴−x⁵) 是對應的直線鋪磚數。

## 研究空白

離線 OEIS 全庫（快照 091a90f51479，402,063 條）沒有任何條目的文字提到 "identifying code" 或 "locating-dominating"；兩條計數序列的前 18 項都不在庫裡。網路粗查（兩次搜尋，見查詢紀錄）只找到最小大小的結果，沒找到個數。

## 查詢紀錄

- S001 離線全庫：`discovery.newseq.lookup.find` 查三條計數序列；`line.text LIKE '%identifying code%' / '%locating%dominat%'` → 0 條。
- S002 WebSearch（extended）"number of identifying codes in paths cycles enumeration counting locating-dominating sets generating function"：只有最小大小的論文（Exoo–Junnila–Laihonen、arXiv:0908.2750、Junnila 論文、BCHL 2004）。
- S003 WebSearch "identifying code polynomial / number of identifying codes / locating-dominating polynomial path graph"：沒有計數結果。
- 沒查 MathSciNet、zbMATH（需要使用者登入）。
