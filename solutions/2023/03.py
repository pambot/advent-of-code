import re
from collections import defaultdict


def num2inds(line, r):
    return [
        (int(m.group(0)), [(r, c) for c in range(m.start(0), m.end(0))])
        for m in re.finditer("\d+", line)
    ]

def _expand_ind(ind, exclude, max_r, max_c):
    r0, c0 = ind
    possible = [
        (r0 - 1, c0 - 1), (r0 - 1, c0), (r0 - 1, c0 + 1),
        (r0, c0 - 1), (r0, c0 + 1),
        (r0 + 1, c0 - 1), (r0 + 1, c0), (r0 + 1, c0 + 1),
    ]
    expanded = []
    for p in possible:
        r1, c1 = p
        if (r1 >= 0 and c1 >= 0
            and r1 < max_r and c1 < max_c
            and (r1, c1) not in exclude
        ):
            expanded.append(p)
    return expanded


def expand_inds(inds, max_r, max_c):
    collect = []
    for ind in inds:
        collect.extend(_expand_ind(ind, inds, max_r, max_c))
    return sorted(set(collect))


def first_star(data):
    grid = data.splitlines()
    max_r = len(grid)
    max_c = len(grid[0])
    num_sum = 0
    for r, line in enumerate(grid):
        n2i = num2inds(line, r)
        for v in n2i:
            num, inds = v
            surr = expand_inds(inds, max_r, max_c)
            for s in surr:
                check_r, check_c = s
                if grid[check_r][check_c] not in "123456789.":
                    num_sum += num
    return num_sum


def find_gears(line, r):
    return [(r, m.start(0)) for m in re.finditer("\*", line)]


def second_star(data):
    grid = data.splitlines()
    max_r = len(grid)
    max_c = len(grid[0])

    gears = []
    surr2num = defaultdict(list)
    for r, line in enumerate(grid):
        gears.extend(find_gears(line, r))
        n2i = num2inds(line, r)
        for v in n2i:
            num, inds = v
            surr = expand_inds(inds, max_r, max_c)
            for s in surr:
                surr2num[s].append(num)

    gear_ratio = 0
    for gear in gears:
        adj = surr2num.get(gear, None)
        if adj and len(adj) == 2:
            gear_ratio += adj[0] * adj[1]

    return gear_ratio


if __name__ == "__main__":
    with open(f"data/2023/03.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
