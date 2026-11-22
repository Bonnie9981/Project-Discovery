# 省 token 規則

目的：同樣的研究品質，少花 token。**可重現、可驗證、可反駁、獨立審查這四條不能因為省錢而放寬**；省的是重複閱讀、冗長輸出和用太貴的模型做機械工作。

## 1. 每個角色用的模型（`.claude/agents/*.md` 的 `model:`）

| 角色 | 模型 | 理由 |
|---|---|---|
| literature | sonnet | 查詢、整理來源，機械性高 |
| hypothesis | sonnet | 從資料列猜想，有推翻條件把關 |
| experiment | sonnet | 寫雙實作、跑程式，對錯由 `verify` 交叉檢查決定 |
| critic | sonnet | 獨立重算有 impl_c 和 `independence` 把關；**例外見下** |
| proof | opus | Lean 證明難，失敗重試反而更貴 |
| reviewer | opus | 最後一道關，模型也和多數作者不同，增加獨立性 |

例外（必做）：紀錄要判 `PROVEN_*`、`*_POSSIBLY_NEW`、新穎性到 `PENDING_REVIEW` 以上，或是里程碑主結果（`record.json` 寫 `"milestone": true`）時，總控呼叫 critic 必須指定 `model: opus`，並在 `record.json` 寫 `"critic_model": "opus"`。`check_record` 會擋下沒寫的新紀錄。

## 2. 少讀

- 開新執行緒或接手時，先跑 `python -m discovery.digest`（每份紀錄一行），不要整份讀 RESEARCH.md、DEVLOG.md 或舊紀錄。
- 讀某份紀錄先用 `python -m discovery.digest DISC-XXXX`（每段只看第一行），需要時再取單一段落：`python -m discovery.digest DISC-XXXX critic.md "## 未解決的疑點"`。
- 不要 `cat` 整個 JSON（例如 `r003_pilot.json` 25 KB），用 `python -c` 或 `jq` 取需要的欄位。
- 呼叫 subagent 時，提示裡只放紀錄編號、要做的事和相關檔案路徑，不要把前面文件的全文貼進去；subagent 自己用 digest 讀。

## 3. 少印

- 會印很多行的指令（pytest、`lake build`、批次搜尋）一律包成 `python -m discovery.quiet -- <指令>`：完整輸出存在 `logs/`（不進 git），對話只看到結束碼、像錯誤的行和最後 15 行。結束碼照原樣傳回。
- 批次計算寫成腳本，結果存成 JSON 或 CSV，對話只印統計摘要（幾個候選、幾個反例、前幾筆）。不要讓 agent 一筆一筆看資料。
- 測試失敗時只重跑失敗的那幾個（`pytest tests/test_x.py::name`）。檔案沒改就不要重跑已經通過的測試。

## 4. 少寫

- 交付文件寫結論、數字和證據位置（檔名、指令、CI 連結），原始輸出放檔案。建議長度：hypotheses/experiment ≤ 4 KB，literature/critic/proof ≤ 8 KB，review ≤ 8 KB。超過要有理由（例如很多 Lean 定理要逐條對照）。
- subagent 回給總控的訊息 ≤ 15 行：做了什麼、結果、交付檔路徑、未解決的事。總控需要細節時自己讀檔。

## 5. 少輪次

- critic 一輪攻擊；作者修正後，**只有 critic 列為必修的項目**才再請 critic 複查一次（只看修正處）。之後交 reviewer，不再來回。
- reviewer 一輪。如果 reviewer 要求修正，修完後由新的 reviewer 只審修正項與最終判定，不重審整份紀錄。
- 重現檢查不省：每一位 reviewer（包括只審修正項的新 reviewer）都要親自跑一次 `experiment.md` 的重現指令。包在 `discovery.quiet` 裡時，要核對的數字若不在最後幾行，就調高 `--tail` 或直接讀 `logs/` 裡的完整紀錄，不能只看摘要。

## 6. 長執行緒要收尾重開

脈絡越長，每一輪都要重新讀一次前面的內容，成本會一直變高。

- 每完成一個里程碑（或對話很長、已經過一次自動摘要），就收尾：PR 合併、更新 DEVLOG、在專案記憶寫下「下一步」，然後開新執行緒。
- 新執行緒開頭只讀：專案記憶、`python -m discovery.digest`、DEVLOG 最後 5 行。

## 7. 和 ChatGPT 討論（Chrome）

- 只在里程碑或真正需要方向判斷時找 ChatGPT，不要每一步都問。
- 用 `get_page_text` 讀回覆，不要截圖（截圖很貴）；需要定位元素時才用 `find`。
- 提問只貼 GitHub 連結和 5～10 行摘要，讓 ChatGPT 自己讀 repo，不要把整份文件貼進對話框。
- 一次問完所有問題，避免來回多輪。
