from functools import cache


@cache
def match_design(design, towels):
    if all(not design.startswith(t) for t in towels):
        return False
    elif any(t == design for t in towels):
        return True
    else:
        return any(
            match_design(design[len(t):], towels)
            for t in towels if design.startswith(t)
        )


@cache
def count_design(design, towels):
    if design == "":
        return 1

    count = 0
    for t in towels:
        if design.startswith(t):
            count += count_design(design[len(t):], towels)

    return count


def first_star(data):
    towels = tuple(data.strip().split("\n\n")[0].split(", "))
    designs = tuple(data.strip().split("\n\n")[1].split("\n"))
    possible = 0
    for design in designs:
        if match_design(design, towels):
            possible += 1

    return possible


def second_star(data):
    towels = tuple(data.strip().split("\n\n")[0].split(", "))
    designs = tuple(data.strip().split("\n\n")[1].split("\n"))
    counts = 0
    for design in designs:
        counts += count_design(design, towels)

    return counts


if __name__ == "__main__":
    with open(f"data/2024/19.txt", "r") as f:
        data = f.read()
        #         data = """r, wr, b, g, bwu, rb, gb, br

        # brwrr
        # bggr
        # gbbr
        # rrbgbr
        # ubwu
        # bwurrg
        # brgr
        # bbrgwb
        # """

    print(first_star(data))
    print(second_star(data))
