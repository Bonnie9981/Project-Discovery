"""Phase 0.5 research-integrity checks."""
import gzip
import json
import sys

import pytest

from discovery import check_record, independence, lean_decls, limits, novelty, oeis_offline, records, verify
from discovery.verify import Conjecture


# ---------------------------------------------------------------- novelty

def test_empty_and_short_queries_never_match():
    assert novelty.contains_run([], [1, 2, 3]) is None
    rep = novelty.check_sequence([], use_network=False, use_offline_oeis=False)
    assert rep.status == novelty.NOT_CHECKED and rep.known is None


def test_no_match_is_never_new():
    rep = novelty.check_sequence([7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5], use_network=False, use_offline_oeis=False)
    assert rep.status == novelty.SOURCE_UNAVAILABLE   # only the hand-made table answered
    assert rep.known is None


def test_known_sequence_with_offset_matches():
    # A014556 is 2,3,5,11,17,41: a run starting at offset 1 must still match.
    rep = novelty.check_sequence([3, 5, 11, 17, 41], use_network=False, use_offline_oeis=False)
    assert rep.status == novelty.MATCH_FOUND
    assert rep.matches[0]["offset"] == 1


@pytest.mark.parametrize("q,transform", [
    ([-2, -3, -5, -11, -17, -41], "negated"),
    ([41, 17, 11, 5, 3, 2], "reversed"),
])
def test_transformed_match_is_partial(q, transform):
    rep = novelty.check_sequence(q, use_network=False, use_offline_oeis=False)
    assert rep.status == novelty.PARTIAL_MATCH
    assert rep.matches[0]["transform"] == transform


