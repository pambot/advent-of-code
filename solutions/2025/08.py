import math
from collections import defaultdict


def parse(data):
    coords = [list(map(int, d.split(","))) for d in data.strip().split("\n")]
    return coords


import math
from collections import defaultdict


def pairwise_distances(coords):
    distances = defaultdict(list)
    for i, (c1x, c1y, c1z) in enumerate(coords):
        for j, (c2x, c2y, c2z) in enumerate(coords):
            if i < j:
                d = math.sqrt((c2x - c1x)**2 + (c2y - c1y)**2 + (c2z - c1z)**2)
                distances[d] = (i, j)
    return sorted(distances.items())


def distance_graph(distances, top):
    C = defaultdict(list)
    for _, (i, j) in distances[:top]:
        C[i].append(j)
        C[j].append(i)

    return C


def subgraph_nodes(C, start):
    visited = {start}
    queue = [start]

    while queue:
        current = queue.pop()
        for neighbour in C[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return visited


def first_star(data):
    coords = parse(data)
    top = 1000

    distances = pairwise_distances(coords)
    C = distance_graph(distances, top)

    junction_nodes = C.keys()
    global_visited = set()
    subgraph_sizes = []
    for junction in junction_nodes:
        if junction not in global_visited:
            visited = subgraph_nodes(C, junction)
            subgraph_sizes.append(len(visited))
            global_visited = global_visited | visited

    subgraph_sizes += [1] * len(set(range(len(coords))) - global_visited)
    return math.prod(sorted(subgraph_sizes, reverse=True)[:3])


def second_star(data):
    coords = parse(data)
    min_top = 1000

    distances = pairwise_distances(coords)
    C = distance_graph(distances, min_top)

    for top in range(min_top, len(distances)):
        _, (i, j) = distances[top]
        C[i].append(j)
        C[j].append(i)

        junction = list(C.keys())[0]
        visited = subgraph_nodes(C, junction)

        if len(visited) == len(coords):
            break

    return coords[i][0] * coords[j][0]


if __name__ == "__main__":
    with open(f"data/2025/08.txt", "r") as f:
        data = f.read()
        #         data = """162,817,812
        # 57,618,57
        # 906,360,560
        # 592,479,940
        # 352,342,300
        # 466,668,158
        # 542,29,236
        # 431,825,988
        # 739,650,466
        # 52,470,668
        # 216,146,977
        # 819,987,18
        # 117,168,530
        # 805,96,715
        # 346,949,466
        # 970,615,88
        # 941,993,340
        # 862,61,35
        # 984,92,344
        # 425,690,689"""


    print(first_star(data))
    print(second_star(data))
