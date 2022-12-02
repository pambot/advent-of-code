import sys
import os
import requests


def fetch_input_data(year, day):
    with open("SESSION", "r") as f:
        session = f.read().strip()
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        headers={"User-Agent": "github.com/pambot/advent-of-code"},
        cookies={"session": session}
    )
    filename = f"data/{year}/{day:02d}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(response.content)
    return


def make_solution_file(year, day):
    solution_template = f"""
def first_star(data):
    return "first answer goes here"


def second_star(data):
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/{year}/{day:02d}.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))"""

    filename = f"solutions/{year}/{day:02d}.py"
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(solution_template)
    return


if __name__ == "__main__":
    year, day = map(int, sys.argv[1:3])
    fetch_input_data(year, day)
    make_solution_file(year, day)
