import re
import numpy as np


def parse_input(data):
    return [
        [int(n) for n in re.findall("-?\d+", d)]
          for d in data.splitlines()
    ]


def get_minus_collect(nums_list):
    minus_collect = []
    for nums in nums_list:
        minus_nums = nums
        minus_group = []
        while len(set(minus_nums)) != 1:
            minus_nums = [m - n for m, n in zip(minus_nums, [0] + minus_nums[:-1])][1:]
            minus_group.append(minus_nums)
        minus_group = [nums] + minus_group
        minus_collect.append(minus_group)
    return minus_collect


def first_star(data):
    nums_list = parse_input(data)
    minus_collect = get_minus_collect(nums_list)

    history = 0
    for minus_group in minus_collect:
        starter = minus_group.pop()
        next = None
        while minus_group:
            next = minus_group.pop()
            next += [next[-1] + starter[-1]]
            starter = next

        history += next[-1]
    return history


def second_star(data):
    nums_list = parse_input(data)
    minus_collect = get_minus_collect(nums_list)

    history = 0
    for minus_group in minus_collect:
        starter = minus_group.pop()
        next = None
        while minus_group:
            next = minus_group.pop()
            next = [next[0] - starter[0]] + next
            starter = next

        history += next[0]
    return history


if __name__ == "__main__":
    with open(f"data/2023/09.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
