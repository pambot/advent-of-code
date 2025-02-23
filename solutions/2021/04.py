import numpy as np


def parse(data):
    raw = data.strip().split("\n\n")
    nums = raw.pop(0).split(",")
    boards = [[[n for n in v.split(" ") if n] for v in r.split("\n")] for r in raw]
    boards = [np.array(b) for b in boards]
    return nums, boards


def first_star(data):
    nums, boards = parse(data)
    br, bc = boards[0].shape
    bingo = False
    for n in nums:
        for board in boards:
            board[board == n] = "X"

            for r in range(br):
                if (board[r, :] == "X").all():
                    bingo = True
                    win = board

            for c in range(bc):
                if (board[:, c] == "X").all():
                    bingo = True
                    win = board

        if bingo:
            break

    uncalled = win[win != "X"].flatten().astype(int)
    return int(n) * uncalled.sum()


def second_star(data):
    nums, boards = parse(data)
    br, bc = boards[0].shape
    wins = list()
    for n in nums:
        for b, board in enumerate(boards):
            board[board == n] = "X"

            for r in range(br):
                if (board[r, :] == "X").all():
                    if b not in wins:
                        wins.append(b)

            for c in range(bc):
                if (board[:, c] == "X").all():
                    if b not in wins:
                        wins.append(b)

        if len(wins) == len(boards):
            win = boards[wins[-1]]
            break

    uncalled = win[win != "X"].flatten().astype(int)
    return int(n) * uncalled.sum()


if __name__ == "__main__":
    with open(f"data/2021/04.txt", "r") as f:
        data = f.read()
        #         data = """
        # 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        # 22 13 17 11  0
        #     8  2 23  4 24
        # 21  9 14 16  7
        #     6 10  3 18  5
        #     1 12 20 15 19

        #     3 15  0  2 22
        #     9 18 13 17  5
        # 19  8  7 25 23
        # 20 11 10 24  4
        # 14 21 16 12  6

        # 14 21 17 24  4
        # 10 16 15  9 19
        # 18  8 23 26 20
        # 22 11 13  6  5
        #     2  0 12  3  7
        # """

    print(first_star(data))
    print(second_star(data))
