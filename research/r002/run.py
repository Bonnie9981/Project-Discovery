"""DISC-0005 run (R-002). Run: python -m research.r002.run [W] [W_BIG] [OUT_DIR]

Writes OUT_DIR/result.json (default records/DISC-0005). Uses the OEIS offline
snapshot if data/oeis/raw has one; otherwise the screen is SOURCE_UNAVAILABLE.
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

from discovery import oeis_offline, records
from research.r002 import candidates, engine

ROOT = Path(__file__).resolve().parents[2]

LEVELS = {  # set after reading the checks; reasons are in report.md
    # C02: rule 146 differs from 18 only on pattern 111, so it is C01 plus "no 111 occurs".
    # C05, C06: rules 153 and 105 are affine (XNOR), so the transient follows from the
    # linear-algebra analysis of Martin, Odlyzko and Wolfram (1984).
    # Downgraded after the independent review (records/DISC-0005/review.md, section C):
    # C01: odd-width rule 18 is even-width rule 90 minus the antipodal cell (always 0).
    # C03: Phi(u)_i = u_i or u_{i+1} conjugates rule 18 to rule 126, so (T,P)_126(w) = (T,P)_18(w+1).
    # C11: even part reduces to rule 90; odd part has a ten-line fixed-point proof.
    # C04, C08: only the odd-width part counts (the even part is rule 90, A160467).
    "R2-C01": "L0", "R2-C02": "L0", "R2-C03": "L0", "R2-C04": "L1", "R2-C05": "L0",
    "R2-C06": "L0", "R2-C07": "L1", "R2-C08": "L1", "R2-C09": "L1", "R2-C10": "L1", "R2-C11": "L0",
}


def main(w: int = 22, w_big: int = 40, out: Path | None = None) -> dict:
    t0 = time.time()
    snap = oeis_offline.load_default()
    idx = None
    if snap is not None:
        from research.r001.batch.engine import OeisIndex
        idx = OeisIndex(snap)
    agree = engine.agreement(12)
    data = engine.scan(w)
    sym = engine.symmetry_failures(data)
    screen = engine.oeis_screen(data, idx)
    dmg = engine.damage()
    cands = candidates.check_all(w_big)
    for c in cands:
        c["level"] = LEVELS[c["id"]] if c["holds"] else "REFUTED"
        c["novelty"] = "NOT_CHECKED"
        lead = next((s for s in screen if s["quantity"] == c["source_lead"][0] and c["rule"] in s["rules"]), None)
        c["sequence_oeis"] = lead["oeis"] if lead else "rule is not a mirror-class representative"
    l1 = [c["id"] for c in cands if c["level"] == "L1"]
    result = {
        "id": "DISC-0005",
        "params": {"w": w, "w_big": w_big, "w_agreement": 12},
        "agreement_failures": agree,
        "symmetry_failures": sym,
        "orbits": {str(r): v for r, v in data.items()},
        "oeis_screen": screen,
        "oeis_screen_summary": dict(Counter(s["oeis_status"] for s in screen)),
        "damage_fraction": {str(r): v for r, v in dmg.items()},
        "damage_classes": {"heals(0)": sum(v == 0 for v in dmg.values()),
                           "local(<0.05)": sum(0 < v < 0.05 for v in dmg.values()),
                           "spreads(>=0.05)": sum(v >= 0.05 for v in dmg.values())},
        "candidates": cands,
        "aggregate": {
            "goal": "R-002 batch: Level-1 candidates on ECA orbit sizes (contributes to M1.2)",
            "status": "SUPPORTED_NOVELTY_UNCHECKED" if l1 else "INCONCLUSIVE",
            "level1": l1,
            "refuted": [c["id"] for c in cands if not c["holds"]],
            "novelty": {"status": "NOT_CHECKED", "open": l1,
                        "note": "the period sequences are largely in OEIS (A334496-A334515); transient "
                                "formulas need a literature check (Martin-Odlyzko-Wolfram 1984 and later)"},
        },
        "oeis_snapshot": snap.label if snap else None,
        "meta": records.provenance({"w": w, "w_big": w_big}),
        "seconds": None,
    }
    result["seconds"] = round(time.time() - t0, 1)
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / "result.json").write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    a = sys.argv[1:]
    out = Path(a[2]) if len(a) > 2 else ROOT / "records" / "DISC-0005"
    r = main(int(a[0]) if a else 22, int(a[1]) if len(a) > 1 else 40, out)
    print(json.dumps({k: r[k] for k in ("agreement_failures", "symmetry_failures", "oeis_screen_summary",
                                        "damage_classes", "aggregate", "seconds")}, indent=1))
