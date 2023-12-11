import numpy as np
from scipy.spatial.distance import cdist


def get_expansions(universe):
    expand_rows = []
    for r in range(universe.shape[0]):
        if (universe[r, :] == ".").all():
            expand_rows.append(r)

    expand_cols = []
    for c in range(universe.shape[1]):
        if (universe[:, c] == ".").all():
            expand_cols.append(c)
    return expand_rows, expand_cols


def first_star(data):
    universe = np.array([list(d) for d in data.splitlines()])
    expand_rows, expand_cols = get_expansions(universe)
    o = 0
    for r in expand_rows:
        universe = np.insert(universe, r + o, ".", axis=0)
        o += 1

    o = 0
    for r in expand_cols:
        universe = np.insert(universe, r + o, ".", axis=1)
        o += 1

    galaxies = list(zip(*np.where(universe == "#")))
    return int(np.tril(cdist(galaxies, galaxies, "cityblock")).sum())


def second_star(data):
    universe = np.array([list(d) for d in data.splitlines()])
    expand_rows, expand_cols = get_expansions(universe)

    factor = 10**6
    galaxies = list(zip(*np.where(universe == "#")))
    distances = np.tril(cdist(galaxies, galaxies, "cityblock"))

    total = 0
    ind_pairs = list(zip(*np.where(distances > 0)))
    for pair in ind_pairs:
        i1, i2 = pair
        g1 = galaxies[i1]
        g2 = galaxies[i2]
        extra_rows = len([
            r for r in expand_rows
            if min(g1[0], g2[0]) < r < max(g1[0], g2[0])
        ]) * (factor - 1)
        extra_cols = len([
            c for c in expand_cols
            if min(g1[1], g2[1]) < c < max(g1[1], g2[1])
        ]) * (factor - 1)
        orig_dist = distances[i1, i2]
        total += orig_dist + extra_rows + extra_cols

    return int(total)


if __name__ == "__main__":
    with open(f"data/2023/11.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
