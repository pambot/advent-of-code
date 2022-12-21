
def swap_numbers(numbers, number, curr_index):
    next_index = (curr_index + number) % (len(numbers) - 1)
    curr_number = numbers.pop(curr_index)
    numbers = numbers[:next_index] + [curr_number] + numbers[next_index:]
    return numbers


def grove_coords(numbers):
    zero_index = [
        c for c, (n, i) in enumerate(numbers) if n == 0
    ][0]
    coords = []
    for number in (1000, 2000, 3000):
        coord_index = (zero_index + number) % len(numbers)
        coord_number, _ = numbers[coord_index]
        coords.append(coord_number)
    return sum(coords)


def first_star(data):
    numbers = [(int(d), i) for i, d in enumerate(data.splitlines())]
    for r in range(len(numbers)):
        curr_index, (number, _) = [
            (c, (n, i)) for c, (n, i) in enumerate(numbers) if i == r
        ][0]
        if number > 0:
            numbers = swap_numbers(numbers, number, curr_index)
        else:
            numbers.reverse()
            numbers = swap_numbers(
                numbers, -number, len(numbers) - 1 - curr_index
            )
            numbers.reverse()
    return grove_coords(numbers)


def second_star(data):
    decryption_key = 811589153
    numbers = [
        (int(d) * decryption_key, i) for i, d in enumerate(data.splitlines())
    ]
    for _ in range(10):
        for r in range(len(numbers)):
            curr_index, (number, _) = [
                (c, (n, i)) for c, (n, i) in enumerate(numbers) if i == r
            ][0]
            if number > 0:
                numbers = swap_numbers(numbers, number, curr_index)
            else:
                numbers.reverse()
                numbers = swap_numbers(
                    numbers, -number, len(numbers) - 1 - curr_index
                )
                numbers.reverse()
    return grove_coords(numbers)


if __name__ == "__main__":
    with open(f"data/2022/20.txt", "r") as f:
        data = f.read()

    example = """
    1
    2
    -3
    3
    -2
    0
    4
    """.strip()

    print(first_star(data))
    print(second_star(data))
