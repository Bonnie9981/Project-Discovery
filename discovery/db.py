"""SQLite task queue and append-only result log.

Results and events cannot be updated or deleted: SQLite triggers reject it.
This is how "failed results are never overwritten" is enforced, not just promised.

Tasks and runs are mutable *operational state* (status, finished_at). Every change
to them is also written to the append-only events table, so their history is kept.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    line TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('queued','running','done','failed')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,               -- DISC-0001 ...
    task_id TEXT NOT NULL REFERENCES tasks(id),
    started_at TEXT NOT NULL,
    finished_at TEXT,
    git_commit TEXT,
    params TEXT NOT NULL               -- JSON
);
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL REFERENCES runs(id),
    conjecture TEXT NOT NULL,
    status TEXT NOT NULL,
    details TEXT NOT NULL,             -- JSON
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS results_no_update BEFORE UPDATE ON results
BEGIN SELECT RAISE(ABORT, 'results are append-only'); END;
CREATE TRIGGER IF NOT EXISTS results_no_delete BEFORE DELETE ON results
BEGIN SELECT RAISE(ABORT, 'results are append-only'); END;
CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DB:
    def __init__(self, path: str | Path = "discovery.db"):
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # tasks ---------------------------------------------------------------
    def add_task(self, task_id: str, line: str, title: str) -> None:
        t = now()
        self.conn.execute(
            "INSERT OR IGNORE INTO tasks VALUES (?,?,?,?,?,?)",
            (task_id, line, title, "queued", t, t),
        )
        self.conn.commit()

    def set_task_status(self, task_id: str, status: str) -> None:
        self.conn.execute(
            "UPDATE tasks SET status=?, updated_at=? WHERE id=?", (status, now(), task_id)
        )
        self.log(None, f"task {task_id} status -> {status}")

    def pending_tasks(self) -> list[sqlite3.Row]:
        """Tasks to resume: queued, or left 'running' by an interrupted session."""
        return list(self.conn.execute(
            "SELECT * FROM tasks WHERE status IN ('queued','running') ORDER BY created_at"
        ))

    def tasks(self) -> list[sqlite3.Row]:
        return list(self.conn.execute("SELECT * FROM tasks ORDER BY id"))

    # runs ----------------------------------------------------------------
    def next_run_id(self, existing: set[str] | None = None) -> str:
        """Next DISC id, never reusing one already in the DB or on disk."""
        used = {r["id"] for r in self.conn.execute("SELECT id FROM runs")}
        used |= existing or set()
        nums = [int(x.split("-")[1]) for x in used if x.startswith("DISC-")]
        return f"DISC-{(max(nums) + 1 if nums else 1):04d}"

    def start_run(self, run_id: str, task_id: str, git_commit: str | None, params: dict) -> None:
        self.conn.execute(
            "INSERT INTO runs VALUES (?,?,?,?,?,?)",
            (run_id, task_id, now(), None, git_commit, json.dumps(params, sort_keys=True)),
        )
        self.conn.commit()

    def finish_run(self, run_id: str) -> None:
        self.conn.execute("UPDATE runs SET finished_at=? WHERE id=?", (now(), run_id))
        self.log(run_id, "run finished")

    def runs(self) -> list[sqlite3.Row]:
        return list(self.conn.execute("SELECT * FROM runs ORDER BY id"))

    # append-only ---------------------------------------------------------
    def add_result(self, run_id: str, conjecture: str, status: str, details: dict) -> None:
        self.conn.execute(
            "INSERT INTO results (run_id, conjecture, status, details, created_at) VALUES (?,?,?,?,?)",
            (run_id, conjecture, status, json.dumps(details, sort_keys=True), now()),
        )
        self.conn.commit()

    def log(self, run_id: str | None, message: str) -> None:
        self.conn.execute(
            "INSERT INTO events (run_id, message, created_at) VALUES (?,?,?)",
            (run_id, message, now()),
        )
        self.conn.commit()

    def results(self, run_id: str) -> list[sqlite3.Row]:
        return list(self.conn.execute("SELECT * FROM results WHERE run_id=? ORDER BY id", (run_id,)))
