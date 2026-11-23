#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll;
static ll gcdl(ll a,ll b){while(b){ll t=a%b;a=b;b=t;}return a;}
static ll inv(ll a,ll m){ /* a^-1 mod m, gcd=1 */ ll g=m,x=0,x1=1,a1=a%m; if(m==1)return 0; ll b=a1; ll old_r=b,r=m,old_s=1,s=0; while(r){ll q=old_r/r,t=old_r-q*r;old_r=r;r=t;t=old_s-q*s;old_s=s;s=t;} old_s%=m; if(old_s<0)old_s+=m; return old_s;}
static ll cnt(ll r,ll k,ll q,ll M){ ll g=gcdl(k,q); if(r%g)return 0; ll kg=k/g; ll t0= kg==1?0: ((r/g)%kg)*inv((q/g)%kg,kg)%kg; ll L=kg*q; ll m0=q*t0; if(m0==0)m0=L; return m0<=M?(M-m0)/L+1:0;}
int main(int c,char**v){ ll N=atoll(v[1]); ll lo=c>2?atoll(v[2]):1;
 int *spf=calloc(N+2,sizeof(int)); for(ll i=2;i<=N+1;i++) if(!spf[i]) for(ll j=i;j<=N+1;j+=i) if(!spf[j])spf[j]=i;
 ll prev=-1, maxa=0;
 for(ll n=lo;n<=N+1;n++){ ll a;
  if(n==1){a=1;} else {
   ll ps[16],es[16]; int w=0; ll x=n; while(x>1){ll p=spf[x];int e=0;while(x%p==0){x/=p;e++;} ps[w]=p;es[w]=e;w++;}
   for(ll k=1;;k++){ int fail=0;
     for(ll r=0;r<k && !fail;r++){ int all=1;
       for(int i=0;i<w && all;i++){ ll s=0; for(ll q=ps[i]; q<=n-1 && s<es[i]; q*=ps[i]) s+=cnt(r,k,q,n-1); if(s<es[i]) all=0; }
       if(all) fail=1; }
     if(!fail){a=k;break;} }
  }
  if(a==prev) printf("eq %lld %lld\n",n-1,a);
  if(a>maxa){maxa=a;}
  if(n<=34) fprintf(stderr,"%lld,",a);
  prev=a; }
 fprintf(stderr,"\nmax a=%lld\n",maxa); }
