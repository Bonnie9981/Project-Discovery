"""Verification layer.

A conjecture is checked by two (optionally three) independently written
implementations of the same predicate. A counterexample counts only if all
implementations agree on it; any disagreement makes the whole result
INCONCLUSIVE (the system itself is wrong). Passing a finite search is
evidence, never a proof.

Independence (docs/RESEARCH_STANDARDS.md section 2b): implementations must use
different algorithms and must not share core helper functions. When
``domain_b`` is given the search domain is generated twice, independently, and
any difference between the two is also INCONCLUSIVE. ``discovery.independence``
checks the import rule statically.

Every check runs under a budget (``discovery.limits``): hitting it gives
INCONCLUSIVE with ``stopped_reason`` set, never a silent partial "supported".
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Iterable

from discovery.limits import Budget

REFUTED = "REFUTED"
SUPPORTED_KNOWN = "SUPPORTED_KNOWN"
SUPPORTED_NOVELTY_UNCHECKED = "SUPPORTED_NOVELTY_UNCHECKED"
# Only after human novelty review (novelty status NOVELTY_SUPPORTED or PENDING_REVIEW); never set by code.
SUPPORTED_POSSIBLY_NEW = "SUPPORTED_POSSIBLY_NEW"
INCONCLUSIVE = "INCONCLUSIVE"
# Internal status before the novelty check runs.
SUPPORTED_IN_RANGE = "SUPPORTED_IN_RANGE"


@dataclass
class Conjecture:
    """'For every n in domain, holds(n)' — stated precisely, with its search domain."""
    id: str
    statement: str
    domain: Callable[[], Iterable[int]]
    domain_desc: str
    holds_a: Callable[[int], bool]   # implementation A
    holds_b: Callable[[int], bool]   # implementation B, written independently
    holds_c: Callable[[int], bool] | None = None          # optional third (e.g. the Critic's)
    domain_b: Callable[[], Iterable[int]] | None = None   # domain generated independently


@dataclass
class Verdict:
    conjecture_id: str
    status: str
    checked: int = 0
    counterexample: int | None = None
    disagreements: list[int] = field(default_factory=list)
    implementations: int = 2
    domain_independent: bool = False
    stopped_reason: str | None = None
    # How strong the counterexample claim is (2026-11-27 red-team review):
    #   LEAST_IN_TESTED_ORDER - the domain was strictly increasing up to the
    #       counterexample, so no smaller n in that domain fails. It is the least
    #       counterexample overall only if the domain covers every candidate n.
    #   FOUND - a counterexample, with no claim that it is the least.
    counterexample_scope: str | None = None

    def as_dict(self) -> dict:
        return {
            "status": self.status,
            "checked": self.checked,
            "counterexample": self.counterexample,
            "disagreements": self.disagreements,
            "implementations": self.implementations,
            "domain_independent": self.domain_independent,
            "stopped_reason": self.stopped_reason,
            "counterexample_scope": self.counterexample_scope,
        }


def check(conj: Conjecture, stop_at_first_counterexample: bool = True,
          budget: Budget | None = None) -> Verdict:
    budget = budget or Budget.default()
    impls = [conj.holds_a, conj.holds_b] + ([conj.holds_c] if conj.holds_c else [])
    t0 = time.monotonic()

    def verdict(status, **kw) -> Verdict:
        return Verdict(conj.id, status, implementations=len(impls),
                       domain_independent=conj.domain_b is not None, **kw)

    if conj.domain_b is not None:
        da = budget.take(conj.domain(), "domain A")
        db = budget.take(conj.domain_b(), "domain B")
        if isinstance(da, str) or isinstance(db, str):
            return verdict(INCONCLUSIVE, stopped_reason=da if isinstance(da, str) else db)
        if da != db:
            diff = sorted(set(da) ^ set(db))[:5]
            return verdict(INCONCLUSIVE, disagreements=diff, stopped_reason="domains differ")
        domain: Iterable[int] = da
    else:
        domain = conj.domain()

    checked = 0
    disagreements: list[int] = []
    counterexample: int | None = None
    # A least-counterexample claim needs the domain in strictly increasing order.
    # A range or list is checked up front; any other iterable only as far as it was
    # walked, so an early stop on it gives no least claim.
    if isinstance(domain, range):
        known_sorted = domain.step > 0
    elif isinstance(domain, (list, tuple)):
        known_sorted = all(x < y for x, y in zip(domain, domain[1:]))
    else:
        known_sorted = None
    ascending = True
    prev: int | None = None
    stopped_early = False
    for n in domain:
        if prev is not None and n <= prev:
            ascending = False
        prev = n
        if checked >= budget.max_iterations:
            return verdict(INCONCLUSIVE, checked=checked, stopped_reason=f"max_iterations={budget.max_iterations}")
        if time.monotonic() - t0 > budget.max_seconds:
            return verdict(INCONCLUSIVE, checked=checked, stopped_reason=f"max_seconds={budget.max_seconds}")
        answers = [f(n) for f in impls]
        checked += 1
        if len(set(answers)) > 1:
            disagreements.append(n)
            if len(disagreements) >= 5:
                break
            continue
        if not answers[0] and counterexample is None:
            counterexample = n
            if stop_at_first_counterexample:
                stopped_early = True
                break
    if disagreements:
        return verdict(INCONCLUSIVE, checked=checked, counterexample=counterexample, disagreements=disagreements)
    if counterexample is not None:
        least = known_sorted if known_sorted is not None else (ascending and not stopped_early)
        scope = "LEAST_IN_TESTED_ORDER" if least else "FOUND"
        return verdict(REFUTED, checked=checked, counterexample=counterexample,
                       counterexample_scope=scope)
    return verdict(SUPPORTED_IN_RANGE, checked=checked)
