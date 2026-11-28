# Always-turning walks and contact-free walks on the Manhattan lattice

Chi Hsia, 2026-11-28. (Prepared with the help of an AI assistant (Claude); to be checked by the author before any OEIS submission.)

- A189722(m), m >= 2: self-avoiding walks with m unit steps on Z^2 that turn by 90 degrees at every vertex, the first turn being to the left.
- A336662(k): k-step self-avoiding walks on the Manhattan lattice with no non-contiguous adjacencies (no two vertices at distance 1 unless consecutive on the walk).
- A337353(n): n-step self-avoiding walks on Z^2 in which no step has the same direction as the previous one.

Manhattan lattice M: the horizontal line y = Y is directed east if Y is even and west if Y is odd; the vertical line x = X is directed north if X is even and south if X is odd. At every site exactly two steps are allowed, one horizontal and one vertical.

## Theorem. A336662(k) = 2*A189722(k+1) for k >= 1; A337353(n) = 8*A189722(n) for n >= 2, and A337353(n) = 4*A336662(n-1) for n >= 1.

(The formula a(n) = 4*A336662(n) currently in A337353 is off by one; it fails for every n >= 1 in the stored data, e.g. A337353(1) = 4 but 4*A336662(1) = 8. With A322419(n) = 4*A189722(n), already in OEIS, this also gives A336662(n) = A322419(n+1)/2 and A337353(n) = 2*A322419(n) for n >= 1.)

The second statement follows from the first: a walk counted by A337353 with n >= 2 steps cannot reverse (it would revisit a vertex), so it turns at every vertex; there are 4 choices of first direction and 2 of first turn, and rotations and reflections preserve self-avoidance, so A337353(n) = 8*A189722(n); together with A336662(n-1) = 2*A189722(n) this gives 4*A336662(n-1) for n >= 2, and n = 1 is checked directly (4 = 4*1).

## Proof of A336662(k) = 2*A189722(k+1)

This is the edge-midpoint (covering-lattice) bijection between self-avoiding walks and neighbour-avoiding walks (Watson, J. Phys. C 3 (1970) L28-L30), made explicit for always-turning walks.

Let W = v_0 v_1 ... v_m (m >= 2) be a walk with unit steps e_i = v_i - v_{i-1} that turns at every vertex, normalised so that e_1 = (1,0) and the first turn is to the left (e_2 = (0,1)). Write t_i in {L, R} for the turn at v_i (i = 1..m-1), so t_1 = L, and W is determined by t_2, ..., t_{m-1}.

Midpoint walk. Put p_i = v_{i-1} + v_i (twice the midpoint of the i-th step) and q_i = A(p_i - p_1), where A(a,b) = ((a+b)/2, (a-b)/2). Since e_i is perpendicular to e_{i+1}, p_{i+1} - p_i = e_i + e_{i+1} is one of (±1,±1), and A maps these to the four unit steps. So q = q_1 ... q_m is a walk with k = m-1 unit steps starting at the origin, and q_2 - q_1 = A(1,1) = (1,0).

Step 1 (contacts). Doubled midpoints of a horizontal and a vertical step differ by (±1,±1) exactly when the two steps share an endpoint; doubled midpoints of two steps of the same kind differ by a vector with both coordinates even, so they are never at distance 1 after A (they may still share an endpoint, e.g. steps 1 and 5 of E N W S W). Also q_i = q_j iff steps i and j are the same edge. If q is not self-avoiding or has a non-contiguous adjacency, then two non-consecutive steps of W share an edge or an endpoint, so W visits a vertex twice. Conversely, if v_a = v_b with a < b, then b - a is even (Z^2 is bipartite) and b - a >= 4 (b = a + 2 would be a reversal); the steps a+1 and b both contain this vertex, are not consecutive, and since b - (a+1) is odd and W alternates horizontal and vertical steps, one of them is horizontal and the other vertical, so q_{a+1} and q_b are at distance 1. So: W is self-avoiding iff q is self-avoiding with no non-contiguous adjacencies.

Step 2 (turns of q). If t_{i+1} != t_i then e_{i+2} = e_i, so q repeats its step: q goes straight at q_{i+1}. If t_{i+1} = t_i, then e_{i+2} = -e_i and p_{i+2} - p_{i+1} = e_{i+1} - e_i, which is p_{i+1} - p_i rotated by 90 degrees towards t_i; A reverses orientation, so q turns at q_{i+1} towards the side opposite to t_i. Since t changes at every straight step of q and stays at every turn of q, t_i = L iff (i - 1) - tau_i is even, where tau_i is the number of turns of q at q_2, ..., q_i. Writing j = i for the turn of q at q_{j+1} (after j steps), q turns left there iff j + tau_j is even.

Step 3 (the Manhattan rule). Let u be a walk on M from the origin whose first step is east. At a site (X,Y) entered in direction d, the allowed turn is to the left iff X + Y + [d vertical] is even (check the four cases: east on even Y turns north iff X even; west on odd Y turns south iff X odd; north on even X turns west iff Y odd; south on odd X turns east iff Y even). After j steps X + Y has the parity of j, and d is vertical iff an odd number of turns has occurred. Going straight is always allowed. So a walk on M from the origin with first step east is the same thing as a choice, at each of its k - 1 inner vertices, of "straight" or "turn", with the turn after j steps being to the left iff j + tau_j is even.

By Steps 2 and 3, W -> q is a bijection from the normalised always-turning walks with m steps onto the walks on M with m - 1 steps from the origin starting east (both are parametrised by the same straight/turn words, with the same handedness rule), and by Step 1 it maps self-avoiding walks exactly onto the walks counted by A336662 that start east. The reflection (x,y) -> (y,x) maps M onto itself (horizontal line Y with direction east iff Y even goes to vertical line X = Y with direction north iff Y even), fixes the origin, swaps walks starting east with walks starting north and preserves contacts. Hence A336662(m-1) = 2*A189722(m). QED

## Checks

`results/A336662/code/check_a336662.py`: brute-force counts of all three families for n <= 16 (always-turning walks, contact-free Manhattan walks, walks with no repeated direction), the midpoint map applied to all 2^(m-2) normalised always-turning walks for m <= 16 (q starts east, obeys the orientation of M, and W is self-avoiding iff q is contact-free), and the relations on all terms stored in A189722, A336662, A337353 (k <= 38, n <= 39).
