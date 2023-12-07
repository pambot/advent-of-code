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

        store = {"source": list(), "target": list(), "delta": list()}
        for target, source, length in map_values:
            store["source"].append((source, source + length - 1)) # inclusive
            store["target"].append((target, target + length - 1))
            store["delta"].append(target - source)

        maps[map_type] = store
    return seeds, maps


def seed_to_location(seed, maps, start_type="seed", end_type="location"):
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


def interval_overlap(source, rseed):
    """
        (s1, e1)
        (s2, e2)
    """
    s1, e1, = source
    s2, e2 = rseed
    if e2 < s1 or s2 > e1: # none
        return None
    elif s2 >= s1 and e2 <= e1: # full inner
        return [(s2, e2)]
    elif s2 >= s1 and s2 <= e1 and e2 > e1: # right
        return [(s2, e1), (e1 + 1, e2)]
    elif s2 < s1 and s1 <= e2 and e1 >= e2: # left
        return [(s2, s1 - 1), (s1, e2)]
    elif s2 < s1 and e2 > e1: # full outer
        return [(s2, s1 - 1), (s1, e1), (e1 + 1, e2)]
    else:
        raise Exception(source, rseed, "match problem")


def seed_ranges_to_location(rseeds, maps):
    stages = [("seed", "soil"), ("soil", "fertilizer"), ("fertilizer", "water"),
            ("water", "light"), ("light", "temperature"), ("temperature", "humidity"),
            ("humidity", "location")]

    while stages:
        stage = stages.pop(0)

        # check all intervals, split if necessary
        while True:
            new_sources = []
            for rseed in rseeds:
                for source in maps[stage]["source"]:
                    overlaps = interval_overlap(source, rseed)
                    if overlaps:
                        new_sources += overlaps
                if all(not interval_overlap(s, rseed) for s in maps[stage]["source"]):
                    new_sources.append(rseed)
            new_sources = list(set(new_sources))
            if len(new_sources) == len(rseeds):
                break
            else:
                rseeds = new_sources

        # split intervals should only match once now or not at all
        targets = []
        for ns in new_sources:
            for source, d in zip(maps[stage]["source"], maps[stage]["delta"]):
                overlaps = interval_overlap(source, ns)
                assert overlaps == None or len(overlaps) == 1
                if overlaps:
                    ov = overlaps[0]
                    targets.append((ov[0] + d, ov[1] + d))
            if all(not interval_overlap(s, ns) for s in maps[stage]["source"]):
                targets.append(ns)

        rseeds = targets

    return targets


def first_star(data):
    seeds, maps = parse_input(data)
    locations = []
    for seed in seeds:
        locations.append(seed_to_location(seed, maps))
    return min(locations)


def second_star(data):
    seeds, maps = parse_input(data)
    rseeds = [(s, s + l - 1) for s, l in zip(seeds[0::2], seeds[1::2])]
    location_ranges = seed_ranges_to_location(rseeds, maps)
    return sorted(location_ranges, key=lambda t: t[0])[0][0]


if __name__ == "__main__":
    with open(f"data/2023/05.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
