import numpy as np
from itertools import cycle


def parse(data):
    return [
        [list(map(int, v.split(","))) for v in d.split(" -> ")]
          for d in data.strip().split("\n")
    ]


def get_grid(lines):
    max_x, max_y = 0, 0
    for (x0, y0), (x1, y1) in lines:
        if x0 > max_x:
            max_x = x0
        if x1 > max_x:
            max_x = x1
        if y0 > max_y:
            max_y = y0
        if y1 > max_y:
            max_y = y1

    grid = np.zeros((max_y + 1, max_x + 1))
    return grid


def first_star(data):
    lines = parse(data)
    grid = get_grid(lines)

    hvlines = [
        ((x0, y0), (x1, y1))
        for (x0, y0), (x1, y1) in lines
        if x0 == x1 or y0 == y1
    ]

    for (x0, y0), (x1, y1) in hvlines:
        if x0 == x1:
            y0, y1 = min([y0, y1]), max([y0, y1])
            for y in range(y0, y1 + 1):
                grid[y, x0] += 1

        elif y0 == y1:
            x0, x1 = min([x0, x1]), max([x0, x1])
            for x in range(x0, x1 + 1):
                grid[y0, x] += 1

    return len(grid[grid > 1])


def second_star(data):
    lines = parse(data)
    grid = get_grid(lines)

    for (x0, y0), (x1, y1) in lines:
        if x1 >= x0:
            x_step = 1
        else:
            x_step = -1

        if y1 >= y0:
            y_step = 1
        else:
            y_step = -1

        xs = [x0]
        while x0 != x1:
            x0 += x_step
            xs.append(x0)

        ys = [y0]
        while y0 != y1:
            y0 += y_step
            ys.append(y0)

        for x, y in zip(xs, cycle(ys)) if len(xs) > len(ys) else zip(cycle(xs), ys):
            grid[y, x] += 1

    return len(grid[grid > 1])


if __name__ == "__main__":
    with open(f"data/2021/05.txt", "r") as f:
        data = f.read()
        #         data = """
        # 0,9 -> 5,9
        # 8,0 -> 0,8
        # 9,4 -> 3,4
        # 2,2 -> 2,1
        # 7,0 -> 7,4
        # 6,4 -> 2,0
        # 0,9 -> 2,9
        # 3,4 -> 1,4
        # 0,0 -> 8,8
        # 5,5 -> 8,2
        # """

    print(first_star(data))
    print(second_star(data))
