"""Static check that independent implementations really are independent.

Convention (docs/RESEARCH_STANDARDS.md section 2b): a research line puts its
implementations in separate files named ``impl_a.py``, ``impl_b.py`` and,
optionally, ``impl_c.py`` (the Critic's). Each one must be self-contained:

- it must not import another ``impl_*`` module;
- it must not import any other module of its own research line
  (shared helpers are exactly how one bug ends up in "both" implementations);
- it must not import ``research.*`` at all.

The standard library and third-party packages are allowed. This check cannot
prove the *algorithms* differ; the Critic and Reviewer still judge that, and
each impl file must say in its docstring which method it uses.

Run: python -m discovery.independence   (CI runs it)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import: always inside the research line
                mods.add("." * node.level + (node.module or ""))
            elif node.module:
                mods.add(node.module)
                mods |= {f"{node.module}.{a.name}" for a in node.names}
    return mods


def check_dir(d: Path) -> list[str]:
    impls = sorted(d.glob("impl_*.py"))
    if not impls:
        return []
    errs = []
    if len(impls) < 2:
        errs.append(f"{d.relative_to(ROOT)}: only one impl_*.py; need at least impl_a and impl_b")
    local = {p.stem for p in d.glob("*.py")}
    for p in impls:
        if not (ast.get_docstring(ast.parse(p.read_text(encoding="utf-8"))) or "").strip():
            errs.append(f"{p.relative_to(ROOT)}: missing docstring naming its method")
        for m in imported_modules(p):
            head = m.split(".")[0]
            if m.startswith("."):
                errs.append(f"{p.relative_to(ROOT)}: relative import {m!r}")
            elif head == "research":
                errs.append(f"{p.relative_to(ROOT)}: imports {m!r} (implementations must be self-contained)")
            elif head in local:
                errs.append(f"{p.relative_to(ROOT)}: imports sibling module {m!r}")
    return errs


def main() -> int:
    dirs = sorted({p.parent for p in RESEARCH.rglob("impl_*.py")})
    errs = [e for d in dirs for e in check_dir(d)]
    for e in errs:
        print("FAIL", e)
    print(f"checked {len(dirs)} research dirs with impl_*.py, {len(errs)} problems")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
