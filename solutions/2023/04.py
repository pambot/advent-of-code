def parse_card(line):
    l1, l2 = line.split(": ")
    card_num = int(l1.split(" ")[-1])

    win_nums = [int(n) for n in l2.split(" | ")[0].split(" ") if n]
    your_nums = [int(n) for n in l2.split(" | ")[1].split(" ") if n]
    return card_num, win_nums, your_nums

def first_star(data):
    score = 0
    for line in data.splitlines():
        _, win_nums, your_nums = parse_card(line)
        wins = set(win_nums) & set(your_nums)
        if len(wins) >= 1:
            score += 2**(len(wins) - 1)
    return score


def second_star(data):
    card_wins = {}
    for line in data.splitlines():
        card_num, win_nums, your_nums = parse_card(line)
        card_wins[card_num] = len(set(win_nums) & set(your_nums))

    card_seen = dict(zip(card_wins.keys(), [1] * len(card_wins)))
    for card in card_seen.keys():
        wins = card_wins[card]
        more_cards = [card + i for i in range(1, wins + 1)]
        for mcard in more_cards:
            card_seen[mcard] += card_seen[card]

    return sum(card_seen.values())


if __name__ == "__main__":
    with open(f"data/2023/04.txt", "r") as f:
        data = f.read()

    #     data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    # Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    # Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    # Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    # Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    # Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    print(first_star(data))
    print(second_star(data))
