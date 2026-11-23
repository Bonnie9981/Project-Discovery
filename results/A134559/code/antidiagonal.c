/* independent: antidiagonal recurrence b_{n+1}(k+1)=b_n(k)-(k+1)[ (k+1)|(n-k) ], b_n(0)=sigma(n) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
static u64 gcdu(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
int main(int argc,char**argv){
  long N=atol(argv[1]);
  u64 *sig=calloc(N+3,8); for(long d=1;d<=N+2;d++) for(long m=d;m<=N+2;m+=d) sig[m]+=d;
  u64 *b=calloc(N/2+4,8); unsigned char *g1=calloc(N+3,1), *g2=calloc(N+3,1);
  /* n=1: ceil(1/2)=1, b_1(0)=1 */
  b[0]=1;
  for(long n=1;n<=N+1;n++){
    long K=(n+1)/2; /* number of k */
    u64 pr=1%n; for(long k=0;k<K;k++) pr=(pr*(b[k]%n))%n;
    u64 g=gcdu(pr,n); g1[n]=(g==1); g2[n]=(g==2);
    if(n==4934||n==4933||n==54217) printf("gcd(P(%ld),%ld)=%llu\n",n,n,g);
    /* advance to n+1 */
    long K2=(n+2)/2;
    for(long k=K2-2;k>=0;k--){ u64 v=b[k]; if((n-k)%(k+1)==0) v-=(k+1); b[k+1]=v; }
    b[0]=sig[n+1];
    if(n==4933){ printf("b_4934(134)=%llu b_4934(0)=%llu\n",b[134],b[0]); }
  }
  char *isp=calloc(N+3,1); for(long i=2;i<=N+2;i++) isp[i]=1;
  for(long i=2;i*i<=N+2;i++) if(isp[i]) for(long j=i*i;j<=N+2;j+=i) isp[j]=0;
  long cnt=0,fails=0,extra=0;
  for(long n=1;n<=N;n++){
    int s=g1[n]&&g2[n+1];
    int a=(n>5 && isp[n] && (n+1)%2==0 && isp[(n+1)/2]);
    cnt+=s;
    if(s!=a){ printf("%s %ld g1=%d g2(n+1)=%d\n", a?"FAIL_in_A005383":"EXTRA", n,g1[n],g2[n+1]); if(a)fails++; else extra++; }
  }
  printf("N=%ld solutions=%ld fails=%ld extra=%ld\n",N,cnt,fails,extra);
}
