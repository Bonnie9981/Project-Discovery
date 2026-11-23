// DISC-0016 S003: run in a browser console on any oeis.org page (2026-11-23).
// Checks every b-file term: a(n) | P = 2^D(2^s-1); counts failures of the literal comment (P | a(n)); lists a(n) = n.
const t = await (await fetch('/A085588/b085588.txt')).text();
const rows = t.split('\n').filter(l => /^\d+\s+\d+/.test(l)).map(l => l.trim().split(/\s+/));
let bad = [], lit = [], eq = [];
for (const [ns, as] of rows) {
  const n = +ns, a = BigInt(as); let D = 0, m = n; while (m % 2 == 0) { m /= 2; D++; }
  let s = 1, p = 2 % m; if (m > 1) { while (!(p == 1 || p == m - 1)) { p = (p * 2) % m; s++; } }
  const P = (1n << BigInt(D)) * ((1n << BigInt(s)) - 1n);
  if (P % a !== 0n) bad.push(n); if (a % P !== 0n) lit.push(n); if (a === BigInt(n)) eq.push(n);
}
JSON.stringify({count: rows.length, bad, litCount: lit.length, litFirst: lit.slice(0, 20), eq});
// 2026-11-23 output: count 998, bad [], litCount 174, litFirst [4,6,8,12,13,16,24,26,32,37,...], eq [7,14,15,28,...,992]
