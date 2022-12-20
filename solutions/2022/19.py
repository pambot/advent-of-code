import math


class BluePrint():
  def __init__(self, blueprint):
    id, robots = blueprint[10:-1].split(": ")
    self.id = int(id)
    self.robots = dict()
    for _, robot in enumerate(reversed(robots.split(". "))):
      typ, costs = robot[5:].split(" robot costs ")
      self.robots[typ] = {resource: int(cnt) for cnt, resource in (cost.split(" ") for cost in costs.split(" and "))}
    self.maxes = {t: max(res.get(t, 0) for res in self.robots.values()) for t in self.robots.keys()}

  def geodes(self, minutes):
    resources = {t: 0 for t in self.robots}
    robots = {t: int(t == "ore") for t in self.robots}

    q = []
    q.append((minutes, resources, robots, None))
    max_geodes = 0
    while len(q):
      time, resources, robots, last = q.pop()
      if time == 0:
        max_geodes = max(max_geodes, resources["geode"])
        continue
      if max_geodes - resources["geode"] >= (time * (2 * robots["geode"] + time - 1)) // 2:
        continue
      time -= 1
      wait = False
      for typ, res in self.robots.items():
        if typ != "geode" and robots[typ] * time + resources[typ] > self.maxes[typ] * time:
          continue
        if (last is None or last == typ) and all(v <= resources[t] - robots[t] for t, v in res.items()):
          continue
        if any(resources[t] < v for t, v in res.items()):
          wait = wait or all(robots[t] > 0 for t in res.keys())
          continue

        next_resources = {t: v + robots[t] - res.get(t, 0) for t, v in resources.items()}
        next_robots = {t: v + int(t == typ) for t, v in robots.items()}
        q.append((time, next_resources, next_robots, typ))
      if wait:
        next_resources = {t: v + robots[t] for t, v in resources.items()}
        q.append((time, next_resources, robots, None))
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
