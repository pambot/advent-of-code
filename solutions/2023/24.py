import numpy as np
from itertools import combinations
from sympy import solve
from sympy.abc import a, b, c, x, y, z, s, t, u


def parse_input(data):
    hail_data = [
        [list(map(int, l.split(","))) for l in d.split("@")]
        for d in data.split("\n")
    ]
    hail = dict(x=list(), y=list(), z=list())
    for i, h in enumerate(hail_data):
        p, v = h
        hail["x"].append([v[0], p[0]])
        hail["y"].append([v[1], p[1]])
        hail["z"].append([v[2], p[2]])

    for k in hail:
        hail[k] = np.vstack(hail[k])
    return hail


def first_star(data, min_v, max_v):
    hail = parse_input(data)
    intersect = 0
    for h0, h1 in combinations(range(hail["x"].shape[0]), 2):
        x0 = hail["x"][h0]
        y0 = hail["y"][h0]
        x1 = hail["x"][h1]
        y1 = hail["y"][h1]

        solution = solve(
            [
                (x0[0]*s + x0[1]) - (x1[0]*t + x1[1]),
                (y0[0]*s + y0[1]) - (y1[0]*t + y1[1])
            ], [s, t], dict=True
        )
        if solution:
            sv = float(solution[0][s])
            tv = float(solution[0][t])

            x_int = x0[0] * sv + x0[1]
            y_int = y0[0] * sv + y0[1]

            if (sv > 0 and tv > 0
                and min_v <= x_int <= max_v
                and min_v <= y_int <= max_v
            ):
                intersect += 1
    return intersect


def second_star(data):
    hail = parse_input(data)
    x0 = hail["x"][0]
    y0 = hail["y"][0]
    z0 = hail["z"][0]
    x1 = hail["x"][1]
    y1 = hail["y"][1]
    z1 = hail["z"][1]
    x2 = hail["x"][2]
    y2 = hail["y"][2]
    z2 = hail["z"][2]

    solution = solve(
        [
            (x0[0]*s + x0[1] - a*s - x),
            (y0[0]*s + y0[1] - b*s - y),
            (z0[0]*s + z0[1] - c*s - z),
            (x1[0]*t + x1[1] - a*t - x),
            (y1[0]*t + y1[1] - b*t - y),
            (z1[0]*t + z1[1] - c*t - z),
            (x2[0]*u + x2[1] - a*u - x),
            (y2[0]*u + y2[1] - b*u - y),
            (z2[0]*u + z2[1] - c*u - z),
        ], [a, b, c, x, y, z, s, t, u], dict=True
    )
    if solution:
        xv = float(solution[0][x])
        yv = float(solution[0][y])
        zv = float(solution[0][z])
    return int(xv + yv + zv)


if __name__ == "__main__":
    with open(f"data/2023/24.txt", "r") as f:
        data = f.read()

    #     data = """19, 13, 30 @ -2,  1, -2
    # 18, 19, 22 @ -1, -1, -2
    # 20, 25, 34 @ -2, -2, -4
    # 12, 31, 28 @ -1, -2, -1
    # 20, 19, 15 @  1, -5, -3"""

    # print(first_star(data, min_v=7, max_v=27))
    print(first_star(data, min_v=200000000000000, max_v=400000000000000))
    print(second_star(data))
