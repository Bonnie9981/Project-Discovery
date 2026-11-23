import sys
def factor(n):
    f={};p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
T=[0]*5001
for i in range(1,5001):
    for j in range(i,5001,i): T[j]+=1
def vp(x,p):
    e=0
    while x%p==0: x//=p; e+=1
    return e
def V(p,m): return (m-1)*vp(m,p)+sum(vp(k,p)*T[m-k] for k in range(p,m,p))
def a(n):
    if n==1: return 1
    f=factor(n); m=max(f)
    while not all(V(p,m)>=e for p,e in f.items()): m+=1
    return m
assert [a(n) for n in range(1,31)]==[1,2,3,4,5,3,7,4,3,5,11,4,13,7,5,4,17,3,19,5,7,11,23,4,5,13,6,7,29,5]
sols=[];mx=0
for line in open(sys.argv[1]):
    n=int(line); x,y=a(n),a(n+1); mx=max(mx,x,y)
    if x==y: sols.append((n,x))
print("solutions:",sols,"max a seen:",mx)
