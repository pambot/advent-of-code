
class Board:
    def __init__(self, data):
        bmap = [
            list(d) for d in data.splitlines()
            if d and (d[0] in (".", "#", " "))
        ]
        max_cols = max([len(r) for r in bmap])
        for i, _ in enumerate(bmap):
            bmap[i].extend([" "] * (max_cols - len(bmap[i])))
        start_ind = bmap[0].index(".")
        bmap[0][start_ind] = ">"
        self.map = bmap
        self.start_coord = (0, start_ind)
        self.final_coord = None
        self.final_dir = None

        path = [
            d for d in data.splitlines()
            if d and d[0].isnumeric()
        ][0]
        pathl = path.replace("L", ",L,").replace("R", ",R,").split(",")
        self.path = list()
        for p in pathl:
            if p.isnumeric():
                self.path.append(int(p))
            else:
                self.path.append(p)

        dirlookup = {
            "N": "^", "E": ">",
            "S": "v", "W": "<",
        }

        self.dir2arrow = dirlookup
        self.arrow2dir = {v: k for k, v in dirlookup.items()}
        self.dirs = ["N", "E", "S", "W", "N", "E", "S", "W"] # clockwise
        self.dir2rcoord = {
            "N": (-1, 0), "E": (0, 1),
            "S": (1, 0), "W": (0, -1),
        }
        self.dir2score = {
            "N": 3, "E": 0,
            "S": 1, "W": 2,
        }

    def print(self):
            print(
                "\n".join(
                    ["".join(m) for m in self.map]
                )
            )

    def get_next_dir(self, curr_dir, turn=None):
        if turn == "L":
            next_dir = self.dirs[self.dirs.index(curr_dir) - 1]
        elif turn == "R":
            next_dir = self.dirs[self.dirs.index(curr_dir) + 1]
        else:
            next_dir = curr_dir
        return next_dir

    def get_next_pos(self, pos, next_dir):
        r1, c1 = pos
        rr, rc = self.dir2rcoord[next_dir]
        r2, c2 = (r1 + rr, c1 + rc)
        next_found = False
        while next_found == False:
            if r2 >= len(self.map):
                r2, c2 = 0, c2
            elif r2 < 0:
                r2, c2 = len(self.map) - 1, c2
            elif c2 >= len(self.map[r2]):
                r2, c2 = r2, 0
            elif c2 < 0:
                r2, c2 = r2, len(self.map[r2]) - 1
            elif self.map[r2][c2] == " ":
                r2, c2 = (r2 + rr, c2 + rc)
            elif self.map[r2][c2] in ["."] + list(self.arrow2dir.keys()):
                next_found = True
            elif self.map[r2][c2] == "#":
                r2, c2 = r1, c1
                next_found = True
        return r2, c2

    def move(self):
        r1, c1 = self.start_coord
        for path in self.path:
            arrow = self.map[r1][c1]
            curr_dir = self.arrow2dir[arrow]
            if isinstance(path, int):
                for _ in range(path):
                    next_dir = curr_dir
                    r2, c2 = self.get_next_pos((r1, c1), next_dir)
                    if (r1, c1) == (r2, c2):
                        break
                    self.map[r2][c2] = arrow
                    r1, c1 = r2, c2
                    self.final_coord = (r2 + 1, c2 + 1)
            else:
                r2, c2 = r1, c1
                next_dir = self.get_next_dir(curr_dir, turn=path)
                self.map[r2][c2] = self.dir2arrow[next_dir]
                self.final_dir = next_dir


def first_star(data):
    B = Board(data)
    B.move()
    r, c = B.final_coord
    f = B.dir2score[B.final_dir]
    return 1000 * r + 4 * c + f


def second_star(data):
    B = Board(data)
    B.print()
    return


if __name__ == "__main__":
    with open(f"data/2022/22.txt", "r") as f:
        data = f.read()

    example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

    # assert Board(example).get_next_dir("N", "L") == "W"
    # assert Board(example).get_next_dir("W", "R") == "N"
    # assert Board(example).get_next_pos((0, 8), "E") == (0, 9) # simple move forward
    # assert Board(example).get_next_pos((0, 10), "E") == (0, 10) # simple blocked
    # assert Board(example).get_next_pos((7, 1), "S") == (4, 1) # wrapped down
    # assert Board(example).get_next_pos((8, 14), "N") == (8, 14) # tries to wrap, hits rock

    print(first_star(data))
    print(second_star(data))
