import numpy as np


def scan_guard(m, x, g, r, c, seen, done):
    done = 0
    if g == '^':
        scan = m[:r, c].tolist() # get the path in front of guard
        try:
            o = scan[::-1].index("#") # check for first obstacle
            g = '>' # turn the guard 90 degrees
            m[r, c] = '.' # replace old guard position with blank
            m[r - o, c] = g # give new guard position the guard marker
            x[r - o:r + 1, c] = 'X' # fill in x matrix with X for path
            r = r - o # calculate next guard position
            c = c
            if (g, r, c) not in seen: # check if guard was there before at orientation
                seen.add((g, r, c)) # add to tracker
            else:
                done = 2 # mark as cycle
        except ValueError: # can't see obstacle
            m[r, c] = '.' # clear old guard position
            x[:r + 1, c] = 'X' # mark path off grid with X
            done = 1 # mark as overflow
    elif g == '>':
        scan = m[r, c:].tolist()
        try:
            o = scan.index("#")
            g = 'v'
            m[r, c] = '.'
            m[r, c + o - 1] = g
            x[r, c:c + o] = 'X'
            r = r
            c = c + o - 1
            if (g, r, c) not in seen:
                seen.add((g, r, c))
            else:
                done = 2
        except ValueError:
            m[r, c] = '.'
            x[r, c:] = 'X'
            done = 1
    elif g == 'v':
        scan = m[r + 1:, c].tolist()
        try:
            o = scan.index("#")
            g = '<'
            m[r, c] = '.'
            m[o + r, c] = g
            x[r:o + r + 1, c] = 'X'
            r = o + r
            c = c
            if (g, r, c) not in seen:
                seen.add((g, r, c))
            else:
                done = 2
        except ValueError:
            m[r, c] = '.'
            x[r:, c] = 'X'
            done = 1
    elif g == '<':
        scan = m[r, :c].tolist()
        try:
            o = scan[::-1].index("#")
            g = '^'
            m[r, c] = '.'
            m[r, c - o] = g
            x[r, c - o:c + 1] = 'X'
            r = r
            c = c - o
            if (g, r, c) not in seen:
                seen.add((g, r, c))
            else:
                done = 2
        except ValueError:
            m[r, c] = '.'
            x[r, :c + 1] = 'X'
            done = 1

    return m, x, g, r, c, seen, done


def get_origin(m):
    for r in range(len(m[0])):
        for c in range(len(m)):
            for g in ['v', '<', '^', '>']:
                if m[r][c] == g:
                    guard = (g, r, c)

    g, r, c = guard
    return g, r, c


def simulate_guard(m, g, r, c):
    x = np.copy(m)
    seen = set()
    done = 0
    while not done:
        m, x, g, r, c, seen, done = scan_guard(m, x, g, r, c, seen, done)
    return m, x, done


def first_star(data):
    m = [list(s) for s in data.strip().split()]
    m = np.array(m)
    g, r, c = get_origin(m)
    m, x, _ = simulate_guard(m, g, r, c)
    return np.count_nonzero(x == 'X')


def second_star(data):
    m = [list(s) for s in data.strip().split()]
    m = np.array(m)
    g, r, c = get_origin(m)

    _, x0, done = simulate_guard(m.copy(), g, r, c)

    cycles = 0
    xi = np.where(x0 == 'X') # only use path of guard
    xs = list(set(list(zip(*xi))) - set([(r, c)]))
    for xr, xc in xs:
        m1 = m.copy()
        m1[xr, xc] = '#'
        _, _, done = simulate_guard(m1, g, r, c)
        if done == 2:
            cycles += 1
    return cycles


if __name__ == "__main__":
    with open(f"data/2024/06.txt", "r") as f:
        data = f.read()
        #         data = """....#.....
        # .........#
        # ..........
        # ..#.......
        # .......#..
        # ..........
        # .#..^.....
        # ........#.
        # #.........
        # ......#..."""

    print(first_star(data))
    print(second_star(data))
