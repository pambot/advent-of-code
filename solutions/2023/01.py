import re


def first_star(data):
    calibration = 0
    for line in data.splitlines():
        nums = []
        for v in line:
            try:
                nums.append(int(v))
            except ValueError:
                pass
        calibration += int(f"{nums[0]}{nums[-1]}")
    return calibration


def second_star(data):
    for s in (
        "ten", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety",
        "hundred", "thousand"
    ):
        assert s not in data

    digits = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6",
        "seven": "7", "eight": "8", "nine": "9"
    }

    calibration = 0
    for line in data.splitlines():

        min_ind = 2**31
        max_ind = -1

        for d in list(digits.keys()) + list(digits.values()):
            inds = [x.start() for x in re.finditer(d, line)]
            if inds and min(inds) < min_ind:
                min_ind = min(inds)
                first_num = digits.get(d, d)
            if inds and max(inds) > max_ind:
                max_ind = max(inds)
                last_num = digits.get(d, d)

        calibration += int(f"{first_num}{last_num}")
    return calibration


if __name__ == "__main__":
    with open(f"data/2023/01.txt", "r") as f:
        data = f.read()

    #     data = """1abc2
    # pqr3stu8vwx
    # a1b2c3d4e5f
    # treb7uchet"""

    print(first_star(data))

    #     data = """two1nine
    # eightwothree
    # abcone2threexyz
    # xtwone3four
    # 4nineeightseven2
    # zoneight234
    # 7pqrstsixteen"""

    print(second_star(data))
