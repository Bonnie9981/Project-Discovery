"""DISC-0012 critic: third, self-contained check (no repo imports).

Method: numpy uint8 arrays on the full (unfolded) ring, one step =
``x ^ (roll(x, 1) | roll(x, -1))``.  No cycle detection: the claimed
transient/period are tested directly by comparing whole states
(x_{w-4+4} != x_{w-4}, x_{w-3+4} == x_{w-3}, x_{w-3+p} != x_{w-3}, p=1..3).
For w <= 401 an independent brute-force first-repeat search (bytes hashing)
is also run.  The phase-wall description G is re-coded from the text of
records/DISC-0012/hypotheses.md (not from Lean or l05) and compared cell by
cell for every t in [0, w + 12].

Extra attacks (all printed):
  * the "wrong" centre defect t = 2 (mod 4) must fail for some w;
  * w = 5 and w = 9, 13 (outside / at the edge of the Lean general argument);
  * relaxed cone_seg (t + 3 <= m) as a pure statement about Cf, for every
    width 3..W (even and odd), and whether t + 2 <= m would also hold.

Run: python research/r003/critic_c_mod1.py [W]   (default 1201)
"""
from __future__ import annotations

import sys

import numpy as np


def ether(t, d):
    """E(t, d): t even -> d = t (mod 4); t odd -> d != t + 1 (mod 4).  Vectorised in d."""
    if t % 2 == 0:
        return (d % 4) == (t % 4)
    return (d % 4) != ((t + 1) % 4)


def g_state(w, t, d, centre_rule="m"):
    m = w // 2
    front = (d + t) < w
    if centre_rule == "m":
        cdef = (d == m) & (t % 4 == m % 4)
    else:
        cdef = (d == m) & (t % 4 == 2)
    defect = ((d == 0) & (t % 4 == 2)) | cdef
    behind = ether(t + 1, d + 3) ^ defect
    return np.where(front, ether(t, d), behind).astype(np.uint8)


def step(x):
    return x ^ (np.roll(x, 1) | np.roll(x, -1))


def check_width(w, centre_rule="m"):
    m = w // 2
    i = np.arange(w)
    d = np.minimum(i, w - i)
    x = np.zeros(w, dtype=np.uint8)
    x[0] = 1
    hist = []
    bad = []
    for t in range(0, w + 13):
        hist.append(x.copy())
        if t <= m - 2:
            want = ((d <= t) & ether(t, d)).astype(np.uint8)
            if not np.array_equal(x, want):
                bad.append(("H1", t))
        if t >= m - 2:
            if not np.array_equal(x, g_state(w, t, d, centre_rule)):
                bad.append(("H2", t))
        x = step(x)
    T = w - 3
    if np.array_equal(hist[T - 1 + 4], hist[T - 1]):
        bad.append(("not-minimal", T - 1))
    if not np.array_equal(hist[T + 4], hist[T]):
        bad.append(("no-period", T))
    for p in (1, 2, 3):
        if np.array_equal(hist[T + p], hist[T]):
            bad.append(("period-divides", p))
    return bad


def brute(w):
    x = np.zeros(w, dtype=np.uint8)
    x[0] = 1
    seen = {}
    t = 0
    while x.tobytes() not in seen:
        seen[x.tobytes()] = t
        x = step(x)
        t += 1
    mu = seen[x.tobytes()]
    return mu, t - mu


# ---- cone_seg as a statement about Cf (independent of any simulation) ----
def E1(t, d):
    return (d % 4 == t % 4) if t % 2 == 0 else (d % 4 != (t + 1) % 4)


def Cf(t, d):
    return d <= t and E1(t, d)


def lo(d):
    return 1 if d == 0 else d - 1


def up(w, d):
    if d == w // 2:
        return d - 1 if w % 2 == 0 else d
    return d + 1


def cone_seg_holds(w, slack):
    """Does Cf(t+1,d) = Cf(t,d) xor (Cf(t,lo d) or Cf(t,up d)) for all t+slack <= m, d <= m?"""
    m = w // 2
    fails = []
    for t in range(0, max(0, m - slack + 1)):
        for d in range(m + 1):
            if Cf(t + 1, d) != (Cf(t, d) ^ (Cf(t, lo(d)) or Cf(t, up(w, d)))):
                fails.append((t, d))
    return fails


def main(W):
    widths = [w for w in range(9, W + 1) if w % 4 == 1]
    bad = {w: b for w in widths if (b := check_width(w))}
    print(f"main: {len(widths)} widths 9..{W}, failures: {len(bad)}", list(bad.items())[:3])
    br = {w: brute(w) for w in widths if w <= 401}
    wrong = {w: v for w, v in br.items() if v != (w - 3, 4)}
    print(f"brute first-repeat w<=401: {len(br)} widths, mismatches: {wrong}")
    alt = [w for w in widths if w <= 101 and check_width(w, "2")]
    print("centre-defect t=2 (mod 4) variant fails at w =", alt[:6])
    print("w=5 brute:", brute(5), " w=9:", check_width(9) or "ok", " w=13:", check_width(13) or "ok")
    f3 = [w for w in range(3, 601) if cone_seg_holds(w, 3)]
    f2 = {w: cone_seg_holds(w, 2)[:2] for w in range(3, 61) if cone_seg_holds(w, 2)}
    print("cone_seg with t+3<=m: widths 3..600 failing:", f3)
    print("cone_seg with t+2<=m would fail at (first few):", list(f2.items())[:4])
    return 1 if (bad or wrong or f3) else 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 1201))
