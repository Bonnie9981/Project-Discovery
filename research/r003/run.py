"""Run the R-003 R3-A pilot and write records/DISC-0007/r003_pilot.json.

python -m research.r003.run      (about 30 s)
"""
from __future__ import annotations

import json
import platform
import subprocess
from pathlib import Path

from research.r002.engine import mirror, scan
from research.r003 import arith_match as am

REDUCTION = {
    18: "R2-C01 (L0): T18(w) = T90(2*ceil(w/2))",
    26: "R2-C04: even part is rule 90 (A160467); odd part T = 0",
    60: "additive rule (Martin-Odlyzko-Wolfram 1984)",
    90: "additive rule; even-width transient is A160467",
    146: "R2-C02 (L0): differs from 18 only on 111, never visited",
    153: "R2-C05 (L0): affine rule",
    154: "differs from 26 only on 111, never visited: same single-seed orbit as 26",
    165: "affine rule (complement of 90)",
    167: "one step gives NOT(seed); NOT F167(s) = F26(NOT s), so (T,P)167 = (T26 + 1, P26)",
}


def main(w_check: int = am.W_CHECK) -> dict:
    data = scan(am.W_FIT)
    leads = am.search(data)
    reps = [l for l in leads if l["rule"] <= mirror(l["rule"])]
    out = []
    for l in reps:
        row = {"rule": l["rule"], "quantity": l["quantity"], "modulus": l["modulus"],
               "nontrivial": am.nontrivial(l)}
        if row["nontrivial"]:
            rc = am.recheck(l, w_check)
            row["survives_to"] = w_check if rc["survives"] else None
            row["formulas"] = {str(c): [am.show(f) for f in fs] for c, fs in rc["pieces"].items()}
            row["reduction"] = REDUCTION.get(l["rule"], "none found")
        else:
            row["formulas"] = {str(c): [am.show(f) for f in fs[:3]] for c, fs in l["pieces"].items()}
        out.append(row)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    res = {"meta": {"python": platform.python_version(), "commit": commit,
                    "W0": am.W0, "W_FIT": am.W_FIT, "W_CHECK": w_check,
                    "G": list(am.G), "H": list(am.H), "a": list(am.A), "b": list(am.B)},
           "counts": {"leads": len(leads), "mirror_reps": len(reps),
                      "nontrivial": sum(r["nontrivial"] for r in out),
                      "nontrivial_unreduced": sum(r["nontrivial"] and r["reduction"] == "none found" for r in out)},
           "leads": out}
    Path("records/DISC-0007/r003_pilot.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    return res


if __name__ == "__main__":
    print(main()["counts"])
