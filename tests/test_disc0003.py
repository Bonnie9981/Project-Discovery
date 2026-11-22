"""DISC-0003: the two implementations agree with each other and with hand-checked values."""
from research.r001.disc0003 import impl_a as A
from research.r001.disc0003 import impl_b as B


def test_hand_values():
    # 9 = 9 = 4+5 = 2+3+4 ; 15 = 15 = 7+8 = 4+5+6 = 1+2+3+4+5 ; 16 is a power of two
    t = A.rep_table(20)
    assert (t[9], t[15], t[16]) == (3, 4, 1)
    assert [B.rep_count(n) for n in (9, 15, 16)] == [3, 4, 1]
    assert B.rep_count(4, 2) == 2  # 4 = 4 = 1+3 : the H6 counterexample


def test_impls_agree_small():
    for D in (1, 2, 3, 7):
        t = A.rep_table(500, D)
        assert all(t[n] == B.rep_count(n, D) for n in range(1, 501))
    assert all(A.odd_divisor_count(n) == B.odd_divisor_count(n) for n in range(1, 2001))
    assert all(A.divisor_count(n) == B.divisor_count(n) for n in range(1, 2001))
    assert all(A.is_power_of_two(n) == B.is_power_of_two(n) for n in range(1, 2001))
    assert A.domain(50) == B.domain(50)


def test_run_small():
    from research.r001.disc0003 import run
    out = run.main(500)
    st = {r["id"]: r["status"] for r in out["results"]}
    assert st["H6"] == "REFUTED"
    assert all(st[h] == "SUPPORTED_IN_RANGE" for h in ("H1", "H2a", "H2b", "H3", "H4", "H5", "H7"))
    assert all(e["impl_agree"] for e in out["extensions"].values())
