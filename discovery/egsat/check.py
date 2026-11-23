"""獨立檢查：python -m discovery.egsat.check DIR N

不 import encode.py／search.py。三件事：
1. 照 docs/EGSAT.md 的規格自己重建基本子句，確認 CNF 裡的子句 = 基本子句 ∪ 擋圈子句，
   而且每條擋圈子句都真的是 K_n 裡一個長度 4、8 或 16 的簡單圈。
2. 用自寫的正向 RUP 檢查器驗 CaDiCaL 的 DRAT 證明，最後必須推出空子句。
   刪除行只讓子句停用，已推出的單位結論保留（都由原公式推出，不影響正確性）；
   不接受 RAT 步驟（遇到非 RUP 的引理直接失敗）。
3. SAT 的情況：直接檢查圖的最小度和有沒有 4、8、16 圈（暴力 DFS）。
"""
import itertools, json, sys


def spec_clauses(n):
    num = {}
    for a in range(n):
        for b in range(a + 1, n):
            num[(a, b)] = len(num) + 1
    E = len(num)

    def x(a, b):
        return num[(min(a, b), max(a, b))]

    out = set()
    for v in range(n):
        nb = [u for u in range(n) if u != v]
        for drop in itertools.combinations(nb, 2):
            out.add(frozenset(x(v, u) for u in nb if u not in drop))
        for four in itertools.combinations(nb, 4):
            out.add(frozenset([-(E + 1 + v)] + [-x(v, u) for u in four]))
    for (a, b), k in num.items():
        out.add(frozenset([-k, E + 1 + a, E + 1 + b]))
    nxt = E + n
    keys = sorted(num, key=num.get)
    for i in range(n - 1):
        def sw(t):
            return i + 1 if t == i else (i if t == i + 1 else t)
        cmp = [(num[p], x(sw(p[0]), sw(p[1]))) for p in keys if {sw(p[0]), sw(p[1])} != set(p)]
        eq = None
        for j, (u, w) in enumerate(cmp):
            pre = [] if eq is None else [-eq]
            out.add(frozenset(pre + [u, -w]))
            if j < len(cmp) - 1:
                nxt += 1
                out.add(frozenset(pre + [-u, -w, nxt]))
                out.add(frozenset(pre + [u, w, nxt]))
                eq = nxt
    return out, num, nxt


def is_cycle_clause(cl, inv):
    if any(l > 0 for l in cl):
        return False
    edges = []
    for l in cl:
        if -l not in inv:
            return False
        edges.append(inv[-l])
    L = len(edges)
    if L not in (4, 8, 16):
        return False
    deg = {}
    for a, b in edges:
        deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
    if len(deg) != L or any(d != 2 for d in deg.values()):
        return False
    # 連通 = 單一圈
    adj = {v: [] for v in deg}
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    seen, st = set(), [edges[0][0]]
    while st:
        v = st.pop()
        if v not in seen:
            seen.add(v); st.extend(adj[v])
    return len(seen) == L


def read_cnf(path):
    cls = []
    with open(path) as f:
        head = f.readline().split()
        nv = int(head[2])
        for line in f:
            t = list(map(int, line.split()))
            assert t[-1] == 0
            cls.append(t[:-1])
    return nv, cls


