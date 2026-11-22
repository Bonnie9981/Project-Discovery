"""R-003 pilot (R3-A): arithmetic-formula matcher for ECA orbit sizes."""
from research.r002 import impl_b
from research.r002.engine import scan
from research.r003 import arith_match as am


def _orbit(rule, w):
    return impl_b.orbit(rule, w, impl_b.single_seed(w), 1 << 20)


def test_rule90_lead_found_and_survives():
    data = scan(am.W_FIT)
    leads = [l for l in am.search(data, rules=[90]) if l["quantity"] == "T"]
    assert leads and am.nontrivial(leads[0])
    assert am.recheck(leads[0], 26)["survives"]


def test_wrong_formula_is_rejected():
    lead = {"rule": 90, "quantity": "T", "modulus": 1, "pieces": {0: [(1, "n", "w", 0)]}}
    assert not am.recheck(lead, 26)["survives"]


def test_rule154_single_seed_orbit_equals_rule26():
    # 154 and 26 differ only on neighbourhood 111, which the single-seed orbit never shows.
    for w in range(2, 25):
        assert _orbit(154, w) == _orbit(26, w)
    assert _orbit(154, 1) != _orbit(26, 1)


def test_rule167_is_one_step_then_complemented_rule26():
    # One step of 167 from a single seed gives NOT(shifted seed); NOT F167(s) = F26(NOT s).
    assert all(_orbit(167, w) != (lambda o: (o[0] + 1, o[1]))(_orbit(26, w)) for w in (1, 2, 3))
    for w in range(4, 25):
        t167, p167 = _orbit(167, w)
        t26, p26 = _orbit(26, w)
        assert (t167, p167) == (t26 + 1, p26)
