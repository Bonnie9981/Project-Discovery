"""DISC-0027: new-sequence generator, transfer-matrix counter and the path/cycle check script."""
import importlib.util
from pathlib import Path

from discovery.newseq import graphsets as G, transfer as T

ROOT = Path(__file__).resolve().parent.parent


def _check_paths():
    p = ROOT / "results/locating-dominating-path/code/check_paths.py"
    spec = importlib.util.spec_from_file_location("check_paths", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_bruteforce_matches_transfer():
    for fam, W, ns in (("path", 5, range(1, 11)), ("cycle", 5, range(10, 13))):
        for prop in ("dominating", "identifying_code", "locating_dominating", "open_locating"):
            for n in ns:
                g = G.FAMILIES[fam](n)
                S, P = G.properties(g)
                pc = G.popcount(S)
                ok = P[prop]
                cnt = int(ok.sum())
                exp = (cnt, int(pc[ok].min()), int((pc[ok] == pc[ok].min()).sum())) if cnt else (0, 0, 0)
                assert T.stats(g, prop, W) == exp, (fam, prop, n)


def test_known_counts():
    # dominating sets of P_n: A000213-shifted 1, 3, 5, 9, 17, 31, 57
    assert [T.stats(G.path(n), "dominating", 5)[0] for n in range(1, 8)] == [1, 3, 5, 9, 17, 31, 57]


def test_berlekamp_massey_fibonacci():
    assert [int(c) for c in T.berlekamp_massey([1, 1, 2, 3, 5, 8, 13, 21])] == [1, 1]


def test_check_paths_small():
    m = _check_paths()
    from itertools import product
    for n in range(1, 11):
        words = list(product((0, 1), repeat=n))
        assert m.brute(m.path, m.is_ld, n) == sum(map(m.ld_word_path, words)) == m.LD_PATH[n - 1]
        assert m.brute(m.path, m.is_id, n) == sum(map(m.id_word_path, words)) == m.ID_PATH[n - 1]
        if n >= 3:
            assert (m.brute(m.cycle, m.is_ld, n) == m.A001642[n - 1]) == (n != 4)
