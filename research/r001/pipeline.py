"""R-001 minimal research loop.

Hypothesize -> Experiment (implementation A) -> Challenge (counterexample search)
-> Verify (implementation B) -> Novelty check -> Record.

Hypothesis family for this first run (deliberately simple, so the pipeline can be
audited by hand):  for a prime p, "n^2 + n + p is prime for every 0 <= n <= p-2".
"""
from __future__ import annotations

from discovery import novelty, verify
from discovery.verify import Conjecture
from research.r001.primality import is_prime_mr, is_prime_trial

TASK_ID = "R-001"
TITLE = "Prime-generating quadratics n^2+n+p"


def primes_up_to(m: int) -> list[int]:
    return [p for p in range(2, m + 1) if is_prime_trial(p)]


def make_conjecture(p: int) -> Conjecture:
    return Conjecture(
        id=f"Q{p}",
        statement=f"n^2 + n + {p} is prime for every integer 0 <= n <= {p - 2}",
        domain=lambda p=p: range(0, p - 1),
        domain_desc=f"0..{p - 2} (complete: the statement is finite)",
        holds_a=lambda n, p=p: is_prime_trial(n * n + n + p),
        holds_b=lambda n, p=p: is_prime_mr(n * n + n + p),
    )


def run(p_max: int = 2000, use_network: bool = True) -> dict:
    conjs = [make_conjecture(p) for p in primes_up_to(p_max)]
    verdicts = [verify.check(c) for c in conjs]

    supported = [int(v.conjecture_id[1:]) for v in verdicts if v.status == verify.SUPPORTED_IN_RANGE]
    inconclusive = [v for v in verdicts if v.status == verify.INCONCLUSIVE]

    # Aggregate finding: the set of p for which the statement holds.
    nov = novelty.check_sequence(supported, use_network=use_network) if supported else None
    if inconclusive:
        aggregate_status = verify.INCONCLUSIVE
    elif not supported:
        aggregate_status = verify.REFUTED
    elif nov.known:
        aggregate_status = verify.SUPPORTED_KNOWN
    elif nov.known is False:
        aggregate_status = verify.SUPPORTED_POSSIBLY_NEW
    else:
        aggregate_status = verify.SUPPORTED_NOVELTY_UNCHECKED

    return {
        "task": TASK_ID,
        "params": {"p_max": p_max, "use_network": use_network},
        "conjectures": [
            {"id": c.id, "statement": c.statement, "domain": c.domain_desc, **v.as_dict()}
            for c, v in zip(conjs, verdicts)
        ],
        "aggregate": {
            "statement": f"Primes p <= {p_max} for which n^2+n+p is prime for all 0<=n<=p-2",
            "sequence": supported,
            "status": aggregate_status,
            "novelty": nov.as_dict() if nov else None,
        },
    }


def report_markdown(run_id: str, result: dict, meta: dict) -> str:
    agg = result["aggregate"]
    conjs = result["conjectures"]
    refuted = [c for c in conjs if c["status"] == verify.REFUTED]
    held = [c for c in conjs if c["status"] == verify.SUPPORTED_IN_RANGE]
    inconc = [c for c in conjs if c["status"] == verify.INCONCLUSIVE]
    nov = agg["novelty"] or {}
    lines = [
        f"# {run_id}: {TITLE}",
        "",
        f"- 研究線：{TASK_ID}",
        f"- 程式版本：`{meta.get('git_commit')}`",
        f"- 環境：Python {meta['env']['python']}，{meta['env']['platform']}",
        f"- 參數：`{result['params']}`",
        f"- 開始 / 結束：{meta['started_at']} / {meta['finished_at']}",
        "",
        "## 1. 問題（精確定義）",
        "",
        "對每個質數 p ≤ p_max，猜想 Q_p：「對所有整數 0 ≤ n ≤ p−2，n² + n + p 都是質數」。",
        "每個 Q_p 是有限命題，所以檢查完整個範圍就等於判定它的真假（前提是質數判定正確）。",
        "",
        "## 2. 方法",
        "",
        "- 實作 A：試除法判定質數。實作 B：Miller–Rabin（前 12 個質數為底，在本範圍內是確定性的）。",
        "- 兩個實作對每個 n 都要給出相同答案，否則整筆結果判為 INCONCLUSIVE。",
        "- 找到第一個兩邊都同意的反例就判定 Q_p 不成立。",
        "- 成立的 p 組成一個數列，拿去做新穎性檢查。",
        "",
        "## 3. 結果",
        "",
        f"- 測試的猜想數：{len(conjs)}",
        f"- 被反駁：{len(refuted)}",
        f"- 成立：{len(held)} → p = {agg['sequence']}",
        f"- 實作不一致：{len(inconc)}",
        "",
        "被反駁的前 10 個（反例 n）：",
        "",
        "| 猜想 | 反例 n | n²+n+p |",
        "|---|---|---|",
    ]
    for c in refuted[:10]:
        p = int(c["id"][1:])
        n = c["counterexample"]
        lines.append(f"| {c['id']} | {n} | {n * n + n + p} |")
    lines += [
        "",
        "## 4. 新穎性檢查",
        "",
        f"- 已查來源：{nov.get('sources_checked')}",
        f"- 查詢失敗：{nov.get('sources_failed')}",
    ]
    for m in nov.get("matches", []):
        lines.append(f"- 符合：{m['id']} — {m['name']}" + (f"（{m['citation']}）" if m.get("citation") else ""))
    lines += [
        "",
        "## 5. 結論",
        "",
        f"**判定：`{agg['status']}`**",
        "",
    ]
    if agg["status"] == verify.SUPPORTED_KNOWN:
        lines += [
            "系統重新找到了一個已知結果（Euler 的 lucky numbers，Rabinowitsch 1913），新穎性檢查正確地把它標成「已知」。",
            "這**不是新發現**。這次演練的價值在於證明整條流程（生成 → 反例搜尋 → 雙實作驗證 → 新穎性檢查 → 紀錄）能跑通，而且不會把已知結果誤報成新成果。",
        ]
    lines += [
        "",
        "## 6. 限制",
        "",
        "- 只測了 p ≤ p_max。「沒有更大的 p 成立」這件事本次沒有驗證，那需要類數 1 定理（文獻已證明），不是有限搜尋能給的。",
        "- 新穎性檢查若只查到本地已知表，代表 OEIS 沒連上；本地表是人工輸入的，只能用來確認「已知」，不能用來確認「新」。",
        "- 尚未有 Lean 形式化證明。",
        "",
    ]
    return "\n".join(lines)
