
def parse(data):
    return list(map(int, data.strip().split("\n")))

def first_star(data):
    depths = parse(data)
    return sum([
        1 if depths[i] > depths[i - 1] else 0
        for i in range(1, len(depths))
    ])


def second_star(data):
    depths = parse(data)
    windows = [
        sum(depths[i:i + 3])
        for i in range(0, len(depths) - 2)
    ]
    return sum([
        1 if windows[i] > windows[i - 1] else 0
        for i in range(1, len(windows))
    ])


if __name__ == "__main__":
    with open(f"data/2021/01.txt", "r") as f:
        data = f.read()
        #         data = """199
        # 200
        # 208
        # 210
        # 200
        # 207
        # 240
        # 269
        # 260
        # 263"""

    print(first_star(data))
    print(second_star(data))
