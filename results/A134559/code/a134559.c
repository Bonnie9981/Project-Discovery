/* b_n(k)=sum of u in [1,n] with n mod u = k, k=0..ceil(n/2)-1. P(n)=prod b_n(k).
 Conj: n with gcd(P(n),n)=1 and gcd(P(n+1),n+1)=2 are exactly A005383 primes p (p,(p+1)/2 prime) except 3,5. */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll; typedef unsigned long long u64; typedef __uint128_t u128;
static ll gcdl(ll a,ll b){while(b){ll t=a%b;a=b;b=t;}return a;}
static ll *b;
static ll gP(ll n){ /* gcd(P(n),n) */ ll K=(n+1)/2; for(ll k=0;k<K;k++) b[k]=0;
 for(ll u=1;u<=n;u++){ ll r=n%u; if(r<K) b[r]+=u; }
 u64 pr=1%n; for(ll k=0;k<K;k++) pr=(u128)pr*((u64)b[k]%n)%n; return gcdl(pr,n); }
int main(int c,char**v){ ll N=atoll(v[1]); b=malloc(sizeof(ll)*(N+2));
 char *comp=calloc(N+3,1); comp[0]=comp[1]=1; for(ll i=2;i*i<=N+2;i++) if(!comp[i]) for(ll j=i*i;j<=N+2;j+=i) comp[j]=1;
 ll g=gP(1), mis=0, cnt=0, gpp=0;
 for(ll n=1;n<=N;n++){ ll g2=gP(n+1);
  int sat = (g==1 && g2==2);
  int inA = (!comp[n] && n>5 && (n+1)%2==0 && !comp[(n+1)/2]);
  if(inA && g==n){ gpp++; printf("A005383 prime p=%lld with gcd(P(p),p)=p\n",n);}
  if(sat) cnt++;
  if(sat!=inA){ mis++; if(mis<40) printf("MISMATCH n=%lld sat=%d inA=%d g=%lld g2=%lld\n",n,sat,inA,g,g2);}
  g=g2; }
 printf("N=%lld sat=%lld mismatches=%lld\n",N,cnt,mis); }
