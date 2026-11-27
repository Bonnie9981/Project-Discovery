# 給 Claude 的專案規則

- **DEVLOG.md**（開發日誌）只記大事件，新的在下。每個大事件的 PR 順手加一行。
- **RESEARCH.md**（白話研究摘要）：每新增一份 `records/DISC-XXXX/`，或候選狀態改變（被證明、被推翻、查到出處），在同一個 PR 更新對應的一節、「目前候選清單」和「最後更新」日期。`tests/test_research_summary.py` 會擋下漏寫的紀錄。
- 用白話中文寫，不宣稱新穎，判定以 review.md 為準。
- 省 token：照 `docs/TOKEN_BUDGET.md`。先用 `python -m discovery.digest` 看摘要，長輸出包 `python -m discovery.quiet --`，開工前先估算 token 夠不夠，里程碑完成就收尾開新執行緒。
- **DEVLOG.md、RESEARCH.md 衝突**：`.gitattributes` 對這兩個檔設了 `merge=union`，本機 `git merge` 會自動保留兩邊新增的行。GitHub 網頁的衝突檢查不吃這個設定，所以合併 PR 前一律先在本機 `git fetch origin main && git merge origin/main`、跑測試、推上去，再按合併；合併後看一眼 DEVLOG 的順序（新的在下）和 RESEARCH 有沒有重複行。
- **檔案放哪**：新的 OEIS 結果放 `results/A??????/`（README、OEIS 草稿、`code/` 檢查腳本）；OEIS 要連的證明頁放 `paper/`，送出後不准搬或改名；研究過程照舊放 `records/DISC-XXXX/`，Lean 放 `lean/Discovery/`。說明見 `results/README.md`。
- **每個結果都要附兩份高二版中文說明**（使用者 2026-11-27 規定，OEIS 要求送出者本人看得懂）：`results/<序列>/證明方法說明.md`（從定義和小例子講起、每步為何成立、超出高二的地方標明、最後列「自己寫 OEIS 留言時要講的重點」）和 `results/<序列>/程式說明.md`（程式算什麼、怎麼跑、怎麼自己驗證）。內容只能根據 paper/、results/、records/ 既有檔案，跑過的輸出才寫。轉 PDF 後和草稿一起放到使用者電腦該序列資料夾。
