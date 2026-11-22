"""DISC-0004 batch run (M1.2). Run: python -m research.r001.batch.run [N] [N_BIG] [OUT_DIR]

Writes OUT_DIR/result.json and OUT_DIR/report.md (default records/DISC-0004).
Uses the OEIS offline snapshot if data/oeis/raw has one; otherwise the OEIS
screen is recorded as SOURCE_UNAVAILABLE for every lead.
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

from discovery import oeis_offline, records
from research.r001.batch import candidates, engine
from research.r001.batch.library import FUNCS

ROOT = Path(__file__).resolve().parents[3]


def main(n: int = 10_000, n_big: int = 1_000_000, out: Path | None = None) -> dict:
    t0 = time.time()
    snap = oeis_offline.load_default()
    eng = engine.run(n, snap=snap)
    cands = candidates.check_all(n_big)
    for cnd in cands:
        cnd["level"] = candidates.LEVELS[cnd["id"]]
        cnd["status"] = "REFUTED" if not cnd["holds"] else "SUPPORTED_NOVELTY_UNCHECKED"
        cnd["novelty"] = "NOT_CHECKED"
    l1 = [c["id"] for c in cands if c["level"] == "L1" and c["holds"]]
    leads = [{"id": L.id, "kind": L.kind, "statement": L.statement, "score": L.score,
              "oeis_kind": L.oeis_kind, "oeis": [o["id"] for o in L.oeis], "reasons": L.reasons,
              "data": {k: (v[:40] if isinstance(v, list) else v) for k, v in L.data.items()}}
             for L in eng["leads"]]
    result = {
        "id": "DISC-0004",
        "params": {"n": n, "m": eng["m"], "n_big": n_big},
        "library": {k: {"definition": v[0], "oeis": v[1]} for k, v in FUNCS.items()},
        "base_mismatch_a_vs_b": eng["base_mismatch"],
        "dropped": {k: len(v) for k, v in eng["dropped"].items()},
        "n_sequences": eng["n_sequences"],
        "sequence_oeis_status": dict(Counter(eng["seq_status"].values())),
        "n_leads": len(leads),
        "lead_kinds": dict(Counter(x["kind"] for x in leads)),
        "leads": leads,
        "candidates": cands,
        "aggregate": {
            "goal": "M1.2: at least 10 Level-1 candidates",
            "m1_2_met": len(l1) >= 10,
            "status": "SUPPORTED_NOVELTY_UNCHECKED",
            "level1": l1,
            "refuted": [c["id"] for c in cands if not c["holds"]],
            "novelty": {"status": "NOT_CHECKED",
                        "open": [c["id"] for c in cands if c["level"] == "L1" and c["holds"]],
                        "note": "statements (not sequences) are not searchable in the OEIS snapshot; every L1 needs a literature check before M1.3"},
        },
        "oeis_snapshot": snap.label if snap else None,
        "meta": records.provenance({"n": n, "n_big": n_big}),
        "seconds": round(time.time() - t0, 1),
    }
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / "result.json").write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    a = sys.argv[1:]
    out = Path(a[2]) if len(a) > 2 else ROOT / "records" / "DISC-0004"
    r = main(int(a[0]) if a else 10_000, int(a[1]) if len(a) > 1 else 1_000_000, out)
    print(json.dumps({k: r[k] for k in ("n_sequences", "n_leads", "lead_kinds", "aggregate", "seconds")}, indent=1))
