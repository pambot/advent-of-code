import numpy as np
from itertools import combinations


def parse(data):
    return np.array([list(d) for d in data.strip().splitlines()])


def first_star(data):
    city = parse(data)
    freqs = list(np.unique(city))
    freqs.remove(".")
    cr, cc = city.shape

    antinodes = set()
    for freq in freqs:
        locs = list(zip(*np.where(city == freq)))
        pairs = list(combinations(locs, 2))

        for p0, p1 in pairs:
            p0_an = (p0[0] - (p1[0] - p0[0]), p0[1] - (p1[1] - p0[1]))
            p1_an = (p1[0] - (p0[0] - p1[0]), p1[1] - (p0[1] - p1[1]))
            if 0 <= p0_an[0] < cr and 0 <= p0_an[1] < cc:
                antinodes.add(p0_an)
            if 0 <= p1_an[0] < cr and 0 <= p1_an[1] < cc:
                antinodes.add(p1_an)

    for p in antinodes:
        city[p] = 'X'
    return len(antinodes)


def second_star(data):
    city = parse(data)
    freqs = list(np.unique(city))
    freqs.remove(".")
    cr, cc = city.shape

    antinodes = set()
    for freq in freqs:
        locs = list(zip(*np.where(city == freq)))
        pairs = list(combinations(locs, 2))

        for p0, p1 in pairs:
            for f in range(max([cr, cc])):
                p0_an = (p0[0] - f * (p1[0] - p0[0]), p0[1] - f * (p1[1] - p0[1]))
                p1_an = (p1[0] - f * (p0[0] - p1[0]), p1[1] - f * (p0[1] - p1[1]))
                if 0 <= p0_an[0] < cr and 0 <= p0_an[1] < cc:
                    antinodes.add(p0_an)
                if 0 <= p1_an[0] < cr and 0 <= p1_an[1] < cc:
                    antinodes.add(p1_an)

    for p in antinodes:
        city[p] = 'X'
    return len(antinodes)


if __name__ == "__main__":
    with open(f"data/2024/08.txt", "r") as f:
        data = f.read()
        #         data = """
        # ............
        # ........0...
        # .....0......
        # .......0....
        # ....0.......
        # ......A.....
        # ............
        # ............
        # ........A...
        # .........A..
        # ............
        # ............"""

    print(first_star(data))
    print(second_star(data))
