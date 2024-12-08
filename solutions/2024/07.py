from operator import add, mul
from itertools import product


def parse(data):
    v = [
        list(map(int, d.replace(":", "").split(" ")))
        for d in data.strip().split("\n")
    ]
    return [(n[0], n[1:]) for n in v]


def first_star(data):
    nums = parse(data)
    total = 0
    for ans, num in nums:
        permute_ops = list(product([add, mul], repeat=len(num) - 1))
        val = num[0]
        for ops in permute_ops:
            for nu, op in zip(num[1:], ops):
                val = op(val, nu)
                if val > ans:
                    break
            if val == ans:
                total += ans
                break
            val = num[0]
    return total


def cat(a, b):
    return int(str(a) + str(b))


def check_paths(ans, vals):
    paths = []
    def check_last(ans, vals):
        v = vals[-1]
        if len(vals) == 1 and v == ans:
            paths.append(True)
            return
        elif len(vals) == 1 and v != ans:
            paths.append(False)
            return
        elif v > ans or ans <= 0:
            paths.append(False)
            return
        else:
            if ans % v == 0:
                check_last(
                    int(ans / v),
                    vals[:-1]
                )
            if str(ans).endswith(str(v)):
                uncat_ans = str(ans).removesuffix(str(v))
                if not uncat_ans:
                    next_ans = 0
                else:
                    next_ans = uncat_ans
                check_last(
                    int(next_ans),
                    vals[:-1]
                )
            check_last(
                ans - v,
                vals[:-1]
            )
    check_last(ans, vals)
    return any(paths)


def second_star(data):
    nums = parse(data)
    total = 0
    for ans, vals in nums:
        check = check_paths(ans, vals)
        if check:
            total += ans
    return total


if __name__ == "__main__":
    with open(f"data/2024/07.txt", "r") as f:
        data = f.read()
        #         data = """
        # 190: 10 19
        # 3267: 81 40 27
        # 83: 17 5
        # 156: 15 6
        # 7290: 6 8 6 15
        # 161011: 16 10 13
        # 192: 17 8 14
        # 21037: 9 7 18 13
        # 292: 11 6 16 20
        # """

    print(first_star(data))
    print(second_star(data))
