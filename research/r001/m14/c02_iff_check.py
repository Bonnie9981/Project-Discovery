"""DISC-0007: check the Lean statement of c02_iff against direct computation.

python research/r001/m14/c02_iff_check.py 1000000   (prints solutions / mismatch counts)
Written by the proof agent; copied unchanged below this docstring.
"""
import sys
N=int(sys.argv[1])
spf=list(range(N+1))
i=2
while i*i<=N:
    if spf[i]==i:
        for j in range(i*i,N+1,i):
            if spf[j]==j: spf[j]=i
    i+=1
def fac(n):
    d={}
    while n>1:
        if n<=N: p=spf[n]
        else:
            p=None; q=2
            while q*q<=n:
                if n%q==0: p=q;break
                q+=1
            if p is None: p=n
        while n%p==0: d[p]=d.get(p,0)+1; n//=p
    return d
def rad(n):
    r=1
    for p in fac(n): r*=p
    return r
def sigma(n):
    s=1
    for p,e in fac(n).items(): s*=(p**(e+1)-1)//(p-1)
    return s
def sqf(n): return all(e==1 for e in fac(n).values())
def isprime(n): return n>1 and fac(n)=={n:1}
bad=0; cnt=0; c2=[]
for n in range(1,N+1):
    L = rad(sigma(n))==sigma(rad(n))
    A = sqf(n) and sqf(sigma(n))
    B=False
    a=(n&-n).bit_length()-1; p=n>>a
    if isprime(p) and p%2==1 and a%2==1 and a>=3 and sqf(p+1) and (p+1)%3!=0 and (3*(p+1))%rad(2**(a+1)-1)==0:
        B=True
    if L: cnt+=1
    if B: c2.append(n)
    if L!=(A or B): bad+=1; print("MISMATCH",n,L,A,B)
print("N",N,"solutions",cnt,"mismatch",bad,"second-branch",len(c2),c2[:10])
