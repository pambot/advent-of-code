from collections import Counter


def parse(data):
    track = [list(d) for d in data.strip().splitlines()]
    nrows, ncols = len(track), len(track[0])
    start = [(r, c) for r in range(nrows) for c in range(ncols) if track[r][c] == "S"][0]
    end = [(r, c) for r in range(nrows) for c in range(ncols) if track[r][c] == "E"][0]
    return track, start, end


def get_path(track, start, end):
    cr, cc = start
    seen = dict()
    path = list()
    c = 0
    while (cr, cc) != end:
        nr, nc = [
            (cr + ar, cc + ac) for ar, ac in ((1, 0), (0, 1), (-1, 0), (0, -1))
            if track[cr + ar][cc + ac] in (".", "E")
            and (cr + ar, cc + ac) not in seen
        ][0]
        seen[nr, nc] = c
        path.append((nr, nc))
        cr, cc = nr, nc
        c += 1
    return path, seen


def first_star(data):
    track, start, end = parse(data)
    path, seen = get_path(track, start, end)

    cheats = []
    for i, (cr, cc) in enumerate([start] + path, -1):
        for ar, ac in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if track[cr + ar][cc + ac] == "#":
                try:
                    for n in range(4):
                        if (track[cr + ar * n][cc + ac * n] in (".", "E")
                            and seen[(cr + ar * n, cc + ac * n)] > i
                        ):
                            jr, jc = cr + ar * n, cc + ac * n
                            j = seen[(jr, jc)]
                            cheats.append(j - i - n)
                            break
                except Exception:
                    pass

    return sum([v for k, v in Counter(cheats).items() if k >= 100])


def second_star(data):
    track, start, end = parse(data)
    path, seen = get_path(track, start, end)

    circle = list()
    for r in range(-20, 21):
        for c in range(-20, 21):
            if 2 <= abs(r) + abs(c) <= 20:
                circle.append((r, c))

    cheats = []
    for i, (cr, cc) in enumerate([start] + path, -1):
        for ar, ac in circle:
            try:
                if (track[cr + ar ][cc + ac] in (".", "E")
                    and seen[(cr + ar, cc + ac)] > i
                ):
                    jr, jc = cr + ar, cc + ac
                    j = seen[(jr, jc)]
                    cheats.append(j - i - (abs(ar) + abs(ac)))
            except Exception:
                pass

    return sum([v for k, v in Counter(cheats).items() if k >= 100])


if __name__ == "__main__":
    with open(f"data/2024/20.txt", "r") as f:
        data = f.read()
        #         data = """###############
        # #...#...#.....#
        # #.#.#.#.#.###.#
        # #S#...#.#.#...#
        # #######.#.#.###
        # #######.#.#...#
        # #######.#.###.#
        # ###..E#...#...#
        # ###.#######.###
        # #...###...#...#
        # #.#####.#.###.#
        # #.#...#.#.#...#
        # #.#.#.#.#.#.###
        # #...#...#...###
        # ###############"""

    print(first_star(data))
    print(second_star(data))
