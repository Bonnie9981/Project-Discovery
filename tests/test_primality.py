from research.r001.primality import is_prime_mr, is_prime_trial


def test_implementations_agree_up_to_100k():
    assert all(is_prime_trial(n) == is_prime_mr(n) for n in range(-5, 100_000))


def test_known_values():
    assert [n for n in range(30) if is_prime_mr(n)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    # Carmichael numbers and strong pseudoprimes to small bases must be rejected.
    for n in (561, 1105, 1729, 2047, 3215031751, 3825123056546413051):
        assert not is_prime_mr(n)
    assert is_prime_mr(2_147_483_647)  # Mersenne prime 2^31-1


def test_strong_pseudoprime_to_first_12_bases_is_rejected():
    # 399165290221 * 798330580441: passes MR for bases 2..37, caught by base 41.
    assert not is_prime_mr(318665857834031151167461)
