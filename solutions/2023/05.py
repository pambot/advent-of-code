def parse_input(data):
    chunks = data.split("\n\n")

    raw_seeds = chunks.pop(0)
    seeds = [int(n) for n in raw_seeds.split(": ")[1].split(" ")]

    maps = {}
    for chunk in chunks:
        map_raw = chunk.split("\n")
        map_type = tuple(map_raw[0].split(" ")[0].split("-to-"))
        map_values = [list(map(int, m.split(" "))) for m in map_raw[1:] if m]
        map_values.sort(key=lambda x: x[1])

        store = {"source": list(), "target": list()}
        for target, source, length in map_values:
            store["source"].append((source, source + length - 1)) # inclusive
            store["target"].append((target, target + length - 1))

        maps[map_type] = store
    return seeds, maps


def traverse_maps(seed, maps, start_type="seed", end_type="location"):
    map_types = maps.keys()

    map_type = [m for m in map_types if m[0] == start_type][0]
    from_value = seed
    while True:
        _, to_type = map_type
        source_ranges, target_ranges = maps[map_type]["source"], maps[map_type]["target"]
        for s, t in zip(source_ranges, target_ranges):
            if s[0] <= from_value <= s[1]:
                to_value = t[0] + (from_value - s[0])
                break
        else:
            to_value = from_value

        if to_type == end_type:
            break
        else:
            map_type = [m for m in map_types if m[0] == to_type][0]
            from_value = to_value

    return to_value


def first_star(data):
    seeds, maps = parse_input(data)
    locations = []
    for seed in seeds:
        locations.append(traverse_maps(seed, maps))
    return min(locations)


def second_star(data):
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/2023/05.txt", "r") as f:
        data = f.read()

    #     data = """seeds: 79 14 55 13

    # seed-to-soil map:
    # 50 98 2
    # 52 50 48

    # soil-to-fertilizer map:
    # 0 15 37
    # 37 52 2
    # 39 0 15

    # fertilizer-to-water map:
    # 49 53 8
    # 0 11 42
    # 42 0 7
    # 57 7 4

    # water-to-light map:
    # 88 18 7
    # 18 25 70

    # light-to-temperature map:
    # 45 77 23
    # 81 45 19
    # 68 64 13

    # temperature-to-humidity map:
    # 0 69 1
    # 1 0 69

    # humidity-to-location map:
    # 60 56 37
    # 56 93 4"""

    print(first_star(data))
    print(second_star(data))
