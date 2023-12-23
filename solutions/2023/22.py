import numpy as np
import networkx as nx


def parse_input(data):
    return [[list(map(int, l.split(","))) for l in d.split("~")] for d in data.split("\n")]


def convert_coords(sand_blocks):
    max_r = 0
    max_c = 0
    max_d = 0
    block_coords = []
    for i, ((sx, sy, sz), (ex, ey, ez)) in enumerate(sand_blocks):
        xr = ex - sx
        yr = ey - sy
        zr = ez - sz
        if max((sz, ez)) > max_r:
            max_r = max((sz, ez))
        if max((sx, ex)) > max_c:
            max_c = max((sx, ex))
        if max((sy, ey)) > max_d:
            max_d = max((sy, ey))
        this_block = []
        for dz in range(zr + 1):
            this_block.append((sz + dz, sx, sy))
        for dx in range(xr + 1):
            this_block.append((sz, sx + dx, sy))
        for dy in range(yr + 1):
            this_block.append((sz, sx, sy + dy))
        block_coords.append(list(set(this_block)))
    return block_coords, (max_r, max_c, max_d)


def fill_space(block_coords, maxes):
    max_r, max_c, max_d = maxes
    space = np.zeros((max_r + 1, max_c + 1, max_d + 1))
    space[0, :, :] = np.inf
    for i, points in zip(range(1, len(block_coords) + 1), block_coords):
        for p in points:
            space[p] = i
    return space


def gravity(space):
    drop = set()
    last_locs = set(map(tuple, np.argwhere(space != 0)))
    while True:
        for r in range(space.shape[0] - 1):
            level_blocks = set(np.unique(space[r + 1, :, :].flatten())) - set((0,))
            for b in level_blocks:
                where = np.where(space[r + 1, :, :] == b)
                if not space[r, where[0], where[1]].any():
                    space[r, where[0], where[1]] = b
                    space[r + 1, where[0], where[1]] = 0
                    drop.add(b)
        if set(map(tuple, np.argwhere(space != 0))) == last_locs:
            break
        else:
            last_locs = set(map(tuple, np.argwhere(space != 0)))
    return space, len(drop)


def block_graph(space):
    S = nx.DiGraph()
    for r in range(space.shape[0] - 1):
        level_blocks = set(np.unique(space[r, :, :].flatten())) - set((0,))
        for b in level_blocks:
            where = np.where(space[r, :, :] == b)
            on_top = set(np.unique(space[r + 1, where[0], where[1]].flatten())) - set((0,))
            for t in on_top:
                if b != t:
                    S.add_edge(b, t)
    return S



def first_star(data):
    sand_blocks = parse_input(data)
    block_coords, maxes = convert_coords(sand_blocks)
    space = fill_space(block_coords, maxes)
    space, _ = gravity(space)
    S = block_graph(space)

    blast = set()
    for r in range(space.shape[0] - 1):
        level_blocks = set(np.unique(space[r, :, :].flatten())) - set((0,))
        for b in level_blocks:
            if len(list(S.successors(b))) == 0:
                blast.add(b)
            else:
                on_top = S.successors(b)
                if all(len(list(S.predecessors(o))) > 1 for o in on_top):
                    blast.add(b)
    return len(blast)


def second_star(data):
    sand_blocks = parse_input(data)
    block_coords, maxes = convert_coords(sand_blocks)
    space = fill_space(block_coords, maxes)
    space, _ = gravity(space)
    S = block_graph(space)

    blast_sum = 0
    for s in set(S.nodes()) - set((np.inf,)):
        blast_space = space.copy()
        blast_space[blast_space == s] = 0
        _, drop = gravity(blast_space)
        blast_sum += drop
    return blast_sum


if __name__ == "__main__":
    with open(f"data/2023/22.txt", "r") as f:
        data = f.read()

    data = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

    print(first_star(data))
    print(second_star(data))
