from discovery import verify
from discovery.verify import Conjecture


def conj(a, b, hi=100):
    return Conjecture("t", "test", lambda: range(hi), "0..99", a, b)


def test_true_statement_is_only_supported_in_range():
    v = verify.check(conj(lambda n: n >= 0, lambda n: n >= 0))
    assert v.status == verify.SUPPORTED_IN_RANGE and v.checked == 100


def test_counterexample_found():
    v = verify.check(conj(lambda n: n < 42, lambda n: n < 42))
    assert v.status == verify.REFUTED and v.counterexample == 42


def test_disagreement_is_inconclusive_not_refuted():
    v = verify.check(conj(lambda n: True, lambda n: n != 7))
    assert v.status == verify.INCONCLUSIVE and v.disagreements == [7]


def test_euler_41_fails_at_40():
    # Sanity: the famous n^2+n+41 is prime for n=0..39 but not n=40 (40^2+40+41 = 41^2).
    from research.r001.primality import is_prime_mr, is_prime_trial
    c = Conjecture("e", "", lambda: range(41), "", lambda n: is_prime_trial(n*n+n+41),
                   lambda n: is_prime_mr(n*n+n+41))
    v = verify.check(c)
    assert v.status == verify.REFUTED and v.counterexample == 40


def test_counterexample_in_ascending_domain_is_least_in_tested_order():
    v = verify.check(conj(lambda n: n < 42, lambda n: n < 42))
    assert v.counterexample_scope == "LEAST_IN_TESTED_ORDER"


def test_unordered_domain_does_not_claim_least():
    # Red-team case: domain visits 10 before 2, and both fail. 10 must not be called least.
    c = Conjecture("t", "", lambda: [1, 10, 2, 3], "", lambda n: n == 1, lambda n: n == 1)
    v = verify.check(c)
    assert v.status == verify.REFUTED and v.counterexample == 10
    assert v.counterexample_scope == "FOUND"


def test_generator_domain_stopped_early_does_not_claim_least():
    c = Conjecture("t", "", lambda: iter(range(100)), "", lambda n: n < 42, lambda n: n < 42)
    v = verify.check(c)
    assert v.counterexample == 42 and v.counterexample_scope == "FOUND"
    v = verify.check(c, stop_at_first_counterexample=False)
    assert v.counterexample == 42 and v.counterexample_scope == "LEAST_IN_TESTED_ORDER"
