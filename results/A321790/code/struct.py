"""A321790 structural search: a semiprime psp2 k = p*q (p < q) with least
non-witness base >= p needs p-1 | q-1 and q | a^(p-1) - 1 for every prime
a < p.  For each prime p <= P compute G = gcd over those a (q unbounded).

    python results/A321790/code/struct.py 100000
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from discovery.cxsearch import numth  # noqa: E402

P = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
sieve = bytearray([1]) * (P + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(P ** .5) + 1):
    if sieve[i]:
        sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
primes = [i for i in range(P + 1) if sieve[i]]
t = time.time()
hits, leftover = [], 0
for p in primes[1:]:
    G = (1 << (p - 1)) - 1          # base 2
    for a in primes[1:]:            # odd prime bases 3, 5, ... < p
        if a >= p or G == 1:
            break
        G = math.gcd(G, pow(a, p - 1, G) - 1)
    while G % p == 0:
        G //= p
    if G > 1:
        leftover += 1
        hits += [(p, q) for q in numth.factor(G) if q > p and (q - 1) % (p - 1) == 0]
print(f"p <= {P}: G > 1 for {leftover} primes; hits {hits[:20]}; {time.time() - t:.1f} s")
