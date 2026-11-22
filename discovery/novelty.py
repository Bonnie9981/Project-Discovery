"""Novelty check: is a sequence/result already known?

Sources, in order:
1. A local table of known results, each with a citation entered by a human.
2. OEIS online search (https://oeis.org).

If no source could be consulted, the answer is UNCHECKED — never "new".
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

KNOWN_FILE = Path(__file__).with_name("known_results.json")


@dataclass
class NoveltyReport:
    known: bool | None            # True known, False not found in sources checked, None unchecked
    matches: list[dict] = field(default_factory=list)
    sources_checked: list[str] = field(default_factory=list)
    sources_failed: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "known": self.known,
            "matches": self.matches,
            "sources_checked": self.sources_checked,
            "sources_failed": self.sources_failed,
        }


def _is_prefix_match(terms: list[int], ref: list[int]) -> bool:
    """terms appear as a contiguous run inside ref (OEIS-style match)."""
    k = len(terms)
    return any(ref[i:i + k] == terms for i in range(len(ref) - k + 1))


def check_local(terms: list[int], path: Path = KNOWN_FILE) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        {"source": "local", "id": e["id"], "name": e["name"], "citation": e["citation"]}
        for e in data
        if _is_prefix_match(terms, e["terms"])
    ]


def check_oeis(terms: list[int], timeout: float = 15.0) -> list[dict]:
    q = urllib.parse.quote(",".join(map(str, terms)))
    url = f"https://oeis.org/search?q={q}&fmt=json"
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    results = payload.get("results") if isinstance(payload, dict) else payload
    out = []
    for r in results or []:
        out.append({"source": "oeis", "id": f"A{int(r['number']):06d}", "name": r.get("name", "")})
    return out


def check_sequence(terms: list[int], use_network: bool = True) -> NoveltyReport:
    rep = NoveltyReport(known=None)
    try:
        rep.matches += check_local(terms)
        rep.sources_checked.append("local")
    except Exception as e:  # noqa: BLE001
        rep.sources_failed.append(f"local: {e}")
    if use_network:
        try:
            rep.matches += check_oeis(terms)
            rep.sources_checked.append("oeis")
        except Exception as e:  # noqa: BLE001
            rep.sources_failed.append(f"oeis: {type(e).__name__}: {e}")
    if rep.matches:
        rep.known = True
    elif "oeis" in rep.sources_checked:
        rep.known = False
    # Only the local table was consulted and it had nothing: still UNCHECKED.
    return rep
