import numpy as np


ARROWS = {
    "^": (-1, 0), ">": (0, 1),
    "<": (0, -1), "v": (1, 0)
}


def draw(blizzard):
    print("\n".join(["".join([c for c in r]) for r in blizzard]), "\n")


def iterate_blizzard(blizzard):
    next = np.copy(blizzard)
    arrow_coords = dict()
    for arrow in ARROWS:
        arrow_loc = np.where(next == arrow)
        arrow_coords[arrow] = [(r, c) for r, c in zip(*arrow_loc)]
        next[arrow_loc] = "."

    seen = []
    for arrow in arrow_coords:
        for r, c in arrow_coords[arrow]:
            rr, rc = ARROWS[arrow]
            nr, nc = r + rr, c + rc
            if nr < 1:
                nr, nc = len(next) - 2, nc
            elif nr >= len(next) - 1:
                nr, nc = 1, nc
            elif nc < 1:
                nr, nc = nr, len(next[0]) - 2
            elif nc >= len(next[0]) - 1:
                nr, nc = nr, 1

            if (nr, nc) not in seen:
                next[nr, nc] = arrow
            else:
                pass # multi arrows
            seen.append((nr, nc))

    return next


def first_star(data):
    blizzard = np.array([list(d) for d in data.splitlines()])
    start, end = (0, 1), (len(blizzard) - 1, len(blizzard[0]) - 2)

    return iterate_blizzard(blizzard)


def second_star(data):
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/2022/24.txt", "r") as f:
        data = f.read()

    example = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

    print(first_star(example))
    print(second_star(data))
