from collections import defaultdict


def first_star(data):
    stones = list(map(int, data.strip().split()))

    for _ in range(25):
        new = []
        for s in stones:
            ss = str(s)
            if s == 0:
                new.append(1)
            elif len(ss) % 2 == 0:
                mid = len(ss) // 2
                new.extend([int(ss[:mid]), int(ss[mid:])])
            else:
                new.append(s * 2024)
        stones = new
    return len(new)


def second_star(data):
    stones = defaultdict(int)

    for d in data.strip().split():
        stones[int(d)] = 1

    for _ in range(75):
        new = defaultdict(int)
        for s in stones.keys():
            ss = str(s)
            if s == 0:
                new[1] += stones[s]
            elif len(ss) % 2 == 0:
                mid = len(ss) // 2
                new[int(ss[:mid])] += stones[s]
                new[int(ss[mid:])] += stones[s]
            else:
                new[s * 2024] += stones[s]
        stones = new
    return sum([v for v in new.values()])


if __name__ == "__main__":
    with open(f"data/2024/11.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
