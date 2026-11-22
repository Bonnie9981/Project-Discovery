# DISC-0002 review.md

作者：reviewer（獨立 subagent）

我沒有參與這份研究。讀過的檔案：`records/DISC-0002/` 全部七個檔案、`research/r001/drill.py`、`research/r001/primality.py`、`discovery/verify.py`、`discovery/check_record.py`、`discovery/known_results.json`、`lean/Discovery/R001.lean`、`lean/AxiomCheck.lean`、`lean/lakefile.toml`、`lean/lake-manifest.json`、`.github/workflows/lean.yml`、`.github/workflows/test.yml`、`tests/test_primality.py`，以及 `git log` 和 commit `5288d72` 的 diff。

## 審查項目

### R1. 結論是否被證據支持（逐項）

| 猜想 | 證據 | 我的判定 | 理由 |
|---|---|---|---|
| H1 | Lean `boundary_eq`、`boundary_not_prime`，CI 編譯通過；另有 p = 2..10000 的雙實作檢查 | `PROVEN_KNOWN` | 一般情形由 Lean 證明，不是只靠有限檢查。結果是一行代數，屬常識，不是新的。 |
| H2 | Lean `euler41`（`interval_cases` + `norm_num`），CI 通過；雙實作 40 個值 | `PROVEN_KNOWN` | 有限命題，Lean 已完整證明。Euler (1772) 的經典結果，本地已知成果表 A014556 含 41。 |
| H3 | Lean `euler41_fails`，CI 通過；1681 = 41² | `PROVEN_KNOWN` | 同上。 |
| H4 | 只有 p ≤ 100000 的雙實作檢查，無 Lean | `SUPPORTED_KNOWN` | 範圍內成立；清單與本地已知成果表 A014556 一致。一般情形（沒有更大的 p）依賴類數 1 定理，紀錄沒有說成已證明。 |
| H5 | 只有 p ≤ 100000 的雙實作檢查，無 Lean | `SUPPORTED_NOVELTY_UNCHECKED` | 範圍內成立，但 √(p/3) 判準的出處（literature 第 5 條，Ribenboim）是憑記憶寫的，版次頁碼未查證，本地已知成果表也沒有這一條。依 §1，沒有查證成功的來源就不能標 `KNOWN`。我個人預期這是已知結果，但這不算查證。紀錄本身也沒有宣稱它是新的。 |

- 「範圍內成立」與「證明」的區分：hypotheses.md、experiment.md、proof.md 都把 H4、H5 寫成「範圍內成立」，proof.md 明說未形式化，**沒有誇大**。
- Lean 敘述與猜想的對應：我逐條核對，與 critic A7 結論一致。`boundary_eq` 的 `hp : 1 ≤ p` 讓自然數減法不截斷；`∀ n < 40` 對 ℕ 等於 0..39。H1 括號內「n ≤ p−2 已是最長」只是口語推論，proof.md 的「敘述差異」已誠實說明沒有形式化 Q_p。

### R2. 新穎性與文獻主張

- literature.md 清楚標示 OEIS、OpenAlex、arXiv 都**連線失敗**，第 1～6 條「由 agent 依既有知識撰寫，未經線上查證」。這是誠實的。
- 唯一查證成功的來源是本地表 `known_results.json`（A014556），而這張表本身是人工輸入的。所以 H4 的 `KNOWN` 依據是本地表，不是線上 OEIS。
- 第 3 條（Rabinowitsch 判準）已依 critic 修正為「判別式 1−4p 本身」的版本，並保留修正紀錄。修正後的敘述正確。
- 「研究空白」已縮限為「第 1～4 條在 1967 年以前已解決」，第 5 條另外標示未查證。這個修正到位。
- 紀錄沒有任何「新發現」的宣稱。

### R3. critic 的問題是否真的被處理（對照程式與 git log）

