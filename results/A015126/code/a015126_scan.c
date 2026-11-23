// For t<=T: is the least k with phi(k)=t even while some odd k has phi(k)=t?  (A015126 conjecture, Song 2022)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef unsigned long long u64;
int main(int argc,char**argv){
 u64 T=strtoull(argv[1],0,10); double R=atof(argv[2]); u64 K=(u64)(R*T);
 unsigned char *st=calloc(T+1,1);
 u64 sq=(u64)sqrt((double)K)+2; char*c=calloc(sq+1,1); u64*pr=malloc(sizeof(u64)*sq); int np=0;
 for(u64 i=2;i<=sq;i++){if(!c[i]){pr[np++]=i;for(u64 j=i*i;j<=sq;j+=i)c[j]=1;}}
 const u64 S=1<<22; u64*rem=malloc(S*8),*ph=malloc(S*8);
 long long reports=0; u64 oddcnt=0;
 for(u64 L=1;L<=K;L+=S){u64 H=L+S; if(H>K+1)H=K+1; u64 n=H-L;
  for(u64 i=0;i<n;i++){rem[i]=L+i;ph[i]=1;}
  for(int a=0;a<np;a++){u64 p=pr[a]; if(p*p>=H)break; u64 s=((L+p-1)/p)*p;
   for(u64 m=s;m<H;m+=p){u64 i=m-L; rem[i]/=p; ph[i]*=p-1; while(rem[i]%p==0){rem[i]/=p;ph[i]*=p;}}}
  for(u64 i=0;i<n;i++){ if(rem[i]>1)ph[i]*=rem[i]-1; u64 k=L+i; if((k&3)==2)continue; u64 t=ph[i]; if(t>T)continue;
   if(st[t]==0) st[t]=(k&1)?1:2; else if(st[t]==2 && (k&1)){ st[t]=3; reports++; if(reports<=20)printf("t=%llu odd k=%llu (least preimage even)\n",t,k);} }
 }
 // sanity: count of t with least preimage even
 u64 ev=0; for(u64 t=1;t<=T;t++) if(st[t]>=2) ev++;
 printf("T=%llu K=%llu reports=%lld totients-with-even-least=%llu\n",T,K,reports,ev);
}
