"""R-002 implementation A — elementary cellular automata on a ring, cell by cell.

Method: the state is a Python list of 0/1. Each step builds the next list by
reading (left, centre, right) for every cell, with wrap-around, and looking up
bit (4*l + 2*c + r) of the Wolfram rule number. Cycle detection stores every
visited state (as a tuple) with the step it was first seen.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations


def step(state: list[int], rule: int) -> list[int]:
    w = len(state)
    return [(rule >> (4 * state[(i - 1) % w] + 2 * state[i] + state[(i + 1) % w])) & 1 for i in range(w)]


def orbit(rule: int, width: int, init: list[int], max_steps: int) -> tuple[int, int] | None:
    """(transient, period) of the orbit from init, or None if no repeat within max_steps."""
    seen = {}
    s = list(init)
    for t in range(max_steps + 1):
        key = tuple(s)
        if key in seen:
            return seen[key], t - seen[key]
        seen[key] = t
        s = step(s, rule)
    return None


def single_seed(width: int) -> list[int]:
    s = [0] * width
    s[0] = 1
    return s
