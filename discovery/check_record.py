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
    names: set[str] = set()
    for f in LEAN.rglob("*.lean"):
        if ".lake" in f.parts:
            continue
        text = f.read_text(encoding="utf-8")
        ns = re.findall(r"^namespace\s+(\S+)", text, re.M)
        for n in re.findall(r"^theorem\s+(\S+)", text, re.M):
            names.add(n)
            if ns:
                names.add(f"{ns[0]}.{n}")
    return names


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
    if m.get("reviewer") and m.get("reviewer") in m.get("authors", []):
        errs.append(f"{d.name}: reviewer must be independent of authors")
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
