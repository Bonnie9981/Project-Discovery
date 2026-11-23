import sys
from sympy import factorint
def vp_fact(x,p):
    s=0
    while x: x//=p; s+=x
    return s
def f(p,e,r):
    # smallest m with sum_{t=1..m} [vp((t+r-1)!) - vp((t-1)!)] >= e
    s=0;m=0
    while s<e:
        m+=1; s+=vp_fact(m+r-1,p)-vp_fact(m-1,p)
    return m
def K(p,e):
    m=0
    while True:
        m+=p
        if vp_fact(m,p)>=e: return m
def a(n):
    if n==1: return 1
    F=factorint(n)
    Kn=max(K(p,e) for p,e in F.items())
    return sum(max(f(p,e,r) for p,e in F.items()) for r in range(1,Kn+1))
if __name__=='__main__':
    print([a(n) for n in range(1,58)])
