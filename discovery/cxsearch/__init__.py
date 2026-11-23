"""Counterexample searcher for OEIS conjectures (internal module, not released).

Pipeline: entry.py (parse, align with DATA/b-file, flag comments that may
already settle the question) -> catalog.py (psp2 / Carmichael lists with
published-count checks) -> conjectures.py (one predicate per conjecture) ->
independent re-check of every failure -> DISC record + Lean certificate.
See docs/CXSEARCH.md.
"""
