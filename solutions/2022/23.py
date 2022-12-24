import numpy as np
import itertools


ELF = "#"
GROUND = "."
CHECK_COORDS = {
    "N": ((-1, -1), (-1, 0), (-1, 1)),
    "E": ((-1, 1), (0, 1), (1, 1)),
    "S": ((1, 1), (1, 0), (1, -1)),
    "W": ((1, -1), (0, -1), (-1, -1))
}
CHECK_ALL = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, 1), (1, 1), (1, -1),
    (0, -1), (1, 0)
)


def is_occupied(elf_coords, coord, check_dir=None):
    if check_dir:
        check_coords = CHECK_COORDS[check_dir]
    else:
        check_coords = CHECK_ALL
    r, c = coord
    check = False
    for cr, cc in check_coords:
        if (r + cr, c + cc) in elf_coords:
            check = True
    return check


def propose_coord(coord, move_dir):
    r, c = coord
    mr, mc = CHECK_COORDS[move_dir][1]
    return (r + mr, c + mc)


def draw_tiles(elf_coords):
    min_r = min([r for r, _ in elf_coords])
    max_r = max([r for r, _ in elf_coords])
    min_c = min([c for _, c in elf_coords])
    max_c = max([c for _, c in elf_coords])
    nrows, ncols = (max_r - min_r), (max_c - min_c)
    r_trans = [r - min_r for r, _ in elf_coords]
    c_trans = [c - min_c for _, c in elf_coords]
    display = np.array([["." for _ in range(ncols + 1)] for _ in range(nrows + 1)])
    display[r_trans, c_trans] = "#"
    print("\n".join(["".join([c for c in r]) for r in display]), "\n")
    return len(np.where(display == ".")[0])


def first_half(elf_coords, dir_order):
    doubles = set()
    for coord in elf_coords:
        # check all 8, if all F, stay same
        occupied = is_occupied(elf_coords, coord)
        if not occupied:
            elf_coords[coord] = coord
            continue

        # check each direction, propose first valid
        proposed = False
        for this_dir in dir_order:
            occupied = is_occupied(elf_coords, coord, this_dir)
            if not occupied:
                maybe = propose_coord(coord, this_dir)
                # check if proposed coord is already seen
                if maybe in elf_coords.values():
                    doubles.add(maybe)
                elf_coords[coord] = maybe
                proposed = True
                break
        if not proposed:
            elf_coords[coord] = coord
    return elf_coords, doubles


def second_half(elf_coords, doubles):
    next_coords = dict()
    for coord in elf_coords:
        maybe = elf_coords[coord]
        if maybe in doubles:
            next_coords[coord] = None
        else:
            next_coords[maybe] = None
    return next_coords



def first_star(data):
    grove = np.array([list(d) for d in data.splitlines()])
    rows, cols = np.where(grove == ELF)
    elf_coords = {(r, c): None for r, c in zip(rows, cols)}
    dir_order = ["N", "S", "W", "E"]
    for _ in range(10):
        elf_coords, doubles = first_half(elf_coords, dir_order)
        next_coords = second_half(elf_coords, doubles)
        if set(elf_coords.keys()) == set(next_coords.keys()):
            break
        else:
            elf_coords = next_coords
        dir_order = dir_order[1:] + [dir_order[0]]
    return draw_tiles(elf_coords)


def second_star(data):
    grove = np.array([list(d) for d in data.splitlines()])
    rows, cols = np.where(grove == ELF)
    elf_coords = {(r, c): None for r, c in zip(rows, cols)}
    dir_order = ["N", "S", "W", "E"]
    n = 1
    while True:
        elf_coords, doubles = first_half(elf_coords, dir_order)
        next_coords = second_half(elf_coords, doubles)
        if set(elf_coords.keys()) == set(next_coords.keys()):
            break
        else:
            elf_coords = next_coords
        dir_order = dir_order[1:] + [dir_order[0]]
        n += 1
    return n


if __name__ == "__main__":
    with open(f"data/2022/23.txt", "r") as f:
        data = f.read()

    small_example = """.....
..##.
..#..
.....
..##.
....."""

    large_example = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""

    print(first_star(data))
    print(second_star(data))