| critic 項目 | 處理狀況 | 我查到的 |
|---|---|---|
| A5 MR 12 個底的上界寫錯 | **已修** | commit `5288d72`：`_MR_BASES` 加入 41，docstring 改為 3317044064679887385961981；`tests/test_primality.py` 新增 318665857834031151167461 必須判為合數的測試。我在 worktree 跑 pytest，16 個全部通過。新上界與 critic 的實測一致（該數通過 2..41 全部 13 個底，所以是 13 個底的正確上界）。 |
| A6 H3 狀態名稱不合規 | **已修** | `drill.py` 的 `h3()` 改用 `verify.SUPPORTED_IN_RANGE` / `REFUTED` / `INCONCLUSIVE`；`experiment_data.json` 中 H3 為 `SUPPORTED_IN_RANGE`。 |
| A7 Lean 檔頭提到未定義的 `Q` | **已修** | 檔頭改為「Context (not formalised here)」。但 `boundary_not_prime` 的 doc comment 仍寫「in `Q p`」，只是註解，不影響正確性。 |
| A8 literature 第 3 條錯誤、「1967 年以前」過度概括 | **已修** | 見 R2。 |
| A3 H5 檢驗力不足 | **只記錄為限制** | experiment.md「已知限制」有寫，H5 沒有被升級。處理方式合理。 |
| A4 H4/H5 雙實作共用定義域與範圍邏輯 | **只記錄為限制，程式未改** | `drill.py` 仍只用 `is_prime_trial` 產生質數、共用 `q_holds` 與 `isqrt_p_over_3`。這次靠 critic 與我各自的獨立重算補強（見下方），但這是結構性弱點，之後的研究線應修。 |
| A9 可重現性 | 已重新確認 | 見「重現結果」。 |

### R4. 其他發現（小問題）

1. experiment.md 寫「第一版（commit `9a837f1`）結果相同」，但第一版 H3 的狀態字串是 `REFUTED_EXTENSION`，與第二版不同。應改成「除 H3 狀態名稱外結果相同」。
2. `record.json` 的 `status` 目前是 `INCONCLUSIVE`（預設佔位），必須改成本審查的最終狀態，否則 `check_record` 會因 `review.md` 與 `record.json` 不一致而失敗。
3. `record.json` 的 `lean_theorems` 已列出四個定理，名稱都確實存在於 `lean/Discovery/R001.lean`。
4. proof.md 說第一次編譯失敗後才修好：CI 紀錄中 `af387cd`、`5740632` 的 lean run 失敗，`3911f24` 起成功，與敘述相符。
5. 工作目錄 HEAD 現在是 `23470b7`（只改 README），在 `5288d72` 之後，不影響程式與結果。

## 重現結果

### 1. 依 experiment.md 指令重現

- 在暫存 worktree checkout `5288d723beb169dfc2a614c808c52f9ec9a142b2`，執行 `python -m research.r001.drill 100000 > out.json`。
- 環境：Python 3.13.18，Linux-6.18.44-fc-v726-x86_64-with-glibc2.39。耗時 1.27 秒。
- 輸出的 `git_commit` = `5288d723beb169dfc2a614c808c52f9ec9a142b2`，沒有 `-dirty`。
- **`results` 與 `experiment_data.json` 完全相同**（Python 比對 `==` 為 True）。
- 同一個 worktree 跑 `python -m pytest -q`：16 passed。
- 完成後已 `git worktree remove`。

### 2. 我自己的獨立重算（不 import 任何專案程式）

用篩法（上限 4×10⁶）加試除法判定質數，精確的 ⌊√(p/3)⌋ 用整數比較 3(b+1)² ≤ p 計算，以 `python3 -I` 執行：

```
primes <= 100000: 9592
Q_p holds for: [2, 3, 5, 11, 17, 41]
H5 mismatches (full vs short check): []
H2 all prime: True ; 1681 prime: False ; 1681 == 41*41: True
H1 identity holds for p = 0..10000: True
```

與紀錄和 critic 的重算都一致。

### 3. Lean 在 CI 的編譯

- Run：**44999795444**（workflow `lean`，head_sha `5288d723beb169dfc2a614c808c52f9ec9a142b2`，conclusion `success`），https://github.com/Bonnie9981/Project-Discovery/actions/runs/44999795444
- Job 137138598401 `build`：所有步驟 success（manifest 已鎖定，所以「Generate lake-manifest.json」被跳過）。
- 日誌中有 `✔ Built Discovery.R001` 與 `Build completed successfully.`
- 「Reject unfinished proofs」步驟通過（沒有 `sorry`/`admit`/`axiom`）。
- `#print axioms` 輸出：

