"""R-002 implementation B — bit-parallel ring update on one integer.

Method: the state is an int whose bit i is cell i. Left and right neighbour
words are obtained by rotating the whole word; the next word is the OR, over
the 8 neighbourhood patterns whose output bit is 1, of the AND of the three
(possibly complemented) words. Cycle detection uses Brent's algorithm (no
table of visited states), so it shares no logic with implementation A.

Self-contained: standard library only (docs/RESEARCH_STANDARDS.md 2b).
"""
from __future__ import annotations


def _step(x: int, rule: int, w: int, mask: int) -> int:
    left = ((x << 1) | (x >> (w - 1))) & mask      # bit i holds cell i-1
    right = ((x >> 1) | ((x & 1) << (w - 1))) & mask  # bit i holds cell i+1
    out = 0
    for pat in range(8):
        if (rule >> pat) & 1:
            l = left if pat & 4 else ~left & mask
            c = x if pat & 2 else ~x & mask
            r = right if pat & 1 else ~right & mask
            out |= l & c & r
    return out


def orbit(rule: int, width: int, init_word: int, max_steps: int) -> tuple[int, int] | None:
    """Brent cycle detection: (transient, period), or None past max_steps."""
    mask = (1 << width) - 1
    f = lambda x: _step(x, rule, width, mask)   # noqa: E731
    power = lam = 1
    tortoise = init_word
    hare = f(init_word)
    steps = 1
    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1
        steps += 1
        if steps > 2 * max_steps:
            return None
    mu = 0
    tortoise = hare = init_word
    for _ in range(lam):
        hare = f(hare)
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
    if mu + lam > max_steps:
        return None
    return mu, lam


def single_seed(width: int) -> int:
    return 1


def evolve(rule: int, width: int, word: int, steps: int) -> int:
    """State after `steps` updates (used for damage spreading)."""
    mask = (1 << width) - 1
    for _ in range(steps):
        word = _step(word, rule, width, mask)
    return word
