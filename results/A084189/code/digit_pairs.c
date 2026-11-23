// find p<=q primes, all decimal digits in {4..9}, p*q palindrome, p*q < LIM
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static u64 mulmod(u64 a,u64 b,u64 m){return (u128)a*b%m;}
static u64 pw(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static int isprime(u64 n){if(n<2)return 0;static const u64 sp[]={2,3,5,7,11,13,17,19,23,29,31,37};
 for(int i=0;i<12;i++){if(n%sp[i]==0)return n==sp[i];}
 u64 d=n-1;int s=0;while(!(d&1)){d>>=1;s++;}
 for(int i=0;i<12;i++){u64 x=pw(sp[i],d,n);if(x==1||x==n-1)continue;int ok=0;for(int r=1;r<s;r++){x=mulmod(x,x,n);if(x==n-1){ok=1;break;}}if(!ok)return 0;}return 1;}
static int ispal(u64 n){u64 r=0,m=n;while(m){r=r*10+m%10;m/=10;}return r==n;}
u64 *P; size_t np=0,cap=0;
void gen(u64 v,int left){ if(v&&isprime(v)){if(np==cap){cap=cap?cap*2:1024;P=realloc(P,cap*8);}P[np++]=v;}
 if(!left)return; for(int d=4;d<=9;d++)gen(v*10+d,left-1);}
int cmp(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
int main(int c,char**v){int D=atoi(v[1]); u64 LIM=strtoull(v[2],0,10);
 gen(0,D); qsort(P,np,8,cmp); fprintf(stderr,"primes %zu\n",np);
 long long cnt=0;
 for(size_t i=0;i<np;i++){u64 p=P[i]; if((u128)p*p>=LIM)break;
  for(size_t j=i;j<np;j++){u128 N=(u128)p*P[j]; if(N>=LIM)break; if(ispal((u64)N)){printf("%llu = %llu * %llu\n",(u64)N,p,P[j]);fflush(stdout);cnt++;}}}
 fprintf(stderr,"found %lld\n",cnt);}
