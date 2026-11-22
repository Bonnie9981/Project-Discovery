"""Deterministic completeness check for DISC records (run in CI and tests).

An agent saying "done" is not evidence. This script checks the files exist,
required sections are present, the final status is a legal one, and any Lean
theorem a record cites actually exists in lean/ with no sorry/admit.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "records"
LEAN = ROOT / "lean"

STATUSES = {
    "REFUTED", "SUPPORTED_KNOWN", "SUPPORTED_NOVELTY_UNCHECKED",
    "SUPPORTED_POSSIBLY_NEW", "INCONCLUSIVE", "PROVEN_KNOWN", "PROVEN_POSSIBLY_NEW",
}

FULL_SECTIONS = {
    "literature.md": ["## 問題", "## 已知成果", "## 研究空白", "## 查詢紀錄"],
    "hypotheses.md": ["## 猜想", "## 推翻條件"],
    "experiment.md": ["## 方法", "## 結果", "## 重現方式"],
    "critic.md": ["## 攻擊項目", "## 獨立重算", "## 未解決的疑點"],
    "proof.md": ["## 定理對照", "## 編譯結果", "## 敘述差異"],
    "review.md": ["## 審查項目", "## 重現結果", "## 最終判定", "## 給 CEO 的摘要"],
}


def lean_theorems() -> set[str]:
    from discovery.lean_decls import source_theorems
    return set(source_theorems(LEAN))


def lean_has_sorry() -> list[str]:
    bad = []
    for f in LEAN.rglob("*.lean"):
        if ".lake" in f.parts:
            continue
        if re.search(r"\b(sorry|admit)\b", f.read_text(encoding="utf-8")):
            bad.append(str(f.relative_to(ROOT)))
    return bad


def check(d: Path) -> list[str]:
    errs: list[str] = []
    manifest = d / "record.json"
    if not manifest.exists():
        # Experiment-only record (e.g. DISC-0001).
        for f in ("report.md", "result.json"):
            if not (d / f).exists():
                errs.append(f"{d.name}: missing {f}")
        if (d / "result.json").exists():
            st = json.loads((d / "result.json").read_text(encoding="utf-8"))["aggregate"]["status"]
            if st not in STATUSES:
                errs.append(f"{d.name}: illegal status {st}")
        return errs

    m = json.loads(manifest.read_text(encoding="utf-8"))
    if m.get("status") not in STATUSES:
        errs.append(f"{d.name}: illegal status {m.get('status')}")
    for fname, heads in FULL_SECTIONS.items():
        p = d / fname
        if not p.exists():
            errs.append(f"{d.name}: missing {fname}")
            continue
        text = p.read_text(encoding="utf-8")
        for h in heads:
            if h not in text:
                errs.append(f"{d.name}/{fname}: missing section '{h}'")
    review = d / "review.md"
    if review.exists():
        mm = re.search(r"^STATUS:\s*(\S+)", review.read_text(encoding="utf-8"), re.M)
        if not mm:
            errs.append(f"{d.name}/review.md: no 'STATUS:' line")
        elif mm.group(1) != m.get("status"):
            errs.append(f"{d.name}: record.json status {m.get('status')} != review {mm.group(1)}")
    if str(m.get("status", "")).startswith("PROVEN"):
        known = lean_theorems()
        for t in m.get("lean_theorems", []):
            if t not in known:
                errs.append(f"{d.name}: cites Lean theorem {t} which does not exist")
        if not m.get("lean_theorems"):
            errs.append(f"{d.name}: PROVEN status but no lean_theorems listed")
        for f in lean_has_sorry():
            errs.append(f"{f}: contains sorry/admit")
    cited = m.get("lean_theorems", [])
    proof = d / "proof.md"
    if cited and proof.exists():
        text = proof.read_text(encoding="utf-8")
        table = text.split("## 定理對照", 1)[-1].split("\n## ", 1)[0]
        for t in cited:
            if t not in table:
                errs.append(f"{d.name}: Lean theorem {t} is cited but has no row in proof.md '## 定理對照'")
    errs += _novelty_errors(d.name, m)
    errs += _critic_model_errors(d.name, m)
    if m.get("reviewer") and m.get("reviewer") in m.get("authors", []):
        errs.append(f"{d.name}: reviewer must be independent of authors")
    return errs


CRITIC_MODEL_SINCE = "2026-11-22T12:00"  # docs/TOKEN_BUDGET.md section 1; older records are history


def _critic_model_errors(name: str, m: dict) -> list[str]:
    """Important results must have been attacked by an opus critic (TOKEN_BUDGET 1)."""
    if m.get("created_at") and str(m["created_at"]) < CRITIC_MODEL_SINCE:
        return []
    st = str(m.get("status", ""))
    nov = str((m.get("novelty") or {}).get("status", ""))
    important = st.startswith("PROVEN") or st.endswith("POSSIBLY_NEW") or nov in {
        "PENDING_REVIEW", "NOVELTY_SUPPORTED", "NOVELTY_CONFIRMED"} or m.get("milestone")
    if important and m.get("critic_model") != "opus":
        return [f"{name}: status {st} needs record.json critic_model = \"opus\" (docs/TOKEN_BUDGET.md section 1)"]
    return []


def _novelty_errors(name: str, m: dict) -> list[str]:
    """RESEARCH_STANDARDS 1b: no-match is never novelty; NOVELTY_* needs a named human reviewer."""
    from discovery import novelty as nv
    errs = []
    nov = m.get("novelty") or {}
    st = nov.get("status")
    if st is not None and st not in nv.NOVELTY_STATUSES:
        errs.append(f"{name}: illegal novelty status {st}")
    if str(m.get("status", "")).endswith("POSSIBLY_NEW") and st not in (
            nv.PENDING_REVIEW, nv.NOVELTY_SUPPORTED, nv.NOVELTY_CONFIRMED):
        errs.append(f"{name}: *_POSSIBLY_NEW needs novelty.status PENDING_REVIEW or later, got {st}")
    if st in nv.HUMAN_ONLY_STATUSES:
        who = nov.get("reviewed_by")
        if not who:
            errs.append(f"{name}: novelty {st} needs novelty.reviewed_by (a human)")
        elif who in m.get("authors", []) or who == m.get("reviewer"):
            errs.append(f"{name}: novelty reviewer {who} must not be an author or the AI reviewer")
        if not nov.get("evidence"):
            errs.append(f"{name}: novelty {st} needs novelty.evidence (search evidence ids)")
    if st == nv.NOVELTY_CONFIRMED and not nov.get("expert"):
        errs.append(f"{name}: NOVELTY_CONFIRMED needs novelty.expert (independent domain expert)")
    return errs


def main() -> int:
    dirs = sorted(p for p in RECORDS.iterdir() if p.is_dir() and p.name.startswith("DISC-"))
    errs = [e for d in dirs for e in check(d)]
    for e in errs:
        print("FAIL", e)
    print(f"checked {len(dirs)} records, {len(errs)} problems")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
