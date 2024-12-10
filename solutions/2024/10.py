import numpy as np
from collections import defaultdict


def parse(data):
    return np.array([list(map(int, list(s))) for s in data.strip().split()])


def get_trails(topo):
    zeros = list(zip(*np.where(topo == 0)))
    nines = list(zip(*np.where(topo == 9)))
    nrows, ncols = topo.shape
    stack = [[z] for z in zeros]
    paths = []

    while stack:
        path = stack.pop()
        lr, lc = path[-1]

        if (lr, lc) in nines:
            paths.append(path)
        else:
            around = ((-1, 0), (0, -1), (1, 0), (0, 1))
            steps = [
                (lr + ar, lc + ac) for ar, ac in around
                if 0 <= lr + ar < nrows and 0 <= lc + ac < ncols
                and topo[lr + ar, lc + ac] == topo[lr, lc] + 1
            ]
            for step in steps:
                if step not in path:
                    new_path = path + [step]
                    stack.append(new_path)
    return paths


def first_star(data):
    topo = parse(data)
    trails = get_trails(topo)

    start_end = defaultdict(set)
    for p in trails:
        start_end[p[0]].add(p[-1])

    scores = [len(start_end[t]) for t in start_end.keys()]
    return sum(scores)


def second_star(data):
    topo = parse(data)
    trails = get_trails(topo)

    distinct = defaultdict(set)
    for p in trails:
        distinct[p[0]].add(tuple(p))

    ratings = [len(distinct[t]) for t in distinct.keys()]
    return sum(ratings)


if __name__ == "__main__":
    with open(f"data/2024/10.txt", "r") as f:
        data = f.read()
        #         data = """
        # 89010123
        # 78121874
        # 87430965
        # 96549874
        # 45678903
        # 32019012
        # 01329801
        # 10456732"""

    print(first_star(data))
    print(second_star(data))
