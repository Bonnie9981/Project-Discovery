"""R3-L01 (DISC-0008): numerical checks for the rule-26 odd-ring period proof.

python results/A334504/code/l01_check.py [W_MAX]      (default W_MAX = 61)

Checks, for every odd 3 <= w <= W_MAX, two independent ways:

  Way 1 (impl_b): simulate with research/r002/impl_b.py (bit-parallel word),
         compare every state x_t, 0 <= t <= P + 2w, with the closed form
             x_t(i) = 1  iff  s = (i + t) mod w is even and C(t, s/2) is odd     (Lemma 1)
         and compare impl_b's Brent (transient, period) with (0, w * 2^floor(log2 w)).
  Way 2 (own list simulation, rule table read off the Wolfram code, no import from
         the repo): first-return time of the seed, and the set
             {t <= 3P : x_t = x_0}  ==  {t <= 3P : w | t and 2^k | t}           (Theorem)
  Lemma 2 (Pascal mod 2, via math.comb, independent of the CA):
         2^m | t  =>  C(t, j) even for 0 < j < 2^m;
         t > 0    =>  C(t, 2^{v_2(t)}) odd.                     (t <= 2000, m <= 11)
  Lemma 3 (local step in s-coordinates): exhaustive over s' in [0, w) and t <= 64.
Also prints, for even w, that P26(w) equals the rule-90 period (orbit never shows '11').
Standard library only.
"""
from __future__ import annotations

import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from research.r002 import impl_b  # noqa: E402


def closed_form(w: int, t: int) -> int:
    word = 0
    for i in range(w):
        s = (i + t) % w
        if s % 2 == 0 and comb(t, s // 2) % 2 == 1:
            word |= 1 << i
    return word


def period_formula(w: int) -> int:
    return w * 2 ** (w.bit_length() - 1)


# ---- Way 2: independent list simulation -------------------------------------------
def step_list(cells: list[int], rule: int) -> list[int]:
    w = len(cells)
    return [(rule >> (4 * cells[i - 1] + 2 * cells[i] + cells[(i + 1) % w])) & 1
            for i in range(w)]


def way2(w: int) -> None:
    P = period_formula(w)
    k = w.bit_length() - 1
    seed = [1] + [0] * (w - 1)
    cells = seed
    hits = []
    for t in range(1, 3 * P + 1):
        cells = step_list(cells, 26)
        if cells == seed:
            hits.append(t)
    expect = [t for t in range(1, 3 * P + 1) if t % w == 0 and t % (2 ** k) == 0]
    assert hits == expect, (w, hits[:5], expect[:5])
    assert hits[0] == P


def way1(w: int) -> None:
    P = period_formula(w)
    mask = (1 << w) - 1
    x = impl_b.single_seed(w)
    for t in range(P + 2 * w + 1):
        assert x == closed_form(w, t), (w, t)
        x = impl_b._step(x, 26, w, mask)
    assert impl_b.orbit(26, w, 1, 10 * P) == (0, P), w


def lemma2() -> None:
    for t in range(1, 2001):
        for m in range(12):
            if t % (2 ** m) == 0:
                assert all(comb(t, j) % 2 == 0 for j in range(1, 2 ** m))
        v = (t & -t).bit_length() - 1
        assert comb(t, 2 ** v) % 2 == 1


def lemma3(w: int) -> None:
    """X_{t+1}(s') = rule26(X_t(s'-2), X_t(s'-1), X_t(s')) with indices mod w."""
    X = lambda t, s: int(s % 2 == 0 and comb(t, s // 2) % 2 == 1)  # noqa: E731
    for t in range(65):
        for sp in range(w):
            l, c, r = X(t, (sp - 2) % w), X(t, (sp - 1) % w), X(t, sp)
            assert X(t + 1, sp) == (26 >> (4 * l + 2 * c + r)) & 1, (w, t, sp)


def even_widths(w_max: int) -> None:
    for w in range(2, w_max + 1, 2):
        mask = (1 << w) - 1
        x, seen = 1, set()
        for _ in range(4 * w * w):
            assert x & ((x << 1) | (x >> (w - 1))) & mask == 0  # no adjacent 11
            x = impl_b._step(x, 26, w, mask)
        assert impl_b.orbit(26, w, 1, 10 ** 6) == impl_b.orbit(90, w, 1, 10 ** 6), w


def main(w_max: int = 61) -> None:
    lemma2()
    for w in range(3, w_max + 1, 2):
        way1(w)
        way2(w)
        lemma3(w)
    even_widths(min(w_max, 40))
    print(f"OK: odd 3 <= w <= {w_max}: closed form (impl_b), period w*2^floor(log2 w) "
          f"(impl_b Brent + own list sim, return set = multiples of P up to 3P); "
          f"Lemma 2 (t <= 2000); Lemma 3; even 2 <= w <= {min(w_max, 40)}: orbit = rule 90 orbit")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 61)
