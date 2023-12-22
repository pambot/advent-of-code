import numpy as np

def display(layout):
    print("\n".join(["".join(l) for l in layout.tolist()]))


def gigantify_farm(farm, factor):
    assert factor > 1 and factor % 2 == 1
    large_farm = farm.copy()
    large_farm[np.where(large_farm == "S")] = "."
    large_farm = np.vstack([np.hstack([large_farm] * factor)] * factor)
    nrows, ncols = large_farm.shape
    large_farm[int((nrows - 1)/2), int((ncols - 1)/2)] = "S"
    return large_farm


def garden_walk(farm, steps, factor=1, part=1):
    rocks = set([tuple(l) for l in np.argwhere(farm == "#")])
    prev_nodes = [tuple(l) for l in np.argwhere(farm == "S")]
    fs = farm.shape[0] / factor

    gardens = []
    for n in range(1, steps + 1):
        next_nodes = []
        for pr, pc in prev_nodes:
            for mr, mc in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                next_node = (pr + mr, pc + mc)
                if not next_node in rocks:
                    next_nodes.append(next_node)

        prev_nodes = list(set(next_nodes))
        if part == 1 and n == 64:
            return len(prev_nodes)
        if part == 2 and n in (fs // 2, fs // 2 + fs, fs // 2 + fs * 2):
            gardens.append([n, len(prev_nodes)])
    return gardens


def first_star(data):
    farm = np.array([list(d) for d in data.splitlines()])
    return garden_walk(farm, 64, 1, 1)


def second_star(data):
    farm = np.array([list(d) for d in data.splitlines()])
    large_farm = gigantify_farm(farm, factor=3)
    factor = 3
    fs = large_farm.shape[0] / factor
    print(garden_walk(large_farm, int(fs * factor), factor, 2))

    # used Wolfram for curve fit
    t = (26501365 - 65) / 131
    return 15197 * t**2 + 15303 * t + 3868


if __name__ == "__main__":
    with open(f"data/2023/21.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
