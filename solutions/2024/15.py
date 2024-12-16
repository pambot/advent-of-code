import numpy as np


MOVE = {
    "<": (0, -1),
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
}


def get_move_group(grid, robot, m, to_move):
    sr, sc = np.array(robot) + np.array(MOVE[m])
    item = grid[sr, sc]
    to_move.append(robot)
    if item == "#":
        return (sr, sc), False, to_move
    elif item == ".":
        return (sr, sc), True, to_move
    elif m in "v^" and item == "[":
        left, is_left_move, to_move = get_move_group(grid, (sr, sc), m, to_move)
        right, is_right_move, to_move = get_move_group(grid, (sr, sc + 1), m, to_move)
        return left, is_left_move and is_right_move, to_move
    elif m in "v^" and item == "]":
        left, is_left_move, to_move = get_move_group(grid, (sr, sc - 1), m, to_move)
        right, is_right_move, to_move = get_move_group(grid, (sr, sc), m, to_move)
        return right, is_left_move and is_right_move, to_move
    elif (m in "<>" and item in "[]") or item == "O":
        return get_move_group(grid, (sr, sc), m, to_move)


def parse(data):
    raw_grid, raw_moves = data.strip().split("\n\n")
    grid = np.array([list(r) for r in raw_grid.split("\n")])
    moves = raw_moves.replace("\n", "")
    return grid, moves


def first_star(data):
    grid, moves = parse(data)
    rr, rc = list(zip(*np.where(grid == "@")))[0]

    for m in moves:
        _, is_move, to_move = get_move_group(grid, (rr, rc), m, list())
        if is_move:
            orig = {(mr, mc): grid[mr, mc] for mr, mc in to_move}
            nr, nc = MOVE[m]

            for mr, mc in to_move:
                grid[mr, mc] = "."

            for mr, mc in to_move:
                grid[mr + nr, mc + nc] = orig[(mr, mc)]

            rr, rc = rr + nr, rc + nc

    brs, bcs = np.where(grid == "O")
    return np.sum(brs * 100 + bcs)


def parse_wide(data):
    expand = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.',
    }

    raw_grid, raw_moves = data.strip().split("\n\n")
    for orig, exp in expand.items():
        raw_grid = raw_grid.replace(orig, exp)

    grid = np.array([list(r) for r in raw_grid.split("\n")])
    moves = raw_moves.replace("\n", "")
    return grid, moves


def second_star(data):
    grid, moves = parse_wide(data)
    rr, rc = list(zip(*np.where(grid == "@")))[0]

    for m in moves:
        _, is_move, to_move = get_move_group(grid, (rr, rc), m, list())
        if is_move:
            orig = {(mr, mc): grid[mr, mc] for mr, mc in to_move}
            nr, nc = MOVE[m]

            for mr, mc in to_move:
                grid[mr, mc] = "."

            for mr, mc in to_move:
                grid[mr + nr, mc + nc] = orig[(mr, mc)]

            rr, rc = rr + nr, rc + nc

    brs, bcs = np.where(grid == "[")
    return np.sum(brs * 100 + bcs)


def print_grid(grid):
    print("\n".join(["".join(g) for g in grid.tolist()]))


if __name__ == "__main__":
    with open(f"data/2024/15.txt", "r") as f:
        data = f.read()
        #         data = """
        # ##########
        # #..O..O.O#
        # #......O.#
        # #.OO..O.O#
        # #..O@..O.#
        # #O#..O...#
        # #O..O..O.#
        # #.OO.O.OO#
        # #....O...#
        # ##########

        # <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
        # vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
        # ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
        # <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
        # ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
        # ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
        # >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
        # <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
        # ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
        # v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

    print(first_star(data))
    print(second_star(data))
