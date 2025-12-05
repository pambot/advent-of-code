
def parse(data):
    fresh_input, available_input = data.split("\n\n")

    fresh_ids = [list(map(int, f.split("-"))) for f in fresh_input.split("\n") if f]
    available_ids = [int(a) for a in available_input.split("\n") if a]

    return fresh_ids, available_ids


def first_star(data):
    fresh_ids, available_ids = parse(data)
    fresh_count = 0
    for _id in available_ids:
        for fl, fr in fresh_ids:
            if fl <= _id <= fr:
                fresh_count += 1
                break
    return fresh_count


def second_star(data):
    fresh_ids, _ = parse(data)
    fresh_ids = sorted(fresh_ids, key=lambda x: x[0])

    intervals = [fresh_ids[0]]
    for cl, cr in fresh_ids[1:]:
        pl, pr = intervals[-1]
        if pr >= cl and pr < cr:
            intervals[-1] = [pl, cr]
        elif pr < cl and pr < cr:
            intervals.append([cl, cr])
        else:
            pass

    s = 0
    for il, ir in intervals:
        s += ir - il + 1

    return s


if __name__ == "__main__":
    with open(f"data/2025/05.txt", "r") as f:
        data = f.read()
        data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

    print(first_star(data))
    print(second_star(data))
