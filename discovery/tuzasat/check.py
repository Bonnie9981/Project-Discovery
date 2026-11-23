"""獨立檢查：python -m discovery.tuzasat.check DIR N K...

不 import search.py。照 docs/TUZASAT.md 自己重建基本子句，然後：
1. CNF = 基本子句（逐條相同）＋ JSON 依序列出的擋子句；
   P 子句：見證是 k+1 個三角形，兩兩沒有共用邊，子句 = 這 3(k+1) 條邊的負字面；
   C 子句：見證是 ≤ 2k 條邊的集合 C，子句 = 所有不碰 C 的三角形變數（正字面）。
2. 用 egsat 的自寫 RUP 檢查器驗 DRAT，必須推出空子句。
3. SAT 的情況：暴力算 ν 與 τ，確認 τ ≥ 2k+1 且 ν ≤ k。
"""
import itertools, json, sys
from discovery.egsat.check import RUP, read_cnf


def spec(n):
    E = list(itertools.combinations(range(n), 2))
    x = {e: i + 1 for i, e in enumerate(E)}
    T = list(itertools.combinations(range(n), 3))
    t = {tr: len(E) + 1 + i for i, tr in enumerate(T)}
    top = len(E) + len(T)
    cl = []
    for tr in T:
        a, b, c = tr
        es = [x[(a, b)], x[(a, c)], x[(b, c)]]
        for l in es:
            cl.append([-t[tr], l])
        cl.append([t[tr]] + [-l for l in es])
    for (a, b) in E:
        cl.append([-x[(a, b)]] + [t[tuple(sorted((a, b, c)))] for c in range(n) if c not in (a, b)])
    for i in range(n - 1):
        sw = {i: i + 1, i + 1: i}
        cmp = []
        for p in E:
            q = tuple(sorted((sw.get(p[0], p[0]), sw.get(p[1], p[1]))))
            if q != p:
                cmp.append((x[p], x[q]))
        eq = None
        for j, (u, w) in enumerate(cmp):
            pre = [] if eq is None else [-eq]
            cl.append(pre + [u, -w])
            if j < len(cmp) - 1:
                top += 1
                cl.append(pre + [-u, -w, top]); cl.append(pre + [u, w, top])
                eq = top
    return cl, x, t, T, top


def tri_edges(tr):
    a, b, c = sorted(tr)
    return {(a, b), (a, c), (b, c)}


def check_unsat(d, n, k):
    stem = f"{d}/tuza_{n}_{k}"
    res = json.load(open(stem + ".json"))
    nv, cls = read_cnf(stem + ".cnf")
    base, x, t, T, top = spec(n)
    assert nv == top, (nv, top)
    assert [sorted(c) for c in cls[:len(base)]] == [sorted(c) for c in base], "基本子句不符"
    rest = cls[len(base):]
    assert len(rest) == len(res["blocks"]), "擋子句數目不符"
    for c, w in zip(rest, res["blocks"]):
        if "P" in w:
            trs = [tuple(tr) for tr in w["P"]]
            assert len(trs) == k + 1 and len(set(trs)) == k + 1
            es = [tri_edges(tr) for tr in trs]
            assert all(len(a & b) == 0 for a, b in itertools.combinations(es, 2)), "P 見證有共用邊"
            want = {-x[e] for s in es for e in s}
        else:
            C = {tuple(sorted(e)) for e in w["C"]}
            assert len(C) <= 2 * k, "C 見證太大"
            want = {t[tr] for tr in T if not (tri_edges(tr) & C)}
        assert set(c) == want and len(c) == len(want), f"擋子句不符 {c}"
    r = RUP(nv)
    for c in cls:
        r.add(c)
    r.propagate(0) or setattr(r, "inconsistent", True)
    steps = 0
    with open(stem + ".drat") as f:
        for line in f:
            tok = line.split()
            if not tok:
                continue
            if tok[0] == "d":
                r.delete([int(z) for z in tok[1:-1]]); continue
            lem = [int(z) for z in tok[:-1]]
            if not r.is_rup(lem):
                raise SystemExit(f"n={n} k={k} 第 {steps} 個引理不是 RUP")
            steps += 1
            if not lem:
                print(f"n={n} k={k} 證書通過：{len(base)} 基本、{len(rest)} 擋子句、{steps} 引理")
                return True
            r.add(lem)
    if r.inconsistent:
        print(f"n={n} k={k} 證書通過（單位傳播已矛盾，{steps} 引理）"); return True
    raise SystemExit("證明沒推出空子句")


def nu_tau(n, edges):
    E = {tuple(sorted(e)) for e in edges}
    tris = [tr for tr in itertools.combinations(range(n), 3) if tri_edges(tr) <= E]
    nu = 0
    def pack(i, used, cnt):
        nonlocal nu
        nu = max(nu, cnt)
        for j in range(i, len(tris)):
            s = tri_edges(tris[j])
            if not (s & used):
                pack(j + 1, used | s, cnt + 1)
    pack(0, set(), 0)
    El = sorted(E)
    for size in range(len(El) + 1):
        for C in itertools.combinations(El, size):
            Cs = set(C)
            if all(tri_edges(tr) & Cs for tr in tris):
                return nu, size


if __name__ == "__main__":
    d, n = sys.argv[1], int(sys.argv[2])
    for k in map(int, sys.argv[3:]):
        res = json.load(open(f"{d}/tuza_{n}_{k}.json"))
        if res["status"] == "UNSAT":
            check_unsat(d, n, k)
        else:
            nu, tau = nu_tau(n, res["edges"])
            print(f"n={n} k={k} 圖：ν={nu} τ={tau}")
            if tau > 2 * nu:
                print("!!! 疑似反例，立刻人工檢查")
