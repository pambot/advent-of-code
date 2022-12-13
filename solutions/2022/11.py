import math


class Monkey:
    def __init__(self, starting_items, operation, test):
        self.starting_items = starting_items
        self.operation = operation
        self.test = test
        self.total_thrown = 0


def make_monkeys():
    return [
        Monkey([66, 71, 94], lambda o: o * 5, lambda t: 7 if t % 3 == 0 else 4),
        Monkey([70], lambda o: o + 6, lambda t: 3 if t % 17 == 0 else 0),
        Monkey([62, 68, 56, 65, 94, 78], lambda o: o + 5, lambda t: 3 if t % 2 == 0 else 1),
        Monkey([89, 94, 94, 67], lambda o: o + 2, lambda t: 7 if t % 19 == 0 else 0),
        Monkey([71, 61, 73, 65, 98, 98, 63], lambda o: o * 7, lambda t: 5 if t % 11 == 0 else 6),
        Monkey([55, 62, 68, 61, 60], lambda o: o + 7, lambda t: 2 if t % 5 == 0 else 1),
        Monkey([93, 91, 69, 64, 72, 89, 50, 71], lambda o: o + 1, lambda t: 5 if t % 13 == 0 else 2),
        Monkey([76, 50], lambda o: o * o, lambda t: 4 if t % 7 == 0 else 6)
    ]


def first_star(data):
    monkeys = make_monkeys()
    for _ in range(20):
        for monkey in monkeys:
            for _ in range(len(monkey.starting_items)):
                worry = monkey.starting_items.pop(0)
                worry = monkey.operation(worry)
                worry = math.floor(worry / 3)
                throw_to = monkey.test(worry)
                monkeys[throw_to].starting_items += [worry]
                monkey.total_thrown += 1
    thrown = sorted([m.total_thrown for m in monkeys])
    return thrown[-1] * thrown[-2]


def second_star(data):
    monkeys = make_monkeys()
    supermodulo = 3 * 17 * 2 * 19 * 11 * 5 * 13 * 7
    for _ in range(10000):
        for monkey in monkeys:
            for _ in range(len(monkey.starting_items)):
                worry = monkey.starting_items.pop(0)
                worry = monkey.operation(worry)
                worry = worry % supermodulo
                throw_to = monkey.test(worry)
                monkeys[throw_to].starting_items += [worry]
                monkey.total_thrown += 1
    thrown = sorted([m.total_thrown for m in monkeys])
    return thrown[-1] * thrown[-2]


if __name__ == "__main__":
    with open(f"data/2022/11.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
