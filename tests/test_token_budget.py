"""Token-saving tooling: agent models are pinned, digest and quiet work and keep evidence intact."""
import re
import sys
from pathlib import Path

from discovery import digest, quiet

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".claude" / "agents"


def _front(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    block = text.split("---")[1]
    return dict(line.split(": ", 1) for line in block.strip().splitlines())


def test_every_agent_pins_a_model():
    models = {p.stem: _front(p).get("model") for p in AGENTS.glob("*.md")}
    assert set(models) == {"literature", "hypothesis", "experiment", "critic", "proof", "reviewer"}
    assert all(m in {"haiku", "sonnet", "opus", "inherit"} for m in models.values()), models
    # The final independent gate and the Lean prover stay on the strongest model.
    assert models["reviewer"] == "opus" and models["proof"] == "opus"


def test_agents_point_to_token_rules():
    for p in AGENTS.glob("*.md"):
        assert "discovery.digest" in p.read_text(encoding="utf-8"), p.name


def test_digest_overview_lists_every_record():
    out = digest.overview()
    for d in (ROOT / "records").glob("DISC-*"):
        assert d.name in out


def test_digest_section_roundtrip(tmp_path):
    d = tmp_path / "DISC-9999"
    d.mkdir()
    (d / "review.md").write_text("# x\n\n## 最終判定\n\nSTATUS: REFUTED\n\n更多\n\n## 給 CEO 的摘要\n\n短\n",
                                 encoding="utf-8")
    (d / "record.json").write_text('{"status": "REFUTED", "title": "t"}', encoding="utf-8")
    s = digest.record_digest(d)
    assert "STATUS=REFUTED" in s and "## 最終判定: STATUS: REFUTED" in s
    assert digest.one_section(d, "review.md", "## 最終判定") == "## 最終判定\n\nSTATUS: REFUTED\n\n更多"


def test_quiet_keeps_full_log_and_exit_code(tmp_path, capsys):
    log = tmp_path / "out.log"
    code = "import sys\nfor i in range(100): print('line', i)\nprint('ERROR boom')\nsys.exit(3)"
    rc = quiet.main(["--tail", "5", "--log", str(log), "--", sys.executable, "-c", code])
    assert rc == 3
    assert len(log.read_text(encoding="utf-8").splitlines()) == 101
    shown = capsys.readouterr().out
    assert "exit=3" in shown and "ERROR boom" in shown
    assert len(shown.splitlines()) < 12


def test_quiet_surfaces_errors_above_the_tail():
    lines = ["ok"] * 10 + ["Traceback here"] + ["ok"] * 50
    out = quiet.summarize(lines, tail=5, max_err=20)
    assert any(re.search("Traceback", l) for l in out)


def test_quiet_missing_command_returns_127(tmp_path):
    assert quiet.main(["--log", str(tmp_path / "x.log"), "--", "no-such-program-xyz"]) == 127


def test_digest_rejects_paths_outside_records():
    assert digest.main(["../discovery"]) == 2
    assert digest.main(["DISC-0007", "../../CLAUDE.md", "## x"]) == 2


def test_important_new_records_need_opus_critic():
    from discovery.check_record import _critic_model_errors
    new = {"created_at": "2026-12-01T00:00:00+00:00", "status": "PROVEN_KNOWN"}
    assert _critic_model_errors("D", new)
    assert not _critic_model_errors("D", {**new, "critic_model": "opus"})
    assert not _critic_model_errors("D", {**new, "status": "REFUTED"})
    assert _critic_model_errors("D", {**new, "status": "REFUTED", "milestone": True})
    assert not _critic_model_errors("D", {**new, "created_at": "2026-11-22T11:10:00+00:00"})
