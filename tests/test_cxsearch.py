"""Counterexample searcher (discovery/cxsearch): catalog, alignment, self-tests."""
from discovery.cxsearch import catalog, conjectures, entry, numth

CAT = catalog.DATA / "psp2_1e10.txt.gz"


def test_numth_basics():
    assert numth.factor(3048841) == {61: 1, 151: 1, 331: 1}
    assert numth.is_prime(2**61 - 1) and not numth.is_prime(3215031751)
    assert numth.mult_order(2, 31) == 5
    assert numth.is_carmichael(561) and not numth.is_carmichael(341)


def test_python_reference_matches_catalog_prefix():
    psp = catalog.load(CAT)
    assert catalog.python_psp2(10**5) == [n for n in psp if n < 10**5]


def test_catalog_counts_and_members():
    psp = catalog.load(CAT)
    assert catalog.check(psp, 10**10) == {
        "limit": 10**10, "psp2": 14884, "carmichael": 1547,
        "counts_checked": [3, 4, 5, 6, 7, 8, 9, 10]}


def test_a215944_definition_matches_bfile():
    # (count, sum) of b-file terms below 10^k, read 2026-11-23 (DISC-0019-S003)
    want = {7: (65, 220926779), 8: (155, 4301817421), 9: (370, 99483523854),
            10: (798, 1994907788036)}
    members = [n for n in catalog.load(CAT) if conjectures.in_a215944(n)]
    for k, (c, s) in want.items():
        below = [n for n in members if n < 10**k]
        assert (len(below), sum(below)) == (c, s)


def test_a215944_counterexample():
    r = conjectures.scan("A215944", catalog.load(CAT), 10**10, keep=1)
    assert r["failures"] == 211 and r["first"][0]["n"] == 3048841
    assert numth.is_psp(3048841) and numth.is_psp(151 * 331)


def test_self_test_rediscovers_known_counterexample():
    # A218010: Greathouse 2014 reported 3380740301; the pipeline must find it.
    carm = catalog.carmichael(catalog.load(CAT))
    r = conjectures.scan("A218010", carm, 10**10)
    assert [f["n"] for f in r["first"]] == [3380740301]


def test_no_failures_where_proved_or_open():
    psp = catalog.load(CAT)
    for key in ("A218483#1", "A321790"):
        assert conjectures.scan(key, psp, 10**10)["failures"] == 0
    assert conjectures.scan("A058128", range(1, 400), 400)["failures"] == 0


def test_entry_parse_and_align():
    text = ("%I A000027 #1\n%S A000027 1,2,3,4,5,\n%T A000027 6,7\n%N A000027 The positive integers.\n"
            "%C A000027 Conjecture: never 0. This is true.\n%O A000027 1,2\n")
    e = entry.parse(text)
    assert e.offset == 1 and e.terms == [1, 2, 3, 4, 5, 6, 7]
    assert entry.align(lambda n: n, e) is None
    assert entry.align(lambda n: n - 1, e) == (1, 1, 0)
    assert e.settled_hints()


def test_saved_entries_align():
    psp = catalog.load(CAT)

    def a321790(i):
        k, b = psp[i - 1], 3
        while pow(b, k - 1, k) == 1:
            b += 1
        return b
    assert entry.align(a321790, entry.load("A321790")) is None
    assert entry.align(lambda n: 1 if n == 1 else (n**n - n) // (n - 1) ** 2, entry.load("A058128")) is None
    assert any("All three conjectures are true" in c for c in entry.load("A218483").settled_hints())


def test_a362070_aligns_and_counterexample():
    from discovery.cxsearch.conjectures import a362070_value, REGISTRY
    assert entry.align(a362070_value, entry.load("A362070")) is None
    assert a362070_value(1715) == a362070_value(1716) == 91
    c = REGISTRY["A362070"]
    assert [n for n in range(1700, 1730) if c.test(n)] == [1715]
