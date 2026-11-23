// Independent critic implementation (Go). Does not use project code.
// mulmod via bits.Mul64 + bits.Rem64; exponentiation left-to-right (MSB first).
package main

import (
	"fmt"
	"math/big"
	"math/bits"
	"os"
	"strconv"
	"sync"
)

func mulmod(a, b, m uint64) uint64 { h, l := bits.Mul64(a, b); return bits.Rem64(h, l, m) }

// left-to-right binary exponentiation
func powL(b, e, m uint64) uint64 {
	if m == 1 { return 0 }
	r := uint64(1); b %= m
	for i := 63; i >= 0; i-- {
		r = mulmod(r, r, m)
		if (e>>uint(i))&1 == 1 { r = mulmod(r, b, m) }
	}
	return r
}

// a(n) by definition: least k>0 with k*2^(2n) == 1 mod 2n+1, via big.Int and ext. Euclid
func aBig(n *big.Int) *big.Int {
	m := new(big.Int).Add(new(big.Int).Lsh(n, 1), big.NewInt(1))
	// 2^(2n) mod m by repeated squaring on big ints, MSB first
	e := new(big.Int).Lsh(n, 1); x := big.NewInt(1); two := big.NewInt(2)
	for i := e.BitLen() - 1; i >= 0; i-- {
		x.Mul(x, x).Mod(x, m)
		if e.Bit(i) == 1 { x.Mul(x, two).Mod(x, m) }
	}
	// extended Euclid
	r0, r1 := new(big.Int).Set(m), new(big.Int).Set(x)
	s0, s1 := big.NewInt(0), big.NewInt(1)
	for r1.Sign() != 0 {
		q := new(big.Int).Div(r0, r1)
		r0, r1 = r1, new(big.Int).Sub(r0, new(big.Int).Mul(q, r1))
		s0, s1 = s1, new(big.Int).Sub(s0, new(big.Int).Mul(q, s1))
	}
	if r0.Cmp(big.NewInt(1)) != 0 { panic("not invertible") }
	return s0.Mod(s0, m)
}

// brute: all odd m in [3,B), test m | c*2^(m-1)+1 ; also cases c=-2 style for a=2, a=2n
func brute(B uint64, c uint64) []uint64 {
	var mu sync.Mutex; var out []uint64; var wg sync.WaitGroup
	W := uint64(4)
	for w := uint64(0); w < W; w++ {
		wg.Add(1)
		go func(w uint64) {
			defer wg.Done()
			for m := 3 + 2*w; m < B; m += 2 * W {
				x := powL(2, m-1, m)
				if (mulmod(c%m, x, m)+1)%m == 0 { mu.Lock(); out = append(out, m); mu.Unlock() }
			}
		}(w)
	}
	wg.Wait(); return out
}

func isqrt(n uint64) uint64 { r := uint64(1); for (r+1)*(r+1) <= n { r++ }; return r }

// generic structural scan: m <= M composite with least prime p, m=p*k, k>=p odd.
// condition mod p: c*2^(k-1) == -1  <=> 2^(k-1) == t := -1/c mod p.
// plus prime m: m | c+1.
var mod6 bool
var skipped int
func gcdu(a, b uint64) uint64 { for b != 0 { a, b = b, a%b }; return a }
func scan(M uint64, c uint64) ([]uint64, []uint64) {
	L := isqrt(M)
	sieve := make([]bool, L+1)
	var adm []uint64
	var hits []uint64
	for p := uint64(3); p <= L; p += 2 {
		if sieve[p] { continue }
		for q := p * p; q <= L; q += p { sieve[q] = true }
		if c%p == 0 { continue }
		// t = -c^{-1} mod p via Fermat
		inv := powL(c%p, p-2, p); t := (p - inv) % p
		// walk powers of 2: find order d and first r with 2^r == t
		x := uint64(1); r := int64(-1); var d uint64
		for j := uint64(0); ; j++ {
			if x == t && r < 0 { r = int64(j) }
			x <<= 1; if x >= p { x -= p }
			if x == 1 { d = j + 1; break }
		}
		if r < 0 { continue }
		if mod6 && p%6 != 1 { continue }
		adm = append(adm, p)
		// k ≡ 1+r (mod d) and k odd (generic) or k ≡ 1 (mod 6) (mod6 mode); CRT by search
		mod := uint64(2); res := uint64(1)
		if mod6 { mod = 6 }
		step := d / gcdu(d, mod) * mod
		k := uint64(0); found := false
		for kk := (1 + uint64(r)) % d; kk < step+d; kk += d { if kk%mod == res { k = kk; found = true; break } }
		if !found { skipped++; continue }
		fmt.Fprintln(os.Stderr, p, d, r)
		for k < p { k += step }
		var wg sync.WaitGroup; var mu sync.Mutex
		for w := uint64(0); w < 4; w++ {
			wg.Add(1)
			go func(k0 uint64) {
				defer wg.Done()
				for kk := k0; kk <= M/p; kk += 4 * step {
					m := p * kk
					if (mulmod(c%m, powL(2, m-1, m), m)+1)%m == 0 { mu.Lock(); hits = append(hits, m); mu.Unlock() }
				}
			}(k + w*step)
		}
		wg.Wait()
	}
	fmt.Println("primes with no compatible k class:", skipped)
	// prime m dividing c+1 (m odd >=3)
	for q := uint64(3); q <= c+1 && q <= M; q += 2 {
		if (c+1)%q == 0 { if (mulmod(c%q, powL(2, q-1, q), q)+1)%q == 0 { hits = append(hits, q) } }
	}
	return hits, adm
}

func main() {
	switch os.Args[1] {
	case "verify":
		n, _ := new(big.Int).SetString("9814447404", 10)
		a := aBig(n)
		want := new(big.Int).Sub(new(big.Int).Lsh(n, 1), big.NewInt(2))
		fmt.Println("a(n) =", a, "2n-2 =", want, "equal:", a.Cmp(want) == 0)
		fmt.Println("367*53484727 =", uint64(367)*53484727)
		m := uint64(19628894809)
		fmt.Println("uint64 path (3*2^(m-1)+1) mod m =", (mulmod(3, powL(2, m-1, m), m)+1)%m)
		s := ""
		for k := int64(1); k <= 30; k++ { s += aBig(big.NewInt(k)).String() + "," }
		fmt.Println("a(1..30):", s)
	case "brute":
		B, _ := strconv.ParseUint(os.Args[2], 10, 64); c, _ := strconv.ParseUint(os.Args[3], 10, 64)
		h := brute(B, c); fmt.Println("brute c=", c, "B=", B, "hits:", h)
	case "scan":
		mod6 = len(os.Args) > 4
		M, _ := strconv.ParseUint(os.Args[2], 10, 64); c, _ := strconv.ParseUint(os.Args[3], 10, 64)
		h, adm := scan(M, c)
		fmt.Println("scan c=", c, "M=", M, "hits:", h, "#admissible primes:", len(adm))
		if len(adm) > 12 { adm = adm[:12] }
		fmt.Println("first admissible:", adm)
	}
}
