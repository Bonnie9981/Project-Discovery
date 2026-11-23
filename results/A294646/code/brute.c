#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u;typedef unsigned __int128 W;
u pm(u b,u e,u m){u r=1%m;b%=m;while(e){if(e&1)r=(W)r*b%m;b=(W)b*b%m;e>>=1;}return r;}
int main(int c,char**v){u lo=atoll(v[1]),hi=atoll(v[2]);
 for(u m=lo|1;m<hi;m+=2){ if(m<3)continue; u x=pm(2,m-1,m); // 2^{m-1}
   u y=(W)3*x%m; if((y+1)%m==0)printf("2n-2: %llu\n",m);
   if((x+1)%m==0)printf("2n: %llu\n",m);
   if((2*x)%m==1)printf("2: %llu\n",m);}
 return 0;}
