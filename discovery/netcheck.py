"""Record which literature sources this machine's code can reach.

    python -m discovery.netcheck            # prints JSON, exit 0 even if all fail

A failure is a result, not an error: it is written down so nobody assumes a
source was searched when it was not (status SOURCE_UNAVAILABLE).
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone

SOURCES = {
    "oeis": "https://oeis.org/search?q=id:A000045&fmt=json",
    "openalex": "https://api.openalex.org/works?search=consecutive%20integers&per-page=1",
    "arxiv": "https://export.arxiv.org/api/query?search_query=all:integer%20sequence&max_results=1",
    "crossref": "https://api.crossref.org/works?query=sum%20of%20consecutive%20integers&rows=1",
}


def probe(url: str, timeout: float = 10.0) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "project-discovery-netcheck"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"ok": True, "http": r.status}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}"[:200]}


def main() -> int:
    out = {"checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "results": {k: probe(u) for k, u in SOURCES.items()}}
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
