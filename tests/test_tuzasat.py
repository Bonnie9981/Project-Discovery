"""Tuza 猜想小範圍 SAT 驗證（discovery/tuzasat）的自我測試。"""
import json, itertools
import pytest

pytest.importorskip("pysat")
nx = pytest.importorskip("networkx")

from pysat.solvers import Cadical195
from discovery.tuzasat import check, search


def test_symmetry_breaking_keeps_every_class():
    """基本子句（含 LEX）的解，涵蓋每一個『每條邊都在三角形裡』的圖的同構類。"""
    from networkx.generators.atlas import graph_atlas_g
    for n in (4, 5, 6):
        enc = search.Enc(n)
        s = Cadical195(bootstrap_with=enc.base())
        found = []
        while s.solve():
            m = {l for l in s.get_model() if l > 0}
            G = nx.Graph(); G.add_nodes_from(range(n))
            G.add_edges_from(e for e, v in enc.x.items() if v in m)
            found.append(G)
            s.add_clause([-v if v in m else v for v in enc.x.values()])
        for G in graph_atlas_g():
            if G.number_of_nodes() != n:
                continue
            if all(any(c in G[a] and c in G[b] for c in G) for a, b in G.edges()):
                assert any(nx.is_isomorphic(G, H) for H in found)


def test_relaxed_bound_finds_tight_example():
    """把條件放寬成 τ > 2k−1，應該找到 K4 這種 τ = 2ν 的緊例。"""
    res = search.search(5, 1, cover_bound=1, verbose=False)
    assert res["status"] == "SAT"
    nu, tau = check.nu_tau(5, res["edges"])
    assert (nu, tau) == (1, 2)


def test_small_n_unsat_and_certificates(tmp_path):
    for n in (5, 6, 7):
        for k in range(1, search.kmax(n) + 1):
            assert search.search(n, k, str(tmp_path), verbose=False)["status"] == "UNSAT"
            assert check.check_unsat(str(tmp_path), n, k)


def test_checker_rejects_bad_witness(tmp_path):
    n, k = 7, 2
    search.search(n, k, str(tmp_path), verbose=False)
    p = tmp_path / f"tuza_{n}_{k}.json"
    res = json.loads(p.read_text())
    i = next(i for i, b in enumerate(res["blocks"]) if "C" in b)
    res["blocks"][i]["C"] = res["blocks"][i]["C"][:-1]  # 拿掉一條覆蓋邊，子句就對不上
    p.write_text(json.dumps(res))
    with pytest.raises(AssertionError):
        check.check_unsat(str(tmp_path), n, k)


def test_bruteforce_atlas():
    """第二個實作：所有 ≤ 7 點的圖暴力算 ν、τ，確認 τ ≤ 2ν。"""
    from networkx.generators.atlas import graph_atlas_g
    for G in graph_atlas_g():
        n = G.number_of_nodes()
        if n < 3:
            continue
        nu, tau = check.nu_tau(n, list(G.edges()))
        assert tau <= 2 * nu
