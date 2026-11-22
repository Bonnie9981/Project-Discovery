from discovery import novelty, verify
from research.r001 import pipeline


def test_r001_finds_eulers_lucky_numbers_and_marks_them_known():
    res = pipeline.run(p_max=500, use_network=False)
    agg = res["aggregate"]
    assert agg["sequence"] == [2, 3, 5, 11, 17, 41]
    assert agg["status"] == verify.SUPPORTED_KNOWN
    assert agg["novelty"]["matches"][0]["id"] == "A014556"


def test_unknown_sequence_without_network_is_unchecked_not_new():
    rep = novelty.check_sequence([7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5], use_network=False)
    assert rep.known is None  # must never be reported as "new" without a real search
