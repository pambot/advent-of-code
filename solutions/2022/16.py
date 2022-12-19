import re
import functools
import itertools
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


def first_star(data):
    regex_extract = parse_input(data)
    start_node = "AA"

    G = make_full_graph(regex_extract)
    V = make_valve_graph(G, start_node)

    path_cache = dict()
    total_time = 30
    @functools.lru_cache(maxsize=None)
    def dfs(G, curr_node, visited, time_cost, flow_rate):
        visited += (curr_node,)
        if curr_node != start_node:
            time_cost += V[visited[-2]][curr_node]["time_cost"] + 1
        flow_rate += (total_time - time_cost) * V.nodes[curr_node]["flow_rate"]
        for node in G.neighbors(curr_node):
            if node not in visited and time_cost <= total_time:
                dfs(G, node, visited, time_cost, flow_rate)
        path_cache[visited] = dict(time_cost=time_cost, flow_rate=flow_rate)

    initial_flow = V.nodes[start_node]["flow_rate"]
    dfs(V, start_node, (), 0, initial_flow)
    return max([v["flow_rate"] for _, v in path_cache.items()])


def second_star(data):
    regex_extract = parse_input(data)
    start_node = "AA"

    G = make_full_graph(regex_extract)
    V = make_valve_graph(G, start_node)

    path_cache = dict()
    me_total_time = 26
    el_total_time = 26
    @functools.lru_cache(maxsize=None)
    def double_dfs(
        G, me_node, el_node, me_visited, el_visited,
        me_time_cost, el_time_cost, flow_rate
    ):
        me_visited += (me_node,)
        el_visited += (el_node,)
        visited = me_visited + el_visited
        if me_node != start_node and el_node != start_node:
            me_time_cost += V[me_visited[-2]][me_node]["time_cost"] + 1
            el_time_cost += V[el_visited[-2]][el_node]["time_cost"] + 1
        flow_rate += (me_total_time - me_time_cost) * V.nodes[me_node]["flow_rate"]
        flow_rate += (el_total_time - el_time_cost) * V.nodes[el_node]["flow_rate"]
        next_me_nodes = list(set(G.neighbors(me_node)) - set(visited))
        next_el_nodes = list(set(G.neighbors(el_node)) - set(visited))
        for next_me_node, next_el_node in itertools.product(next_me_nodes, next_el_nodes):
            if (
                next_me_node != next_el_node and
                me_time_cost <= me_total_time and el_time_cost <= el_total_time
            ):
                double_dfs(
                    G, next_me_node, next_el_node, me_visited, el_visited,
                    me_time_cost, el_time_cost, flow_rate
                )
        path_cache[(me_visited, el_visited)] = dict(
            me_time_cost=me_time_cost, el_time_cost=el_time_cost, flow_rate=flow_rate
        )
    initial_flow = V.nodes[start_node]["flow_rate"]
    double_dfs(V, start_node, start_node, (), (), 0, 0, initial_flow)
    return max([v["flow_rate"] for _, v in path_cache.items()])


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
    print(second_star(data))
