from collections import Counter


def parse(data):
    nums = [list(map(int, s.split("   "))) for s in data.splitlines()]
    firsts = sorted([f[0] for f in nums])
    seconds = sorted([f[1] for f in nums])
    return firsts, seconds


def first_star(data):
    firsts, seconds = parse(data)
    compare = sum([abs(f - s) for f, s in zip(firsts, seconds)])
    return compare


def second_star(data):
    firsts, seconds = parse(data)
    counts = Counter(seconds)
    return sum([f * counts.get(f, 0) for f in firsts])


if __name__ == "__main__":
    with open(f"data/2024/01.txt", "r") as f:
        data = f.read()
        #         data = """3   4
        # 4   3
        # 2   5
        # 1   3
        # 3   9
        # 3   3"""

    print(first_star(data))
    print(second_star(data))
