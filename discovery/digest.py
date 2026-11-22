"""Short summaries of DISC records, so agents read a digest instead of whole files.

    python -m discovery.digest                      # one line per record (start of a new thread)
    python -m discovery.digest DISC-0007            # status, sizes, headings + first line of each section
    python -m discovery.digest DISC-0007 critic.md "## 未解決的疑點"   # print one section only

This only shortens what goes into the conversation. It never replaces checks:
reviewers still rerun the reproduce command, and check_record still reads every file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RECORDS = Path(__file__).resolve().parent.parent / "records"
FIRST_LINE_MAX = 160


def _status(d: Path) -> str:
    for name, key in (("record.json", None), ("result.json", "aggregate")):
        p = d / name
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                return "?"
            data = data.get(key, {}) if key else data
            return str(data.get("status", "?"))
    return "?"


def _title(d: Path) -> str:
    p = d / "record.json"
    if p.exists():
        try:
            return str(json.loads(p.read_text(encoding="utf-8")).get("title", ""))
        except ValueError:
            return ""
    return ""


def overview(records: Path = RECORDS) -> str:
    lines = []
    for d in sorted(p for p in records.glob("DISC-*") if p.is_dir()):
        t = _title(d)
        lines.append(f"{d.name}  {_status(d)}" + (f"  {t}" if t else ""))
    return "\n".join(lines)


def sections(text: str) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((line.strip(), []))
        elif out:
            out[-1][1].append(line)
    return out


def _first(body: list[str]) -> str:
    for line in body:
        s = line.strip()
        if s:
            return s if len(s) <= FIRST_LINE_MAX else s[:FIRST_LINE_MAX] + "…"
    return "（空）"


def record_digest(d: Path) -> str:
    lines = [f"{d.name}  STATUS={_status(d)}"]
    t = _title(d)
    if t:
        lines.append(f"title: {t}")
    for f in sorted(p for p in d.iterdir() if p.is_file()):
        lines.append(f"- {f.name} ({f.stat().st_size} B)")
        if f.suffix == ".md":
            for head, body in sections(f.read_text(encoding="utf-8")):
                lines.append(f"    {head}: {_first(body)}")
    return "\n".join(lines)


def one_section(d: Path, fname: str, heading: str) -> str:
    for head, body in sections((d / fname).read_text(encoding="utf-8")):
        if head == heading.strip():
            return "\n".join([head, *body]).strip()
    raise KeyError(f"{fname}: no section {heading!r}")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(overview())
        return 0
    d = RECORDS / args[0]
    if not d.is_dir():
        print(f"no such record: {args[0]}", file=sys.stderr)
        return 2
    if len(args) == 3:
        try:
            print(one_section(d, args[1], args[2]))
        except (KeyError, OSError) as e:
            print(e, file=sys.stderr)
            return 2
        return 0
    print(record_digest(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
