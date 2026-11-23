import sys
from math import gcd
def T(n,k): return sum(d for d in range(k,n+1) if n%d==0)
def P_factors(n):
    return [T(n-k,k+1) for k in range(0,(n+1)//2)]
for n in [4934,6998,11114]:
    p=n//2
    bs=P_factors(n)
    hits=[(k,v) for k,v in enumerate(bs) if v%p==0]
    from functools import reduce
    g=gcd(reduce(lambda a,b:a*b,bs),n)
    print(n,"gcd=",g,"k with p|b:",hits[:5])
