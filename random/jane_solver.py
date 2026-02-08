#!/usr/bin/env python3
"""Solver for the subtiles polyomino puzzle."""
import sys, time
from collections import defaultdict

ROWS, COLS = 13, 13
PRE = {
    (0,4):15,(1,7):11,
    (2,1):15,(2,3):5,(2,6):15,(2,8):11,(2,10):11,
    (3,4):15,(3,7):8,(3,9):12,(3,11):12,
    (4,1):16,(4,5):8,(4,10):6,
    (5,3):16,(5,12):6,
    (6,2):16,(6,4):3,(6,6):16,(6,8):1,(6,10):12,
    (7,0):13,(7,9):4,
    (8,2):7,(8,7):12,(8,11):10,
    (9,1):2,(9,3):13,(9,5):16,(9,8):14,
    (10,2):13,(10,4):14,(10,6):14,(10,9):14,(10,11):10,
    (11,5):9,(12,8):9,
}
PRE_BY_K = defaultdict(set)
for pos, val in PRE.items():
    PRE_BY_K[val].add(pos)

def normalize(cells):
    mr = min(r for r,c in cells); mc = min(c for r,c in cells)
    return tuple(sorted((r-mr, c-mc) for r,c in cells))

def rot90(cells): return [(c,-r) for r,c in cells]
def refl(cells): return [(r,-c) for r,c in cells]

def canonical(cells):
    best = None; cur = list(cells)
    for _ in range(4):
        cur = rot90(cur)
        for v in [cur, refl(cur)]:
            n = normalize(v)
            if best is None or n < best: best = n
    return best

def orientations(shape):
    out = set(); cur = list(shape)
    for _ in range(4):
        cur = rot90(cur)
        out.add(normalize(cur)); out.add(normalize(refl(cur)))
    return out

def extend(shape):
    cells = set(shape); nbrs = set()
    for r,c in cells:
        for dr,dc in ((-1,0),(1,0),(0,-1),(0,1)):
            n = (r+dr,c+dc)
            if n not in cells: nbrs.add(n)
    out = set()
    for n in nbrs: out.add(canonical(list(cells)+[n]))
    return out

def can_place(shape, k):
    """Can shape be placed covering pre-placed k-cells? (ignores used cells)"""
    req = PRE_BY_K.get(k, set())
    if not req: return True
    anchor = min(req)
    for orient in orientations(shape):
        for sc in orient:
            dr,dc = anchor[0]-sc[0], anchor[1]-sc[1]
            trans = set(); ok = True
            for r,c in orient:
                gr,gc = r+dr, c+dc
                if not(0<=gr<ROWS and 0<=gc<COLS): ok=False; break
                trans.add((gr,gc))
            if not ok: continue
            if not req <= trans: continue
            if not any(cell in PRE and PRE[cell]!=k for cell in trans):
                return True
    return False

def _iter_placements(shape, k, used):
    """Yield valid placements for value k, avoiding used cells."""
    req = PRE_BY_K.get(k, set())
    anchor = min(req) if req else None
    seen = set()
    for orient in orientations(shape):
        ol = list(orient)
        if anchor:
            for sc in ol:
                dr,dc = anchor[0]-sc[0], anchor[1]-sc[1]
                trans = []; ok = True
                for r,c in ol:
                    gr,gc = r+dr, c+dc
                    if not(0<=gr<ROWS and 0<=gc<COLS) or (gr,gc) in used:
                        ok=False; break
                    trans.append((gr,gc))
                if not ok: continue
                tset = frozenset(trans)
                if tset in seen: continue
                if req <= tset and not any(cell in PRE and PRE[cell]!=k for cell in tset):
                    seen.add(tset); yield tset
        else:
            for dr in range(ROWS):
                for dc in range(COLS):
                    trans = []; ok = True
                    for r,c in ol:
                        gr,gc = r+dr, c+dc
                        if not(0<=gr<ROWS and 0<=gc<COLS) or (gr,gc) in used:
                            ok=False; break
                        trans.append((gr,gc))
                    if not ok: continue
                    tset = frozenset(trans)
                    if tset in seen: continue
                    if not any(cell in PRE and PRE[cell]!=k for cell in tset):
                        seen.add(tset); yield tset

