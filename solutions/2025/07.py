from collections import defaultdict


def parse(data):
    dsplit = data.strip("\n").split("\n")
    start = (0, dsplit[0].index("S"))

    nrows, ncols = len(dsplit), len(dsplit[0])

    splitters = set()
    for i in range(nrows):
        for j in range(ncols):
            if dsplit[i][j] == "^":
                splitters.add((i, j))

    return start, splitters, (nrows, ncols)


def first_star(data):
    start, splitters, (nrows, ncols) = parse(data)

    tachyon_init = [start]
    split_count = 0
    while tachyon_init[0][0] + 1 < nrows:
        tachyon_next = set()
        for tii, tij in tachyon_init:
            if (tii + 1, tij) in splitters:
                split_count += 1
                tachyon_split = ((tii + 1, tij - 1), (tii + 1, tij + 1))
                for tsi, tsj in tachyon_split:
                    if 0 < tsj < ncols:
                        tachyon_next.add((tsi, tsj))
            else:
                tachyon_next.add((tii + 1, tij))

        tachyon_init = list(tachyon_next)

    return split_count


def second_star(data):
    start, splitters, (nrows, ncols) = parse(data)

    tachyon_init = [start]
    path_count = defaultdict(int)
    path_count[start] = 1
    while tachyon_init[0][0] + 1 < nrows:
        tachyon_next = set()
        for tii, tij in tachyon_init:
            if (tii + 1, tij) in splitters:
                tachyon_split = ((tii + 1, tij - 1), (tii + 1, tij + 1))
                for tsi, tsj in tachyon_split:
                    if 0 <= tsj < ncols:
                        tachyon_next.add((tsi, tsj))
                        path_count[(tsi, tsj)] += path_count[(tii, tij)]
            else:
                tachyon_next.add((tii + 1, tij))
                path_count[(tii + 1, tij)] += path_count[(tii, tij)]

        tachyon_init = list(tachyon_next)

    return sum([pc for (pi, _), pc in path_count.items() if pi == nrows - 1])


if __name__ == "__main__":
    with open(f"data/2025/07.txt", "r") as f:
        data = f.read()
        #         data = """

        # """

    print(first_star(data))
    print(second_star(data))
