"""DISC-0004 batch engine (small ranges so CI stays fast)."""
from research.r001.batch import candidates, engine, impl_a, impl_b, impl_c
from research.r001.batch.library import FUNCS


def test_all_base_functions_agree_a_b():
    for f in FUNCS:
        assert impl_a.table(f, 600) == impl_b.table(f, 600), f


def test_impl_c_agrees_with_a():
    c = impl_c.C(3000)
    for f in ("sigma", "sigma_odd", "usigma", "phi", "psi", "rad", "core", "d", "J2"):
        a = impl_a.table(f, 3000)
        assert all(getattr(c, f)(n) == a[n] for n in range(1, 3001)), f


def test_engine_small_run_without_snapshot():
    r = engine.run(400, snap=None)
    assert r["base_mismatch"] == [] and not r["dropped"]["disagree"]
    kinds = {L.kind for L in r["leads"]}
    assert "equality_set" in kinds
    # Liouville(g(n)) is multiplicative by construction: must not be reported as a lead
    assert not any(L.id.startswith("M-liouville(") for L in r["leads"])


def test_candidate_c10_is_refuted_beyond_1e4():
    res = {c["id"]: c for c in candidates.check_all(12_000)}
    assert res["C10"]["holds"] is False and res["C10"]["counterexample"] == 10711
    assert all(res[k]["holds"] for k in ("C01", "C02", "C03", "C05", "C06", "C07", "C08", "C09", "C11", "C12"))
