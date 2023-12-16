from itertools import chain, zip_longest
from functools import lru_cache


def parse_input(data, part=1):
    springs = [
        (d.split(" ")[0], tuple(map(int, d.split(" ")[1].split(","))))
          for d in data.splitlines()
    ]
    if part == 2:
        redo_springs = []
        for spring in springs:
            blueprint, lengths = spring
            redo_springs.append(("?".join([blueprint] * 5), lengths * 5))
        springs = redo_springs
    return springs


@lru_cache
def space_combos(length, total_sum):
    if length == 1:
        return [(total_sum,)]
    else:
        collect = []
        for value in range(total_sum + 1):
            perms = space_combos(length - 1, total_sum - value)
            for perm in perms:
                collect.append((value,) + perm)
        return collect


def first_star(data):
    springs = parse_input(data, part=1)
    result = []
    for blueprint, broken in springs:
        spaces = [spaces for spaces in space_combos(
            len(broken) + 1, len(blueprint) - sum(broken)
        ) if 0 not in spaces[1:-1]]
        guesses = []
        hashes = ["#" * h for h in broken]
        for s in spaces:
            dots = ["." * d for d in s]
            g = [x for x in chain(*zip_longest(dots, hashes)) if x is not None]
            guesses.append("".join(g))

        matches = []
        for guess in set(guesses):
            if all([b == g for b, g in zip(blueprint, guess) if b == "#" or b == "."]):
                matches.append(guess)
        result.append(len(matches))
    return sum(result)


@lru_cache(maxsize=1000)
def check_blueprint(blueprint, broken):
    result = 0

    if not blueprint and len(broken) > 0:
        return 0
    elif not blueprint and len(broken) == 0:
        return 1
    elif blueprint and len(broken) == 0:
        return 1 if "#" not in blueprint else 0

    b, lueprint = blueprint[0], blueprint[1:]
    if b == ".":
        result += check_blueprint(lueprint, broken)
    elif b == "?":
        result += check_blueprint("." + lueprint, broken)
        result += check_blueprint("#" + lueprint, broken)
    elif b == "#":
        group = broken[0]
        if len(broken) > 1:
            if (len(blueprint) >= group + 1
                and all(x in ("#", "?") for x in blueprint[:group])
                and blueprint[group] != "#"
            ):
                result += check_blueprint(blueprint[group + 1:], broken[1:])
            else:
                return 0
        else:
            if (len(blueprint) >= group
                and all(x in ("#", "?") for x in blueprint[:group])
            ):
                result += check_blueprint(blueprint[group:], broken[1:])
    return result


def second_star(data):
    springs = parse_input(data, part=2)
    result = 0
    for blueprint, broken in springs:
        result += check_blueprint(blueprint, broken)
    return result



if __name__ == "__main__":
    with open(f"data/2023/12.txt", "r") as f:
        data = f.read()

    #     data = """???.### 1,1,3
    # .??..??...?##. 1,1,3
    # ?#?#?#?#?#?#?#? 1,3,1,6
    # ????.#...#... 4,1,1
    # ????.######..#####. 1,6,5
    # ?###???????? 3,2,1"""

    print(first_star(data))
    print(second_star(data))
