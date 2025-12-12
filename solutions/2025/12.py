
def parse(data):
    lines = [d for d in data.strip().split("\n\n")]
    shapes = [l[3:].split("\n") for l in lines[:6]]
    shape_counts = ["".join(s).count("#") for s in shapes]
    box_raw = [b.split(":") for b in lines[6:][0].split("\n")]
    box_dims = [list(map(int, b[0].split("x"))) for b in box_raw]
    box_fill = [list(map(int, b[1].strip().split(" "))) for b in box_raw]

    return shape_counts, box_dims, box_fill


def first_star(data):
    shape_counts, box_dims, box_fill = parse(data)
    c = 0
    for bd, bfill in zip(box_dims, box_fill):
        area = bd[0] * bd[1]
        if area >= sum([sc * bf for sc, bf in zip(shape_counts, bfill)]):
            c += 1

    return c


def second_star(data):
    parse(data)
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/2025/12.txt", "r") as f:
        data = f.read()
        #         data = """

        # """

    print(first_star(data))
    print(second_star(data))
