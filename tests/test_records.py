import json

from discovery import check_record


def test_all_committed_records_pass():
    dirs = [p for p in check_record.RECORDS.iterdir() if p.name.startswith("DISC-")]
    assert dirs
    for d in dirs:
        assert check_record.check(d) == [], d.name


def _full(tmp_path, status="PROVEN_KNOWN", review_status=None, theorems=("nonexistent_thm",)):
    d = tmp_path / "DISC-9999"
    d.mkdir()
    for f, heads in check_record.FULL_SECTIONS.items():
        body = "\n".join(heads)
        if f == "review.md":
            body = body.replace("## 最終判定", f"## 最終判定\nSTATUS: {review_status or status}")
        (d / f).write_text(body, encoding="utf-8")
    (d / "record.json").write_text(json.dumps(
        {"status": status, "lean_theorems": list(theorems), "authors": ["a"], "reviewer": "r"}))
    return d


def test_citing_missing_lean_theorem_fails(tmp_path):
    errs = check_record.check(_full(tmp_path))
    assert any("does not exist" in e for e in errs)


def test_status_mismatch_fails(tmp_path):
    errs = check_record.check(_full(tmp_path, "SUPPORTED_KNOWN", review_status="PROVEN_KNOWN", theorems=()))
    assert any("!=" in e for e in errs)


def test_missing_section_fails(tmp_path):
    d = _full(tmp_path, "SUPPORTED_KNOWN", theorems=())
    (d / "critic.md").write_text("nothing", encoding="utf-8")
    assert any("critic.md" in e for e in check_record.check(d))
