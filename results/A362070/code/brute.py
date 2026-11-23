# fully naive: directly use the definition with big integers
from math import prod
def rf(t,k): return prod(range(t,t+k))
def mmin(n,k):
    P=1;m=0
    while True:
        m+=1; P*=rf(m,k)
        if P%n==0: return m
def kempner(n):
    f=1;m=0
    while True:
        m+=1;f*=m
        if f%n==0: return m
def a(n): return sum(mmin(n,r) for r in range(1,kempner(n)+1))
import sys
for n in map(int,sys.argv[1:]): print(n,a(n),kempner(n))
