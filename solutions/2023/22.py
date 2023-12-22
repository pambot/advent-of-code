
def first_star(data):
    return "first answer goes here"


def second_star(data):
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/2023/22.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))