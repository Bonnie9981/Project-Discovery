# Partitions into 4 parts and integer triangles: weighted first differences

Chi Hsia, 2026-11-27. (Prepared with the help of an AI assistant (Claude); to be checked by the author before any OEIS submission.)

## Notation

- P(n): partitions of n into exactly 4 parts, written a >= b >= c >= d >= 1, a+b+c+d = n.
- T(m): integer-sided triangles of perimeter m, written 1 <= x <= y <= z, x+y > z, x+y+z = m.

OEIS sums over P(n): A308760 (sum of a), A308759 (b), A308758 (c), A308733 (d), A308775 (all parts), A026810 (count).
OEIS sums over T(m): A307686 (sum of x), A308096 (y), A307966 (z), A005044 (count).

## Theorem 1

For n >= 2 (for n = 1 both sides are 0 if the missing 0th terms of A307686, A308096, A307966 are read as 0):

1. A308758(n) - A308758(n-1) = A307686(n-1).
2. A308759(n) - A308759(n-1) = A308096(n-1).
3. A308733(n) - A308733(n-1) = A307966(n-1) - A308096(n-1) + A005044(n-1).
4. A308760(n) - A308760(n-1) = A026810(n-1) + A308096(n-1).

(The count version A026810(n) - A026810(n-1) = A005044(n-1) is already in the OEIS.)

**Proof.** The map (a,b,c,d) -> (a+1,b,c,d) sends P(n-1) injectively into P(n), and its image is exactly the partitions with a > b. It keeps b, c, d and raises a by 1. So for the weight w in {b, c, d}

  sum_{P(n)} w - sum_{P(n-1)} w = sum_{E(n)} w,   where E(n) = {(a,a,c,d) in P(n)},

and for the weight a the left side is |P(n-1)| + sum_{E(n)} a.

Now (a,a,c,d) -> (x,y,z) = (c, a, a+d-1) is a bijection E(n) -> T(n-1):
- x+y+z = c + 2a + d - 1 = n - 1;
- 1 <= x <= y <= z because 1 <= d <= c <= a and d >= 1;
- x + y > z  is  c + a > a + d - 1, i.e. c >= d, which holds.
The inverse is (x,y,z) -> (a,a,c,d) = (y, y, x, z-y+1): here d >= 1 because z >= y, c >= d because x+y > z, and a >= c because y >= x. The two maps are inverse to each other, since (c, a, a+d-1) -> (a, a, c, (a+d-1)-a+1) = (a, a, c, d) and (y, y, x, z-y+1) -> (x, y, y+(z-y+1)-1) = (x, y, z).

Under this bijection c = x, a = y and d = z - y + 1, which gives 1-4. QED

## Theorem 2 (the conjectured g.f.s are correct)

Write a partition in P(n) as d = y4, c = y4+y3, b = y4+y3+y2, a = y4+y3+y2+y1 with y4 >= 1 and y1, y2, y3 >= 0; then n = y1 + 2y2 + 3y3 + 4y4 and this is a bijection. With F = x^4/((1-x)(1-x^2)(1-x^3)(1-x^4)) (the g.f. of A026810), the g.f. of sum y_i is F*x^i/(1-x^i) for i = 1, 2, 3 and F/(1-x^4) for i = 4. Adding up gives the g.f.s of A308733 (d), A308758 (c), A308759 (b), A308760 (a) and A308775 as explicit rational functions. All of them have the common denominator Q0^2 with Q0 = (1-x)(1-x^2)(1-x^3)(1-x^4). They equal the g.f.s conjectured by Colin Barker (Jun 23-24 2019) in those five entries: for each, numerator1*denominator2 - numerator2*denominator1 is the zero polynomial (exact integer polynomial arithmetic, `check_gf_exact` in `results/A308758/code/check_a308758.py`; checked independently by a second program).

By Theorem 1 the g.f.s of A307686, A308096 and A307966 are (1-x)/x times the g.f. of A308758, of A308759, and (1-x)/x times the g.f. of A308733 plus that of A308096 minus x^3/((1-x^2)(1-x^3)(1-x^4)) (the classical g.f. of A005044). These also agree with Barker's conjectured g.f.s (May 2019) by the same exact check. Since each denominator is the characteristic polynomial of the recurrence Barker lists, those recurrences hold for every n larger than the numerator degree (terms with negative index read as 0), which covers the ranges he states.

## Checks

`results/A308758/code/check_a308758.py`: brute-force enumeration of P(n) and T(n-1) for n <= 200; the bijection checked element by element; the g.f. identities; and the stored OEIS terms of all nine entries.
