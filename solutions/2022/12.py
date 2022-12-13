import numpy as np
import string
import networkx as nx


def make_alphabet_lookup():
    alphabet = dict(zip(string.ascii_lowercase, list(range(26))))
    alphabet["S"] = 0
    alphabet["E"] = 25
    return alphabet


def extract_coords(heightmap, v):
    return list(zip(*np.where(heightmap == v)))


def calculate_next_steps(heightmap, coords):
    alphabet = make_alphabet_lookup()
    current_elevation = heightmap[coords]
    next_steps = []
    for coord in (
        (coords[0] - 1, coords[1]), # up
        (coords[0] + 1, coords[1]), # down
        (coords[0], coords[1] - 1), # left
        (coords[0], coords[1] + 1), # right
    ):
        if (0 <= coord[0] < heightmap.shape[0] and 0 <= coord[1] < heightmap.shape[1]):
            next_elevation = heightmap[coord]
        else:
            continue
        if (alphabet[next_elevation] - alphabet[current_elevation] <= 1):
            next_steps.append(coord)
    return next_steps


def generate_graph(heightmap):
    P = nx.DiGraph()
    r, c = heightmap.shape
    for m in range(r):
        for n in range(c):
            next_steps = calculate_next_steps(heightmap, (m, n))
            for s in next_steps:
                P.add_edge((m, n), s)
    return P


def first_star(data):
    heightmap = np.array([list(d) for d in data.splitlines()])
    start = extract_coords(heightmap, "S")[0]
    end = extract_coords(heightmap, "E")[0]
    P = generate_graph(heightmap)
    return nx.shortest_path_length(P, start, end)


def second_star(data):
    heightmap = np.array([list(d) for d in data.splitlines()])
    heightmap[heightmap == "S"] = "a"
    starts = extract_coords(heightmap, "a")
    end = extract_coords(heightmap, "E")[0]
    P = generate_graph(heightmap)
    paths = []
    for start in starts:
        try:
            paths.append(nx.shortest_path_length(P, start, end))
        except Exception:
            continue
    return min(paths)


if __name__ == "__main__":
    with open(f"data/2022/12.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
