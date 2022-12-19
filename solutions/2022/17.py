import itertools
import math


# coords in (x, y), not numpy coords
ROCK_FLOOR = [(0, 0), (1, 0), (2, 0), (3, 0)]
ROCK_PLUS = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
ROCK_LFLIP = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
ROCK_COLUMN = [(0, 0), (0, 1), (0, 2), (0, 3)]
ROCK_SQUARE = [(0, 0), (1, 0), (0, 1), (1, 1)]
ROCK_ORDER = [ROCK_FLOOR, ROCK_PLUS, ROCK_LFLIP, ROCK_COLUMN, ROCK_SQUARE]


def rock_movement(rock, heights, jet_streams, j, settled):
    # start coord is where (0, 0) is for the rock
    start_x = 2
    start_y = max([y for _, y in heights]) + 4
    rock = [(x + start_x, y + start_y) for x, y in rock]
    i = 0
    while True:
        if i % 2 == 0:
            cycle_j = j % len(jet_streams)
            jet = jet_streams[cycle_j]
            if jet == "<":
                rock_next = [(x - 1, y) for x, y in rock]
                if all([x >= 0 and (x, y) not in settled for x, y in rock_next]):
                    rock = rock_next
            if jet == ">":
                rock_next = [(x + 1, y) for x, y in rock]
                if all([x < len(heights) and (x, y) not in settled for x, y in rock_next]):
                    rock = rock_next
            i += 1
            j += 1
        else:
            rock_next = [(x, y - 1) for x, y in rock]
            if all([c not in settled for c in rock_next]):
                rock = rock_next
                i += 1
            else:
                break

    settled.update(rock)
    for i in range(len(heights)):
        hx, hy = heights[i]
        uy = max([ry for rx, ry in rock if rx == hx] + [hy])
        heights[i] = (hx, uy)
    return heights, settled, j


def first_star(data):
    jet_streams = data.strip()
    heights = [(i, -1) for i in range(7)]
    settled = set(heights)
    c = 1
    j = 0
    for rock in itertools.cycle(ROCK_ORDER):
        heights, settled, j = rock_movement(rock, heights, jet_streams, j, settled)
        if c == 2022:
            break
        c += 1
    return max([y for _, y in heights]) + 1


def get_remainder(total_cycles, start, period):
    # use this to lookup remainder height
    return (total_cycles - start) % period

def rock_cycles_height(
    total_cycles, start, start_height, period, cycle_height, remainder_height
):
    div = (total_cycles - start) // period
    return start_height + div * cycle_height + remainder_height


def second_star(data):
    total_cycles = 1_000_000_000_000

    # in example, cycle begins at c = 16
    # r = 0 has j = 2, 28, 15, 5, 34, 21, 10
    # cycle period is 7 * len(ROCK_ORDER) = 35
    # c = 16 -> h = 25; c = 51, h = 78; c = 86, h = 131
    # 131 - 78 = 53; 78 - 25 = 53
    # (total_cycles - 16) % 35 = 34
    # delta(h) from c = 16 to c = 50 is 53

    if data == ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>":
        assert get_remainder(total_cycles, 16, 35) == 34
        assert rock_cycles_height(
            total_cycles, 16, 25, 35, 53, 53
        ) == 1514285714288

    # in data, cycle begins at c = 1726
    # r = 0 has j = 14, ...
    # cycle period is 1715
    # c = 1725, h = 2607; c = 3441, h = 5181
    # 5181 - 2607 = 2574
    # rem = 4
    # delta(h) from

    assert get_remainder(total_cycles, 1726, 1715) == 4
    h = rock_cycles_height(
        total_cycles, 1726, 2607, 1715, 2574, 8
    )

    # # uncomment this to generate data for the estimates
    # jet_streams = data.strip()
    # heights = [(i, -1) for i in range(7)]
    # settled = set(heights)
    # c = 1
    # j = 0
    # for r, rock in itertools.cycle(enumerate(ROCK_ORDER)):
    #     if c >= 1726 and c <= 1750:
    #         print(c, r, j % len(jet_streams), j, max([y for _, y in heights]) + 1)
    #     heights, settled, j = rock_movement(rock, heights, jet_streams, j, settled)
    #     if c == 20000:
    #         break
    #     c += 1
    return h


if __name__ == "__main__":
    with open(f"data/2022/17.txt", "r") as f:
        data = f.read()

    example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

    print(first_star(data))
    print(second_star(data))
