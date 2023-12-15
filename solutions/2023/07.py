from collections import Counter
from functools import cmp_to_key


def parse_input(data):
    return [[l.split(" ")[0], int(l.split(" ")[1])] for l in data.split("\n") if l]


def rank_hand(h):
    if sorted(h.values()) == [5]:
        return 6 # five of a kind
    elif sorted(h.values()) == [1, 4]:
        return 5 # four of a kind
    elif sorted(h.values()) == [2, 3]:
        return 4 # full house
    elif sorted(h.values()) == [1, 1, 3]:
        return 3 # three pair
    elif sorted(h.values()) == [1, 2, 2]:
        return 2 # two pair
    elif sorted(h.values()) == [1, 1, 1, 2]:
        return 1 # one pair
    elif list(h.values()) == [1, 1, 1, 1, 1]:
        return 0 # high card
    else:
        raise Exception(h)


def hand_type(hand):
    h = Counter(hand)
    return rank_hand(h)


def hand_type_joker(hand):
    h = Counter(hand)
    if "J" not in h or hand == "JJJJJ":
        return rank_hand(h)
    else:
        j = h.pop("J")
        max_k = max(h, key=h.get)
        h[max_k] += j
        return rank_hand(h)


def set_card_rank(hand_func, card_rank):
    def compare_hands(hand1, hand2, hand_func=hand_func, card_rank=card_rank):
        v1 = hand_func(hand1[0])
        v2 = hand_func(hand2[0])
        if v1 != v2:
            return v1 - v2
        else:
            for h1, h2 in zip(hand1[0], hand2[0]):
                if h1 != h2:
                    i1 = card_rank.index(h1)
                    i2 = card_rank.index(h2)
                    return i2 - i1
    return compare_hands



def first_star(data):
    hand_bids = parse_input(data)
    compare_hands = set_card_rank(hand_type, "AKQJT98765432")
    results = sorted(hand_bids, key=cmp_to_key(compare_hands))
    w = 0
    for i, r in enumerate(results):
        w += (i + 1) * r[1]
    return w


def second_star(data):
    hand_bids = parse_input(data)
    compare_hands = set_card_rank(hand_type_joker, "AKQT98765432J")
    results = sorted(hand_bids, key=cmp_to_key(compare_hands))
    w = 0
    for i, r in enumerate(results):
        w += (i + 1) * r[1]
    return w

if __name__ == "__main__":
    with open(f"data/2023/07.txt", "r") as f:
        data = f.read()

    #     data = """32T3K 765
    # T55J5 684
    # KK677 28
    # KTJJT 220
    # QQQJA 483"""

    print(first_star(data))
    print(second_star(data))
