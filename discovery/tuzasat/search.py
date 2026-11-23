"""Tuza 猜想（τ ≤ 2ν）小範圍反例搜尋：python -m discovery.tuzasat.search N K... [--out DIR]

對固定 n、k 找 n 點圖 G：ν(G) ≤ k 且 τ(G) ≥ 2k+1（就是反例）。
外層 SAT 出候選圖，內層兩個小 SAT：
  找到 k+1 個邊互斥三角形 → 擋「這些邊全有」（P 子句）；
  找到 ≤ 2k 條邊的三角形覆蓋 C → 要求「至少一個不碰 C 的三角形存在」（C 子句）。
UNSAT 時寫出 DIR/tuza_n_k.cnf、.drat（CaDiCaL）、.json（每條擋子句的見證），交給 check.py。
編號規格見 docs/TUZASAT.md。
"""
import argparse, itertools, json, os, time
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


class Enc:
    def __init__(self, n):
        self.n = n
        self.E = list(itertools.combinations(range(n), 2))
        self.x = {e: i + 1 for i, e in enumerate(self.E)}
        self.T = list(itertools.combinations(range(n), 3))
        self.t = {tr: len(self.E) + 1 + i for i, tr in enumerate(self.T)}
        self.top = len(self.E) + len(self.T)

    @staticmethod
    def tedges(tr):
        a, b, c = tr
        return ((a, b), (a, c), (b, c))

    def base(self):
        n, x, t = self.n, self.x, self.t
        cl = []
        for tr in self.T:  # TRI: t <-> 三條邊都在
            es = [x[e] for e in self.tedges(tr)]
            cl += [[-t[tr], l] for l in es]
            cl.append([t[tr]] + [-l for l in es])
        for (a, b) in self.E:  # INT: 每條邊都在某個三角形裡
            cl.append([-x[(a, b)]] + [t[tuple(sorted((a, b, c)))] for c in range(n) if c not in (a, b)])
        keys = self.E  # LEX：和 egsat 同一個構造
        for i in range(n - 1):
            def sw(v):
                return i + 1 if v == i else (i if v == i + 1 else v)
            cmp = [(x[p], x[tuple(sorted((sw(p[0]), sw(p[1]))))]) for p in keys if {sw(p[0]), sw(p[1])} != set(p)]
            eq = None
            for j, (u, w) in enumerate(cmp):
                pre = [] if eq is None else [-eq]
                cl.append(pre + [u, -w])
                if j < len(cmp) - 1:
                    self.top += 1
                    cl.append(pre + [-u, -w, self.top])
                    cl.append(pre + [u, w, self.top])
                    eq = self.top
        return cl


def _packing(tris, size):
    pool = IDPool(); tv = {tr: pool.id(tr) for tr in tris}
    byedge = {}
    for tr in tris:
        for e in Enc.tedges(tr):
            byedge.setdefault(e, []).append(tv[tr])
    cl = []
    for lits in byedge.values():
        if len(lits) > 1:
            cl += CardEnc.atmost(lits, 1, vpool=pool, encoding=EncType.seqcounter).clauses
    cl += CardEnc.atleast(list(tv.values()), size, vpool=pool, encoding=EncType.totalizer).clauses
    with Cadical195(bootstrap_with=cl) as s:
        if s.solve():
            m = set(l for l in s.get_model() if l > 0)
            return [tr for tr in tris if tv[tr] in m][:size]
    return None


def _cover(edges, tris, bound):
    pool = IDPool(); ev = {e: pool.id(e) for e in edges}
    cl = [[ev[e] for e in Enc.tedges(tr)] for tr in tris]
    cl += CardEnc.atmost([ev[e] for e in edges], bound, vpool=pool, encoding=EncType.totalizer).clauses
    with Cadical195(bootstrap_with=cl) as s:
        if s.solve():
            m = set(l for l in s.get_model() if l > 0)
            return [e for e in edges if ev[e] in m]
    return None


def search(n, k, outdir=None, verbose=True, cover_bound=None):
    # cover_bound 只給測試用（放寬成 τ > cover_bound，用來確認找得到 K4 這種緊例）
    cb = 2 * k if cover_bound is None else cover_bound
    t0 = time.time()
    enc = Enc(n)
    clauses = enc.base()
    nbase = len(clauses)
    blocks = []
    s = Cadical195(bootstrap_with=clauses)
    graph = None
    while s.solve():
        m = set(l for l in s.get_model() if l > 0)
        edges = [e for e in enc.E if enc.x[e] in m]
        tris = [tr for tr in enc.T if enc.t[tr] in m]
        P = _packing(tris, k + 1) if tris else None
        if P is not None:
            cl = sorted({-enc.x[e] for tr in P for e in enc.tedges(tr)})
            blocks.append({"P": [list(tr) for tr in P]})
        else:
            C = _cover(edges, tris, cb) if tris else []
            if C is None:
                graph = edges
                break
            Cs = set(C)
            cl = [enc.t[tr] for tr in enc.T if not (set(enc.tedges(tr)) & Cs)]
            blocks.append({"C": [list(e) for e in C]})
        s.add_clause(cl); clauses.append(cl)
    s.delete()
    res = {"n": n, "k": k, "status": "SAT" if graph else "UNSAT", "base_clauses": nbase,
           "blocks": blocks, "top": enc.top, "seconds": round(time.time() - t0, 2)}
    if graph:
        res["edges"] = graph
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        stem = os.path.join(outdir, f"tuza_{n}_{k}")
        if not graph:
            with open(stem + ".cnf", "w") as f:
                f.write(f"p cnf {enc.top} {len(clauses)}\n")
                for c in clauses:
                    f.write(" ".join(map(str, c)) + " 0\n")
            s2 = Cadical195(bootstrap_with=clauses, with_proof=True)
            assert not s2.solve()
            with open(stem + ".drat", "w") as f:
                for line in s2.get_proof():
                    f.write(line + "\n")
            s2.delete()
        with open(stem + ".json", "w") as f:
            json.dump(res, f)
    if verbose:
        print(f"n={n} k={k} {res['status']} 擋子句 {len(blocks)} 秒 {res['seconds']}", flush=True)
    return res


def kmax(n):
    # τ ≤ m/2 ≤ n(n-1)/4，所以反例要 2k+1 ≤ n(n-1)/4
    return (n * (n - 1) // 4 - 1) // 2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("k", type=int, nargs="*")
    ap.add_argument("--out")
    a = ap.parse_args()
    for k in (a.k or range(1, kmax(a.n) + 1)):
        search(a.n, k, a.out)
