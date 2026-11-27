// k such that every binary index j of k (bit j-1 set) has prime(j) | k.  Exhaustive for bit length <= LMAX.
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
static u64 P[200]; static int LMAX; static long long nodes=0, hits=0;
static void pr(u128 x){char b[50];int i=49;b[i]=0;if(!x){printf("0");return;}while(x){b[--i]='0'+(int)(x%10);x/=10;}printf("%s",b+i);}
static int full_ok(u128 k){ for(int j=1;j<=LMAX && (k>>(j-1));j++) if((k>>(j-1))&1){ if(k%P[j]) return 0;} return 1;}
static void dfs(int r, u128 v, u128 M){ // positions 1..r undecided
  nodes++;
  u128 lo=v<<r, span=((u128)1)<<r;
  if(span/M < 8){ u128 k=lo+(M-lo%M)%M; for(;k<lo+span;k+=M){ if(full_ok(k)){hits++; pr(k); printf("\n"); fflush(stdout);} } return; }
  dfs(r-1, v<<1, M);
  dfs(r-1, (v<<1)|1, M*P[r]);
}
int main(int c,char**argv){LMAX=atoi(argv[1]); int n=0; for(u64 x=2;n<LMAX+1;x++){int ok=1;for(u64 d=2;d*d<=x;d++)if(x%d==0){ok=0;break;} if(ok)P[++n]=x;}
 for(int L=1;L<=LMAX;L++) dfs(L-1,1,P[L]);
 fprintf(stderr,"LMAX=%d nodes=%lld hits=%lld\n",LMAX,nodes,hits);}
