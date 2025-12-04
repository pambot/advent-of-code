
def parse(data):
    grid = [["."] + list(d) + ["."] for d in data.split("\n") if d]
    gc, _ = len(grid[0]), len(grid)
    grid = [["."] * (gc)] + grid + [["."] * (gc)]
    return grid

AROUND = [
    (0, 1), (1, 0), (-1, 0), (0, -1),
    (-1, -1), (1, 1), (-1, 1), (1, -1)
]

def first_star(data):
    grid = parse(data)
    gr, gc = len(grid[0]), len(grid)

    c = 0
    for i in range(1, gr - 1):
        for j in range(1, gc - 1):
            if grid[i][j] == "@":
                rolls = [
                    grid[i + ai][j + aj]
                    for ai, aj in AROUND
                    if grid[i + ai][j + aj] in ("@", "x")
                ]
                if len(rolls) < 4:
                    grid[i][j] = "x"
                    c += 1

    return c


def count_rolls(grid, gc, gr):
    return sum([1 for j in range(1, gc - 1) for i in range(1, gr - 1) if grid[i][j] == "@"])


def second_star(data):
    grid = parse(data)
    gr, gc = len(grid[0]), len(grid)

    nr1 = count_rolls(grid, gc, gr)

    cp = 2**31
    cn = 2**31
    while cp > 0 and cn > 0:
        cp = cn
        cn = 0
        for i in range(1, gr - 1):
            for j in range(1, gc - 1):
                if grid[i][j] == "@":
                    rolls = [
                        grid[i + ai][j + aj]
                        for ai, aj in AROUND
                        if grid[i + ai][j + aj] in ("@", "x")
                    ]
                    if len(rolls) < 4:
                        grid[i][j] = "x"
                        cn += 1

        for i in range(1, gr - 1):
            for j in range(1, gc - 1):
                if grid[i][j] == "x":
                    grid[i][j] = "."

    nr2 = count_rolls(grid, gc, gr)
    return nr1 - nr2


if __name__ == "__main__":
    with open(f"data/2025/04.txt", "r") as f:
        data = f.read()
        #         data = """

        # """

    print(first_star(data))
    print(second_star(data))
