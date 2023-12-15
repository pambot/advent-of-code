from collections import defaultdict


def hash_string(string):
    current_value = 0
    for s in string:
        current_value += ord(s)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def first_star(data):
    data = data.strip().split(",")
    save = 0
    for d in data:
        save += hash_string(d)
    return save


def second_star(data):
    data = data.strip().split(",")
    box_map = defaultdict(list)
    for d in data:
        if "=" in d:
            label, focal = d.split("=")
            box = hash_string(label)
            find_label = [b for b in box_map[box] if b[0] == label]
            if find_label:
                old = find_label[0]
                box_map[box] = [(label, focal) if b == old else b for b in box_map[box]]
            else:
                box_map[box] += [(label, focal)]
        elif "-" in d:
            label, _ = d.split("-")[0], None
            box = hash_string(label)
            box_map[box] = [b for b in box_map[box] if b[0] != label]

    focusing_power = 0
    for box in box_map:
        for i, (label, focal) in enumerate(box_map[box]):
            focusing_power += (box + 1) * (i + 1) * int(focal)

    return focusing_power


if __name__ == "__main__":
    with open(f"data/2023/15.txt", "r") as f:
        data = f.read()

    # data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

    print(first_star(data))
    print(second_star(data))
