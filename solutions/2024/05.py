from collections import defaultdict


def parse(data):
    raw_rules, raw_updates = data.strip().split("\n\n")
    rules = [tuple(map(int, r.split("|"))) for r in raw_rules.split("\n")]
    updates = [tuple(map(int, u.split(","))) for u in raw_updates.split("\n")]
    return rules, updates


def make_rules_lookup(rules):
    rules_lookup = defaultdict(list)
    for r in rules:
        a, b = r
        rules_lookup[a].append(r)
        rules_lookup[b].append(r)
    return rules_lookup


def first_star(data):
    rules, updates = parse(data)
    rules_lookup = make_rules_lookup(rules)
    mid = 0
    for update in updates:
        u_lookup = {update[s]: s for s in range(len(update))}
        passed = True
        for u in u_lookup.keys():
            u_rules = rules_lookup[u]
            for r0, r1 in u_rules:
                if (
                    (r0 in u_lookup and r1 in u_lookup) and
                    (not u_lookup[r0] < u_lookup[r1])
                ):
                    passed = False

        if passed:
            m = int((len(update) + 1) / 2 - 1)
            mid += update[m]

    return mid


def topological_sort(graph, start):
    stack = [start]
    seen = set()
    result = []
    while stack:
        visit = stack[-1] # just inspect
        seen.add(visit)
        next = [n for n in graph[visit] if n not in seen]
        if not next:
            result = [visit] + result
            stack.pop()
        else:
            stack.append(next[0])
    return result


def second_star(data):
    rules, updates = parse(data)
    mid = 0
    for update in updates:
        update_nodes = set(update)
        node_nodes = set()
        edge_nodes = set()
        graph = defaultdict(list)
        for r0, r1 in rules:
            if r0 in update_nodes and r1 in update_nodes:
                graph[r0].append(r1)
                node_nodes.add(r0)
                edge_nodes.add(r1)
        start = list(node_nodes - edge_nodes)[0]
        path = topological_sort(graph, start)
        fixed = []
        for p in path:
            if p in update_nodes:
                fixed.append(p)
        fixed = tuple(fixed)
        if fixed != update:
            m = int((len(fixed) + 1) / 2 - 1)
            mid += fixed[m]
    return mid


if __name__ == "__main__":
    with open(f"data/2024/05.txt", "r") as f:
        data = f.read()
        #         data = """47|53
        # 97|13
        # 97|61
        # 97|47
        # 75|29
        # 61|13
        # 75|53
        # 29|13
        # 97|29
        # 53|29
        # 61|53
        # 97|53
        # 61|29
        # 47|13
        # 75|47
        # 97|75
        # 47|61
        # 75|61
        # 47|29
        # 75|13
        # 53|13

        # 75,47,61,53,29
        # 97,61,53,29,13
        # 75,29,13
        # 75,97,47,61,53
        # 61,13,29
        # 97,13,75,29,47"""

    print(first_star(data))
    print(second_star(data))
