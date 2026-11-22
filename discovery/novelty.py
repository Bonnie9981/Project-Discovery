"""Novelty check: is a sequence/result already known?

Sources:
1. ``local``        - a table of known results, each with a citation entered by a human.
2. ``oeis_offline`` - a local snapshot of OEIS ``stripped.gz``/``names.gz`` (see ``oeis_offline``).
3. ``oeis``         - OEIS online search (often unreachable from our machines).

Rules (docs/RESEARCH_STANDARDS.md section 1b):
- A search that finds nothing gives ``NO_MATCH_IN_SCOPE``. It never means "new".
- ``NOVELTY_SUPPORTED`` / ``NOVELTY_CONFIRMED`` are never assigned by code.
- If no real source could be consulted the status is ``SOURCE_UNAVAILABLE``
  (``NOT_CHECKED`` when the query was not searchable at all).
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

KNOWN_FILE = Path(__file__).with_name("known_results.json")

NOT_CHECKED = "NOT_CHECKED"
CHECKING = "CHECKING"
SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
MATCH_FOUND = "MATCH_FOUND"
PARTIAL_MATCH = "PARTIAL_MATCH"
NO_MATCH_IN_SCOPE = "NO_MATCH_IN_SCOPE"
PENDING_REVIEW = "PENDING_REVIEW"
NOVELTY_SUPPORTED = "NOVELTY_SUPPORTED"      # multi-source + human review only
NOVELTY_CONFIRMED = "NOVELTY_CONFIRMED"      # independent domain expert only

NOVELTY_STATUSES = (
    NOT_CHECKED, CHECKING, SOURCE_UNAVAILABLE, MATCH_FOUND, PARTIAL_MATCH,
    NO_MATCH_IN_SCOPE, PENDING_REVIEW, NOVELTY_SUPPORTED, NOVELTY_CONFIRMED,
)
AUTOMATIC_STATUSES = {NOT_CHECKED, SOURCE_UNAVAILABLE, MATCH_FOUND, PARTIAL_MATCH, NO_MATCH_IN_SCOPE}
HUMAN_ONLY_STATUSES = {NOVELTY_SUPPORTED, NOVELTY_CONFIRMED}

# Shorter queries match almost anything, so they are not searched.
MIN_TERMS = 4
# Transformed queries are looser, so they must be longer to count (tested on the real OEIS
# snapshot: 5-term parity subsequences of random data matched unrelated sequences).
MIN_TERMS_TRANSFORMED = 6
MIN_TERMS_SUBSAMPLED = 8
SUBSAMPLED = {"even_index_terms", "odd_index_terms"}


@dataclass
class NoveltyReport:
    status: str = NOT_CHECKED
    matches: list[dict] = field(default_factory=list)
    sources_checked: list[str] = field(default_factory=list)
    sources_failed: list[str] = field(default_factory=list)
    query: list[int] = field(default_factory=list)

    @property
    def known(self) -> bool | None:
        """True when something matched, otherwise None. Never False: not finding is not 'new'."""
        return True if self.status in (MATCH_FOUND, PARTIAL_MATCH) else None

    def as_dict(self) -> dict:
        return {
            "status": self.status,
            "known": self.known,
            "matches": self.matches,
            "sources_checked": self.sources_checked,
            "sources_failed": self.sources_failed,
            "query": self.query,
        }


# --------------------------------------------------------------------------- matching

def contains_run(terms: list[int], ref: list[int]) -> int | None:
    """Offset where ``terms`` occurs as a contiguous run inside ``ref``, else None.

    This is a substring match (as OEIS does), so it also covers index offsets.
    An empty query never matches.
    """
    k = len(terms)
    if k == 0 or k > len(ref):
        return None
    first = terms[0]
    for i in range(len(ref) - k + 1):
        if ref[i] == first and ref[i:i + k] == terms:
            return i
    return None


def _diff(s: list[int]) -> list[int]:
    return [b - a for a, b in zip(s, s[1:])]


def _psum(s: list[int]) -> list[int]:
    out, t = [], 0
    for x in s:
        t += x
        out.append(t)
    return out


# "identity" is an exact run match (MATCH_FOUND); every other transform gives PARTIAL_MATCH.
TRANSFORMS: dict[str, Callable[[list[int]], list[int]]] = {
    "identity": lambda s: list(s),
    "negated": lambda s: [-x for x in s],
    "reversed": lambda s: list(reversed(s)),
    "abs": lambda s: [abs(x) for x in s],
    "alternating_sign": lambda s: [x if i % 2 == 0 else -x for i, x in enumerate(s)],
    "first_differences": _diff,
    "partial_sums": _psum,
    "even_index_terms": lambda s: s[0::2],
    "odd_index_terms": lambda s: s[1::2],
}


def query_variants(terms: list[int]) -> list[tuple[str, list[int]]]:
    """Distinct transformed queries that are still long enough to mean something."""
    seen: set[tuple[int, ...]] = set()
    out = []
    for name, f in TRANSFORMS.items():
        v = f(terms)
        key = tuple(v)
        need = MIN_TERMS if name == "identity" else (
            MIN_TERMS_SUBSAMPLED if name in SUBSAMPLED else MIN_TERMS_TRANSFORMED)
        if len(v) < need or key in seen:
            continue
        seen.add(key)
        out.append((name, v))
    return out


def search_table(terms: list[int], table: Iterable[tuple[str, str, list[int]]],
                 source: str, max_matches: int = 50) -> list[dict]:
    """Search rows of (id, name, terms). Exact (identity) matches are listed first;
    transformed matches follow, each row reported once with its first matching transform."""
    variants = query_variants(terms)
    exact: list[dict] = []
    partial: list[dict] = []
    for sid, name, ref in table:
        for tname, q in variants:
            if tname != "identity" and len(partial) >= max_matches:
                break
            off = contains_run(q, ref)
            if off is not None:
                hit = {"source": source, "id": sid, "name": name, "transform": tname, "offset": off}
                (exact if tname == "identity" else partial).append(hit)
                break
        if len(exact) >= max_matches:
            break
    return (exact + partial)[:max_matches]


# --------------------------------------------------------------------------- sources

def _local_rows(path: Path):
    for e in json.loads(path.read_text(encoding="utf-8")):
        yield e["id"], e["name"], e["terms"]


def check_local(terms: list[int], path: Path = KNOWN_FILE) -> list[dict]:
    cites = {e["id"]: e["citation"] for e in json.loads(path.read_text(encoding="utf-8"))}
    hits = search_table(terms, _local_rows(path), "local")
    for h in hits:
        h["citation"] = cites[h["id"]]
    return hits


def check_oeis(terms: list[int], timeout: float = 15.0) -> list[dict]:
    q = urllib.parse.quote(",".join(map(str, terms)))
    url = f"https://oeis.org/search?q={q}&fmt=json"
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    results = payload.get("results") if isinstance(payload, dict) else payload
    return [
        {"source": "oeis", "id": f"A{int(r['number']):06d}", "name": r.get("name", ""), "transform": "identity"}
        for r in results or []
    ]


def check_sequence(terms: list[int], use_network: bool = True, use_offline_oeis: bool = True,
                   oeis_dir: Path | None = None) -> NoveltyReport:
    rep = NoveltyReport(query=list(terms))
    if len(terms) < MIN_TERMS:
        rep.sources_failed.append(f"query has {len(terms)} terms; need >= {MIN_TERMS}")
        return rep  # NOT_CHECKED

    try:
        rep.matches += check_local(terms)
        rep.sources_checked.append("local")
    except Exception as e:  # noqa: BLE001
        rep.sources_failed.append(f"local: {e}")

    if use_offline_oeis:
        from discovery import oeis_offline
        try:
            snap = oeis_offline.load(oeis_dir) if oeis_dir else oeis_offline.load_default()
            if snap is None:
                rep.sources_failed.append("oeis_offline: no snapshot in data/oeis/raw")
            else:
                rep.matches += snap.search(terms)
                rep.sources_checked.append(f"oeis_offline@{snap.label}")
        except Exception as e:  # noqa: BLE001
            rep.sources_failed.append(f"oeis_offline: {type(e).__name__}: {e}")

    if use_network:
        try:
            rep.matches += check_oeis(terms)
            rep.sources_checked.append("oeis")
        except Exception as e:  # noqa: BLE001
            rep.sources_failed.append(f"oeis: {type(e).__name__}: {e}")

    if any(m.get("transform", "identity") == "identity" for m in rep.matches):
        rep.status = MATCH_FOUND
    elif rep.matches:
        rep.status = PARTIAL_MATCH
    elif any(s != "local" for s in rep.sources_checked):
        rep.status = NO_MATCH_IN_SCOPE   # a real snapshot/search found nothing: still not "new"
    else:
        # Only the hand-made local table answered. It can confirm "known", never "not found".
        rep.status = SOURCE_UNAVAILABLE
    return rep
