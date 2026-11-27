"""Offline full-text OEIS (every entry, every comment and formula line).

The data comes from the official OEIS git mirror https://github.com/oeis/oeisdata
(one ``seq/Annn/Annnnnn.seq`` file per entry, internal format, synced daily,
CC BY-SA 4.0). It is NOT committed here: ``fetch`` clones it into
data/oeis/oeisdata/ (gitignored) and ``build`` writes a SQLite index to
data/oeis/index/oeisdb.sqlite.

    python -m discovery.oeisdb fetch            # clone or update (~400k files)
    python -m discovery.oeisdb build            # parse -> SQLite (a few minutes)
    python -m discovery.oeisdb stats
    python -m discovery.oeisdb conj --kind never --since 2015 --open --limit 30
    python -m discovery.oeisdb grep "is never" --tag C
    python -m discovery.oeisdb show A294646
    python -m discovery.oeisdb export A294646   # -> data/cx/entries/ for cxsearch

``conj`` lists conjecture lines (Conjecture / It seems / apparently / ...),
tagged by structure (never, divides, periodic, base_digits, ...). ``--open``
drops entries whose other lines already use words like counterexample,
disproved, proved; this is a coarse filter, a hit still has to be read by a
person (lesson of A218483). The snapshot commit is printed with every query so
a record can cite exactly what was searched; absence from the snapshot says
nothing about novelty.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "oeis" / "oeisdata"
DB = ROOT / "data" / "oeis" / "index" / "oeisdb.sqlite"
ENTRY_DIR = ROOT / "data" / "cx" / "entries"
REPO = "https://github.com/oeis/oeisdata"

LINE = re.compile(r"^%([A-Za-z]) (A\d{6}) ?(.*)$")
TEXT_TAGS = "NCFEY"  # lines kept for text search
CONJ = re.compile(
    r"\b(conjectur\w*|it seems|seems that|it appears|appears that|apparently|"
    r"empirical\w*|presumably|probably|it is likely|we guess)\b", re.I)
# Strong words on some other line of the entry: maybe already settled.
SETTLED = re.compile(
    r"counterexample|disprove|is false|fails for|not true|\bproved\b|\bproven\b|"
    r"proof of (the|this) conjecture|conjecture (is|was) (true|confirmed)|confirmed", re.I)
KINDS = {
    "never": r"\bnever\b|\bno term\b|\bnone of\b",
    "no_solutions": r"no (other |more |further )?solutions?|\bhas no\b|there (is|are) no",
    "always_prime": r"always (a )?prime|are (all )?primes?\b|\bis prime\b",
    "divides": r"\bdivid|divisib|\bmod\b|\(mod |congruent|==",
    "periodic": r"periodic|\bperiod\b",
    "finite": r"finite|no more terms|only terms|full list|complete list|the only",
    "infinite": r"infinitely many|infinite",
    "base_digits": r"\bbase \d+|in base|palindrom|\bdigits?\b|revers|concatenat",
    "gf": r"\bg\.f\.|generating function",
    "recurrence": r"a\(n\) = .*a\(n-\d+\)|recurrence",
    "asymptotic": r" ~ |asymptotic|\blimit\b",
    "inequality": r"<=|>=|\bless than\b|\bgreater than\b|\bat most\b|\bat least\b",
}
KIND_RE = {k: re.compile(v, re.I) for k, v in KINDS.items()}
DATE = re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d{1,2} (\d{4})\b")
SIG = re.compile(r"_([^_]{2,60})_,? (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d{1,2} \d{4}")


def kinds_of(text: str) -> list[str]:
    return [k for k, r in KIND_RE.items() if r.search(text)]


def parse_seq(text: str) -> dict:
    """Parse one entry in OEIS internal format."""
    e = {"anum": None, "name": "", "keywords": "", "offset": 0, "author": "",
         "year": None, "modified": "", "data": "", "lines": []}
    for raw in text.splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        tag, anum, body = m.groups()
        e["anum"] = e["anum"] or anum
        if tag in "STU":
            e["data"] += body.strip()
        elif tag == "N":
            e["name"] = body
        elif tag == "K":
            e["keywords"] = body.strip()
        elif tag == "O":
            try:
                e["offset"] = int(body.split(",")[0])
            except ValueError:
                pass
        elif tag == "A":
            e["author"] = body
            d = DATE.search(body)
            e["year"] = int(d.group(1)) if d else None
        elif tag == "I":
            e["modified"] = body.split("#", 1)[-1].strip()
        if tag in TEXT_TAGS:
            e["lines"].append((tag, body))
    if e["anum"] is None:
        raise ValueError("no OEIS lines")
    return e


def conj_rows(e: dict):
    """(tag, text, kinds, year, by) for every conjecture-like C/F line."""
    for tag, body in e["lines"]:
        # A line that reports a counterexample/proof is a settlement, not a conjecture.
        if tag in "CF" and CONJ.search(body) and not SETTLED.search(body):
            d = DATE.search(body)
            s = SIG.search(body)
            yield (tag, body, ",".join(kinds_of(body)),
                   int(d.group(1)) if d else e["year"], s.group(1) if s else "")


def settled(e: dict, conj_texts: set[str]) -> bool:
    return any(SETTLED.search(b) for t, b in e["lines"]
               if t in "CFE" and b not in conj_texts)


SCHEMA = """
create table meta(k text primary key, v text);
create table seq(anum text primary key, name text, keywords text, offset int,
  author text, year int, modified text, nterms int, settled int);
