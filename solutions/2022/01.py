
def first_star(data):
    str_bags = [d.split("\n") for d in data.split("\n\n")]
    elf_bags = [[int(n) for n in sb if n] for sb in str_bags]
    elf_sums = [sum(cb) for cb in elf_bags]
    return max(elf_sums)


def second_star(data):
    str_bags = [d.split("\n") for d in data.split("\n\n")]
    elf_bags = [[int(n) for n in sb if n] for sb in str_bags]
    elf_sums = [sum(cb) for cb in elf_bags]

    elf_maxes = []
    for n in range(3):
        max_ind = elf_sums.index(max(elf_sums))
        elf_maxes.append(elf_sums.pop(max_ind))

    return sum(elf_maxes)


if __name__ == "__main__":
    with open(f"data/2022/01.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
