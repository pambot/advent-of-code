
def parse(data):
    return [(i[0], int(i[1:])) for i in data.strip().split("\n")]


def first_star(data):
    turns = parse(data)
    c = 50
    z = 0
    for t in turns:
        d, n = t
        if d == "L":
            r = c - n
        elif d == "R":
            r = c + n

        c = r % 100
        if c == 0:
            z += 1
    return z


def second_star(data):
    turns = parse(data)
    c = 50
    z = 0
    for t in turns:
        d, n = t
        if d == "R":
            r = c + n
            s = range(c + 1, r + 1, 1)
        elif d == "L":
            r = c - n
            s = range(c - 1, r - 1, -1)

        c = r % 100
        z += sum([n % 100 == 0 for n in s])
    return z


if __name__ == "__main__":
    with open(f"data/2025/01.txt", "r") as f:
        data = f.read()
        #         data = """L68
        # L30
        # R48
        # L5
        # R60
        # L55
        # L1
        # L99
        # R14
        # L82"""

    print(first_star(data))
    print(second_star(data))
