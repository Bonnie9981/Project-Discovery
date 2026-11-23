"""CEGAR 搜尋：python -m discovery.egsat.search N [--out DIR]

UNSAT 時寫出 DIR/egN.cnf（最終公式）、egN.drat（CaDiCaL 證明）、egN.json（摘要與擋掉的圈）。
SAT 時把圖寫進 egN.json，交給 check.py 重驗。
"""
import argparse, json, os, sys, time
from pysat.solvers import Cadical195
from .encode import Enc, cycle_clause, find_cycle

FORBID = (8, 16)


def search(n, outdir=None, verbose=True):
    t0 = time.time()
    enc = Enc(n)
    clauses = enc.base()
    blocked = []
    lens = [L for L in FORBID if L <= n]
    s = Cadical195(bootstrap_with=clauses)
    graph = None
    while s.solve():
        m = set(l for l in s.get_model() if l > 0)
        adj = [set() for _ in range(n)]
        for (a, b), v in enc.idx.items():
            if v in m:
                adj[a].add(b); adj[b].add(a)
        new = 0
        for L in lens:
            # 每輪多擋幾個：重複找圈、把已擋的邊暫時移掉一條
            work = [set(x) for x in adj]
            for _ in range(50):
                c = find_cycle(work, L)
                if c is None:
                    break
                cl = cycle_clause(enc, c)
                s.add_clause(cl); clauses.append(cl); blocked.append(c); new += 1
                a, b = c[0], c[1]
                work[a].discard(b); work[b].discard(a)
        if new == 0:
            graph = sorted((a, b) for a in range(n) for b in adj[a] if a < b)
            break
    s.delete()
    res = {"n": n, "status": "SAT" if graph else "UNSAT", "base_clauses": len(clauses) - len(blocked),
           "blocked_cycles": blocked, "aux_top": enc.top, "seconds": round(time.time() - t0, 2)}
    if graph:
        res["edges"] = graph
    if outdir and not graph:
        os.makedirs(outdir, exist_ok=True)
        cnf = os.path.join(outdir, f"eg{n}.cnf")
        with open(cnf, "w") as f:
            f.write(f"p cnf {enc.top} {len(clauses)}\n")
            for c in clauses:
                f.write(" ".join(map(str, c)) + " 0\n")
        s2 = Cadical195(bootstrap_with=clauses, with_proof=True)
        assert not s2.solve()
        with open(os.path.join(outdir, f"eg{n}.drat"), "w") as f:
            for line in s2.get_proof():
                f.write(line + "\n")
        s2.delete()
    if outdir:
        with open(os.path.join(outdir, f"eg{n}.json"), "w") as f:
            json.dump(res, f)
    if verbose:
        print(n, res["status"], "blocked", len(blocked), "sec", res["seconds"], flush=True)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int, nargs="+")
    ap.add_argument("--out")
    a = ap.parse_args()
    for n in a.n:
        search(n, a.out)
