// For m in [lo,hi]: report composite m with m | a(m) (WEAK) and m^2 | a(m) (STRONG), plus primes p with p^3 | a(p) (P3)
// a(m) = numerator(-1/m + sum_{k=1..m} 2^(k-1)/k)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128; typedef uint64_t u64; typedef int64_t i64;
static u64 mulm(u64 a,u64 b,u64 M){return (u64)((u128)a*b%M);}
static i64 inv(i64 a,i64 M){ i64 g=M,x=0,x1=1,a1=a%M; while(a1){i64 q=g/a1,t=g-q*a1;g=a1;a1=t;t=x-q*x1;x=x1;x1=t;} return ((x%M)+M)%M;}
// returns v = min(v_q(S), cap)  where cap <= cap
static int vS(i64 m,i64 q,int cap){
  int t=0; i64 pw=1; while(pw<=m/q){pw*=q;t++;}           // t = floor(log_q m)
  // M = q^(t+cap); guard overflow
  i64 M=1; for(int i=0;i<t+cap;i++){ if(M> (INT64_MAX/ q)) return -999; M*=q; }
  i64 *qp=malloc(sizeof(i64)*(t+1)); qp[0]=1; for(int i=1;i<=t;i++) qp[i]=qp[i-1]*q;
  u64 T=0, two=1;
  for(i64 k=1;k<=m;k++){
    i64 kk=k; int v=0; while(kk%q==0){kk/=q;v++;}
    u64 term=mulm(mulm(two,(u64)qp[t-v],M),(u64)inv(kk,M),M);
    T=(T+term)%M; two=(two*2)%M;  // two < M < 2^63 so two*2 fits
  }
  { i64 kk=m; int v=0; while(kk%q==0){kk/=q;v++;} u64 term=mulm((u64)qp[t-v],(u64)inv(kk,M),M); T=(T+M-term)%M; }
  free(qp);
  // v_q(T) - t
  int vt=0; if(T==0) vt=t+cap; else { while(T%q==0 && vt<t+cap){T/=q;vt++;} }
  return vt-t;
}
int main(int argc,char**argv){
  i64 lo=atoll(argv[1]),hi=atoll(argv[2]);
  for(i64 m=lo;m<=hi;m++){
    if(m<2) continue;
    i64 r=m; int weak=1,strong=1,isprime=1; int nfac=0;
    for(i64 q=2;q*q<=r;q++) if(r%q==0){ int e=0; while(r%q==0){r/=q;e++;} nfac++; isprime=0;
        int v=vS(m,q,2*e); if(v==-999){printf("OVF m=%lld q=%lld\n",(long long)m,(long long)q);weak=strong=0;break;}
        if(v<e) {weak=0;strong=0;break;} if(v<2*e) strong=0; }
    if(r>1 && (weak||isprime)){ if(r==m){ // prime
          if(m>3){ int v=vS(m,m,3); if(v<2) printf("PRIMEFAIL p=%lld v=%d\n",(long long)m,v); if(v>=3) printf("P3 p=%lld\n",(long long)m);} continue; }
        int v=vS(m,r,2); if(v<1){weak=0;strong=0;} else if(v<2) strong=0; }
    if(!isprime && weak) printf("WEAK m=%lld%s\n",(long long)m, strong?" STRONG":"");
  }
  printf("done %lld..%lld\n",(long long)lo,(long long)hi);
}
