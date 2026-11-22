"""DISC-0003 novelty layer: search the baseline and extension sequences.

Run: python -m research.r001.disc0003.novelty_run > records/DISC-0003/novelty_data.json

Uses discovery.novelty.check_sequence (local table, offline OEIS snapshot, online OEIS).
A result of NO_MATCH_IN_SCOPE never means "new" (docs/RESEARCH_STANDARDS.md 1b).
"""
from __future__ import annotations

import json

from discovery import novelty
from discovery.records import git_commit
from research.r001.disc0003 import impl_a as A
from research.r001.disc0003.run import EXT_TERMS, EXTENSIONS


def main() -> dict:
    seqs = {"H1_R1": ("R(N), N >= 1 (baseline)", A.rep_table(EXT_TERMS)[1:])}
    for key, (D, f, desc) in EXTENSIONS.items():
        seqs[key] = (desc, A.rep_table(EXT_TERMS, D, f)[1:])
    out = {"git_commit": git_commit(), "terms_per_query": EXT_TERMS, "results": {}}
    for key, (desc, terms) in seqs.items():
        rep = novelty.check_sequence(terms, use_network=True, use_offline_oeis=True)
        d = rep.as_dict()
        d["matches"] = d["matches"][:8]
        out["results"][key] = {"description": desc, **d}
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
