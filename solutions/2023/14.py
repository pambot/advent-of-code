import numpy as np
import re


def roll_north(rocks):
    nrows, ncols = rocks.shape
    for rr in range(nrows):
        for cc in range(ncols):
            element = rocks[rr, cc]
            if element == "O":
                roll_path = list(rocks[:rr, cc])
                roll_path.reverse()
                steps = 0
                for ele in roll_path:
                    if ele != ".":
                        break
                    steps += 1
                rocks[rr, cc] = "."
                rocks[rr - steps, cc] = "O"
    return rocks


def roll_west(rocks):
    nrows, ncols = rocks.shape
    for rr in range(nrows):
        for cc in range(ncols):
            element = rocks[rr, cc]
            if element == "O":
                roll_path = list(rocks[rr, :cc])
                roll_path.reverse()
                steps = 0
                for ele in roll_path:
                    if ele != ".":
                        break
                    steps += 1
                rocks[rr, cc] = "."
                rocks[rr, cc - steps] = "O"
    return rocks


def roll_south(rocks):
    nrows, ncols = rocks.shape
    for rr in range(nrows - 1, -1, -1):
        for cc in range(ncols):
            element = rocks[rr, cc]
            if element == "O":
                roll_path = list(rocks[rr + 1:, cc])
                steps = 0
                for ele in roll_path:
                    if ele != ".":
                        break
                    steps += 1
                rocks[rr, cc] = "."
                rocks[rr + steps, cc] = "O"
    return rocks


def roll_east(rocks):
    nrows, ncols = rocks.shape
    for rr in range(nrows):
        for cc in range(ncols - 1, -1, -1):
            element = rocks[rr, cc]
            if element == "O":
                roll_path = list(rocks[rr, cc + 1:])
                steps = 0
                for ele in roll_path:
                    if ele != ".":
                        break
                    steps += 1
                rocks[rr, cc] = "."
                rocks[rr, cc + steps] = "O"
    return rocks


def first_star(data):
    rocks = np.array([list(d) for d in data.splitlines()])
    nrows, _ = rocks.shape
    rocks = roll_north(rocks)
    load = sum([nrows - rr for rr, _ in zip(*np.where(rocks == "O"))])
    return load


def second_star(data):
    rocks = np.array([list(d) for d in data.splitlines()])
    nrows, _ = rocks.shape

    loads = []
    for _ in range(1000):
        rocks = roll_north(rocks)
        rocks = roll_west(rocks)
        rocks = roll_south(rocks)
        rocks = roll_east(rocks)
        loads.append(sum([nrows - rr for rr, _ in zip(*np.where(rocks == "O"))]))

    # manual inspection
    offset = [104291, 104174, 103888, 103717, 103547, 103335, 103190, 103032, 102955, 102787, 102658, 102483, 102297, 102186, 102042, 101908, 101826, 101680, 101582, 101489, 101352, 101212, 101056, 100902, 100766, 100629, 100487, 100352, 100197, 100047, 99893, 99775, 99650, 99550, 99436, 99303, 99135, 98997, 98869, 98755, 98648, 98537, 98441, 98332, 98215, 98100, 97985, 97872, 97769, 97631, 97507, 97387, 97270, 97159, 97058, 96961, 96874, 96779, 96706, 96655, 96619, 96575, 96543, 96486, 96419, 96353, 96291, 96232, 96169, 96092, 96021, 95941, 95852, 95761, 95706, 95631, 95551, 95479, 95406, 95332, 95290, 95228, 95146, 95091, 95021, 94977, 94926, 94863, 94835, 94773, 94705, 94636, 94566, 94506, 94444, 94382, 94337, 94279, 94264, 94255, 94247, 94244]
    cycle = [94245, 94255, 94263, 94278, 94295, 94312, 94313, 94315, 94309, 94302, 94283, 94269, 94258, 94253]
    # offset = [87, 69]
    # cycle = [69, 69, 65, 64, 65, 63, 68]

    offset_len = len(offset)
    return loads[offset_len + (1000000000 - offset_len - 1) % len(cycle)]


if __name__ == "__main__":
    with open(f"data/2023/14.txt", "r") as f:
        data = f.read()

    #     data = """O....#....
    # O.OO#....#
    # .....##...
    # OO.#O....O
    # .O.....O#.
    # O.#..O.#.#
    # ..O..#O..O
    # .......O..
    # #....###..
    # #OO..#...."""

    print(first_star(data))
    print(second_star(data))
