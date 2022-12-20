import math


class BluePrint:
    def __init__(self, blueprint):
        id, robots = blueprint[10:-1].split(": ")
        self.id = int(id)
        self.robots = dict()
        for _, robot in enumerate(reversed(robots.split(". "))):
            typ, costs = robot[5:].split(" robot costs ")
            self.robots[typ] = {
                resource: int(cnt)
                for cnt, resource in (cost.split(" ") for cost in costs.split(" and "))
            }
        self.maxes = {
            t: max(res.get(t, 0) for res in self.robots.values())
            for t in self.robots.keys()
        }

    def geodes(self, minutes):
        resources = {t: 0 for t in self.robots}
        robots = {t: int(t == "ore") for t in self.robots}

        queue = []
        queue.append((minutes, resources, robots, None))
        max_geodes = 0
        while len(queue):
            time, resources, robots, last = queue.pop()
            if time == 0:
                max_geodes = max(max_geodes, resources["geode"])
                continue
            if (
                max_geodes - resources["geode"]
                >= (time * (2 * robots["geode"] + time - 1)) // 2
            ):
                continue
            time -= 1
            wait = False
            for res_type, resources in self.robots.items():
                if (
                    res_type != "geode"
                    and robots[res_type] * time + resources[res_type] > self.maxes[res_type] * time
                ):
                    continue
                if (last is None or last == res_type) and all(
                    v <= resources[t] - robots[t] for t, v in resources.items()
                ):
                    continue
                if any(resources[t] < v for t, v in resources.items()):
                    wait = wait or all(robots[t] > 0 for t in resources.keys())
                    continue

                next_resources = {
                    t: v + robots[t] - resources.get(t, 0) for t, v in resources.items()
                }
                next_robots = {t: v + int(t == res_type) for t, v in robots.items()}
                queue.append((time, next_resources, next_robots, res_type))
            if wait:
                next_resources = {t: v + robots[t] for t, v in resources.items()}
                queue.append((time, next_resources, robots, None))
        return max_geodes


def first_star(data):
    blueprints = [BluePrint(line.rstrip()) for line in data.splitlines()]
    quality_level = sum(bp.id * bp.geodes(24) for bp in blueprints)
    return quality_level


def second_star(data):
    blueprints = [BluePrint(line.rstrip()) for line in data.splitlines()]
    geodes = [bp.geodes(32) for bp in blueprints[:3]]
    return math.prod(geodes)


if __name__ == "__main__":
    with open(f"data/2022/19.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
