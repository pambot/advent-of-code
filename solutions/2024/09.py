def make_disk(data):
    disk_map = list(map(int, list(data.strip())))
    length = disk_map[::2]
    free = disk_map[1::2]
    if len(length) == len(free) + 1:
        free = free + [0]
    elif len(free) == len(length) + 1:
        length = length + [0]
    ids = list(range(len(length)))
    disk = []
    for l, f, i in zip(length, free, ids):
        disk.extend([i] * l)
        disk.extend(['.'] * f)
    return disk, length, free


def first_star(data):
    disk, _, free = make_disk(data)
    keep_disk = disk[:-sum(free)]
    move_files = [d for d in disk[-sum(free):] if d != '.']
    for i, k in enumerate(keep_disk):
        if k == ".":
            m = move_files.pop()
            keep_disk[i] = m
    checksum = 0
    for i, k in enumerate(keep_disk):
        checksum += i * k
    return checksum


def second_star(data):
    disk, _, _ = make_disk(data)
    idx = max([d for d in disk if isinstance(d, int)])
    while idx > 0:
        idx_i = [i for i, d in enumerate(disk) if d == idx]
        for j in range(min(idx_i)):
            if all(d == "." for d in disk[j:j + len(idx_i)]):
                disk[j:j + len(idx_i)] = [idx] * len(idx_i)
                for i in idx_i:
                    disk[i] =  "."
                break
        idx -= 1

    checksum = 0
    for i, k in enumerate(disk):
        if k != ".":
            checksum += i * k
    return checksum


if __name__ == "__main__":
    with open(f"data/2024/09.txt", "r") as f:
        data = f.read()
        # data = "2333133121414131402"

    print(first_star(data))
    print(second_star(data))
