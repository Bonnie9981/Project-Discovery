"""Command line: python -m discovery {run,list} ..."""
from __future__ import annotations

import argparse
import importlib
from pathlib import Path

from discovery import records
from discovery.db import DB, now

LINES = {"R-001": "research.r001.pipeline"}
DB_PATH = Path(__file__).resolve().parent.parent / "discovery.db"


def cmd_run(args) -> int:
    mod = importlib.import_module(LINES[args.line])
    db = DB(args.db)
    db.add_task(mod.TASK_ID, args.line, mod.TITLE)
    run_id = db.next_run_id(records.existing_ids())
    params = {"p_max": args.p_max, "use_network": not args.offline}
    commit = records.git_commit()
    db.start_run(run_id, mod.TASK_ID, commit, params)
    db.set_task_status(mod.TASK_ID, "running")
    db.log(run_id, "run started")
    started = now()
    try:
        result = mod.run(**params)
    except Exception as e:
        db.log(run_id, f"run failed: {e!r}")
        db.set_task_status(mod.TASK_ID, "failed")
        raise
    for c in result["conjectures"]:
        db.add_result(run_id, c["id"], c["status"], c)
    db.add_result(run_id, "aggregate", result["aggregate"]["status"], result["aggregate"])
    db.finish_run(run_id)
    db.set_task_status(mod.TASK_ID, "done")
    meta = {"git_commit": commit, "env": records.environment(), "started_at": started, "finished_at": now(),
            "provenance": records.provenance(params)}
    result["meta"] = meta
    path = records.write_record(run_id, result, mod.report_markdown(run_id, result, meta))
    db.log(run_id, f"record written to {path.name}")
    print(f"{run_id}: {result['aggregate']['status']}  sequence={result['aggregate']['sequence']}")
    print(f"record: {path}")
    return 0


def cmd_new(args) -> int:
    """Create an empty full-loop record for the six agents to fill in."""
    import json
    from discovery.check_record import FULL_SECTIONS
    db = DB(args.db)
    db.add_task(args.line, args.line, args.title)
    run_id = db.next_run_id(records.existing_ids())
    d = records.RECORDS_DIR / run_id
    d.mkdir(parents=True)
    for fname, heads in FULL_SECTIONS.items():
        (d / fname).write_text(f"# {run_id} {fname}\n\n" + "\n\n".join(f"{h}\n\n（待填）" for h in heads) + "\n",
                               encoding="utf-8")
    (d / "record.json").write_text(json.dumps({
        "id": run_id, "line": args.line, "title": args.title, "status": "INCONCLUSIVE",
        "authors": [], "reviewer": None, "lean_theorems": [], "created_at": now(),
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    db.start_run(run_id, args.line, records.git_commit(), {"kind": "full", "title": args.title})
    db.log(run_id, "full record created")
    print(d)
    return 0


def cmd_list(args) -> int:
    db = DB(args.db)
    print("tasks:")
    for t in db.tasks():
        print(f"  {t['id']}  {t['status']:8}  {t['title']}")
    print("runs:")
    for r in db.runs():
        agg = [x for x in db.results(r["id"]) if x["conjecture"] == "aggregate"]
        print(f"  {r['id']}  {r['task_id']}  {agg[0]['status'] if agg else '(unfinished)'}")
    pending = db.pending_tasks()
    if pending:
        print("to resume:", ", ".join(t["id"] for t in pending))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="discovery")
    ap.add_argument("--db", default=str(DB_PATH))
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run a research line")
    r.add_argument("line", choices=sorted(LINES))
    r.add_argument("--p-max", type=int, default=2000)
    r.add_argument("--offline", action="store_true", help="skip online novelty sources")
    r.set_defaults(func=cmd_run)
    n = sub.add_parser("new", help="create an empty full-loop DISC record")
    n.add_argument("line")
    n.add_argument("title")
    n.set_defaults(func=cmd_new)
    sub.add_parser("list", help="list tasks and runs").set_defaults(func=cmd_list)
    args = ap.parse_args(argv)
    return args.func(args)
