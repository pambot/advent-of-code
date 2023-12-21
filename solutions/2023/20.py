import copy
import networkx as nx
from math import lcm


def parse_line(d):
    source, target = d.split(" -> ")
    targets = target.split(", ")
    attrs = {
        "receive_pulse": None,
        "send_pulse": None
    }
    if "%" in d or "&" in d:
        name = source[1:]
        attrs["symbol"] = source[0]

        if "%" in d:
            attrs["on"] = False
        else:
            attrs["inputs"] = dict()
    elif "broadcaster" in d:
        name = "broadcaster"
        attrs["symbol"] = name
    return name, targets, attrs


# gather data
def make_modules(data):
    D = nx.DiGraph()
    for d in data.strip().split("\n"):
        name, targets, attrs = parse_line(d)

        D.add_node(name, **attrs)
        for o, out in enumerate(targets):
            D.add_edge(name, out, order=o)

    # add conjunction inputs
    for node in D.nodes():
        if not "symbol" in D.nodes[node]:
            D.nodes[node]["symbol"] = "output"
            D.nodes[node]["receive_pulse"] = None

        elif D.nodes[node]["symbol"] == "&":
            inputs = D.predecessors(node)
            D.nodes[node]["inputs"] = {k: "low" for k in inputs}

    D.add_node("button", symbol="button", send_pulse="low")
    D.add_edge("button", "broadcaster")
    return D


def receive_pulse(D, prev_node, curr_node):
    curr_data = D.nodes[curr_node]
    prev_data = D.nodes[prev_node]
    curr_data["receive_pulse"] = prev_data["send_pulse"]

    pulses = {"low": 0, "high": 0}
    pulses[curr_data["receive_pulse"]] += 1

    if curr_data["symbol"] == "broadcaster":
        curr_data["send_pulse"] = curr_data["receive_pulse"]

    elif curr_data["symbol"] == "%":
        on2pulse = {True: "high", False: "low"}
        if curr_data["receive_pulse"] == "low":
            curr_data["on"] = not curr_data["on"]
            curr_data["send_pulse"] = on2pulse[curr_data["on"]]

    elif curr_data["symbol"] == "&":
        curr_data["inputs"][prev_node] = curr_data["receive_pulse"]
        inv = "low" if all(
            x == "high" for x in curr_data["inputs"].values()
        ) else "high"
        curr_data["send_pulse"] = inv

    return pulses


def end_cycle(D):
    flipflops_false = all(
        not data["on"]
        for _, data in D.nodes(data=True)
        if data["symbol"] == "%"
    )
    conjunctions_low = all(
        all(v == "low" for v in data["inputs"].values())
        for _, data in D.nodes(data=True)
        if data["symbol"] == "&"
    )
    return flipflops_false and conjunctions_low


def display(D):
    print("nodes:")
    for n in D.nodes(data=True):
        print(n)
    print("\n", "edges:")
    print(D.edges(data=True))
    return


def start_machine(data, max_buttons=1000):
    D = make_modules(data)
    start_pulses = [("button", "broadcaster")]
    next_pulses = copy.deepcopy(start_pulses)
    pulses = {"low": 0, "high": 0}
    high_pulses = {}
    buttons = 1
    while (next_pulses or not end_cycle(D)) and buttons <= max_buttons:
        prev_node, curr_node = next_pulses.pop(0)

        curr_pulse = receive_pulse(D, prev_node, curr_node)
        pulses["low"] += curr_pulse["low"]
        pulses["high"] += curr_pulse["high"]

        next_nodes = [node[0] for node in sorted(
            [(s, D.edges[curr_node, s]) for s in D.successors(curr_node)],
            key=lambda x: (x[1]["order"])
        )]

        curr_data = D.nodes[curr_node]
        if not (curr_data["symbol"] == "%" and curr_data["receive_pulse"] == "high"):
            next_pulses += [(curr_node, node) for node in next_nodes if (curr_node, node)]

        if curr_data.get("send_pulse", None) == "high" and curr_node not in high_pulses:
            high_pulses[curr_node] = buttons

        if not next_pulses and not end_cycle(D):
            next_pulses = copy.deepcopy(start_pulses)
            buttons += 1
    return pulses, high_pulses


def first_star(data):
    pulses, _ = start_machine(data, max_buttons=1000)
    return pulses["low"] * pulses["high"]


def check_graph(D):
    view_nodes = ["rx"] + list(D.predecessors("rx")) + [
        list(D.predecessors(n)) for n in list(D.predecessors("rx"))
    ][0]

    S = D.subgraph(view_nodes)
    display(S)
    return


def second_star(data):
    _, high_pulses = start_machine(data, max_buttons=5000)
    second_last = {k: v for k, v in high_pulses.items() if k in ("mm", "fk", "ff", "lh")}
    return lcm(*second_last.values())


if __name__ == "__main__":
    with open(f"data/2023/20.txt", "r") as f:
        data = f.read()

    #     data = """broadcaster -> a, b, c
    # %a -> b
    # %b -> c
    # %c -> inv
    # &inv -> a"""

    #     data = """broadcaster -> a
    # %a -> inv, con
    # &inv -> b
    # %b -> con
    # &con -> output"""

    print(first_star(data))
    print(second_star(data))
