import numpy as np


XMAS = ["X", "M", "A", "S"]
MAS = ["M", "A", "S"]


def look_south(letters, r, c):
    return int(letters[r:r + 4, c].tolist() == XMAS)

def look_north(letters, r, c):
    return int(letters[r - 3:r + 1, c].tolist()[::-1] == XMAS)

def look_east(letters, r, c):
    return int(letters[r, c:c + 4].tolist() == XMAS)

def look_west(letters, r, c):
    return int(letters[r, c - 3:c + 1].tolist()[::-1] == XMAS)

def look_southeast(letters, r, c):
    return int([letters[r + m, c + m] for m in range(4)] == XMAS)

def look_northeast(letters, r, c):
    return int([letters[r - m, c + m] for m in range(4) if r - m >= 0] == XMAS)

def look_southwest(letters, r, c):
    return int([letters[r + m, c - m] for m in range(4) if c - m >= 0] == XMAS)

def look_northwest(letters, r, c):
    return int([letters[r - m, c - m] for m in range(4) if r - m >= 0 and c - m >= 0] == XMAS)


def first_star(data):
    letters = np.array([list(s) for s in data.split()])
    nrows, ncols = letters.shape
    found = 0
    for r in range(nrows):
        for c in range(ncols):
            if letters[r, c] == "X":
                for look in [
                    look_east, look_north, look_northeast, look_northwest,
                    look_south, look_southeast, look_southwest, look_west
                ]:
                    try:
                        found += look(letters, r, c)
                        # if look(letters, r, c): print(r, c, look.__name__)
                    except Exception:
                        pass
    return found


def look_around(letters, r, c):
    if r - 1 >= 0 and c - 1 >= 0:
        diag1 = [
            letters[r - 1, c - 1],
            letters[r, c],
            letters[r + 1, c + 1]
        ]
        diag2 = [
            letters[r - 1, c + 1],
            letters[r, c],
            letters[r + 1, c - 1]
        ]
        return int(
            (diag1 == MAS or diag1[::-1] == MAS) &
            (diag2 == MAS or diag2[::-1] == MAS)
        )
    else:
        return 0


def second_star(data):
    letters = np.array([list(s) for s in data.split()])
    nrows, ncols = letters.shape
    found = 0
    for r in range(nrows):
        for c in range(ncols):
            if letters[r, c] == "A":
                try:
                    found += look_around(letters, r, c)
                except Exception:
                    pass
    return found


if __name__ == "__main__":
    with open(f"data/2024/04.txt", "r") as f:
        data = f.read()
        #         data = """MMMSXXMASM
        # MSAMXMSMSA
        # AMXSXMAAMM
        # MSAMASMSMX
        # XMASAMXAMM
        # XXAMMXXAMA
        # SMSMSASXSS
        # SAXAMASAAA
        # MAMMMXMMMM
        # MXMXAXMASX"""

    print(first_star(data))
    print(second_star(data))