class RUP:
    def __init__(self, nv):
        self.val = [0] * (nv + 1)
        self.trail = []
        self.cls = []
        self.alive = []
        self.watch = {}
        self.byKey = {}
        self.inconsistent = False

    def v(self, l):
        x = self.val[abs(l)]
        return x if l > 0 else -x

    def assign(self, l):
        self.val[abs(l)] = 1 if l > 0 else -1
        self.trail.append(l)

    def propagate(self, start):
        i = start
        while i < len(self.trail):
            fl = -self.trail[i]  # 變成假的字面
            i += 1
            ws = self.watch.get(fl, [])
            keep = []
            conflict = False
            for k, ci in enumerate(ws):
                if conflict or not self.alive[ci]:
                    if conflict:
                        keep.append(ci)
                    continue
                c = self.cls[ci]
                if c[0] == fl:
                    c[0], c[1] = c[1], c[0]
                if self.v(c[0]) == 1:
                    keep.append(ci); continue
                moved = False
                for j in range(2, len(c)):
                    if self.v(c[j]) != -1:
                        c[1], c[j] = c[j], c[1]
                        self.watch.setdefault(c[1], []).append(ci)
                        moved = True
                        break
                if moved:
                    continue
                keep.append(ci)
                if self.v(c[0]) == -1:
                    conflict = True
                else:
                    self.assign(c[0])
            self.watch[fl] = keep
            if conflict:
                return False
        return True

    def add(self, lits):
        c = list(dict.fromkeys(lits))
        if self.inconsistent:
            return
        if any(-l in c for l in c):
            return
        c.sort(key=lambda l: {1: 0, 0: 1, -1: 2}[self.v(l)])
        if not c or self.v(c[0]) == -1:
            self.inconsistent = True
            return
        if len(c) == 1 or self.v(c[1]) == -1:
            if self.v(c[0]) == 0:
                st = len(self.trail)
                self.assign(c[0])
                if not self.propagate(st):
                    self.inconsistent = True
            if len(c) == 1:
                return
        ci = len(self.cls)
        self.cls.append(c); self.alive.append(True)
        self.watch.setdefault(c[0], []).append(ci)
        self.watch.setdefault(c[1], []).append(ci)
        self.byKey.setdefault(frozenset(c), []).append(ci)

    def delete(self, lits):
        ids = self.byKey.get(frozenset(lits))
        if ids:
            self.alive[ids.pop()] = False

    def is_rup(self, lits):
        if self.inconsistent:
            return True
        st = len(self.trail)
        ok = False
        for l in lits:
            x = self.v(l)
            if x == 1:
                ok = True; break
            if x == 0:
                self.assign(-l)
        if not ok:
            ok = not self.propagate(st)
        for l in self.trail[st:]:
            self.val[abs(l)] = 0
        del self.trail[st:]
        return ok


def check_unsat(d, n):
    nv, cls = read_cnf(f"{d}/eg{n}.cnf")
    base, num, top = spec_clauses(n)
    inv = {k: p for p, k in num.items()}
    assert nv == top, (nv, top)
    seen = set()
    ncyc = 0
    for c in cls:
        fc = frozenset(c)
        if fc in base:
            seen.add(fc)
        elif is_cycle_clause(c, inv):
            ncyc += 1
        else:
            raise SystemExit(f"不明子句 {c}")
    assert seen == base, "少了基本子句"
    r = RUP(nv)
    for c in cls:
        r.add(c)
    r.propagate(0) or setattr(r, "inconsistent", True)
    steps = 0
    with open(f"{d}/eg{n}.drat") as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] == "d":
                r.delete([int(z) for z in t[1:-1]]); continue
            lem = [int(z) for z in t[:-1]]
            if not r.is_rup(lem):
                raise SystemExit(f"第 {steps} 個引理不是 RUP：{lem}")
            steps += 1
            if not lem:
                print(f"n={n} 證書通過：{len(base)} 基本子句、{ncyc} 擋圈子句、{steps} 個 RUP 引理")
                return True
            r.add(lem)
    if r.inconsistent:
        print(f"n={n} 證書通過：證明檔沒寫到空子句，但單位傳播已經矛盾（{steps} 個 RUP 引理）"); return True
    raise SystemExit("證明沒推出空子句")


def check_sat(d, n):
    res = json.load(open(f"{d}/eg{n}.json"))
    adj = {v: set() for v in range(n)}
    for a, b in res["edges"]:
        adj[a].add(b); adj[b].add(a)
    mind = min(len(s) for s in adj.values())
    bad = []
    for L in (4, 8, 16):
        for s in range(n):
            def go(path):
                if len(path) == L:
                    return path[0] in adj[path[-1]]
                return any(go(path + [w]) for w in adj[path[-1]] if w > path[0] and w not in path)
            if go([s]):
                bad.append(L); break
    print(f"n={n} 圖：最小度 {mind}，含有的禁止圈長 {bad}")
    return mind >= 3 and not bad


if __name__ == "__main__":
    d = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        st = json.load(open(f"{d}/eg{n}.json"))["status"]
        ok = check_unsat(d, n) if st == "UNSAT" else check_sat(d, n)
        if st == "SAT" and ok:
            print("!!! 疑似反例，立刻人工檢查")
