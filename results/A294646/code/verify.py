"""Check the A294646 counterexample n = 9814447404 directly (Python big integers, no tricks)."""
n = 9814447404
m = 2 * n + 1
assert m == 367 * 53484727
x = pow(2, 2 * n, m)
a = pow(x, -1, m)            # (1/2)^(2n) mod (2n+1) = inverse of 2^(2n)
print("n =", n, " 2n+1 =", m, "= 367 * 53484727")
print("a(n) =", a, " 2n-2 =", 2 * n - 2, " equal:", a == 2 * n - 2)
print("(3*2^(2n)+1) mod (2n+1) =", (3 * x + 1) % m)
# first terms of the entry, as a sanity check of the definition
data = [1,1,1,7,1,1,4,1,1,16,1,11,25,1,1,25,4,1,10,1]
assert [pow(pow(2, 2*k, 2*k+1), -1, 2*k+1) for k in range(1, 21)] == data
print("first 20 DATA terms match")
