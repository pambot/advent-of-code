import re
import ast


def first_star(data):
    muls = re.findall(r"mul\([0-9]+,[0-9]+\)", data)
    nums = [ast.literal_eval(m.replace("mul", "")) for m in muls]
    return sum([n * m for n, m in nums])

def second_star(data):
    muls = re.findall(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", data)
    clean = []
    for m in muls:
        if m.startswith("mul"):
            clean.append(ast.literal_eval(m.replace("mul", "")))
        else:
            clean.append(m)
    do = True
    res = 0
    for c in clean:
        if c == "don't()":
            do = False
        elif c == "do()":
            do = True
        else:
            n, m = c
            if do:
                res += n * m
    return res


if __name__ == "__main__":
    with open(f"data/2024/03.txt", "r") as f:
        data = f.read()
        # data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
        # data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    print(first_star(data))
    print(second_star(data))
