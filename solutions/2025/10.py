import ast
import itertools
import operator
import numpy as np
from functools import reduce
from scipy.optimize import milp, Bounds, LinearConstraint


def parse(data):
    manual = []
    for line in data.strip().split("\n"):
        raw = line.split(" ")
        lights = [1 if r == "#" else 0 for r in raw.pop(0)[1:-1]]
        joltage = ast.literal_eval("[" + raw.pop()[1:-1] + "]")

        buttons_raw = [ast.literal_eval("[" + b[1:-1] + "]") for b in raw]
        buttons = np.zeros((len(buttons_raw), len(lights)), int)
        for i, bw in enumerate(buttons_raw):
            buttons[i, bw] += 1
        manual.append((lights, buttons, joltage))
    return manual


def find_presses(info):
    lights, buttons, _ = info
    choices = list(range(len(buttons)))

    i = 1
    while i < len(buttons):
        presses = itertools.combinations(choices, i)
        for press in presses:
            result = [reduce(operator.xor, b) for b in zip(*buttons[press, :].tolist())]
            if result == lights:
                return len(press)
        i += 1
    return


def first_star(data):
    manual = parse(data)
    n_presses = 0
    for info in manual:
        n_presses += find_presses(info)
    return n_presses


def second_star(data):
    manual = parse(data)
    n_presses = 0
    for info in manual:
        _, buttons, joltage = info

        n_equations = len(buttons)
        objective = np.ones(n_equations)

        constraints = LinearConstraint(buttons.T, lb=joltage, ub=joltage)
        integrality = np.ones(n_equations)
        bounds = Bounds(lb=0, ub=np.inf)

        result = milp(c=objective, constraints=constraints, integrality=integrality, bounds=bounds)

        n_presses += int(sum(result.x))
    return n_presses


if __name__ == "__main__":
    with open(f"data/2025/10.txt", "r") as f:
        data = f.read()
        #         data = """

        # """

    print(first_star(data))
    print(second_star(data))
