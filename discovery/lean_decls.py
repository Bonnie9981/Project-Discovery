"""List the theorems declared in lean/Discovery (namespace-aware).

Used by CI to prove the axiom check covered *every* theorem: the names printed
by AxiomCheck.lean (which enumerates the compiled environment) must include
every theorem found here in the source. Also used by check_record.

Handles nested ``namespace``/``section``/``end``, comments, attributes and the
usual modifiers. It is a cross-check, not a Lean parser: the authoritative list
is the one Lean itself prints.

Run: python -m discovery.lean_decls [axioms.txt]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT / "lean"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

_DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|nonrec)\s+)*(theorem|lemma)\s+([^\s:({\[]+)"
)


def strip_comments(text: str) -> str:
    out, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            out.append("\n" if text[i] == "\n" else " ")
            i += 1
        elif text.startswith("--", i):
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def theorems_in(text: str) -> list[str]:
    stack: list[tuple[str, str]] = []   # (kind, name)
    names = []
    for line in strip_comments(text).splitlines():
        s = line.strip()
        m = re.match(r"namespace\s+(\S+)", s)
        if m:
            stack.append(("namespace", m.group(1)))
            continue
        m = re.match(r"(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$", s)
        if m:
            stack.append(("section", m.group(1) or ""))
            continue
        if re.match(r"end(\s+\S+)?\s*$", s) and stack:
            stack.pop()
            continue
        m = _DECL.match(line)
        if m:
            n = m.group(2)
            if n.startswith("_root_."):
                names.append(n[len("_root_."):])
            else:
                prefix = ".".join(x for k, x in stack if k == "namespace")
                names.append(f"{prefix}.{n}" if prefix else n)
    return names


def source_theorems(lean_dir: Path = LEAN) -> list[str]:
    out = []
    files = [lean_dir / "Discovery.lean", *sorted((lean_dir / "Discovery").rglob("*.lean"))]
    for f in files:
        if f.exists() and ".lake" not in f.parts:
            out += theorems_in(f.read_text(encoding="utf-8"))
    return out


def parse_axiom_output(text: str) -> dict[str, list[str]]:
    """Lines 'AXIOMS <name>: [a, b]' printed by AxiomCheck.lean."""
    res = {}
    for m in re.finditer(r"AXIOMS (\S+): \[([^\]]*)\]", text):
        res[m.group(1)] = [a.strip() for a in m.group(2).split(",") if a.strip()]
    return res


def check_axiom_output(text: str, lean_dir: Path = LEAN) -> list[str]:
    printed = parse_axiom_output(text)
    errs = []
    if not printed:
        errs.append("AxiomCheck printed no theorems")
    for t in source_theorems(lean_dir):
        if t not in printed:
            errs.append(f"theorem {t} is in the source but was not axiom-checked")
    for t, axs in printed.items():
        bad = [a for a in axs if a not in ALLOWED_AXIOMS]
        if bad:
            errs.append(f"{t} uses non-standard axioms {bad}")
    return errs


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("\n".join(source_theorems()))
        return 0
    text = Path(argv[0]).read_text(encoding="utf-8")
    errs = check_axiom_output(text)
    for e in errs:
        print("FAIL", e)
    print(f"{len(parse_axiom_output(text))} theorems axiom-checked, {len(source_theorems())} in source, "
          f"{len(errs)} problems")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
