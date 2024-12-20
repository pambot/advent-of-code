import networkx as nx
import numpy as np


def parse(data):
    corrupt = [tuple(map(int, s.split(","))) for s in data.strip().split("\n")]
    return corrupt


def make_graph(shape, corrupt):
    nrows, ncols = shape
    G = nx.Graph()
    for r in range(nrows):
        for c in range(ncols):
            if (r, c) not in corrupt:
                for ar, ac in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    if (r + ar, c + ac) not in corrupt:
                        G.add_edge((r, c), (r + ar, c + ac))
    return G


def first_star(data):
    cutoff = 1024
    corrupt = parse(data)
    nrows, ncols = (71, 71)
    G = make_graph((nrows, ncols), set(corrupt[:cutoff]))
    return len(nx.shortest_path(G, source=(0, 0), target=(nrows - 1, ncols - 1))) - 1


def second_star(data):
    corrupt = parse(data)
    nrows, ncols = (71, 71)

    left, right = 0, len(corrupt) - 1
    while left <= right:
        mid = (left + right) // 2
        try:
            G = make_graph((nrows, ncols), set(corrupt[:mid]))
            _ = len(nx.shortest_path(G, source=(0, 0), target=(nrows - 1, ncols - 1))) - 1
            left = mid + 1
        except Exception:
            right = mid - 1
    return ",".join(list(map(str, corrupt[left - 1]))) if left < len(corrupt) else -1


if __name__ == "__main__":
    with open(f"data/2024/18.txt", "r") as f:
        data = f.read()
        #         data = """5,4
        # 4,2
        # 4,5
        # 3,0
        # 2,1
        # 6,3
        # 2,4
        # 1,5
        # 0,6
        # 3,3
        # 2,6
        # 5,1
        # 1,2
        # 5,5
        # 2,5
        # 6,5
        # 1,4
        # 0,4
        # 6,4
        # 1,1
        # 6,1
        # 1,0
        # 0,5
        # 1,6
        # 2,0"""

    print(first_star(data))
    print(second_star(data))
