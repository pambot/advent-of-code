import numpy as np


def tree_matrix(data):
    return np.array([[int(i) for i in d] for d in data.splitlines()])


def first_star(data):
    trees = tree_matrix(data)
    rows, cols = trees.shape
    count_v = 0
    for m in range(1, rows - 1):
        for n in range(1, cols - 1):
            t = trees[m, n]

            v_up = np.all(trees[:m, n] < t)
            v_down = np.all(trees[m + 1:, n] < t)
            v_left = np.all(trees[m, :n] < t)
            v_right = np.all(trees[m, n + 1:] < t)

            if any((v_up, v_down, v_left, v_right)):
                count_v += 1

    perimeter = rows * 2 + (cols - 2) * 2
    return count_v + perimeter


def view_distance(view, t):
    if len(view) == 0:
        return 0
    elif np.all(view < t):
        return len(view)
    else:
        return np.argmax(view >= t) + 1


def second_star(data):
    trees = tree_matrix(data)
    rows, cols = trees.shape
    scenic = 0
    for m in range(rows):
        for n in range(cols):
            t = trees[m, n]

            d_up = view_distance(np.flip(trees[:m, n]), t)
            d_down = view_distance(trees[m + 1:, n], t)
            d_left = view_distance(np.flip(trees[m, :n]), t)
            d_right = view_distance(trees[m, n + 1:], t)

            new_scenic = d_up * d_down * d_left * d_right
            if new_scenic > scenic:
                scenic = new_scenic
    return scenic


if __name__ == "__main__":
    with open(f"data/2022/08.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
