import re
import numpy as np


def parse(data):
    lines = data.strip().split("\n")
    button_a = [tuple(map(int, re.findall(r'\d+', s))) for s in lines[::4]]
    button_b = [tuple(map(int, re.findall(r'\d+', s))) for s in lines[1::4]]
    prizes = [tuple(map(int, re.findall(r'\d+', s))) for s in lines[2::4]]
    return button_a, button_b, prizes


def first_star(data):
    button_a, button_b, prizes = parse(data)
    tokens = 0
    for a, b, p in zip(button_a, button_b, prizes):
        m = np.array([a, b]).T
        r = np.linalg.solve(m, p)
        if np.allclose(np.dot(m, np.round(r)), p):
            tokens += r[0] * 3 + r[1]
    return int(tokens)


def second_star(data):
    button_a, button_b, prizes = parse(data)
    prizes = [(10000000000000 + p[0], 10000000000000 + p[1]) for p in prizes]
    tokens = 0
    for a, b, p in zip(button_a, button_b, prizes):
        m = np.array([a, b]).T
        r = np.linalg.solve(m, p)
        if np.array_equal(
            np.round(r, decimals=0),
            np.round(r, decimals=3)
        ):
            tokens += r[0] * 3 + r[1]
    return int(tokens)


if __name__ == "__main__":
    with open(f"data/2024/13.txt", "r") as f:
        data = f.read()
        #         data = """Button A: X+94, Y+34
        # Button B: X+22, Y+67
        # Prize: X=8400, Y=5400

        # Button A: X+26, Y+66
        # Button B: X+67, Y+21
        # Prize: X=12748, Y=12176

        # Button A: X+17, Y+86
        # Button B: X+84, Y+37
        # Prize: X=7870, Y=6450

        # Button A: X+69, Y+23
        # Button B: X+27, Y+71
        # Prize: X=18641, Y=10279"""

    print(first_star(data))
    print(second_star(data))
