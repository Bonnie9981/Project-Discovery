/* A309491: a(n)=sum_{d|n,d>1} phi(n/d)*d/lpf(d); A008590 check: S2=sum phi(n/d)*lpf(d) */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
int main(int c,char**v){ ll N=atoll(v[1]);
 int *spf=calloc(N+1,sizeof(int)); for(ll i=2;i<=N;i++) if(!spf[i]) for(ll j=i;j<=N;j+=i) if(!spf[j])spf[j]=i;
 ll bad309=0, bad8590=0;
 for(ll n=1;n<=N;n++){
  ll ps[16]; int es[16],w=0; ll x=n; while(x>1){ll p=spf[x];int e=0;while(x%p==0){x/=p;e++;}ps[w]=p;es[w++]=e;}
  /* enumerate divisors d with lpf(d), and phi(n/d) */
  ll S1=0,S2=0;
  int idx[16]={0};
  for(;;){ ll d=1,ph=1,lp=0; for(int i=0;i<w;i++){ for(int t=0;t<idx[i];t++) d*=ps[i]; if(idx[i]&&!lp) lp=ps[i];
      int r=es[i]-idx[i]; if(r>0){ ll q=1; for(int t=1;t<r;t++) q*=ps[i]; ph*=q*(ps[i]-1);} }
    if(d>1){ S1+=ph*(d/lp); S2+=ph*lp; }
    int i=0; while(i<w){ idx[i]++; if(idx[i]<=es[i])break; idx[i]=0; i++; } if(i==w)break; }
  if(n<=28) fprintf(stderr,"%lld,",S1);
  if(n%2==0 && S1==n){ ll h=n/2; int pr = (h>1 && spf[h]==h); if(!pr) printf("A309491 even sol n=%lld\n",n); }
  int both = (S1%2==0)&&(S2%2==0); int m8 = n%8==0;
  if(both!=m8){ if(bad8590<20) printf("A008590 mismatch n=%lld S1=%lld S2=%lld\n",n,S1,S2); bad8590++; }
 }
 fprintf(stderr,"\nmismatch8590=%lld\n",bad8590); }
