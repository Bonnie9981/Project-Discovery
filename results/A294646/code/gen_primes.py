from sympy import primerange, n_order, discrete_log
from math import gcd
import sys
P=int(sys.argv[1]); f=open('plist.txt','w'); S=0
for p in primerange(7,P):
    if p%6!=1: continue
    t=(-pow(3,-1,p))%p
    d=n_order(2,p)
    if pow(t,d,p)!=1: continue
    r=discrete_log(p,t,2)%d
    if r%gcd(d,6): continue
    f.write(f"{p} {d} {r}\n"); S+=1/(d*6//gcd(d,6))
print(S)
