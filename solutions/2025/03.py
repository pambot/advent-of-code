
def parse(data):
    return data.strip().split("\n")


def first_star(data):
    batteries = parse(data)
    joltages = list()
    for bank in batteries:
        joltage = 0

        bank_part1 = bank[:-1]
        d = max(bank_part1)
        i1 = bank_part1.index(d)
        joltage += int(bank_part1[i1]) * 10

        bank_part2 = bank[i1 + 1:]
        d = max(bank_part2)
        i2 = bank_part2.index(d)
        joltage += int(bank_part2[i2])

        joltages.append(joltage)

    return sum(joltages)


def second_star(data):
    batteries = parse(data)
    joltages = list()
    for bank in batteries:
        joltage = 0
        l = 0
        r = 11
        bank_part = bank[l:-r]
        while r >= 0:
            d = max(bank_part)
            ld = bank_part.find(d)
            joltage += int(bank_part[ld]) * 10**r
            l += ld + 1
            r -= 1
            if r != 0:
                bank_part = bank[l:-r]
            else:
                bank_part = bank[l:]

        joltages.append(joltage)

    return sum(joltages)


if __name__ == "__main__":
    with open(f"data/2025/03.txt", "r") as f:
        data = f.read()
        #         data = """987654321111111
        # 811111111111119
        # 234234234234278
        # 818181911112111"""

    print(first_star(data))
    print(second_star(data))
