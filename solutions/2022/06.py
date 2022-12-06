
def find_marker(data, l):
    n = 0
    while not len(set(data[n:n + l])) == l and n < len(data) - l:
        n += 1
    return n + l


def first_star(data):
    return find_marker(data, 4)


def second_star(data):
    return find_marker(data, 14)


if __name__ == "__main__":
    with open(f"data/2022/06.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
