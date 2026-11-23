# A counterexample to the conjecture in A073631 and A130058

Chi Hsia, 2026. Written with an LLM (Claude); the counterexample is checked in Lean 4.

**Sequence.** A073631 lists the nonprimes k with k | 3^(k-1) - 2^(k-1). A comment of A. Adamchuk (May 2007), repeated in A130058, conjectures that all nonsquarefree terms are multiples of 23^2, and observes that 1 and 529 = 23^2 appear to be the only perfect squares in the sequence.

**Claim.** Both statements are false. The least counterexample to each is

k = 3842760169^2 = 14766805716452908561.

**Lemma.** If k > 1, k | 3^(k-1) - 2^(k-1), and q is a prime with q^2 | k, then q^2 | 3^(q-1) - 2^(q-1), i.e. q is a Wieferich prime to base 3/2 (A376896).

*Proof.* 3^(k-1) - 2^(k-1) is odd and prime to 3, so q >= 5. Let x = 3 * 2^(-1) mod q^2. Then x^(k-1) = 1 (mod q^2), so the order d of x divides both k - 1 and phi(q^2) = q(q-1). Since q | k, gcd(k-1, q) = 1, hence d | q - 1. QED.

**Counterexample.** q = 3842760169 is a Wieferich prime to base 3/2 (A376896). Since q - 1 divides q^2 - 1, the number k = q^2 satisfies 3^(k-1) = 2^(k-1) (mod k). It is composite, a perfect square, not squarefree, and not divisible by 23^2. The same holds for q = 41975417117.

**Minimality.** Let k be a nonsquarefree term with 23^2 not dividing k. Some prime q != 23 has q^2 | k, and by the lemma q is a Wieferich prime to base 3/2. A direct search over all primes 5 <= p < 2^32 finds only 23 and 3842760169 (matching A376896), so q >= 3842760169 and k >= q^2. For the perfect-square statement, a square term m^2 has every prime factor of m in A376896; if m is a power of 23 with 23^3 | m^2, the lemma's argument modulo 23^3 would give (3/2)^22 = 1 (mod 23^3), which is false, so m = 23.

**Infinitely many?** Each Wieferich prime q to base 3/2 other than 23 gives the counterexample q^2. Only two are known; whether there are infinitely many is open, as for Wieferich primes in general.

**Checks.** Lean 4 (core only, kernel evaluation of modular powers): `Discovery.A073631Counter.a073631_counterexample` and `a073631_counterexample2` in `lean/Discovery/A073631Counter.lean`. C programs and a Python check in `results/A073631/code/`. A direct scan of A073631 up to 10^9 finds 60 nonsquarefree terms, all multiples of 529, so the conjecture holds far beyond the 50 terms it was based on.
