import numpy as np


AIR = "."
SAND = "+"
ROCK = "#"
SAND_START = (500, 0)


def parse_coords(data):
    return [
        [tuple(map(int, c.split(","))) for c in d.split(" -> ")]
         for d in data.splitlines()
    ]


def get_dimensions(paths):
    min_r, max_r, min_c, max_c = 10**9, 0, 10**9, 0
    for path in paths:
        for coord in path:
            c, r = coord
            if r < min_r: min_r = r
            if r > max_r: max_r = r
            if c < min_c: min_c = c
            if c > max_c: max_c = c
    return min_r, max_r, min_c, max_c


def draw_paths(cave, paths, c_norm):
    for path in paths:
        pc, pr = path[0]
        for next_coord in path[1:]:
            nc, nr = next_coord
            if pc == nc:
                for r in range(min(pr, nr), max(pr, nr) + 1):
                    cave[r, nc - c_norm] = ROCK
            if pr == nr:
                for c in range(min(pc, nc), max(pc, nc) + 1):
                    cave[nr, c - c_norm] = ROCK
            pc, pr = nc, nr
    return cave


def sand_fall(cave, sand_start, c_norm):
    sc, sr = sand_start
    msc = sc - c_norm
    cave[sr, msc] = SAND
    while True:
        if cave[sr + 1, msc] == AIR:
            cave[sr, msc] = AIR
            sr += 1
            cave[sr, msc] = SAND
        elif cave[sr + 1, msc] != AIR and cave[sr + 1, msc - 1] == AIR:
            cave[sr, msc] = AIR
            sr += 1
            msc -= 1
            cave[sr, msc] = SAND
        elif cave[sr + 1, msc] != AIR and cave[sr + 1, msc - 1] != AIR and cave[sr + 1, msc + 1] == AIR:
            cave[sr, msc] = AIR
            sr += 1
            msc += 1
            cave[sr, msc] = SAND
        else:
            break
    return cave


def first_star(data):
    paths = parse_coords(data)
    _, max_r, min_c, max_c = get_dimensions(paths)
    cave = np.array([[AIR] * (max_c - min_c + 1)] * (max_r + 1))
    cave = draw_paths(cave, paths, min_c)
    sand_count = 0
    while True:
        try:
            cave = sand_fall(cave, SAND_START, min_c)
            sand_count += 1
        except Exception:
            break
    return sand_count


def second_star(data):
    paths = parse_coords(data)
    _, max_r, _, _ = get_dimensions(paths)
    max_r += 2
    sc, sr = SAND_START
    cave = np.array([[AIR] * (max_r * 2 + 1)] * (max_r + 1))
    cave[max_r, :] = ROCK
    cave = draw_paths(cave, paths, sc - max_r)
    sand_count = 0
    while cave[sr, max_r] != SAND:
        cave = sand_fall(cave, SAND_START, sc - max_r)
        sand_count += 1
    return sand_count


if __name__ == "__main__":
    with open(f"data/2022/14.txt", "r") as f:
        data = f.read()

    example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    print(first_star(data))
    print(second_star(data))
