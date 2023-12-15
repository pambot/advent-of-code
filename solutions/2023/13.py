import numpy as np


def parse_input(data):
    chunks = data.strip().split("\n\n")
    patterns = []
    for chunk in chunks:
        patterns.append(np.array([list(c) for c in chunk.split("\n")]))
    return patterns


def first_star(data):
    patterns = parse_input(data)
    summary = 0
    for pattern in patterns:
        nrows, ncols = pattern.shape
        for rr in range(1, nrows):
            if rr <= nrows // 2:
                orig = pattern[:rr, :]
                reflect = np.flipud(pattern[rr:2 * rr, :])
                if np.array_equal(orig, reflect):
                    summary += 100 * rr
            else:
                orig = pattern[rr:, :]
                reflect = np.flipud(pattern[rr - (nrows - rr):rr, :])
                if np.array_equal(orig, reflect):
                    summary += 100 * rr

        for cc in range(1, ncols):
            if cc <= ncols // 2:
                orig = pattern[:, :cc]
                reflect = np.fliplr(pattern[:, cc:2 * cc])
                if np.array_equal(orig, reflect):
                    summary += cc
            else:
                orig = pattern[:, cc:]
                reflect = np.fliplr(pattern[:, cc - (ncols - cc):cc])
                if np.array_equal(orig, reflect):
                    summary += cc
    return summary


def second_star(data):
    patterns = parse_input(data)
    summary = 0
    for pattern in patterns:
        nrows, ncols = pattern.shape
        for rr in range(1, nrows):
            if rr <= nrows // 2:
                orig = pattern[:rr, :]
                reflect = np.flipud(pattern[rr:2 * rr, :])
                if len(np.where(orig != reflect)[0]) == 1:
                    summary += 100 * rr
            else:
                orig = pattern[rr:, :]
                reflect = np.flipud(pattern[rr - (nrows - rr):rr, :])
                if len(np.where(orig != reflect)[0]) == 1:
                    summary += 100 * rr

        for cc in range(1, ncols):
            if cc <= ncols // 2:
                orig = pattern[:, :cc]
                reflect = np.fliplr(pattern[:, cc:2 * cc])
                if len(np.where(orig != reflect)[0]) == 1:
                    summary += cc
            else:
                orig = pattern[:, cc:]
                reflect = np.fliplr(pattern[:, cc - (ncols - cc):cc])
                if len(np.where(orig != reflect)[0]) == 1:
                    summary += cc
    return summary


if __name__ == "__main__":
    with open(f"data/2023/13.txt", "r") as f:
        data = f.read()

    #     data = """#.##..##.
    # ..#.##.#.
    # ##......#
    # ##......#
    # ..#.##.#.
    # ..##..##.
    # #.#.##.#.

    # #...##..#
    # #....#..#
    # ..##..###
    # #####.##.
    # #####.##.
    # ..##..###
    # #....#..#"""

    print(first_star(data))
    print(second_star(data))
