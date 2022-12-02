H_SCORE = {"rock": 1, "paper": 2, "scissors": 3}
R_SCORE = {"win": 6, "draw": 3, "loss": 0}
O_MAP = {"A": "rock", "B": "paper", "C": "scissors"}


def first_star(data):
    r_map = {
        "rock": {"paper": "win", "scissors": "loss", "rock": "draw"},
        "paper": {"paper": "draw", "scissors": "win", "rock": "loss"},
        "scissors": {"paper": "loss", "scissors": "draw", "rock": "win"}
    }
    s_map = {"X": "rock", "Y": "paper", "Z": "scissors"}

    hands = data.splitlines()
    score = 0
    for h in hands:
        o, s = O_MAP[h[0]], s_map[h[2]]
        r = r_map[o][s]
        score += (H_SCORE[s] + R_SCORE[r])
    return score


def second_star(data):
    s_map = {
        "loss": {"paper": "rock", "scissors": "paper", "rock": "scissors"},
        "draw": {"paper": "paper", "scissors": "scissors", "rock": "rock"},
        "win": {"paper": "scissors", "scissors": "rock", "rock": "paper"}
    }
    r_map = {"X": "loss", "Y": "draw", "Z": "win"}

    hands = data.splitlines()
    score = 0
    for h in hands:
        o, r = O_MAP[h[0]], r_map[h[2]]
        s = s_map[r][o]
        score += (H_SCORE[s] + R_SCORE[r])
    return score


if __name__ == "__main__":
    with open(f"data/2022/02.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
