import networkx as nx


def get_six_sides(coord):
    x, y, z = coord
    return [
        (x - 1, y, z), (x + 1, y, z),
        (x, y - 1, z), (x, y + 1, z),
        (x, y, z - 1), (x, y, z + 1),
    ]


def first_star(data):
    lava_coords = [tuple(map(int, d.split(","))) for d in data.splitlines()]
    lava_coords_set = set(lava_coords)
    exposed_sides = 0
    for coord in lava_coords:
        exposed_sides += len([c for c in get_six_sides(coord) if c not in lava_coords_set])
    return exposed_sides


def make_space_graph(c_max):
    G = nx.Graph()
    for x in range(-1, c_max + 2):
        for y in range(-1, c_max + 2):
            for z in range(-1, c_max + 2):
                this_coord = (x, y, z)
                for next_coord in get_six_sides(this_coord):
                    G.add_edge(this_coord, next_coord)
    return G


def second_star(data):
    lava_coords = set([tuple(map(int, d.split(","))) for d in data.splitlines()])
    c_max = max([c for cs in lava_coords for c in cs])
    G = make_space_graph(c_max)
    space_coords = set(G.nodes())
    G.remove_nodes_from(lava_coords)
    steam_coords = set(nx.dfs_preorder_nodes(G, source=(0, 0, 0)))
    air_pocket_coords = space_coords - steam_coords - lava_coords
    lava_coords.update(air_pocket_coords)
    exposed_sides = 0
    for coord in lava_coords:
        exposed_sides += len([c for c in get_six_sides(coord) if c not in lava_coords])
    return exposed_sides






if __name__ == "__main__":
    with open(f"data/2022/18.txt", "r") as f:
        data = f.read()

    example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

    print(first_star(data))
    print(second_star(data))
