import itertools


def stack_crates(data):
    unpacked = [list(d) for d in data.splitlines()[:8][::-1]]
    extracted = list(map(list, itertools.zip_longest(*unpacked, fillvalue=" ")))[1::4]
    return [[i for i in e if i != " "] for e in extracted]


def get_instructions(data):
    parsed = [
        [int(i) for i in d.split(" ") if i.isnumeric()]
        for d in data.splitlines()[10:]
    ]
    return [(p[0], p[1] - 1, p[2] - 1) for p in parsed] # python indexing


def print_crates(crates):
    for c in crates:
        print("".join(c))
    print("------")


def first_star(data):
    crates = stack_crates(data)
    instructions = get_instructions(data)

    for ins in instructions:
        for _ in range(ins[0]):
            moved = crates[ins[1]].pop()
            crates[ins[2]].append(moved)

    return "".join([c[-1] for c in crates])


def second_star(data):
    crates = stack_crates(data)
    instructions = get_instructions(data)

    for ins in instructions:
        moved = crates[ins[1]][-ins[0]:]
        del crates[ins[1]][-ins[0]:]
        crates[ins[2]].extend(moved)

    return "".join([c[-1] for c in crates])


if __name__ == "__main__":
    with open(f"data/2022/05.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
