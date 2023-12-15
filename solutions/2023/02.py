from functools import reduce


def parse_game(line):
    l1, l2 = line.split(": ")
    game_num = int(l1.split(" ")[1])

    game_result = []
    for round in l2.split("; "):
        rgb = {r.split(" ")[1]: int(r.split(" ")[0]) for r in round.split(", ")}
        game_result.append(rgb)

    return game_num, game_result


def first_star(data):
    sum_games = 0
    for line in data.splitlines():
        game_num, game_result = parse_game(line)

        for gr in game_result:
            if gr.get("red", 0) > 12 or gr.get("green", 0) > 13 or gr.get("blue", 0) > 14:
                break
        else:
            sum_games += game_num
    return sum_games


def second_star(data):
    total_power = 0
    for line in data.splitlines():
        game_num, game_result = parse_game(line)

        game_mins = {"red": 0, "green": 0, "blue": 0}
        for gr in game_result:
            for c in game_mins:
                v = gr.get(c, 0)
                if v > game_mins[c]:
                    game_mins[c] = v

        power = reduce(lambda x, y: x*y, game_mins.values())
        total_power += power
    return total_power


if __name__ == "__main__":
    with open(f"data/2023/02.txt", "r") as f:
        data = f.read()

    #     data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    # Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    # Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    # Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    # Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    print(first_star(data))
    print(second_star(data))
