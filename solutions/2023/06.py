import re
from functools import reduce
from operator import mul


def parse_input1(data):
    time = list(map(int, re.findall("\d+", data.split("\n")[0])))
    distance = list(map(int, re.findall("\d+", data.split("\n")[1])))
    return list(zip(time, distance))


def parse_input2(data):
    time = int("".join(re.findall("\d+", data.split("\n")[0])))
    distance = int("".join(re.findall("\d+", data.split("\n")[1])))
    return time, distance


def boat_wins(time, dist, hold):
    return dist < (time - hold) * hold


def first_star(data):
    boats = parse_input1(data)
    wins = []
    for t, d in boats:
        w = 0
        for h in range(0, t):
            if boat_wins(t, d, h):
                w += 1
        wins.append(w)
    return reduce(mul, wins)


def second_star(data):
    t, d = parse_input2(data)
    w = 0
    for h in range(5 * 10**6, t):
        if boat_wins(t, d, h):
            w += 1
        if w > 0 and not boat_wins(t, d, h):
            break
    return w


if __name__ == "__main__":
    with open(f"data/2023/06.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
