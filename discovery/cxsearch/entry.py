"""OEIS internal-format entries: parse, align a definition with DATA, flag
comments that may already settle a conjecture.

The container cannot reach oeis.org, so entries are fetched in the browser
(`/search?fmt=text&q=id:A......`) and saved under data/cx/entries/.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
ENTRY_DIR = ROOT / "data" / "cx" / "entries"

# Words that mean someone may already have settled a conjecture. A hit is a
# reason for a human to read the comment, never an automatic verdict.
SETTLED = re.compile(
    r"counterexample|disprove|fails for|is false|not true|are true|is true|"
    r"proved|proof|follows from|consequence of", re.I)


@dataclass
class Entry:
    anum: str
    name: str = ""
    offset: int = 0
    terms: list[int] = field(default_factory=list)
    comments: list[str] = field(default_factory=list)
    formulas: list[str] = field(default_factory=list)
    author: str = ""

    def settled_hints(self) -> list[str]:
        return [c for c in self.comments + self.formulas if SETTLED.search(c)]


def parse(text: str) -> Entry:
    lines = [l for l in text.splitlines() if re.match(r"^%[A-Za-z] A\d{6}", l)]
    if not lines:
        raise ValueError("no OEIS lines")
    e = Entry(anum=lines[0][3:10])
    data = ""
    for l in lines:
        tag, body = l[1], l[11:]
        if l[3:10] != e.anum:
            raise ValueError("more than one entry in text")
        if tag in "STU":
            data += body.strip()
        elif tag == "N":
            e.name = body
        elif tag == "O":
            e.offset = int(body.split(",")[0])
        elif tag == "C":
            e.comments.append(body)
        elif tag == "F":
            e.formulas.append(body)
        elif tag == "A":
            e.author = body
    e.terms = [int(t) for t in data.strip(",").split(",") if t]
    return e


def load(anum: str, directory: Path = ENTRY_DIR) -> Entry:
    return parse((directory / f"{anum}.txt").read_text(encoding="utf-8"))


def align(fn: Callable[[int], int], e: Entry, count: int | None = None):
    """Compare fn(n) with DATA from the entry's offset on.

    Returns None when all compared terms agree, else (n, expected, got).
    This is the guard against the offset and definition mistakes that cause
    false counterexamples.
    """
    terms = e.terms if count is None else e.terms[:count]
    for i, want in enumerate(terms):
        n = e.offset + i
        got = fn(n)
        if got != want:
            return (n, want, got)
    return None


def align_list(values: list[int], e: Entry):
    """Same check for a list sequence (e.g. pseudoprimes in increasing order)."""
    for i, want in enumerate(e.terms):
        if i >= len(values) or values[i] != want:
            return (e.offset + i, want, values[i] if i < len(values) else None)
    return None
