"""SAT 編碼：n 點、最小度 >= 3、沒有長度 4/8/16 的圈。

變數編號規格（checker 會獨立重建，改這裡要同步改 docs/EGSAT.md）：
  e(a,b), a<b：按列優先排的上三角位置 + 1，共 E = n(n-1)/2 個。
  d(i) = E + 1 + i：d(i) 為真表示 deg(i) <= 3（只有單向）。
  字典序對稱破缺的輔助變數從 E + n + 1 起，依 i = 0..n-2、比較位置 k = 1.. 依序編號。

子句家族（全部對「邊極小 + 字典序最大標號」的反例成立，所以 UNSAT 表示沒有反例）：
  DEG  每點度 >= 3：對每個點 v 和另外任兩點 T，{e(v,u) : u 不在 T∪{v}} 至少一條。
  C4   每個 4 圈的四條邊不能全有。
  MIN  邊極小：e(a,b) -> d(a) 或 d(b)；d(v) -> v 的任四條邊不全有。
  LEX  相鄰對換 (i,i+1) 的字典序最大：上三角向量 >=lex 對換後的向量。
  CYC  CEGAR 過程中找到的 8 圈、16 圈，四邊（八邊…）不能全有。
"""
from itertools import combinations


def pairs(n):
    return [(a, b) for a in range(n) for b in range(a + 1, n)]


class Enc:
    def __init__(self, n):
        self.n = n
        self.idx = {p: i + 1 for i, p in enumerate(pairs(n))}
        self.E = len(self.idx)
        self.top = self.E + n

    def e(self, a, b):
        return self.idx[(a, b) if a < b else (b, a)]

    def d(self, i):
        return self.E + 1 + i

    def deg(self):
        n = self.n
        for v in range(n):
            others = [u for u in range(n) if u != v]
            for T in combinations(others, 2):
                yield [self.e(v, u) for u in others if u not in T]

    def c4(self):
        for q in combinations(range(self.n), 4):
            a, b, c, d = q
            for cyc in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
                yield cycle_clause(self, cyc)

    def minimal(self):
        n = self.n
        for a, b in pairs(n):
            yield [-self.e(a, b), self.d(a), self.d(b)]
        for v in range(n):
            others = [u for u in range(n) if u != v]
            for F in combinations(others, 4):
                yield [-self.d(v)] + [-self.e(v, u) for u in F]

    def lex(self):
        n = self.n
        order = pairs(n)
        for i in range(n - 1):
            sw = {i: i + 1, i + 1: i}
            seq = []
            for (a, b) in order:
                a2, b2 = sw.get(a, a), sw.get(b, b)
                q = (min(a2, b2), max(a2, b2))
                if q != (a, b):
                    seq.append((self.e(a, b), self.e(*q)))
            prev = None  # None 代表「前綴相等」恆真
            for k, (x, y) in enumerate(seq):
                g = [] if prev is None else [-prev]
                yield g + [x, -y]  # 前綴相等 -> x >= y
                if k + 1 < len(seq):
                    self.top += 1
                    a = self.top
                    yield g + [-x, -y, a]
                    yield g + [x, y, a]
                    prev = a

    def base(self):
        out = []
        for fam in (self.deg, self.c4, self.minimal, self.lex):
            out.extend(fam())
        return out


def cycle_clause(enc, cyc):
    L = len(cyc)
    return [-enc.e(cyc[j], cyc[(j + 1) % L]) for j in range(L)]


def find_cycle(adj, L):
    """回傳一個長度恰好 L 的簡單圈（點列），沒有就回 None。從最小點起頭避免重複。"""
    n = len(adj)
    for s in range(n):
        path = [s]
        onpath = {s}

        def dfs(v):
            if len(path) == L:
                return s in adj[v]
            for w in adj[v]:
                if w > s and w not in onpath:
                    path.append(w); onpath.add(w)
                    if dfs(w):
                        return True
                    path.pop(); onpath.discard(w)
            return False

        if dfs(s):
            return list(path)
    return None
