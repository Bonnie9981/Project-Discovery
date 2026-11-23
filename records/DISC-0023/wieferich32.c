// primes p in [lo,hi) with 3^(p-1) == 2^(p-1) mod p^2 ; segmented sieve, OpenMP
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef unsigned __int128 u128;
static uint64_t pw(uint64_t b,uint64_t e,uint64_t m){uint64_t r=1%m;b%=m;while(e){if(e&1)r=(u128)r*b%m;b=(u128)b*b%m;e>>=1;}return r;}
int main(int c,char**v){uint64_t lo=strtoull(v[1],0,10),hi=strtoull(v[2],0,10);
 uint32_t sq=(uint32_t)sqrt((double)hi)+2; char*s=calloc(sq+1,1); uint32_t*pr=malloc(sizeof(uint32_t)*sq);int np=0;
 for(uint32_t i=2;i<=sq;i++)if(!s[i]){pr[np++]=i;for(uint64_t j=(uint64_t)i*i;j<=sq;j+=i)s[j]=1;}
 const uint64_t SEG=1<<22; uint64_t cnt=0;
 #pragma omp parallel for schedule(dynamic) reduction(+:cnt)
 for(uint64_t st=lo;st<hi;st+=SEG){uint64_t en=st+SEG<hi?st+SEG:hi;char*f=calloc(en-st,1);
  for(int k=0;k<np;k++){uint64_t p=pr[k];if(p*p>=en)break;uint64_t j=(st+p-1)/p*p;if(j<p*p)j=p*p;for(;j<en;j+=p)f[j-st]=1;}
  for(uint64_t n=st;n<en;n++){if(n<5||f[n-st])continue;cnt++;uint64_t m=n*n;
   if(pw(3,n-1,m)==pw(2,n-1,m)){
    #pragma omp critical
    printf("HIT %llu\n",(unsigned long long)n);}}
  free(f);}
 printf("primes_tested %llu in [%llu,%llu)\n",(unsigned long long)cnt,(unsigned long long)lo,(unsigned long long)hi);}
