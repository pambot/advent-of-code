
def next_tail_move(h_coords, t_coords):
    hm, hn = h_coords
    tm, tn = t_coords
    v_space = hm - tm
    h_space = hn - tn
    if not (abs(v_space) + abs(h_space) <= 4):
        raise Exception("Head and tails out of bounds")
    if abs(v_space) <= 1 and abs(h_space) <= 1:
        return tm, tn
    elif (
        (abs(v_space) == 2 and h_space == 0) or
        (v_space == 0 and abs(h_space) == 2) or
        (abs(v_space) == 2 and abs(h_space) == 2)
    ):
        return tm + int(v_space/2), tn + int(h_space/2)
    elif abs(v_space) == 2 and abs(h_space) == 1:
        return tm + int(v_space/2), tn + h_space
    elif abs(v_space) == 1 and abs(h_space) == 2:
        return tm + v_space, tn + int(h_space/2)


DIRECTIONS = {
    "U": (1, 0), "D": (-1, 0), "L": (0, -1), "R": (0, 1)
}


def first_star(data):
    h_coords = 0, 0
    t_coords = 0, 0
    tails_seen = []
    for l in data.splitlines():
        ins = l.split(" ")
        d, step = ins[0], int(ins[1])
        dm, dn = DIRECTIONS[d]
        for _ in range(step):
            h_coords = h_coords[0] + dm, h_coords[1] + dn
            t_coords = next_tail_move(h_coords, t_coords)
            tails_seen.append(t_coords)
    return len(set(tails_seen))


def second_star(data):
    rope = [(0, 0)] * 10
    tails_seen = []
    for l in data.splitlines():
        ins = l.split(" ")
        d, step = ins[0], int(ins[1])
        dm, dn = DIRECTIONS[d]
        for _ in range(step):
            rope[0] = rope[0][0] + dm, rope[0][1] + dn
            for i in range(1, len(rope)):
                rope[i] = next_tail_move(rope[i - 1], rope[i])
            tails_seen.append(rope[-1])
    return len(set(tails_seen))


if __name__ == "__main__":
    with open(f"data/2022/09.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
