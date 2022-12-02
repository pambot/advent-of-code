
def solution_the_first(data):
    str_bags = [d.split("\n") for d in data.split("\n\n")]
    elf_bags = [[int(n) for n in sb if n] for sb in str_bags]
    elf_sums = [sum(cb) for cb in elf_bags]
    return max(elf_sums)


def solution_the_second(data):
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

    print(solution_the_first(data))
    print(solution_the_second(data))
