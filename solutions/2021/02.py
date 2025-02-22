
def parse(data):
    return [
        (d.split()[0], int(d.split()[1]))
        for d in data.strip().split("\n")
    ]


def first_star(data):
    moves = parse(data)
    horizontal, depth = 0, 0
    for direction, value in moves:
        if direction == 'forward':
            horizontal += value
        elif direction == 'down':
            depth += value
        elif direction == 'up':
            depth -= value
    return horizontal * depth


def second_star(data):
    moves = parse(data)
    horizontal, depth, aim = 0, 0, 0
    for direction, value in moves:
        if direction == 'forward':
            horizontal += value
            depth += aim * value
        elif direction == 'down':
            aim += value
        elif direction == 'up':
            aim -= value
    return horizontal * depth


if __name__ == "__main__":
    with open(f"data/2021/02.txt", "r") as f:
        data = f.read()
        #         data = """
        # forward 5
        # down 5
        # forward 8
        # up 3
        # down 8
        # forward 2"""

    print(first_star(data))
    print(second_star(data))