def find_placements(shape, k, used):
    return list(_iter_placements(shape, k, used))

def has_placement_with_used(shape, k, used):
    return any(True for _ in _iter_placements(shape, k, used))

def solve(N=16):
    t0 = time.time()

    # Phase 1: precompute valid shapes per level
    print("Phase 1: valid shapes per level", file=sys.stderr)
    valid = {1: {canonical([(0,0)])}}
    for k in range(2, N+1):
        vk = set()
        for prev in valid[k-1]:
            for ext in extend(prev):
                if ext not in vk and can_place(ext, k):
                    vk.add(ext)
        valid[k] = vk
        print(f"  K={k:2d}: {len(vk):6d} shapes  [{time.time()-t0:.1f}s]", file=sys.stderr)
        if not vk:
            print("  DEAD END!", file=sys.stderr); return

    # Phase 1b: backward reachability pruning
    print("\nPhase 1b: backward pruning", file=sys.stderr)
    reachable = {N: valid[N]}
    for k in range(N-1, 0, -1):
        rk = set()
        for shape in valid[k]:
            if extend(shape) & reachable[k+1]:
                rk.add(shape)
        reachable[k] = rk
        print(f"  K={k:2d}: {len(rk):6d} reachable  (was {len(valid[k])})", file=sys.stderr)
    valid = reachable  # Replace with pruned sets

    # Phase 2: precompute placements and extensions
    print("\nPhase 2: precomputing placements & extensions", file=sys.stderr)
    all_pl = {}   # (shape, k) -> list of frozenset placements
    next_sh = {}  # (shape, k) -> list of valid shapes at k+1
    for k in range(1, N+1):
        for shape in valid[k]:
            all_pl[(shape, k)] = find_placements(shape, k, frozenset())
            if k < N:
                next_sh[(shape, k)] = sorted(extend(shape) & valid[k+1])
    print(f"  done [{time.time()-t0:.1f}s]", file=sys.stderr)

    # Phase 3: backtracking
    print("\nPhase 3: backtracking", file=sys.stderr)
    nodes = [0]
    total_needed = [0]*(N+2)
    for k in range(N, 0, -1): total_needed[k] = total_needed[k+1] + k

    def bt(k, prev_shape, used, assign):
        nodes[0] += 1
        if nodes[0] % 50000 == 0:
            print(f"  k={k} nodes={nodes[0]} [{time.time()-t0:.1f}s]", file=sys.stderr)
        if k > N: return True
        if ROWS*COLS - len(used) < total_needed[k]: return False

        for shape in next_sh.get((prev_shape, k-1), []):
            pls = [p for p in all_pl[(shape, k)] if not (p & used)]
            for pl in pls:
                new_used = used | pl
                # Look-ahead: check k+1 has at least one valid placement
                if k < N:
                    if not any(p for ns in next_sh.get((shape, k), [])
                               for p in all_pl[(ns, k+1)] if not (p & new_used)):
                        continue
                assign[k] = (shape, pl)
                if bt(k+1, shape, new_used, assign): return True
                del assign[k]
        return False

    s1 = canonical([(0,0)]); p1 = frozenset({(6,8)})
    assign = {1: (s1, p1)}

    if bt(2, s1, p1, assign):
        print(f"\nSOLVED! {nodes[0]} nodes, {time.time()-t0:.1f}s\n")
        grid = [[0]*COLS for _ in range(ROWS)]
        for k,(_,pl) in assign.items():
            for r,c in pl: grid[r][c] = k
        for r in range(ROWS):
            print(' '.join(f'{grid[r][c]:2d}' if grid[r][c] else ' .' for c in range(COLS)))
        rsums = [sum(grid[r]) for r in range(ROWS)]
        print(f"\nRow sums: {rsums}")
        print(f"Answer: {min(rsums)} * {max(rsums)} = {min(rsums)*max(rsums)}")
    else:
        print(f"No solution. {nodes[0]} nodes, {time.time()-t0:.1f}s")

if __name__ == '__main__':
    solve()
