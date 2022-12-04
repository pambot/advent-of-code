
def make_pair_ranges(data):
    pair_splits = [d.split(",") for d in data.splitlines()]
    pair_ranges = [
        (list(map(int, p[0].split("-"))), list(map(int, p[1].split("-"))))
        for p in pair_splits
    ]
    return pair_ranges


def first_star(data):
    pair_ranges = make_pair_ranges(data)
    return len(
        [p for p in pair_ranges if
            (p[0][0] >= p[1][0] and p[0][1] <= p[1][1]) or
            (p[1][0] >= p[0][0] and p[1][1] <= p[0][1])]
    )


def second_star(data):
    pair_ranges = make_pair_ranges(data)
    rearrange_pairs = [(p[0], p[1]) if p[0][0] < p[1][0] else (p[1], p[0]) for p in pair_ranges]
    return len([p for p in rearrange_pairs if (p[0][1] >= p[1][0])])


if __name__ == "__main__":
    with open(f"data/2022/04.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
