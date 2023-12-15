from itertools import cycle
from math import lcm
from collections import defaultdict


def parse_input(data):
    lines = data.splitlines()
    right_left = lines[0]
    graph = {l[:3]: (l[7:10], l[12:15]) for l in lines[2:]}
    return right_left, graph


def first_star(data):
    right_left, graph = parse_input(data)
    start, end = "AAA", "ZZZ"
    get_index = {"L": 0, "R": 1}
    node = start
    steps = 0
    for rl in cycle(right_left):
        next_node = graph[node][get_index[rl]]
        steps += 1
        if next_node == end:
            break
        else:
            node = next_node
    return steps



def second_star(data):
    right_left, graph = parse_input(data)
    starts = [k for k in graph.keys() if k[-1] == "A"]

    get_index = {"L": 0, "R": 1}
    nodes = starts
    steps = 0
    ends_seen = defaultdict(list)
    for rl in cycle(right_left):
        next_nodes = [graph[node][get_index[rl]] for node in nodes]
        steps += 1

        ends = [node for node in next_nodes if node[-1] == "Z"]
        for node in ends:
            ends_seen[node].append(steps)

        if (len(ends_seen) == len(starts)
            and all(len(v) >= 3 for v in ends_seen.values())
        ):
            ends_cycles = {k: [v[i] - v[i - 1] for i in range(1, len(v))][0]
                          for k, v in ends_seen.items()}
            break

        nodes = next_nodes

    return lcm(*ends_cycles.values())


if __name__ == "__main__":
    with open(f"data/2023/08.txt", "r") as f:
        data = f.read()

    #     data = """RL

    # AAA = (BBB, CCC)
    # BBB = (DDD, EEE)
    # CCC = (ZZZ, GGG)
    # DDD = (DDD, DDD)
    # EEE = (EEE, EEE)
    # GGG = (GGG, GGG)
    # ZZZ = (ZZZ, ZZZ)"""

    print(first_star(data))

    #     data = """LR

    # 11A = (11B, XXX)
    # 11B = (XXX, 11Z)
    # 11Z = (11B, XXX)
    # 22A = (22B, XXX)
    # 22B = (22C, 22C)
    # 22C = (22Z, 22Z)
    # 22Z = (22B, 22B)
    # XXX = (XXX, XXX)"""

    print(second_star(data))
