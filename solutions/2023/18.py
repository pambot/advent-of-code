import numpy as np


def shoelace(deltas):
    corners = np.array([np.array(deltas)[:i, :].sum(axis=0) for i in range(len(deltas))])
    x, y = corners.T
    close_loop = x[-1] * y[0] - y[-1] * x[0]
    main_area = np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])
    border = np.abs(np.array(deltas)).sum() / 2 + 1
    return 0.5 * np.abs(main_area + close_loop) + border


def first_star(data):
    directions = {
        "R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)
    }
    deltas = [d.split(" ") for d in data.strip().split("\n")]
    deltas = [(directions[a], int(b)) for a, b, _ in deltas]
    deltas = [(b * a[0], a[1] * b) for a, b in deltas]
    return int(shoelace(deltas))


def second_star(data):
    directions = {
        0: (0, 1), 2: (0, -1), 3: (-1, 0), 1: (1, 0)
    }
    deltas = [d.split(" ") for d in data.strip().split("\n")]
    deltas = [(int(c[2:-2], 16), directions[int(c[-2])]) for _, _, c in deltas]
    deltas = [(n * c[0], n * c[1]) for n, c in deltas]
    return int(shoelace(deltas))


if __name__ == "__main__":
    with open(f"data/2023/18.txt", "r") as f:
        data = f.read()

    #     data = """R 6 (#70c710)
    # D 5 (#0dc571)
    # L 2 (#5713f0)
    # D 2 (#d2c081)
    # R 2 (#59c680)
    # D 2 (#411b91)
    # L 5 (#8ceee2)
    # U 2 (#caa173)
    # L 1 (#1b58a2)
    # U 2 (#caa171)
    # R 2 (#7807d2)
    # U 3 (#a77fa3)
    # L 2 (#015232)
    # U 2 (#7a21e3)"""

    print(first_star(data))
    print(second_star(data))
