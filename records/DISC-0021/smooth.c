/* enumerate B-smooth numbers <= X, sort, output consecutive pairs (n,n+1) */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
static u64 *buf; static size_t cnt=0, cap=0; static u64 X; static int pr[32], np;
static void gen(int i, u64 v){ if(i==np){ if(cnt==cap){cap=cap?cap*2:1<<20; buf=realloc(buf,cap*8);} buf[cnt++]=v; return; }
  u64 x=v; for(;;){ gen(i+1,x); if(x> X/pr[i]) break; x*=pr[i]; } }
static int cmp(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
int main(int c,char**v){ int B=atoi(v[1]); X=strtoull(v[2],0,10);
 for(int p=2;p<=B;p++){int ok=1;for(int d=2;d*d<=p;d++)if(p%d==0)ok=0; if(ok)pr[np++]=p;}
 gen(0,1); qsort(buf,cnt,8,cmp); fprintf(stderr,"count=%zu\n",cnt);
 size_t pairs=0; for(size_t i=0;i+1<cnt;i++) if(buf[i+1]==buf[i]+1){ printf("%llu\n",buf[i]); pairs++; }
 fprintf(stderr,"pairs=%zu max=%llu\n",pairs,pairs?0ULL:0ULL); }