create table line(anum text, tag text, text text);
create table conj(anum text, tag text, text text, kinds text, year int, by text);
create index line_anum on line(anum);
create index conj_anum on conj(anum);
create index conj_year on conj(year);
"""


def build(src: Path = SRC, db: Path = DB, progress: bool = True) -> dict:
    files = sorted((src / "seq").glob("A*/A*.seq"))
    if not files:
        raise SystemExit(f"no .seq files under {src}/seq; run `python -m discovery.oeisdb fetch`")
    db.parent.mkdir(parents=True, exist_ok=True)
    tmp = db.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    con = sqlite3.connect(tmp)
    con.executescript(SCHEMA)
    n = nconj = 0
    for i, f in enumerate(files):
        try:
            e = parse_seq(f.read_text(encoding="utf-8", errors="replace"))
        except ValueError:
            continue
        rows = list(conj_rows(e))
        nterms = e["data"].count(",") + 1 if e["data"].strip(",") else 0
        con.execute("insert into seq values(?,?,?,?,?,?,?,?,?)",
                    (e["anum"], e["name"], e["keywords"], e["offset"], e["author"],
                     e["year"], e["modified"], nterms, int(settled(e, {r[1] for r in rows}))))
        con.executemany("insert into line values(?,?,?)", [(e["anum"], t, b) for t, b in e["lines"]])
        con.executemany("insert into conj values(?,?,?,?,?,?)", [(e["anum"], *r) for r in rows])
        n += 1
        nconj += len(rows)
        if progress and i % 50000 == 0:
            print(f"  {i}/{len(files)}", file=sys.stderr)
    meta = {"source": REPO, "commit": _commit(src), "built": _now(),
            "entries": n, "conjecture_lines": nconj}
    con.executemany("insert into meta values(?,?)", [(k, str(v)) for k, v in meta.items()])
    con.commit()
    con.close()
    tmp.replace(db)
    return meta


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _commit(src: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(src), "log", "-1", "--format=%H %cI"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def fetch(src: Path = SRC) -> str:
    """Shallow, sparse clone of seq/ (or pull if present)."""
    if (src / ".git").exists():
        subprocess.run(["git", "-C", str(src), "pull", "-q", "--depth", "1"], check=True)
    else:
        src.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                        REPO, str(src)], check=True)
        subprocess.run(["git", "-C", str(src), "sparse-checkout", "set", "seq"], check=True)
    return _commit(src)


def connect(db: Path = DB) -> sqlite3.Connection:
    if not db.exists():
        raise SystemExit(f"{db} missing; run `python -m discovery.oeisdb fetch` then `build`")
    con = sqlite3.connect(db)
    con.create_function("regexp", 2, lambda p, s: s is not None and re.search(p, s, re.I) is not None)
    return con


def snapshot(con) -> str:
    m = dict(con.execute("select k, v from meta"))
    return f"oeisdata {m.get('commit', '?')[:12]} ({m.get('entries')} entries, built {m.get('built')})"


def excluded() -> set[str]:
    """Entries this project already handled: cx triage + results/ folders."""
    out: set[str] = set()
    tri = ROOT / "data" / "cx" / "triage.json"
    if tri.exists():
        out |= {k for k in json.loads(tri.read_text(encoding="utf-8")) if re.fullmatch(r"A\d{6}", k)}
    res = ROOT / "results"
    if res.exists():
        for p in res.iterdir():
            out |= set(re.findall(r"A\d{6}", p.name))
    return out


def query_conj(con, kinds=(), text=None, since=None, until=None, keyword=None,
               only_open=False, skip_done=False, limit=50, anum_from=None):
    sql = ("select c.anum, c.year, c.kinds, c.by, s.keywords, s.settled, s.name, c.text "
           "from conj c join seq s using(anum) where 1=1")
    args: list = []
    for k in kinds:
        sql += " and (',' || c.kinds || ',') like ?"
        args.append(f"%,{k},%")
    if text:
        sql += " and c.text regexp ?"
        args.append(text)
    if since:
        sql += " and c.year >= ?"
        args.append(since)
    if until:
        sql += " and c.year <= ?"
        args.append(until)
    if keyword:
        sql += " and (',' || s.keywords || ',') like ?"
        args.append(f"%,{keyword},%")
    if only_open:
        sql += " and s.settled = 0"
    if anum_from:
        sql += " and c.anum >= ?"
        args.append(anum_from)
    sql += " order by c.anum"
    done = excluded() if skip_done else set()
    out = []
    for r in con.execute(sql, args):
        if r[0] in done:
            continue
        out.append(dict(zip(("anum", "year", "kinds", "by", "keywords", "settled", "name", "text"), r)))
        if len(out) >= limit:
            break
    return out


def grep(con, pattern, tag=None, limit=50):
    sql, args = "select anum, tag, text from line where text regexp ?", [pattern]
    if tag:
        sql += " and tag = ?"
        args.append(tag)
    return [dict(zip(("anum", "tag", "text"), r))
            for r in con.execute(sql + " order by anum limit ?", args + [limit])]


def entry_text(anum: str, src: Path = SRC) -> str | None:
    p = src / "seq" / anum[:4] / f"{anum}.seq"
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else None


def export(anum: str, out: Path = ENTRY_DIR, src: Path = SRC) -> Path:
    """Copy the verbatim entry into data/cx/entries/ (what cxsearch.entry.load reads)."""
    t = entry_text(anum, src)
    if t is None:
        raise SystemExit(f"{anum} not in {src}")
    out.mkdir(parents=True, exist_ok=True)
    p = out / f"{anum}.txt"
    p.write_text(t, encoding="utf-8")
    return p


def stats(con) -> dict:
    s = {"snapshot": snapshot(con),
         "entries": con.execute("select count(*) from seq").fetchone()[0],
         "conjecture_lines": con.execute("select count(*) from conj").fetchone()[0],
         "entries_with_conjecture": con.execute("select count(distinct anum) from conj").fetchone()[0],
         "open_entries_with_conjecture": con.execute(
             "select count(distinct c.anum) from conj c join seq s using(anum) where s.settled=0").fetchone()[0]}
    s["by_kind"] = {k: con.execute("select count(*) from conj where (','||kinds||',') like ?",
                                   (f"%,{k},%",)).fetchone()[0] for k in KINDS}
    s["by_decade"] = dict(con.execute(
        "select (year/5)*5, count(*) from conj where year is not null group by 1 order by 1"))
    return s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m discovery.oeisdb")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    sub.add_parser("build")
    sub.add_parser("stats")
    c = sub.add_parser("conj", help="list conjecture lines")
    c.add_argument("--kind", action="append", default=[], choices=list(KINDS))
    c.add_argument("--text", help="regex on the conjecture line")
    c.add_argument("--since", type=int)
    c.add_argument("--until", type=int)
    c.add_argument("--keyword", help="OEIS keyword, e.g. nonn, hard, base")
    c.add_argument("--open", action="store_true", help="drop entries that look settled")
    c.add_argument("--new", action="store_true", help="drop entries this project already handled")
    c.add_argument("--from", dest="anum_from", help="start at this A-number")
    c.add_argument("--limit", type=int, default=30)
    c.add_argument("--json", action="store_true")
    g = sub.add_parser("grep", help="regex over N/C/F/E/Y lines")
    g.add_argument("pattern")
    g.add_argument("--tag", choices=list(TEXT_TAGS))
    g.add_argument("--limit", type=int, default=30)
    for name in ("show", "export"):
        p = sub.add_parser(name)
        p.add_argument("anums", nargs="+")
    a = ap.parse_args(argv)

    if a.cmd == "fetch":
        print(fetch())
        return 0
    if a.cmd == "build":
        print(json.dumps(build()))
        return 0
    if a.cmd == "show":
        for x in a.anums:
            print(entry_text(x) or f"{x}: not found")
        return 0
    if a.cmd == "export":
        for x in a.anums:
            print(export(x))
        return 0
    con = connect()
    if a.cmd == "stats":
        print(json.dumps(stats(con), indent=1))
        return 0
    print(f"# {snapshot(con)}")
    if a.cmd == "grep":
        for r in grep(con, a.pattern, a.tag, a.limit):
            print(f"{r['anum']} %{r['tag']} {r['text'][:200]}")
        return 0
    rows = query_conj(con, a.kind, a.text, a.since, a.until, a.keyword, a.open, a.new,
                      a.limit, a.anum_from)
    for r in rows:
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        else:
            flag = "S" if r["settled"] else " "
            print(f"{r['anum']} {r['year'] or '----'} {flag} [{r['kinds']}] {r['text'][:180]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
