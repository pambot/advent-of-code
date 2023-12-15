import re
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial


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


def lagrangian_interpolation(nums, i):
    """
    LI works like this:

    For an array like this: [1, 3, 6]
    Convert to (x, y): [(0, 1), (1, 3), (2, 6)]
    Here, x is just their indices

    Turn distances between pairwise x-values into Lagrangian basis polynomials. This has the property that the i-th basis polynomial plugged with (xi, yi) will be 1 but will be 0 at any (xj, yj) where j != i (and it will be some continuum of real numbers when it's not i or j).

        l(x)[i] = Π[(x - xj) / (xi - xj)], for i != j

    l(x) = [
        (x - 1)/(0 - 1) * (x - 2)/(0 - 2),
        (x - 0)/(1 - 0) * (x - 2)/(1 - 2),
        (x - 0)/(2 - 0) * (x - 1)/(2 - 1)
    ] = [
        -(x - 1) * -1/2(x - 2),
        -x * (x - 2),
        x/2 * (x - 1)
    ]

    The Lagrangian interpolating polynomial, the thing that converts a new data point xk -> yk, is the dot product of your basis polynomials and y, your original array values.

    L(x) = Σ l(x) ⋅ y
    L(x) = -(x - 1) * -1(x - 2)/2 + 3(-x * (x - 2)) + 6(x/2 * (x - 1))
         = (x**2 + 3x + 2)/2

    L(2) = (4 + 6 + 2)/2 = 6
    L(3) = (9 + 9 + 2)/2 = 10
    etc.

    L(6) = (36 + 18 + 2)/2 = 28
    L(-1) = (1 - 3 + 2)/2 = 0

    Since the basis polynomials were just made with the index coordinates, which are always [0, 1, 2, ...] for us, the basis polynomials don't change if you're just extrapolating an array of y-values. You need only as many basis polynomials as the number of data points needed to establish the pattern, which is the number of rows you have to do diffs on until you hit all 0's.

    Okay, now that we've learned all this, is there some easy thing that does does it all for me?
    """
    if not i:
        i = len(nums)

    coefs = lagrange(range(len(nums)), nums)
    poly = Polynomial(coefs.coef[::-1])
    return round(poly(i))


def stars_with_lagrangian(data, i=None):
    history = 0
    for nums in parse_input(data):
        history += lagrangian_interpolation(nums, i)
    return history


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

    #     data = """0 3 6 9 12 15
    # 1 3 6 10 15 21
    # 10 13 16 21 30 45"""

    print(first_star(data))
    print(stars_with_lagrangian(data))
    print(second_star(data))
    print(stars_with_lagrangian(data, -1))
