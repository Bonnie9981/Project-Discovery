import sqlite3

import pytest

from discovery.db import DB


def test_results_are_append_only(tmp_path):
    db = DB(tmp_path / "t.db")
    db.add_task("R-X", "R-X", "t")
    db.start_run("DISC-0001", "R-X", None, {})
    db.add_result("DISC-0001", "c1", "REFUTED", {"n": 3})
    with pytest.raises(sqlite3.IntegrityError):
        db.conn.execute("UPDATE results SET status='SUPPORTED_POSSIBLY_NEW'")
    with pytest.raises(sqlite3.IntegrityError):
        db.conn.execute("DELETE FROM results")
    assert db.results("DISC-0001")[0]["status"] == "REFUTED"


def test_run_ids_never_reused(tmp_path):
    db = DB(tmp_path / "t.db")
    assert db.next_run_id({"DISC-0003"}) == "DISC-0004"
    db.add_task("R-X", "R-X", "t")
    db.start_run("DISC-0001", "R-X", None, {})
    assert db.next_run_id() == "DISC-0002"


def test_interrupted_task_is_resumable(tmp_path):
    db = DB(tmp_path / "t.db")
    db.add_task("R-X", "R-X", "t")
    db.set_task_status("R-X", "running")
    assert [t["id"] for t in db.pending_tasks()] == ["R-X"]
