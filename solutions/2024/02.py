def parse(data):
    return [list(map(int, d.split())) for d in data.splitlines()]


def check_report(report):
    diffs = [j - k for j, k in zip(report[:-1], report[1:])]
    check = 1
    if not (
        all(abs(d) <= 3 for d in diffs)
        and (all(d > 0 for d in diffs) or all(d < 0 for d in diffs))
    ):
        check = 0
    return check


def first_star(data):
    reports = parse(data)
    passes = 0
    for report in reports:
        passes += check_report(report)
    return passes


def second_star(data):
    reports = parse(data)
    passes = 0
    for report in reports:
        check = check_report(report)
        if not check:
            for i in range(len(report)):
                if check_report(report[:i] + report[i + 1 :]):
                    check = 1
        passes += check
    return passes


if __name__ == "__main__":
    with open(f"data/2024/02.txt", "r") as f:
        data = f.read()
        #         data = """7 6 4 2 1
        # 1 2 7 8 9
        # 9 7 6 2 1
        # 1 3 2 4 5
        # 8 6 4 4 1
        # 1 3 6 7 9"""

    print(first_star(data))
    print(second_star(data))
