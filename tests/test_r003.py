"""R-003 pilot (R3-A): arithmetic-formula matcher for ECA orbit sizes."""
from research.r002 import impl_b
from research.r002.engine import scan
from research.r003 import arith_match as am


def _load(rel):
    """Load a check script from results/<sequence>/code/ (folders are not Python packages)."""
    import importlib.util
    from pathlib import Path
    path = Path(__file__).resolve().parents[1] / rel
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def test_l02_even_ring_matches_null_rule90_and_a268754():
    # DISC-0009: A334504(2n+2) = A268754(n), transient one more on the ring.
    l02_check = _load("results/A334504/code/l02_check.py")
    l02_check.main(16)


def test_l04_rule54_mod23_small():
    # DISC-0011: rule 54, w ≡ 2, 3 (mod 4): transient T, period 4, folded cone + centre defect.
    l04_rule54_mod23 = _load("results/rule54-transient/code/l04_rule54_mod23.py")
    assert l04_rule54_mod23.main(60) == 0


def test_l05_rule54_mod1_small():
    # DISC-0012: rule 54, w ≡ 1 (mod 4): transient w - 3, period 4, cone + phase wall.
    l05_rule54_mod1 = _load("results/rule54-transient/code/l05_rule54_mod1.py")
    assert l05_rule54_mod1.main(60) == 0
