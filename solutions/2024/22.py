import math
from functools import cache
from collections import defaultdict


@cache
def secret(s):
    m = s * 64
    s = m ^ s
    s = s % 16777216

    m = int(math.floor(s / 32))
    s = m ^ s
    s = s % 16777216

    m =  s * 2048
    s = m ^ s
    s = s % 16777216
    return s


def first_star(data):
    secrets = list(map(int, data.strip().splitlines()))

    results = []
    for s in secrets:
        for _ in range(2000):
            s = secret(s)
        results.append(s)
    return sum(results)


def second_star(data):
    secrets = list(map(int, data.strip().splitlines()))

    diff_monkeys = []
    price_monkeys = []
    for s in secrets:
        prices = []
        diffs = []
        p = int(str(s)[-1])
        for _ in range(2000):
            s = secret(s)
            v = int(str(s)[-1])
            diffs.append(v - p)
            prices.append(v)
            p = v
        diff_monkeys.append(diffs)
        price_monkeys.append(prices)

    diff2price = defaultdict(list)
    for diffs, prices in zip(diff_monkeys, price_monkeys):
        seen = set()
        for a, b, c, d, p in zip(diffs, diffs[1:], diffs[2:], diffs[3:], prices[3:]):
            if (a, b, c, d) not in seen:
                diff2price[(a, b, c, d)].append(p)
                seen.add((a, b, c, d))

    diff2sum = {k: sum(v) for k, v in diff2price.items()}
    return diff2sum[max(diff2sum, key=diff2sum.get)]


if __name__ == "__main__":
    with open(f"data/2024/22.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
