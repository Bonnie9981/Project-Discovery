"""R-002 (DISC-0005): elementary CA orbit sizes, small ranges so CI stays fast."""
from research.r002 import candidates, engine, impl_a, impl_b, impl_c


def test_three_implementations_agree_all_rules():
    assert engine.agreement(8) == []


def test_symmetries_hold():
    assert engine.symmetry_failures(engine.scan(10), w_sym=10) == []


def test_known_values():
    # rule 90, width 5: period 3 (Martin-Odlyzko-Wolfram); rule 30 width 17: (56, 10846)
    assert impl_b.orbit(90, 5, 1, 1 << 10)[1] == 3
    assert impl_b.orbit(30, 17, 1, 1 << 20) == (56, 10846)
    assert impl_c.orbit(30, 11, impl_c.single_seed(11), 1 << 20) == impl_a.orbit(30, 11, impl_a.single_seed(11), 1 << 20)


def test_candidates_small():
    res = {c["id"]: c for c in candidates.check_all(18)}
    assert all(c["holds"] for c in res.values()), [c for c in res.values() if not c["holds"]]


def test_wrong_formula_is_refuted():
    old = candidates.CANDIDATES["R2-C09"]
    candidates.CANDIDATES["R2-C09"] = (94, "T", lambda w: 2 * ((w + 1) // 4), 3, "old misreading", "T-94")
    try:
        res = {c["id"]: c for c in candidates.check_all(10)}
        assert res["R2-C09"]["status"] == "REFUTED" and res["R2-C09"]["counterexample"]["w"] == 7
    finally:
        candidates.CANDIDATES["R2-C09"] = old


def test_damage_classes():
    d = engine.damage(width=32, steps=32, trials=4)
    assert d[0] == 0 and d[204] > 0 and d[30] > 0.2   # rule 0 kills, identity keeps one flip, 30 spreads
