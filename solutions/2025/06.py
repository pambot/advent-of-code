
def first_parse(data):
    inputs = [d.split() for d in data.strip("\n").split("\n")]
    operators = inputs.pop()
    numbers = [list(map(int, l)) for l in zip(*inputs)]

    return numbers, operators


def second_parse(data):
    inputs = [d for d in data.strip("\n").split("\n")]
    operators = inputs.pop().split()
    number_strings = ["".join(l).strip() for l in zip(*inputs)]

    numbers = list()
    precursor = list()
    for n in number_strings:
        if n != "":
            precursor.append(int(n))
        else:
            numbers.append(precursor)
            precursor = list()
    else:
        numbers.append(precursor)

    return numbers, operators


def evaluate(numbers, operators):
    result = 0
    for nums, op in zip(numbers, operators):
        s = nums[0]
        for n in nums[1:]:
            if op == "*":
                s *= n
            elif op == "+":
                s += n
        result += s

    return result


def first_star(data):
    numbers, operators = first_parse(data)
    return evaluate(numbers, operators)


def second_star(data):
    numbers, operators = second_parse(data)
    return evaluate(numbers, operators)


if __name__ == "__main__":
    with open(f"data/2025/06.txt", "r") as f:
        data = f.read()
        #         data = """123 328  51 64
        # 45 64  387 23
        # 6 98  215 314
        # *   +   *   +
        # """

    print(first_star(data))
    print(second_star(data))
