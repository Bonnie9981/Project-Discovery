// palindromic primes p<=q, all digits in {4..9}, p*q palindrome, p*q<LIM (exhaustive)
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static u64 mulmod(u64 a,u64 b,u64 m){return (u128)a*b%m;}
static u64 pw(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static int isprime(u64 n){if(n<2)return 0;static const u64 sp[]={2,3,5,7,11,13,17,19,23,29,31,37};
 for(int i=0;i<12;i++){if(n%sp[i]==0)return n==sp[i];}
 u64 d=n-1;int s=0;while(!(d&1)){d>>=1;s++;}
 for(int i=0;i<12;i++){u64 x=pw(sp[i],d,n);if(x==1||x==n-1)continue;int ok=0;for(int r=1;r<s;r++){x=mulmod(x,x,n);if(x==n-1){ok=1;break;}}if(!ok)return 0;}return 1;}
static int ispal128(u128 n){char b[50];int k=0;while(n){b[k++]=n%10;n/=10;}for(int i=0;i<k/2;i++)if(b[i]!=b[k-1-i])return 0;return 1;}
u64 *P; size_t np=0,cap=0;
static void push(u64 v){if(np==cap){cap=cap?cap*2:1024;P=realloc(P,cap*8);}P[np++]=v;}
// build palindromes of length L from half digits
static void half(int L,int pos,int h,int *dg){ if(pos==h){u64 v=0;for(int i=0;i<L;i++){int j=i<h?i:L-1-i;v=v*10+dg[j];} if(isprime(v))push(v);return;}
 for(int d=4;d<=9;d++){dg[pos]=d;half(L,pos+1,h,dg);} }
int cmp(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
int main(int c,char**v){int D=atoi(v[1]); double LIM=atof(v[2]); int dg[20];
 for(int L=1;L<=D;L++){half(L,0,(L+1)/2,dg);} qsort(P,np,8,cmp); fprintf(stderr,"palprimes %zu max %llu\n",np,P[np-1]);
 long long cnt=0,pairs=0;
 for(size_t i=0;i<np;i++){u64 p=P[i]; if((double)p*p>=LIM)break;
  for(size_t j=i;j<np;j++){u128 N=(u128)p*P[j]; if((double)N>=LIM)break; pairs++; if(ispal128(N)){printf("%llu * %llu\n",p,P[j]);cnt++;}}}
 fprintf(stderr,"pairs %lld found %lld\n",pairs,cnt);}
