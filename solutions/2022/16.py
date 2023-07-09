import re
import functools
import networkx as nx


def parse_input(data):
    regex_extract = [
        re.findall(r"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z \,]+)", d)
        for d in data.splitlines()
    ]
    return [(r[0][0], int(r[0][1]), r[0][2].split(", ")) for r in regex_extract]


def make_full_graph(regex_extract):
    G = nx.DiGraph()
    for (start_valve, _, end_valves) in regex_extract:
        for ev in end_valves:
            G.add_edge(start_valve, ev)
    nx.set_node_attributes(G,
        {r[0]:{"flow_rate": r[1]} for r in regex_extract}
    )
    return G


def make_valve_graph(G, start_node):
    valve_nodes = [node for node, attr in G.nodes(data=True) if attr["flow_rate"] > 0]
    valve2valve = dict()
    for v1 in [start_node] + valve_nodes:
        for v2 in [start_node] + valve_nodes:
            path = (v1, v2)
            if v1 != v2:
                valve2valve[path] = nx.shortest_path_length(G, v1, v2)
    V = nx.DiGraph()
    for valve, pl in valve2valve.items():
        V.add_edge(valve[0], valve[1], time_cost=pl)
    nx.set_node_attributes(V, dict(G.nodes(data=True)))
    return V


def single_path2flows(V, start_node, total_time):
    visited = tuple()
    time_cost = 0
    start_flow = V.nodes[start_node]["flow_rate"]
    path_cache = dict()
    single_dfs(V, start_node, visited, time_cost, start_flow, total_time, path_cache)
    return max(path_cache.values())


def single_dfs(V, curr_node, visited, time_cost, flow_rate, total_time, path_cache):
    visited += (curr_node,)
    time_left = total_time - time_cost
    if time_left <= 0:
        return

    flow_rate += V.nodes[curr_node]["flow_rate"] * time_left
    path_cache[visited] = flow_rate

    for node in V.neighbors(curr_node):
        if node not in visited:
            next_time_cost = time_cost + V[curr_node][node]["time_cost"] + 1
            single_dfs(V, node, visited, next_time_cost, flow_rate, total_time, path_cache)
    return


def first_star(data):
    regex_extract = parse_input(data)
    start_node = "AA"

    G = make_full_graph(regex_extract)
    V = make_valve_graph(G, start_node)

    return single_path2flows(V, start_node, 30)


PATH_CACHE = dict()


def double_path2flows(V, start_node, total_time):
    me_visited = tuple()
    el_visited = tuple()
    time_cost = 0
    start_flow = V.nodes[start_node]["flow_rate"]
    double_dfs(
        V,
        me_visited, el_visited,
        start_node, start_node,
        time_cost, time_cost,
        start_flow,
        total_time
    )
    return max(PATH_CACHE.values())


@functools.lru_cache(maxsize=None)
def double_dfs(
    V,
    me_visited, el_visited,
    me_curr_node, el_curr_node,
    me_time_cost, el_time_cost,
    flow_rate,
    total_time
):
    # compute cost of this next step (up front), time stops if not moving
    if me_visited and me_curr_node:
        me_time_cost += V[me_visited[-1]][me_curr_node]["time_cost"] + 1

    if el_visited and el_curr_node:
        el_time_cost += V[el_visited[-1]][el_curr_node]["time_cost"] + 1

    me_time_left = total_time - me_time_cost
    el_time_left = total_time - el_time_cost

    # if neither has time left, exit
    if me_time_left < 0 and el_time_left < 0:
        return

    # if one has time left, just use that one, other will be 0
    if me_time_left >= 0:
        me_visited += (me_curr_node,)
        me_flow_rate = V.nodes[me_curr_node]["flow_rate"] * me_time_left
    else:
        me_flow_rate = 0

    if el_time_left >= 0:
        el_visited += (el_curr_node,)
        el_flow_rate = V.nodes[el_curr_node]["flow_rate"] * el_time_left
    else:
        el_flow_rate = 0

    flow_rate += me_flow_rate + el_flow_rate

    global PATH_CACHE
    PATH_CACHE[tuple(sorted((me_visited, el_visited)))] = flow_rate

    if me_time_left >= 0 and el_time_left >= 0:
        for me_node in V.neighbors(me_curr_node):
            for el_node in V.neighbors(el_curr_node):
                if (
                    me_node != el_node and
                    me_node not in me_visited + el_visited and
                    el_node not in me_visited + el_visited
                ):
                    double_dfs(
                        V,
                        me_visited, el_visited,
                        me_node, el_node, # proposed visit, rest is present iteration
                        me_time_cost, el_time_cost,
                        flow_rate,
                        total_time
                    )
    elif me_time_left < 0 and el_time_left >= 0:
        for el_node in V.neighbors(el_curr_node):
            if el_node not in me_visited + el_visited:
                double_dfs(
                    V,
                    me_visited, el_visited,
                    None, el_node,
                    me_time_cost, el_time_cost,
                    flow_rate,
                    total_time
                )
    elif me_time_left >= 0 and el_time_left < 0:
        for me_node in V.neighbors(me_curr_node):
            if me_node not in me_visited + el_visited:
                double_dfs(
                    V,
                    me_visited, el_visited,
                    me_node, None,
                    me_time_cost, el_time_cost,
                    flow_rate,
                    total_time
                )
    return


def second_star(data):
    regex_extract = parse_input(data)
    start_node = "AA"

    G = make_full_graph(regex_extract)
    V = make_valve_graph(G, start_node)

    return double_path2flows(V, start_node, 26)


if __name__ == "__main__":
    with open(f"data/2022/16.txt", "r") as f:
        data = f.read()

    example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

    print(first_star(data))


    #     example = """Valve AA has flow rate=0; tunnels lead to valves BB, CC
    # Valve BB has flow rate=1; tunnels lead to valve AA
    # Valve CC has flow rate=1; tunnels lead to valve AA, DD
    # Valve DD has flow rate=1; tunnels lead to valve CC, EE
    # Valve EE has flow rate=1; tunnels lead to valve DD"""
    print(second_star(data))
