"""Offline OEIS index (discovery.oeisdb) on a two-entry fixture."""
from pathlib import Path

from discovery import oeisdb
from discovery.cxsearch import entry

FIX = Path(__file__).parent / "fixtures" / "oeisdb"


def _db(tmp_path):
    db = tmp_path / "o.sqlite"
    meta = oeisdb.build(FIX, db, progress=False)
    assert meta["entries"] == 3
    return oeisdb.connect(db)


def test_parse_and_year():
    e = oeisdb.parse_seq((FIX / "seq/A294/A294646.seq").read_text())
    assert e["anum"] == "A294646" and e["year"] == 2017 and e["offset"] == 1
    assert e["data"].startswith("1,1,1,7,")


def test_conj_kinds_and_settled(tmp_path):
    con = _db(tmp_path)
    rows = oeisdb.query_conj(con, limit=10)
    by = {r["anum"]: r for r in rows if r["anum"] == "A294646"}
    assert "never" in by["A294646"]["kinds"] and by["A294646"]["settled"] == 0
    fake = [r for r in rows if r["anum"] == "A000001"]
    assert len(fake) == 2 and all(r["settled"] == 1 for r in fake)
    assert {r["year"] for r in fake} == {2021, 2022}  # date on the line, not the entry
    assert [r["anum"] for r in oeisdb.query_conj(con, only_open=True)] == ["A000002", "A294646"]
    assert [r["anum"] for r in oeisdb.query_conj(con, kinds=["periodic"])] == ["A000001"]
    assert len(oeisdb.query_conj(con, since=2022)) == 2
    assert oeisdb.query_conj(con, keyword="base")[0]["anum"] == "A000001"


def test_grep(tmp_path):
    con = _db(tmp_path)
    assert [r["anum"] for r in oeisdb.grep(con, r"A006521", tag="C")] == ["A294646"]


def test_export_feeds_cxsearch(tmp_path):
    p = oeisdb.export("A294646", tmp_path, FIX)
    e = entry.parse(p.read_text())
    assert e.anum == "A294646" and e.offset == 1 and len(e.terms) > 50
    assert entry.align(lambda n: pow(pow(2, -1, 2 * n + 1), 2 * n, 2 * n + 1), e) is None


def test_multiline_conjecture_and_negated_counterexample(tmp_path):
    con = _db(tmp_path)
    [r] = oeisdb.query_conj(con, text="square")
    # paragraph joined through the signed line; "no counterexample" is not a settlement
    assert r["anum"] == "A000002" and r["year"] == 2024 and r["by"] == "Third Person"
    assert "never" in r["kinds"] and "Unsigned remark" not in r["text"] and r["settled"] == 0
    assert oeisdb.is_settled("A counterexample is n = 5.")
    assert not oeisdb.is_settled("Confirmed up to 10^6; no counterexample found.")
