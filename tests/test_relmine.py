"""discovery.relmine：變換和篩選工具的基本檢查（不需要離線 OEIS）。"""
from discovery.relmine import (binom, cfinite_order, euler, invbinom, inveuler, invert,
                               invmobius, key, mobius, psum, diff, scalar_fit, square)

CATALAN = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900,
           2674440, 9694845, 35357670, 129644790, 477638700, 1767263190]


def test_transforms_known_values():
    assert euler([1] * 10) == [1, 2, 3, 5, 7, 11, 15, 22, 30, 42]  # partitions
    assert invert([1] * 6) == [1, 2, 4, 8, 16, 32]
    assert binom([1, 1, 1, 1]) == [1, 2, 4, 8]
    assert square([1] * 5) == [1, 2, 3, 4, 5]
    assert invmobius([1] * 6) == [1, 2, 2, 3, 2, 4]  # number of divisors


def test_inverses():
    a = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8]
    assert inveuler(euler(a)) == a
    assert mobius(invmobius(a)) == a
    assert invbinom(binom(a)) == a
    assert diff(psum(a)) == a[1:]


def test_cfinite_and_fit():
    fib = [1, 1]
    for _ in range(20):
        fib.append(fib[-1] + fib[-2])
    assert cfinite_order(fib) == 2
    assert cfinite_order([n ** 3 for n in range(30)]) == 4
    assert cfinite_order(CATALAN) is None
    assert scalar_fit([2, 4, 6], [1, 2, 3]) == 2
    assert scalar_fit([2, 4, 7], [1, 2, 3]) is None
    assert key(CATALAN[2:16]) == key([3 * x for x in CATALAN[2:16]])
