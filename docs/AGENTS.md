# Agent 分工與研究循環

六個角色定義在 `.claude/agents/`，在 Claude Code 中可直接當 subagent 呼叫。每個角色只負責一份交付文件，寫在 `records/DISC-XXXX/` 下。

| 順序 | 角色 | 交付 | 不能只做 |
|---|---|---|---|
| 1 | literature | `literature.md` | 只列論文 |
| 2 | hypothesis | `hypotheses.md` | 只提一個猜想、敘述含糊 |
| 3 | experiment | `experiment.md` + 資料 | 只給圖、不給重現指令 |
| 4 | critic | `critic.md` | 只說「可能有問題」 |
| 5 | proof | `proof.md` + `lean/Discovery/*.lean` | 只寫文字證明 |
| 6 | reviewer | `review.md`（含 `STATUS:`） | 審查自己寫的東西 |

## Orchestrator（總控）

目前由 Claude Code 主執行緒擔任：

1. `python -m discovery new <研究線> "<題目>"` 建立 `records/DISC-XXXX/` 與 `record.json`。
2. 依序呼叫 1～6，每一步都讀前一步的文件。
3. critic 和 reviewer **必須是獨立的 agent 執行**（新的 subagent、沒有前面步驟的上下文），作者名單寫在 `record.json` 的 `authors`，審查者寫在 `reviewer`。
4. `python -m discovery.check_record` 必須通過，CI 的 `lean` 與 `tests` 必須綠燈。
5. 判定為 `*_POSSIBLY_NEW` 時，依規範向 CEO 回報，不得對外發布。

## 中斷與續跑

任務狀態存在 `discovery.db`。`python -m discovery list` 會列出 `queued`/`running` 的任務；重開 session 時從那裡接續。單次演練設上限：計算不超過 10 分鐘、每個猜想族最多 1 萬個實例。
