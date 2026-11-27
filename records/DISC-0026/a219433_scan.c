// A219433: smallest 3-smooth a with p*a+1 prime; report n with a(n) >= prime(n).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static u64 mulmod(u64 a,u64 b,u64 m){return (u128)a*b%m;}
static u64 pw(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static int isprime(u64 n){if(n<2)return 0;static const u64 sp[]={2,3,5,7,11,13,17,19,23,29,31,37};
 for(int i=0;i<12;i++){if(n%sp[i]==0)return n==sp[i];}
 u64 d=n-1;int s=0;while(!(d&1)){d>>=1;s++;}
 for(int i=0;i<12;i++){u64 x=pw(sp[i],d,n);if(x==1||x==n-1)continue;int ok=0;for(int r=1;r<s;r++){x=mulmod(x,x,n);if(x==n-1){ok=1;break;}}if(!ok)return 0;}return 1;}
int cmp(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
int main(int c,char**v){u64 NMAX=strtoull(v[1],0,10); u64 PLIM=(u64)(NMAX*(log((double)NMAX)+log(log((double)NMAX)))+100);
 u64 S[4000];int ns=0; for(u64 a=1;a<(1ULL<<40);a*=2)for(u64 b=a;b<(1ULL<<40);b*=3)S[ns++]=b; qsort(S,ns,8,cmp);
 char*comp=calloc(PLIM+1,1); for(u64 i=2;i*i<=PLIM;i++)if(!comp[i])for(u64 j=i*i;j<=PLIM;j+=i)comp[j]=1;
 u64 n=0; long exc=0;
 for(u64 p=2;p<=PLIM && n<NMAX;p++){ if(comp[p])continue; n++;
   int i; for(i=0;i<ns;i++){ if((u128)p*S[i]+1 >= ((u128)1<<64)){i=ns;break;} if(isprime(p*S[i]+1)) break; }
   if(i==ns){printf("n=%llu p=%llu NONE<2^40\n",n,p);continue;}
   if(S[i]>=p){exc++; printf("n=%llu p=%llu a=%llu\n",n,p,S[i]); fflush(stdout);} }
 fprintf(stderr,"checked n<=%llu exceptions=%ld\n",n,exc);}
