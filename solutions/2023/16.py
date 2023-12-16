import numpy as np


mirror = {
    # i -> [moves_down, moves_up, moves_right, moves_left]
    # mirror[i] -> array[next_moves]
    ".": [[(1, 0)], [(-1, 0)], [(0, 1)], [(0, -1)]],
    "/": [[(0, -1)], [(0, 1)], [(-1, 0)], [(1, 0)]],
    "\\": [[(0, 1)], [(0, -1)], [(1, 0)], [(-1, 0)]],
    "|": [[(1, 0)], [(-1, 0)], [(1, 0), (-1, 0)], [(1, 0), (-1, 0)]],
    "-": [[(0, 1), (0, -1)], [(0, 1), (0, -1)], [(0, 1)], [(0, -1)]],
}

# k = move
approach = {
    (1, 0): 0, # moves_down
    (-1, 0): 1, # moves_up
    (0, 1): 2, # moves_right
    (0, -1): 3, # moves_left
}


def p(beam, move):
    br, bc = beam
    mr, mc = move
    return (br + mr, bc + mc)


def inside(beam, shape):
    tr, tc = shape
    br, bc = beam
    if 0 <= br < tr and 0 <= bc < tc:
        return True
    else:
        return False


def display(layout):
    print("\n".join(["".join(l) for l in layout.tolist()]))


def energize(contraption, start_light, debug=False):
    if debug:
        display(contraption)
        energized_debug = contraption.copy()

    energized = contraption.copy()
    light = start_light # beam, move
    steps = 0
    seen = set()
    while light:
        beam, move = light.pop(0)
        br, bc = beam
        if inside(beam, contraption.shape):
            energized[br, bc] = "#"

        if debug:
            if contraption[br, bc] == ".":
                energized_debug[br, bc] = "#"

        next_beam = p(beam, move)
        if not inside(next_beam, contraption.shape):
            continue
        nr, nc = next_beam
        next_moves = mirror[contraption[nr, nc]][approach[move]]
        light += [(next_beam, nm) for nm in next_moves if (next_beam, nm) not in seen]

        num_beams = (energized == "#").sum()
        seen.add((beam, move))
        if all(l in seen for l in light):
            break

        steps += 1

        if debug:
            print("-----")
            display(energized_debug)
            print("beam, move:", beam, move)
            print("next_beam, inside", next_beam, inside(next_beam, contraption.shape))
            print("next_moves, thing:", next_moves, contraption[nr, nc])
            print(num_beams)
            print(sorted(light))
            if steps > 100: break
    return num_beams


def first_star(data, debug=False):
    contraption = np.array([list(d) for d in data.splitlines()])
    num_beams = energize(contraption, [((0, -1), (0, 1))], debug)
    return num_beams


def second_star(data, debug=False):
    contraption = np.array([list(d) for d in data.splitlines()])
    nrows, ncols = contraption.shape
    num_beams = []
    for r in range(nrows):
        left_entry = energize(contraption, [((r, -1), (0, 1))], debug)
        right_entry = energize(contraption, [((r, ncols), (0, -1))], debug)
        num_beams.extend([left_entry, right_entry])

    for c in range(ncols):
        top_entry = energize(contraption, [((-1, c), (1, 0))], debug)
        bottom_entry = energize(contraption, [((nrows, c), (-1, 0))], debug)
        num_beams.extend([top_entry, bottom_entry])
    return max(num_beams)


if __name__ == "__main__":
    with open(f"data/2023/16.txt", "r") as f:
        data = f.read()

    #     data = r""".|...\....
    # |.-.\.....
    # .....|-...
    # ........|.
    # ..........
    # .........\
    # ..../.\\..
    # .-.-/..|..
    # .|....-|.\
    # ..//.|...."""

    print(first_star(data))
    print(second_star(data))
