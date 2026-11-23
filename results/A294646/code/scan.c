#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u;typedef unsigned __int128 W;
u pm(u b,u e,u m){u r=1%m;b%=m;while(e){if(e&1)r=(W)r*b%m;b=(W)b*b%m;e>>=1;}return r;}
u gcd(u a,u b){while(b){u t=a%b;a=b;b=t;}return a;}
int main(int c,char**v){u K=atoll(v[1]);int part=atoi(v[2]),np=atoi(v[3]);
 FILE*f=fopen("plist.txt","r");u p,d,r;int idx=0;
 while(fscanf(f,"%llu %llu %llu",&p,&d,&r)==3){ if(idx++%np!=part)continue;
  // k ≡ 1+r mod d, k ≡ 1 mod 6 ; find start by stepping
  u L=d/gcd(d,6)*6; u k0=0; for(u k=(1+r)%d;k<L+d;k+=d){ if(k%6==1){k0=k;break;} }
  if(!k0 && 1%6!=1) continue;
  for(u k=k0;k<=K;k+=L){ if(k<7)continue; u m=p*k; u x=pm(2,m-1,m); if(((W)3*x+1)%m==0)printf("HIT m=%llu p=%llu k=%llu\n",m,p,k);}
 }
 printf("done part %d\n",part);return 0;}
