import string


PRIORITY = {k:v for k, v in zip(string.ascii_letters, range(1, 53))}

def first_star(data):
    rucksacks = [[d[:int(len(d)/2)], d[int(len(d)/2):]] for d in data.splitlines()]
    return sum([PRIORITY[(set(r[0]) & set(r[1])).pop()] for r in rucksacks])


def second_star(data):
    rucksacks = data.splitlines()
    groups = [rucksacks[i:i + 3] for i in range(0, len(rucksacks), 3)]
    return sum([PRIORITY[(set(g[0]) & set(g[1]) & set(g[2])).pop()] for g in groups])


if __name__ == "__main__":
    with open(f"data/2022/03.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
