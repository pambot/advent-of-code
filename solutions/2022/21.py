import operator
import math
from scipy.stats import linregress


OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    "=": operator.eq,
}


def monkey_do(monkeys, m1, m2, operation):
    if isinstance(monkeys[m1], int):
        monkey1 = monkeys[m1]
    else:
        next_m1, next_m2, op = monkeys[m1]
        monkey1 = monkey_do(monkeys, next_m1, next_m2, op)
    if isinstance(monkeys[m2], int):
        monkey2 = monkeys[m2]
    else:
        next_m1, next_m2, op = monkeys[m2]
        monkey2 = monkey_do(monkeys, next_m1, next_m2, op)
    return operation(monkey1, monkey2)


def parse_monkeys(data):
    monkeys = dict()
    for d in data.splitlines():
        monkey, command = d.split(": ")
        try:
            number = int(command)
            monkeys[monkey] = number
        except:
            m1, op, m2 = command.split(" ")
            monkeys[monkey] = (m1, m2, OPERATORS[op])
    return monkeys


def first_star(data):
    monkeys = parse_monkeys(data)
    m1, m2, op = monkeys["root"]
    return monkey_do(monkeys, m1, m2, op)


def return_values(m1, m2):
    return m1, m2


def binary_search(one, search_num):
    low = 0
    high = len(one) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if one[mid] == search_num:
            high = mid - 1
        else:
            return mid
    return -1

def second_star(data):
    monkeys = parse_monkeys(data)
    m1, m2, _ = monkeys["root"]
    x = list()
    y = list()
    for i in range(0, 10000000, 1000000):
        monkeys["humn"] = i
        left, right = monkey_do(monkeys, m1, m2, return_values)
        x.append(i)
        y.append(left)
    ln = linregress(x, y)
    low_estimate = math.floor((right - (ln.intercept + ln.intercept_stderr)) / (ln.slope - ln.stderr))
    high_estimate = math.floor((right - (ln.intercept - ln.intercept_stderr)) / (ln.slope + ln.stderr))

    for try_estimate in range(low_estimate, high_estimate):
        monkeys["humn"] = try_estimate
        match = monkey_do(monkeys, m1, m2, operator.eq)
        if match:
            break
    return try_estimate


if __name__ == "__main__":
    with open(f"data/2022/21.txt", "r") as f:
        data = f.read()

    example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

    print(first_star(data))
    print(second_star(data))
