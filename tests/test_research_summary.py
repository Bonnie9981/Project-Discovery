"""RESEARCH.md 必須為每一份 DISC 紀錄留一節白話摘要。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_record_has_plain_summary():
    text = (ROOT / "RESEARCH.md").read_text(encoding="utf-8")
    records = sorted(p.name for p in (ROOT / "records").iterdir()
                     if p.is_dir() and p.name.startswith("DISC-"))
    assert records, "找不到任何 DISC 紀錄"
    missing = [r for r in records if f"## {r}" not in text]
    assert not missing, f"RESEARCH.md 缺少這些紀錄的白話摘要：{missing}"
