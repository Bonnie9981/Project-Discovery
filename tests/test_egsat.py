"""DISC-0022：Erdős–Gyárfás 小範圍 SAT 重現的自我測試。"""
import pytest

pytest.importorskip("pysat")
nx = pytest.importorskip("networkx")

from pysat.solvers import Cadical195
from discovery.egsat import check, search
from discovery.egsat.encode import Enc, find_cycle


def test_symmetry_breaking_keeps_every_class():
    from networkx.generators.atlas import graph_atlas_g
    for n in (5, 6, 7):
        enc = Enc(n)
        s = Cadical195(bootstrap_with=list(enc.deg()) + list(enc.minimal()) + list(enc.lex()))
        found = []
        while s.solve():
            m = {l for l in s.get_model() if l > 0}
            G = nx.Graph(); G.add_nodes_from(range(n))
            G.add_edges_from(p for p, v in enc.idx.items() if v in m)
            found.append(G)
            s.add_clause([-v if v in m else v for v in enc.idx.values()])
        for G in graph_atlas_g():
            if G.number_of_nodes() != n or min(dict(G.degree()).values(), default=0) < 3:
                continue
            if all(G.degree(a) == 3 or G.degree(b) == 3 for a, b in G.edges()):
                assert any(nx.is_isomorphic(G, H) for H in found)


def test_c4_free_min_degree_3_exists_at_10(monkeypatch):
    monkeypatch.setattr(search, "FORBID", ())
    assert search.search(9, verbose=False)["status"] == "UNSAT"
    r = search.search(10, verbose=False)
    assert r["status"] == "SAT"
    G = nx.Graph(r["edges"])
    assert min(d for _, d in G.degree()) >= 3
    assert find_cycle([set(G[v]) for v in range(10)], 4) is None


def test_find_cycle_matches_networkx():
    G = nx.petersen_graph()
    adj = [set(G[v]) for v in range(10)]
    lens = {len(c) for c in nx.simple_cycles(G, length_bound=10)}
    for L in range(3, 11):
        assert (find_cycle(adj, L) is not None) == (L in lens)


def test_certificate_checks_and_rejects_tampering(tmp_path):
    d = str(tmp_path)
    assert search.search(11, d, verbose=False)["status"] == "UNSAT"
    assert check.check_unsat(d, 11)
    good = (tmp_path / "eg11.drat").read_text()
    (tmp_path / "eg11.drat").write_text("0\n")
    with pytest.raises(SystemExit):
        check.check_unsat(d, 11)
    (tmp_path / "eg11.drat").write_text(good)
    cnf = (tmp_path / "eg11.cnf").read_text().splitlines()
    head = cnf[0].split()
    head[3] = str(int(head[3]) + 1)
    fake = [" ".join(head)] + cnf[1:] + ["-1 -11 -2 0"]  # 不是圈的子句
    (tmp_path / "eg11.cnf").write_text("\n".join(fake) + "\n")
    with pytest.raises(SystemExit):
        check.check_unsat(d, 11)
