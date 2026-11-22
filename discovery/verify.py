"""Verification layer.

A conjecture is checked by two independently written implementations of the
same predicate. A counterexample counts only if both agree on it; any
disagreement makes the whole result INCONCLUSIVE (the system itself is wrong).
Passing a finite search is evidence, never a proof.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable

REFUTED = "REFUTED"
SUPPORTED_KNOWN = "SUPPORTED_KNOWN"
SUPPORTED_NOVELTY_UNCHECKED = "SUPPORTED_NOVELTY_UNCHECKED"
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


@dataclass
class Verdict:
    conjecture_id: str
    status: str
    checked: int = 0
    counterexample: int | None = None
    disagreements: list[int] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "status": self.status,
            "checked": self.checked,
            "counterexample": self.counterexample,
            "disagreements": self.disagreements,
        }


def check(conj: Conjecture, stop_at_first_counterexample: bool = True) -> Verdict:
    checked = 0
    disagreements: list[int] = []
    counterexample: int | None = None
    for n in conj.domain():
        a = conj.holds_a(n)
        b = conj.holds_b(n)
        checked += 1
        if a != b:
            disagreements.append(n)
            if len(disagreements) >= 5:
                break
            continue
        if not a and counterexample is None:
            counterexample = n
            if stop_at_first_counterexample:
                break
    if disagreements:
        return Verdict(conj.id, INCONCLUSIVE, checked, counterexample, disagreements)
    if counterexample is not None:
        return Verdict(conj.id, REFUTED, checked, counterexample)
    return Verdict(conj.id, SUPPORTED_IN_RANGE, checked)
