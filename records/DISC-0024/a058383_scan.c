// x>=7 with phi(x)+phi(x-1) == floor((4x-3)/3); print those where x is not prime of form 1+2^a3^b (a,b>0)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef unsigned long long u64;
static int is23(u64 m,int*a,int*b){*a=*b=0;while(m%2==0){m/=2;(*a)++;}while(m%3==0){m/=3;(*b)++;}return m==1;}
int main(int argc,char**argv){u64 K=(u64)atof(argv[1]);
 u64 sq=(u64)sqrt((double)K)+2; char*c=calloc(sq+1,1); u64*pr=malloc(sizeof(u64)*sq); int np=0;
 for(u64 i=2;i<=sq;i++){if(!c[i]){pr[np++]=i;for(u64 j=i*i;j<=sq;j+=i)c[j]=1;}}
 const u64 S=1<<22; u64*rem=malloc(S*8),*ph=malloc(S*8); u64 prev=0; long sols=0,odd=0;
 for(u64 L=1;L<=K;L+=S){u64 H=L+S; if(H>K+1)H=K+1; u64 n=H-L;
  for(u64 i=0;i<n;i++){rem[i]=L+i;ph[i]=1;}
  for(int a=0;a<np;a++){u64 p=pr[a]; if(p*p>=H)break; u64 s=((L+p-1)/p)*p;
   for(u64 m=s;m<H;m+=p){u64 i=m-L; rem[i]/=p; ph[i]*=p-1; while(rem[i]%p==0){rem[i]/=p;ph[i]*=p;}}}
  for(u64 i=0;i<n;i++){ if(rem[i]>1)ph[i]*=rem[i]-1; u64 x=L+i;
   if(x>=7 && ph[i]+prev==(4*x-3)/3){ sols++; int a,b; int isp=(ph[i]==x-1); int ok=isp&&is23(x-1,&a,&b)&&a>0&&b>0;
     if(!ok){odd++; if(odd<=30)printf("x=%llu phi=%llu phi(x-1)=%llu\n",x,ph[i],prev);} }
   prev=ph[i]; }
 }
 printf("K=%llu solutions=%ld non-A058383=%ld\n",K,sols,odd);}
