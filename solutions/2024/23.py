import networkx as nx


def parse(data):
    links = [t.split("-") for t in data.strip().splitlines()]

    L = nx.Graph()
    for l0, l1 in links:
        L.add_edge(l0, l1)

    return L


def first_star(data):
    L = parse(data)

    three_sets = set()
    for l0, l1 in L.edges():
        ln0 = L.neighbors(l0)
        ln1 = L.neighbors(l1)
        mids = set(ln0) & set(ln1)
        for m in mids:
            three_sets.add(tuple(sorted((l0, m, l1))))

    return len([s for s in three_sets if any(t[0] == 't' for t in s)])


def second_star(data):
    L = parse(data)
    return ','.join(sorted(max(nx.find_cliques(L), key=len)))


if __name__ == "__main__":
    with open(f"data/2024/23.txt", "r") as f:
        data = f.read()
        #         data = """kh-tc
        # qp-kh
        # de-cg
        # ka-co
        # yn-aq
        # qp-ub
        # cg-tb
        # vc-aq
        # tb-ka
        # wh-tc
        # yn-cg
        # kh-ub
        # ta-co
        # de-co
        # tc-td
        # tb-wq
        # wh-td
        # ta-ka
        # td-qp
        # aq-cg
        # wq-ub
        # ub-vc
        # de-ta
        # wq-aq
        # wq-vc
        # wh-yn
        # ka-de
        # kh-ta
        # co-tc
        # wh-qp
        # tb-vc
        # td-yn"""

    print(first_star(data))
    print(second_star(data))
