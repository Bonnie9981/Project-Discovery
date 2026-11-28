# DISC-0031 independent check (critic); no project imports. usage: python research/r003/impl_c.py 12
"""Independent check written by the critic (brute force over S_n(132), all four quadrants, Theorem 13, Dale recurrence); imports nothing from the project."""
import sys, itertools, sqlite3
from fractions import Fraction
from math import comb
NMAX=int(sys.argv[1])
def C(m): return comb(2*m,m)//(m+1)
def has132(p):
    n=len(p)
    for i in range(n):
        for j in range(i+1,n):
            for l in range(j+1,n):
                if p[i]<p[l]<p[j]: return True
    return False
def gen(n):
    # left-to-right, v forbidden iff some earlier p[j]>v has a smaller entry before it
    out=[]
    def go(p,used):
        if len(p)==n: out.append(tuple(p)); return
        m=10**9; bad=set()
        # entries v with prefmin(<j) < v < p[j] forbidden
        for j,y in enumerate(p):
            if m<y:
                bad.update(range(m+1,y))
            m=min(m,y)
        for v in range(1,n+1):
            if v not in used and v not in bad:
                p.append(v); used.add(v); go(p,used); p.pop(); used.discard(v)
    go([],set()); return out
for n in range(0,9):
    a=sorted(p for p in itertools.permutations(range(1,n+1)) if not has132(p))
    assert a==sorted(gen(n)) and len(a)==C(n),n
quad={'I':lambda p,i,j: j>i and p[j]>p[i],'II':lambda p,i,j: j<i and p[j]>p[i],
      'III':lambda p,i,j: j<i and p[j]<p[i],'IV':lambda p,i,j: j>i and p[j]<p[i]}
dist={}
for n in range(NMAX+1):
    ps=gen(n); assert len(ps)==C(n)
    for q,f in quad.items():
        cnt=[[0]*(n+2) for _ in range(6)]
        for p in ps:
            c=[sum(1 for j in range(n) if f(p,i,j)) for i in range(n)]
            for k in range(1,6):
                cnt[k][sum(1 for x in c if x>=k)]+=1
        for k in range(1,6): dist[(q,k,n)]=cnt[k]
L0=80
def smul(a,b):
    r=[0]*L0
    for i,u in enumerate(a):
        if u:
            for j in range(L0-i): r[i+j]+=u*b[j]
    return r
def sinv(a):
    r=[0]*L0; r[0]=Fraction(1,1)/a[0]
    for n in range(1,L0): r[n]=-sum(a[i]*r[n-i] for i in range(1,n+1))/a[0]
    return r
def poly(c): return list(c)+[0]*(L0-len(c))
def formula(k,L):
    P=poly([C(a) for a in range(k)])
    tP=[0]+P[:-1]
    num=[(1 if i==0 else 0)-P[i]+smul(tP,P)[i] for i in range(L0)]
    num=[0]+num[:-1]
    d=sinv([(1 if i==0 else 0)-tP[i] for i in range(L0)])
    r=smul(num,smul(d,smul(d,d)))
    assert all(Fraction(v).denominator==1 for v in r)
    return [int(v) for v in r[:L]]
ok=True
for k in range(1,6):
    f=formula(k,NMAX+1)
    for n in range(NMAX+1):
        if dist[('III',k,n)][1]!=f[n]: ok=False; print('FAIL III',k,n)
print('H1 brute vs formula k=1..5 n<=%d:'%NMAX, ok)
db=sqlite3.connect('/home/user/project-discovery/data/oeis/index/oeisdb.sqlite')
def terms(a):
    S='';off=None
    for line in open('/home/user/project-discovery/data/oeis/oeisdata/seq/A212/%s.seq'%a):
        if line[:2] in ('%S','%T','%U'): S+=line.split(' ',2)[2].strip()
        if line[:2]=='%O': off=int(line.split(' ',2)[2].split(',')[0])
    return [int(x) for x in S.split(',') if x], off
for a,k in (('A212338',2),('A212339',3),('A212341',4)):
    T,off=terms(a); f=formula(k,off+len(T))
    print(a,'offset',off,'nterms',len(T),'gf match',T==f[off:off+len(T)])
    # which quadrant's brute data matches OEIS
    print('  quadrant match with brute:',[q for q in quad if all(dist[(q,k,n)][1]==T[n-off] for n in range(off,NMAX+1))])
# Theorem 13 general k: top coeff C_k C_{n-k}, next a_k C_{n-k}
a={1:1}
for k in range(2,6): a[k]=C(k)+sum(C(i-1)*a[k-i] for i in range(1,k))
print('a_k',a)
bad=[]
for k in range(1,6):
    for n in range(k,NMAX+1):
        d=dist[('II',k,n)]
        if max(i for i,v in enumerate(d) if v)!=n-k or d[n-k]!=C(k)*C(n-k): bad.append(('top',k,n))
        if n>=k+1 and d[n-k-1]!=a[k]*C(n-k): bad.append(('next',k,n,d[n-k-1],a[k]*C(n-k)))
print('Thm13 (0,k,0,0) k=1..5 failures:',bad)
for an,sh,c in (('A212344',3,5),('A212345',4,9)):
    T,off=terms(an); print(an,'offset',off,'match',all(T[i]==c*C(off+i-3) for i in range(len(T))),len(T))
    print('  brute (0,3,0,0) x^(n-%d):'%sh,[dist[('II',3,n)][n-sh] for n in range(off,NMAX+1)])
# Dale recurrence range
T,off=terms('A212339'); A=[0]*off+T
sig=[3,0,1,-12,-3,1,18,12,8]
holds=[n for n in range(9,len(A)) if A[n]==sum(s*A[n-i-1] for i,s in enumerate(sig))]
print('Dale holds (zero-extended) n=',holds[:6],'... first fail',[n for n in range(9,len(A)) if n not in holds])
print('Dale: also check n=7,8 with negative indices zero:',[A[n]==sum(s*(A[n-i-1] if n-i-1>=0 else 0) for i,s in enumerate(sig)) for n in range(0,9)])
# Gladkovskii second CF
def cf(depth,tail):
    T=poly([Fraction(tail)])
    for k in range(depth-1,-1,-1):
        inner=smul(poly([0,-2*(k+2)*(2*k+3)]),sinv(T))
        base=poly([k+2,2*(2*k+1)])
        T=[base[i]+inner[i] for i in range(L0)]
    return [10*v for v in sinv(T)][:15]
s1=cf(30,33); s2=cf(36,1)
print('Glad CF2:',[str(v) for v in s1]); print('5C:',[5*C(i) for i in range(15)],'stable',s1==s2)
