// Independent check: list terms k <= N of A073631 (nonprime, 3^(k-1) == 2^(k-1) mod k)
// that are nonsquarefree, and report those not divisible by 23^2.  gcc -O2 -fopenmp
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static uint64_t pw(uint64_t b,uint64_t e,uint64_t m){uint64_t r=1%m;b%=m;while(e){if(e&1)r=(u128)r*b%m;b=(u128)b*b%m;e>>=1;}return r;}
int main(int c,char**v){uint64_t N=strtoull(v[1],0,10);
 char*comp=calloc(N+1,1); char*sqf=malloc(N+1); for(uint64_t i=0;i<=N;i++)sqf[i]=1;
 for(uint64_t i=2;i*i<=N;i++){ if(!comp[i]) for(uint64_t j=i*i;j<=N;j+=i)comp[j]=1;
   for(uint64_t j=i*i;j<=N;j+=i*i)sqf[j]=0; }
 uint64_t terms=0,nsf=0,bad=0;
 #pragma omp parallel for schedule(dynamic,65536) reduction(+:terms,nsf,bad)
 for(uint64_t k=4;k<=N;k++){ if(!comp[k])continue; if(pw(3,k-1,k)!=pw(2,k-1,k))continue; terms++;
   if(!sqf[k]){nsf++; if(k%529){bad++;
     #pragma omp critical
     printf("BAD %llu\n",(unsigned long long)k);}}}
 printf("N=%llu terms(k>1)=%llu nonsquarefree=%llu not_mult_529=%llu\n",(unsigned long long)N,(unsigned long long)terms,(unsigned long long)nsf,(unsigned long long)bad);}
