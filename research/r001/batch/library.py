"""DISC-0004 function library: precise definitions (metadata only, no computation).

All functions are defined for integers n >= 1. f(1) follows the empty-product /
empty-sum convention unless stated. Computation lives in impl_a / impl_b / impl_c.
"""
FUNCS = {
    "one": ("1 for all n", "A000012"),
    "id": ("n", "A000027"),
    "d": ("number of positive divisors of n", "A000005"),
    "d_odd": ("number of odd positive divisors of n", "A001227"),
    "sigma": ("sum of positive divisors of n", "A000203"),
    "sigma2": ("sum of squares of positive divisors of n", "A001157"),
    "sigma_odd": ("sum of odd positive divisors of n", "A000593"),
    "phi": ("Euler totient: #{1<=k<=n : gcd(k,n)=1}", "A000010"),
    "psi": ("Dedekind psi: n * prod_{p|n} (1 + 1/p)", "A001615"),
    "J2": ("Jordan totient J_2: n^2 * prod_{p|n} (1 - 1/p^2)", "A007434"),
    "omega": ("number of distinct primes dividing n (omega(1)=0)", "A001221"),
    "Omega": ("number of prime factors of n with multiplicity (Omega(1)=0)", "A001222"),
    "mu": ("Moebius function", "A008683"),
    "liouville": ("Liouville lambda: (-1)^Omega(n)", "A008836"),
    "rad": ("product of distinct primes dividing n (rad(1)=1)", "A007947"),
    "core": ("squarefree part: n divided by its largest square divisor", "A007913"),
    "carmichael": ("Carmichael lambda: exponent of the group (Z/nZ)^*; lambda(1)=lambda(2)=1", "A002322"),
    "sopf": ("sum of distinct primes dividing n (sopf(1)=0)", "A008472"),
    "sopfr": ("sum of prime factors of n with multiplicity (sopfr(1)=0)", "A001414"),
    "gpf": ("greatest prime factor of n, gpf(1)=1", "A006530"),
    "lpf": ("least prime factor of n, lpf(1)=1", "A020639"),
    "usigma": ("sum of unitary divisors d of n (gcd(d, n/d) = 1)", "A034448"),
    "d_unitary": ("number of unitary divisors of n = 2^omega(n)", "A034444"),
    "d_square": ("number of square divisors of n", "A046951"),
    "r2": ("#{(x,y) in Z^2 : x^2+y^2 = n}", "A004018"),
    "r3": ("#{(x,y,z) in Z^3 : x^2+y^2+z^2 = n}", "A005875"),
    "r4": ("#{(x,y,z,w) in Z^4 : x^2+y^2+z^2+w^2 = n}", "A000118"),
}

# Inner functions used in compositions f(g(n)): values stay <= ~5 N.
INNER = ["sigma", "phi", "psi", "rad", "core", "sigma_odd", "carmichael", "usigma", "d", "sopfr", "gpf", "Omega"]
# Outer functions (lattice counts excluded: they are only computed up to N).
OUTER = [k for k in FUNCS if k not in ("one", "id", "r2", "r3", "r4")]

# f(x) >= x for all x >= 1 ("up") or f(x) <= x ("down"); used to drop trivial inequalities.
MONOTONE_BOUND = {
    "sigma": "up", "psi": "up", "usigma": "up", "sigma2": "up", "J2": None,
    "phi": "down", "rad": "down", "core": "down", "carmichael": "down", "gpf": "down",
    "lpf": "down", "sigma_odd": None, "d": "down", "sopfr": "down", "sopf": "down",
    "Omega": "down", "omega": "down", "d_odd": "down", "d_unitary": "down", "d_square": "down",
}

# Words an OEIS name uses for each function, to tell a definitional match from a cross-match.
KEYWORDS = {
    "d": ["tau", "number of divisors", "A000005", "d("], "d_odd": ["odd divisors", "A001227"],
    "sigma": ["sigma", "sum of divisors", "A000203"], "sigma2": ["sigma_2", "squares of divisors", "A001157"],
    "sigma_odd": ["odd divisors", "A000593"], "phi": ["phi", "totient", "A000010"],
    "psi": ["psi", "Dedekind", "A001615"], "J2": ["Jordan", "J_2", "A007434"],
    "omega": ["omega", "distinct prime", "A001221"], "Omega": ["Omega", "bigomega", "with multiplicity", "A001222"],
    "mu": ["mu", "Moebius", "Möbius", "A008683"], "liouville": ["Liouville", "A008836"],
    "rad": ["rad", "squarefree kernel", "A007947"], "core": ["core", "squarefree part", "A007913"],
    "carmichael": ["Carmichael", "lambda", "A002322"], "sopf": ["sopf", "distinct primes", "A008472"],
    "sopfr": ["sopfr", "with repetition", "A001414"], "gpf": ["largest prime", "greatest prime", "A006530"],
    "lpf": ["smallest prime", "least prime", "A020639"], "usigma": ["unitary", "A034448"],
    "d_unitary": ["unitary", "A034444"], "d_square": ["square divisors", "A046951"],
}
