import re
import numpy as np
import time


def parse(data):
    lines = data.strip().split("\n")
    nums = [list(map(int, re.findall(r'-?\d+', s))) for s in lines]

    prs = np.array([n[1] for n in nums])
    pcs = np.array([n[0] for n in nums])
    vrs = np.array([n[3] for n in nums])
    vcs = np.array([n[2] for n in nums])
    return prs, pcs, vrs, vcs


def wrap(a, b, max_value):
    return np.mod((a + b), max_value)


def first_star(data):
    prs, pcs, vrs, vcs = parse(data)
    nrows, ncols = 103, 101
    qrow, qcol = int((nrows - 1)/2), int((ncols - 1)/2)
    tiles = np.zeros((nrows, ncols))

    prs = wrap(prs, vrs * 100, nrows)
    pcs = wrap(pcs, vcs * 100, ncols)

    for pr, pc in zip(prs, pcs):
        tiles[pr, pc] += 1

    safety_factor = int(np.product(
        (
            tiles[:qrow, :qcol].sum(),
            tiles[qrow + 1:, :qcol].sum(),
            tiles[:qrow, qcol + 1:].sum(),
            tiles[qrow + 1:, qcol + 1:].sum()
        )
    ))

    return safety_factor


def draw(tiles):
    nrows, ncols = tiles.shape
    draw = np.full((nrows, ncols), ' ', dtype='U1')
    draw[np.where(tiles > 0)] = "X"
    return "".join(["".join(d) + '|\n' for d in draw.tolist()]) + "-" * ncols


def second_star(data):
    prs, pcs, vrs, vcs = parse(data)
    nrows, ncols = 103, 101
    tiles = np.zeros((nrows, ncols))

    for n in range(1, 10**4):
        prs = wrap(prs, vrs, nrows)
        pcs = wrap(pcs, vcs, ncols)

        tiles[prs, pcs] = 1

        drawn = draw(tiles)
        if 'XXXXXXXXXXXX' in drawn:
            with open("tree.txt", "a") as f:
                f.write(f"Iteration {n}\n")
                f.write(drawn + "\n")
            break

        tiles = np.zeros((nrows, ncols))
    return n



if __name__ == "__main__":
    with open(f"data/2024/14.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
