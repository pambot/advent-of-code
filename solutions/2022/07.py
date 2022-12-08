import networkx as nx
import pdb


def dir_name(command):
    return command.split(" ")[-1]


def file_info(command):
    c = command.split(" ")
    return int(c[0]), c[1]


def add_dir(G, current_dir, next_dir=None):
    if next_dir:
        G.add_node(next_dir, size=0, is_dir=True)
        G.add_edge(current_dir, next_dir)
    else:
        G.add_node(current_dir, size=0, is_dir=True)
    return G


def add_file(G, current_dir, file_name, file_size):
    G.add_node(file_name, size=file_size, is_dir=False)
    G.add_edge(current_dir, file_name)
    return G


def fp(file_path):
    return "/".join(file_path)


def make_file_graph(data):
    commands = data.splitlines()
    G = nx.DiGraph()
    for com in commands:
        if com == "$ cd /":
            file_path = ["home"]
            add_dir(G, fp(file_path))
        elif com.startswith("$ cd") and com != "$ cd ..":
            if not G.has_edge(fp(file_path), fp(file_path + [dir_name(com)])):
                add_dir(G, fp(file_path), fp(file_path + [dir_name(com)]))
            file_path.append(dir_name(com))
        elif com.startswith("dir"):
            if not G.has_edge(fp(file_path), fp(file_path + [dir_name(com)])):
                add_dir(G, fp(file_path), fp(file_path + [dir_name(com)]))
        elif com == "$ cd ..":
            file_path.pop()
        elif com[0].isdigit():
            file_size, file_name = file_info(com)
            add_file(G, fp(file_path), fp(file_path + [file_name]), file_size)
    return G


def subdir_size(G, node):
    sub_dir = [n for n in nx.dfs_tree(G, node)]
    return sum([G.nodes(data="size")[s] for s in sub_dir])


def first_star(data):
    G = make_file_graph(data)
    sizes = []
    for node in G.nodes():
        dir_size = subdir_size(G, node)
        if dir_size < 100_000 and G.nodes(data="is_dir")[node]:
            sizes.append(dir_size)
    return sum(sizes)


def second_star(data):
    G = make_file_graph(data)
    dir_size = subdir_size(G, "home")
    need_free = (dir_size - 70_000_000) + 30_000_000
    sizes = []
    for node in G.nodes():
        dir_size = subdir_size(G, node)
        if dir_size >= need_free and G.nodes(data="is_dir")[node]:
            sizes.append(dir_size)
    return min(sizes)


if __name__ == "__main__":
    with open(f"data/2022/07.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
