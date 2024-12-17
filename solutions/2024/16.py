import numpy as np
from collections import defaultdict


def parse(data):
    return np.array([list(r) for r in data.strip().split("\n")])


def shortest_path(maze):
    sr, sc = tuple(zip(*np.where(maze == "S")))[0]
    er, ec = tuple(zip(*np.where(maze == "E")))[0]

    unseen = set()
    starts = set()
    arrive = {(-1, 0): '^', (0, -1): '<', (1, 0): 'v', (0, 1): '>'} # if . at k, v is possible
    for ur, uc in list(zip(*np.where(np.isin(maze, (".", "S", "E"))))):
        for ar, ac in arrive.keys():
            if maze[ur + ar, uc + ac] in (".", "S", "E"):
                ud = arrive[(ar, ac)]
                if (ur, uc) == (sr, sc):
                    starts.add((ur, uc, ud))
                    unseen.add((ur, uc, ud))
                elif (ur, uc) == (er, ec):
                    end = (ur, uc, None)
                    unseen.add((ur, uc, None))
                else:
                    unseen.add((ur, uc, ud))

    leave = {v: k for k, v in arrive.items()}
    graph = defaultdict(list)
    for ur, uc, ud in unseen - {end}:
        ar, ac = leave[ud]
        if (ur + ar, uc + ac, None) == end:
                graph[(ur, uc, ud)].append(end)
        for ad in leave.keys():
            if (ur + ar, uc + ac, ad) in unseen and ud + ad not in ("^v", "v^", "<>", "><"):
                graph[(ur, uc, ud)].append((ur + ar, uc + ac, ad))

    from_start = {(cr, cc, cd): (0 if (cr, cc, cd) in starts else np.inf) for cr, cc, cd in unseen}
    prev = {(cr, cc, cd): list() for (cr, cc, cd) in unseen}

    while unseen:
        unseen_dict = {u: from_start[u] for u in unseen}
        (cr, cc, cd) = min(unseen_dict, key=unseen_dict.get)
        unseen.remove((cr, cc, cd))

        if from_start[(cr, cc, cd)] == np.inf:
            break

        adjacent = graph[(cr, cc, cd)]

        for nr, nc, nd in adjacent:
            dist = 1 + 1000 * (1 if cd + str(nd) in ("^>", ">^", "^<", "<^", "v>", ">v", "v<", "<v") else 0)
            if from_start[(cr, cc, cd)] + dist <= from_start[(nr, nc, nd)]:
                from_start[(nr, nc, nd)] = from_start[(cr, cc, cd)] + dist
                prev[(nr, nc, nd)].append((cr, cc, cd))

        if (cr, cc, cd) == end:
            break

    stack = [(end, [end])]
    paths = list()
    while stack:
        (cr, cc, cd), path = stack.pop()
        if (cr, cc, cd) in starts and path not in paths:
            paths.append(path)
        else:
            for nr, nc, nd in prev[(cr, cc, cd)]:
                if (nr, nc, nd) not in path:
                    stack.append(((nr, nc, nd), path + [(nr, nc, nd)]))

    path = paths[0][::-1]
    fd = ">"
    turns = 0
    steps = 0
    for _, _, pd in path[:-1]:
        if pd != fd:
            turns += 1
            fd = pd
        steps += 1

    return turns * 1000 + steps, len(set([p[:2] for path in paths for p in path]))


def first_star(data):
    maze = parse(data)
    score, count = shortest_path(maze)
    return score, count


def second_star(data):
    return
    # maze = parse(data)
    # _, count = shortest_path(maze)
    # return count


if __name__ == "__main__":
    with open(f"data/2024/16.txt", "r") as f:
        data = f.read()
        #         data = """###############
        # #.......#....E#
        # #.#.###.#.###.#
        # #.....#.#...#.#
        # #.###.#####.#.#
        # #.#.#.......#.#
        # #.#.#####.###.#
        # #...........#.#
        # ###.#.#####.#.#
        # #...#.....#.#.#
        # #.#.#.###.#.#.#
        # #.....#...#.#.#
        # #.###.#.#.#.#.#
        # #S..#.....#...#
        # ###############"""

    print(first_star(data))
    print(second_star(data))
