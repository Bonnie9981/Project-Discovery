"""R-002 implementation C — string rewriting with Floyd cycle detection.

Method: the state is a str of '0'/'1'. The ring is padded with one wrapped
cell on each side and every next cell is read from a 3-character window
through a dict built from the rule's binary expansion. Cycle detection is
Floyd's tortoise-and-hare (no visited-state table and no Brent power steps),
so it shares no algorithm with implementations A or B.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations


def table(rule: int) -> dict[str, str]:
    bits = format(rule, "08b")            # bits[0] is pattern 111, bits[7] is 000
    return {format(7 - k, "03b"): bits[k] for k in range(8)}


def next_state(s: str, t: dict[str, str]) -> str:
    p = s[-1] + s + s[0]
    return "".join(t[p[i:i + 3]] for i in range(len(s)))


def orbit(rule: int, width: int, init: str, max_steps: int) -> tuple[int, int] | None:
    t = table(rule)
    f = lambda s: next_state(s, t)   # noqa: E731
    slow, fast = f(init), f(f(init))
    n = 1
    while slow != fast:
        slow, fast = f(slow), f(f(fast))
        n += 1
        if n > max_steps:
            return None
    mu, slow = 0, init
    while slow != fast:
        slow, fast = f(slow), f(fast)
        mu += 1
    lam, fast = 1, f(slow)
    while slow != fast:
        fast = f(fast)
        lam += 1
    if mu + lam > max_steps:
        return None
    return mu, lam


def single_seed(width: int) -> str:
    return "1" + "0" * (width - 1)
