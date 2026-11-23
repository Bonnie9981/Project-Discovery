/* b(k) = -b(k-1)-b(k-2)+b(k-3)-b(k-4), b0..3 = 2,1,0,-1. For n<=N: check b(n)==1 mod n. compare with primes x^2+55y^2 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef unsigned long long u64; typedef __uint128_t u128; typedef long long ll;
static u64 M;
static void mul(u64 A[4][4],u64 B[4][4],u64 C[4][4]){u64 T[4][4];for(int i=0;i<4;i++)for(int j=0;j<4;j++){u128 s=0;for(int k=0;k<4;k++)s+=(u128)A[i][k]*B[k][j];T[i][j]=s%M;}for(int i=0;i<4;i++)for(int j=0;j<4;j++)C[i][j]=T[i][j];}
static u64 bmod(u64 n,u64 m){ M=m; if(m==1) return 0; /* state (b(k+3),b(k+2),b(k+1),b(k)) */
 u64 A[4][4]={{m-1,m-1,1%m,m-1},{1,0,0,0},{0,1,0,0},{0,0,1,0}}; u64 R[4][4]={{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}};
 for(int i=0;i<4;i++)for(int j=0;j<4;j++){A[i][j]%=m;R[i][j]%=m;}
 if(n<=3){ ll v[4]={2,1,0,-1}; ll x=v[n]%(ll)m; if(x<0)x+=m; return x;}
 u64 e=n-3; while(e){ if(e&1)mul(R,A,R); mul(A,A,A); e>>=1; }
 ll s0[4]={-1,0,1,2}; /* b3,b2,b1,b0 */ u128 s=0; for(int j=0;j<4;j++){ ll x=s0[j]%(ll)m; if(x<0)x+=m; s+=(u128)R[0][j]*(u64)x; } return s%m; }
int main(int c,char**v){ ll N=atoll(v[1]);
 char *comp=calloc(N+1,1); for(ll i=2;i*i<=N;i++) if(!comp[i]) for(ll j=i*i;j<=N;j+=i) comp[j]=1;
 char *form=calloc(N+1,1); for(ll y=1;55*y*y<=N;y++) for(ll x=0;x*x+55*y*y<=N;x++) form[x*x+55*y*y]=1;
 ll np=0,nc=0,mis=0;
 for(ll n=1;n<=N;n++){ int sol = bmod(n,n)==1%n; int pr = n>1&&!comp[n];
  if(sol&&!pr){ nc++; printf("nonprime sol %lld\n",n);} if(sol&&pr) np++;
  if(pr && (sol != form[n])){ mis++; if(mis<50) printf("MISMATCH prime %lld sol=%d form=%d\n",n,sol,form[n]); } }
 printf("N=%lld primesol=%lld nonprimesol=%lld mismatches=%lld\n",N,np,nc,mis); }
