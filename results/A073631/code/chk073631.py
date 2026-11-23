"""Independent big-integer check for DISC-0022 (A073631). Run: python -I chk073631.py"""
def is_prime(n):
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for a in small:
        if n % a == 0:
            return n == a
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:              # deterministic for n < 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def term(k):
    return k > 1 and not is_prime(k) and pow(3, k - 1, k) == pow(2, k - 1, k)

for q in (23, 3842760169, 41975417117):
    assert is_prime(q) and pow(3, q - 1, q * q) == pow(2, q - 1, q * q)
    assert pow(3, q - 1, q ** 3) != pow(2, q - 1, q ** 3)
for q in (3842760169, 41975417117):
    k = q * q
    assert term(k) and k % 529 != 0
    print("counterexample", k, "=", q, "^2")
assert not term(23 ** 4)
print("ok")
