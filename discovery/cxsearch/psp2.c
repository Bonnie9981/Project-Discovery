// List base-2 Fermat pseudoprimes (odd composite n with 2^(n-1) == 1 mod n) in [lo, hi).
// Montgomery arithmetic, exact for n < 2^63. Primes are removed by a segmented sieve.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static inline uint64_t inv64(uint64_t n){uint64_t x=n;for(int i=0;i<6;i++)x*=2-n*x;return x;}
static inline uint64_t redc(u128 t,uint64_t n,uint64_t ni){uint64_t m=(uint64_t)t*ni;u128 u=(t+(u128)m*n)>>64;return u>=n?u-n:u;}
// returns 1 if 2^(n-1) == 1 mod n
static int fermat2(uint64_t n){
  uint64_t ni=-inv64(n); // -n^{-1} mod 2^64
  uint64_t r=(uint64_t)(((u128)1<<64)%n); // 1 in Montgomery form
  uint64_t x=r, two=(uint64_t)(((u128)2<<64)%n);
  uint64_t e=n-1; int b=63-__builtin_clzll(e);
  x=two;
  for(int i=b-1;i>=0;i--){ x=redc((u128)x*x,n,ni); if((e>>i)&1){ x=x+x; if(x>=n) x-=n; } }
  return x==r;
}
int main(int argc,char**argv){
  uint64_t lo=strtoull(argv[1],0,10), hi=strtoull(argv[2],0,10);
  // small primes up to sqrt(hi)
  uint64_t s=1; while(s*s<hi) s++;
  char*sm=calloc(s+1,1); for(uint64_t i=2;i*i<=s;i++) if(!sm[i]) for(uint64_t j=i*i;j<=s;j+=i) sm[j]=1;
  uint64_t*pr=malloc(sizeof(uint64_t)*(s+1)); int np=0; for(uint64_t i=3;i<=s;i++) if(!sm[i]) pr[np++]=i;
  const uint64_t SEG=1<<24; char*comp=malloc(SEG);
  for(uint64_t a=lo|1; a<hi; a+=SEG){
    uint64_t b=a+SEG; if(b>hi) b=hi; memset(comp,0,SEG);
    for(int k=0;k<np;k++){ uint64_t p=pr[k]; if(p*p>=b) break; uint64_t st=((a+p-1)/p)*p; if(st<p*p) st=p*p; if(!(st&1)) st+=p; for(uint64_t j=st;j<b;j+=2*p) comp[j-a]=1; }
    for(uint64_t n=a;n<b;n+=2){ if(n<9||!comp[n-a]) continue; if(fermat2(n)) printf("%llu\n",(unsigned long long)n); }
  }
  return 0;
}