def _fake_oeis(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    with gzip.open(raw / "stripped.gz", "wt") as f:
        f.write("# OEIS stripped\nA000045 ,0,1,1,2,3,5,8,13,21,34,\nA000027 ,1,2,3,4,5,6,7,8,9,10,\n")
    with gzip.open(raw / "names.gz", "wt") as f:
        f.write("A000045 Fibonacci numbers\nA000027 The positive integers\n")
    return tmp_path


def test_offline_snapshot_search_and_manifest(tmp_path):
    d = _fake_oeis(tmp_path)
    m = oeis_offline.register(d)
    assert len(m["files"]["stripped.gz"]["sha256"]) == 64
    rep = novelty.check_sequence([2, 3, 5, 8, 13], use_network=False, oeis_dir=d)
    assert rep.status == novelty.MATCH_FOUND and rep.matches[0]["id"] == "A000045"
    assert any(s.startswith("oeis_offline@sha256:") for s in rep.sources_checked)
    rep = novelty.check_sequence([9, 9, 9, 9, 1], use_network=False, oeis_dir=d)
    assert rep.status == novelty.NO_MATCH_IN_SCOPE and rep.known is None


def test_short_transformed_queries_do_not_count():
    # 5-term parity subsequences matched unrelated OEIS entries on the real snapshot.
    names = [n for n, _ in novelty.query_variants([9, 7, 7, 7, 1, 3, 3, 8, 2, 9, 1])]
    assert "odd_index_terms" not in names and "even_index_terms" not in names
    assert [n for n, _ in novelty.query_variants([1, 2, 3, 4, 5])] == ["identity"]


def test_offline_snapshot_tampering_detected(tmp_path):
    d = _fake_oeis(tmp_path)
    oeis_offline.register(d)
    with gzip.open(d / "raw" / "stripped.gz", "wt") as f:
        f.write("A000001 ,1,1,1,1,\n")
    with pytest.raises(RuntimeError):
        oeis_offline.load(d)


# ---------------------------------------------------------------- verify / independence

def test_third_implementation_disagreement_is_inconclusive():
    c = Conjecture("t", "", lambda: range(10), "", lambda n: True, lambda n: True, holds_c=lambda n: n != 3)
    v = verify.check(c)
    assert v.status == verify.INCONCLUSIVE and v.disagreements == [3] and v.implementations == 3


def test_independent_domains_must_agree():
    c = Conjecture("t", "", lambda: range(10), "", lambda n: True, lambda n: True,
                   domain_b=lambda: [x for x in range(11)])
    v = verify.check(c)
    assert v.status == verify.INCONCLUSIVE and v.stopped_reason == "domains differ"
    c.domain_b = lambda: list(range(10))
    assert verify.check(c).status == verify.SUPPORTED_IN_RANGE


def test_budget_stops_with_inconclusive():
    c = Conjecture("t", "", lambda: range(10**9), "", lambda n: True, lambda n: True)
    v = verify.check(c, budget=limits.Budget(max_iterations=100))
    assert v.status == verify.INCONCLUSIVE and "max_iterations" in v.stopped_reason and v.checked == 100


def test_independence_checker(tmp_path, monkeypatch):
    monkeypatch.setattr(independence, "ROOT", tmp_path)
    d = tmp_path / "line"
    d.mkdir()
    (d / "helpers.py").write_text("def f(): pass\n")
    (d / "impl_a.py").write_text('"""Brute force."""\nimport math\n')
    (d / "impl_b.py").write_text('"""Divisors."""\nfrom helpers import f\nimport impl_a\n')
    errs = independence.check_dir(d)
    assert any("helpers" in e for e in errs) and any("impl_a" in e for e in errs)
    (d / "impl_b.py").write_text('"""Divisors."""\nimport itertools\n')
    assert independence.check_dir(d) == []


def test_limits_config_loads_with_zero_api_budget():
    b = limits.Budget.load()
    assert b.api_budget_usd == 0 and b.host_allowed("api.openalex.org") and not b.host_allowed("evil.com")


@pytest.mark.skipif(sys.platform == "win32", reason="posix limits")
def test_run_limited_timeout():
    r = limits.run_limited([sys.executable, "-c", "import time; time.sleep(5)"], limits.Budget(max_seconds=1))
    assert r["status"] == "timeout"


# ---------------------------------------------------------------- lean / records

def test_lean_decls_handles_nested_namespaces_and_comments():
    src = """
namespace A
-- theorem fake1 : True := trivial
/- theorem fake2 : True := trivial -/
theorem t1 : True := trivial
namespace B
@[simp] protected theorem t2 : True := trivial
end B
section S
lemma t3 : True := trivial
end S
theorem _root_.top : True := trivial
end A
"""
    assert lean_decls.theorems_in(src) == ["A.t1", "A.B.t2", "A.t3", "top"]


def test_axiom_output_must_cover_every_source_theorem():
    names = lean_decls.source_theorems()
    full = "\n".join(f"info: AXIOMS {n}: [propext]" for n in names)
    assert lean_decls.check_axiom_output(full) == []
    missing = "\n".join(f"info: AXIOMS {n}: [propext]" for n in names[1:])
    assert any("not axiom-checked" in e for e in lean_decls.check_axiom_output(missing))
    bad = full + "\ninfo: AXIOMS X.y: [sorryAx]"
    assert any("non-standard" in e for e in lean_decls.check_axiom_output(bad))


def test_record_rejects_novelty_without_human(tmp_path):
    d = tmp_path / "DISC-9998"
    d.mkdir()
    for f, heads in check_record.FULL_SECTIONS.items():
        body = "\n".join(heads).replace("## 最終判定", "## 最終判定\nSTATUS: SUPPORTED_POSSIBLY_NEW")
        (d / f).write_text(body, encoding="utf-8")
    m = {"status": "SUPPORTED_POSSIBLY_NEW", "authors": ["a"], "reviewer": "r",
         "novelty": {"status": "NO_MATCH_IN_SCOPE"}}
    (d / "record.json").write_text(json.dumps(m))
    assert any("POSSIBLY_NEW" in e for e in check_record.check(d))
    m["novelty"] = {"status": "NOVELTY_SUPPORTED", "reviewed_by": "r"}
    (d / "record.json").write_text(json.dumps(m))
    errs = check_record.check(d)
    assert any("must not be" in e for e in errs) and any("evidence" in e for e in errs)


def test_provenance_fields():
    p = records.provenance({"x": 1})
    for k in ("git_commit", "dirty_files", "env", "packages", "lean", "data_snapshots", "params"):
        assert k in p
    assert p["lean"].get("toolchain", "").startswith("leanprover/lean4")


def test_oversized_record_refused(tmp_path):
    with pytest.raises(ValueError):
        records.write_record("DISC-9997", {"x": "a" * 2000}, "r", records_dir=tmp_path, max_mb=0.001)
