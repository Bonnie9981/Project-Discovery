// A362070 scan: a(n)=a(n+1)?  usage: ./a362070 N [dumpN]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64; typedef int64_t i64;
static i64 vpf(i64 x,i64 p){i64 s=0;while(x){x/=p;s+=x;}return s;}
// arrays for prime powers p^e, e>=2: f[r] for r=1..K
typedef struct {int len; int *f;} Arr;
static Arr *pw[64]; // pw[e][index of p]
static int *primes; static int np;
static Arr build(i64 p,int e){
  i64 K=0; do K+=p; while(vpf(K,p)<e);
  i64 L=K+K+5; i64 *G=malloc(sizeof(i64)*(L+1)); G[0]=0; // G(x)=sum_{y<=x} vp(y!)
  for(i64 x=1;x<=L;x++) G[x]=G[x-1]+vpf(x,p);
  Arr A; A.len=(int)K; A.f=malloc(sizeof(int)*(K+1));
  i64 m=K; // f(1)=K
  for(i64 r=1;r<=K;r++){
    // V(m,r)=G(m+r-1)-G(r-1)-G(m-1) ; find smallest m>=1 with V>=e, m nonincreasing
    while(m>1){ i64 mm=m-1; i64 V=G[mm+r-1]-G[r-1]-G[mm-1]; if(V>=e) m=mm; else break; }
    A.f[r]=(int)m;
  }
  free(G); return A;
}
int main(int argc,char**argv){
  i64 N=atoll(argv[1]); i64 dump=argc>2?atoll(argv[2]):0; i64 START=argc>3?atoll(argv[3]):1;
  i64 sq=(i64)sqrtl((long double)N)+2;
  char *c=calloc(sq+1,1); primes=malloc(sizeof(int)*(sq+1)); np=0;
  for(i64 i=2;i<=sq;i++) if(!c[i]){primes[np++]=i; for(i64 j=i*i;j<=sq;j+=i) c[j]=1;}
  // build arrays lazily: index by prime index and e
  Arr **tab=calloc(np,sizeof(Arr*));
  const i64 S=1<<22; i64 *rem=malloc(sizeof(i64)*S); u64 *val=malloc(sizeof(u64)*S);
  // factor lists
  int (*fp)[12]=malloc(sizeof(int[12])*S); unsigned char (*fe)[12]=malloc(12*S); unsigned char *nf=malloc(S);
  unsigned __int128 prev=0; i64 found=0;
  for(i64 lo=START;lo<=N+1;lo+=S){
    i64 hi=lo+S-1; if(hi>N+1) hi=N+1; i64 cnt=hi-lo+1;
    for(i64 i=0;i<cnt;i++){rem[i]=lo+i;nf[i]=0;}
    for(int k=0;k<np;k++){ i64 p=primes[k]; if(p*p>hi) break;
      i64 st=((lo+p-1)/p)*p;
      for(i64 n=st;n<=hi;n+=p){ i64 i=n-lo; int e=0; while(rem[i]%p==0){rem[i]/=p;e++;} fp[i][nf[i]]=k; fe[i][nf[i]]=e; nf[i]++; }
    }
    for(i64 i=0;i<cnt;i++){
      i64 n=lo+i; unsigned __int128 a;
      if(n==1){a=1;}
      else{
        i64 P=rem[i]>1?rem[i]:0; // largest e=1 prime candidate
        int L=0; Arr *use[12]; int nu=0;
        for(int j=0;j<nf[i];j++){ int k=fp[i][j],e=fe[i][j]; i64 p=primes[k];
          if(e==1){ if(p>P) P=p; }
          else { if(!tab[k]) tab[k]=calloc(64,sizeof(Arr));
                 if(!tab[k][e].f) tab[k][e]=build(p,e);
                 use[nu++]=&tab[k][e]; if(tab[k][e].len>L) L=tab[k][e].len; } }
        i64 Kn = P>L?P:L; a=0;
        for(i64 r=1;r<=Kn;r++){
          i64 m = (r<=P)? P-r+1 : 1;
          if(r<=L) for(int j=0;j<nu;j++) if(r<=use[j]->len && use[j]->f[r]>m) m=use[j]->f[r];
          a+=m;
          if(r>L && r<=P){ // remaining linear part closed form
            i64 t=P-r; a += (unsigned __int128)t*(t+1)/2; break; }
        }
      }
      if(n<=dump) printf("%llu ",(unsigned long long)a);
      if(n>START && a==prev){ printf("\nHIT n=%lld a=%llu\n",(long long)(n-1),(unsigned long long)a); found++; }
      if(a==(unsigned __int128)n){ /* a(n)=n: report unless n=T(p), p odd prime */
        i64 p=(i64)((sqrtl(8.0L*n+1)-1)/2); while(p*(p+1)/2<n)p++; while(p*(p+1)/2>n)p--;
        int tri = (p*(p+1)/2==n) && p>2; if(tri){ for(i64 d=2;d*d<=p;d++) if(p%d==0){tri=0;break;} }
        if(!tri) printf("\nFIX n=%lld\n",(long long)n); }
      prev=a;
    }
    fflush(stdout);
  }
  printf("\ndone N=%lld hits=%lld\n",(long long)N,(long long)found);
}
