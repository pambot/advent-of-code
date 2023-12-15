import networkx as nx
from shapely import Polygon, Point


def find_start(pipes):
    for sr, pipe in enumerate(pipes):
        for sc, p in enumerate(pipe):
            if p == "S":
                return (sr, sc)


def expand_grid(coord, shape):
    tr, tc = shape
    r, c = coord
    outer_grid = [
        (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
        (r, c - 1), (r, c + 1),
        (r + 1, c - 1), (r + 1, c), (r + 1, c + 1),
    ]
    return [p for p in outer_grid if 0 <= p[0] < tr and 0 <= p[1] < tc]


def find_loop(pipes):
    sr, sc = find_start(pipes)

    move_to = {
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
        "7": [(1, 0), (0, -1)],
        "F": [(1, 0), (0, 1)],
        ".": [(0, 0)],
        "S": [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    }

    D = nx.DiGraph()
    D.add_node((sr, sc))

    steps = 0
    dead_ends = set()
    while True:
        leaves = [
            node for node in D.nodes()
            if D.out_degree(node) == 0
            and node not in dead_ends
        ]
        while leaves:
            cr, cc = leaves.pop()
            parents = list(D.predecessors((cr, cc)))
            bounded_grid = expand_grid((cr, cc), (len(pipes), len(pipes[0])))
            valid_moves = set([
                (cr + vr, cc + vc) for vr, vc in move_to[pipes[cr][cc]]
                if (cr + vr, cc + vc) not in parents
                and (cr + vr, cc + vc) in bounded_grid
                and any([br == -vr and bc == -vc for (br, bc) in move_to[pipes[cr + vr][cc + vc]]])
            ])
            if not valid_moves:
                dead_ends.add((cr, cc))
            for mr, mc in valid_moves:
                D.add_edge((cr, cc), (mr, mc))

        steps += 1

        try:
            loop_edges = nx.find_cycle(D, source=(sr, sc), orientation="ignore")
            break
        except nx.NetworkXNoCycle:
            continue
    return steps, loop_edges


def first_star(data):
    pipes = data.splitlines()
    steps, _ = find_loop(pipes)
    return steps


def draw_loop(pipes, loop_path):
    redraw = {
        "|": "│",
        "-": "─",
        "L": "└",
        "J": "┘",
        "7": "┐",
        "F": "┌",
        ".": "▫",
        "S": "S",
    }
    draw = []
    for r in range(len(pipes)):
        row = []
        for c in range(len(pipes[0])):
            if (r, c) in loop_path:
                row.append(redraw[pipes[r][c]])
            else:
                row.append("\33[43m" + "▫" + "\033[0m")
        draw.append("".join(row))
    draw = "\n".join(draw)
    print(draw)


def second_star(data):
    pipes = data.splitlines()
    _, loop_edges = find_loop(pipes)
    loop_edges = [(n1, n2) for n1, n2, _ in loop_edges]
    L = nx.DiGraph()
    L.add_edges_from(loop_edges)
    loop_path = nx.cycle_basis(L.to_undirected())[0]

    t = 0
    for r in range(len(pipes)):
        for c in range(len(pipes[0])):
            if Polygon(loop_path).contains(Point(r, c)):
                t += 1

    draw_loop(pipes, loop_path)
    return t


if __name__ == "__main__":
    with open(f"data/2023/10.txt", "r") as f:
        data = f.read()

    #     data = """7-F7-
    # .FJ|7
    # SJLL7
    # |F--J
    # LJ.LJ"""

    #     data = """FF7FSF7F7F7F7F7F---7
    # L|LJ||||||||||||F--J
    # FL-7LJLJ||||||LJL-77
    # F--JF--7||LJLJ7F7FJ-
    # L---JF-JLJ.||-FJLJJ7
    # |F|F-JF---7F7-L7L|7|
    # |FFJF7L7F-JF7|JL---7
    # 7-L-JL7||F7|L7F-7F7|
    # L.L7LFJ|||||FJL7||LJ
    # L7JLJL-JLJLJL--JLJ.L"""

    print(first_star(data))
    print(second_star(data))