```
'Discovery.smoke_infinitely_many_primes' depends on axioms: [propext, Classical.choice, Quot.sound]
'Discovery.R001.boundary_eq' depends on axioms: [propext, Quot.sound]
'Discovery.R001.boundary_not_prime' depends on axioms: [propext, Quot.sound]
'Discovery.R001.euler41' depends on axioms: [propext, Classical.choice, Quot.sound]
'Discovery.R001.euler41_fails' depends on axioms: [propext]
```

  只用到標準公理，與 proof.md 一致。同一 commit 的 `tests` run 44999795438 也是 success。

## 最終判定

STATUS: SUPPORTED_NOVELTY_UNCHECKED

逐項狀態：H1、H2、H3 = `PROVEN_KNOWN`；H4 = `SUPPORTED_KNOWN`；H5 = `SUPPORTED_NOVELTY_UNCHECKED`。

整體取這個狀態的理由：

1. **不能用 `PROVEN_*`**：§1 規定只有 Lean 證明才能升級。H4、H5 才是這份紀錄標題「Rabinowitsch 判準」的實質內容，它們只有範圍內證據。整體標 `PROVEN_KNOWN` 會讓人以為整份紀錄都證明了。H1～H3 雖然已證明，但都是簡單的代數或有限計算。
2. **不能用 `SUPPORTED_KNOWN`**：H5 的 √(p/3) 判準沒有任何查證成功的來源（線上全部連不到，本地表沒有這條）。標 `KNOWN` 等於假裝查過了。
3. **整體狀態取最弱、且已查證的那一項**，才不會讓任何一個猜想被說得比證據更強。`SUPPORTED_NOVELTY_UNCHECKED` 的意思是「範圍內成立、新穎性沒查成」，**不可宣稱是新的**。我預期 H5 是已知結果，等有網路能查到 Ribenboim 的出處後，應以**新的 DISC 編號**重新判定為 `SUPPORTED_KNOWN`（依 §3 不改舊紀錄）。

要求修正（不影響判定，但應在合併前處理）：

1. **必要**：`record.json` 的 `status` 改為 `SUPPORTED_NOVELTY_UNCHECKED`，與本檔一致，否則 `check_record` 會失敗。
2. experiment.md「第一版結果相同」改為「除 H3 狀態名稱外相同」。
3. `R001.lean` 中 `boundary_not_prime` 的 doc comment 還提到 `Q p`，建議改寫，與檔頭一致。
4. 之後的研究線：B 實作應自己產生定義域（例如篩法）與自己的範圍迴圈，不要和 A 共用 `q_holds`、`isqrt_p_over_3`（critic A4）。
5. 有網路時複核 literature 第 1～5 條，特別是第 5 條的出處。

## 給 CEO 的摘要

1. 這次沒有新發現，也沒有宣稱新發現。這是一次完整流程演練，六個角色都跑完了。
2. 三個簡單結果（H1～H3，例如 n² + n + 41 在 n = 0..39 都是質數）已由 Lean 證明，GitHub 上的編譯通過（run 44999795444）。
3. 兩個比較深的說法（H4、H5）只在 p ≤ 100000 內檢查成立，不是證明；我自己重跑和獨立重算，結果都一樣。
4. H5 用到的文獻因為連不上網路沒有查到，所以整體標 `SUPPORTED_NOVELTY_UNCHECKED`：意思是「沒查完，不能說是新的」，不是「可能是新的」。
5. 需要先把 `record.json` 的狀態改成和這份審查一致，CI 才會過。

## 處理狀況（orchestrator 補記，非 reviewer 原文）

- 修正 1～3 已完成：`record.json` 狀態改為 `SUPPORTED_NOVELTY_UNCHECKED`，experiment.md 措辭已改，Lean doc comment 已改（只動註解，不影響證明）。
- 修正 4、5 列為之後的工作，見 PR 說明。
