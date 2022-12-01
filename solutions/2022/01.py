
def solution_the_first(data):
    food = data.splitlines()
    elf_bags = list()
    bag = list()
    for f in food:
        if f:
            bag.append(int(f))
        else:
            elf_bags.append(bag)
            bag = list()

    elf_sums = [sum(e) for e in elf_bags]
    return max(elf_sums)


def solution_the_second(data):
    food = data.splitlines()
    elf_bags = list()
    bag = list()
    for f in food:
        if f:
            bag.append(int(f))
        else:
            elf_bags.append(bag)
            bag = list()

    elf_sums = [sum(e) for e in elf_bags]

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
