#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
static int *tau;
static ll V(ll p, ll m, ll need){ /* v_p(F(m)), F(m)=m^(m-1) prod_{k<m} k^tau(m-k); stops early once >= need */
  ll vm=0,x=m; while(x%p==0){x/=p;vm++;}
  ll s=(m-1)*vm; if(s>=need) return s;
  for(ll q=p;q<m;q*=p){ for(ll k=q;k<m;k+=q){ s+=tau[m-k]; if(s>=need) return s; } if(q>m/p) break; }
  return s; }
int main(int c,char**v){ ll N=atoll(v[1]);
 tau=calloc(N+2,sizeof(int)); for(ll i=1;i<=N+1;i++) for(ll j=i;j<=N+1;j+=i) tau[j]++;
 int *spf=calloc(N+2,sizeof(int)); for(ll i=2;i<=N+1;i++) if(!spf[i]) for(ll j=i;j<=N+1;j+=i) if(!spf[j])spf[j]=i;
 ll prev=-1;
 for(ll n=1;n<=N+1;n++){ ll a;
  if(n==1) a=1; else {
   ll ps[16],es[16]; int w=0; ll x=n,P=0; while(x>1){ll p=spf[x];int e=0;while(x%p==0){x/=p;e++;}ps[w]=p;es[w++]=e; if(p>P)P=p;}
   for(ll m=P;;m++){ int ok=1; for(int i=0;i<w&&ok;i++){ ll lb=(m-1)/ps[i]; if(lb>=es[i]) continue; if(V(ps[i],m,es[i])<es[i]) ok=0; } if(ok){a=m;break;} }
  }
  if(n<=30) fprintf(stderr,"%lld,",a);
  if(a==prev) printf("eq n=%lld a=%lld\n",n-1,a);
  prev=a; }
 fprintf(stderr,"\n"); }
