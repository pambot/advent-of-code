import re
import copy
from functools import reduce


def parse_input(data):
    workflows_raw, ratings_raw = data.strip().split("\n\n")
    workflows = {}
    for raw in workflows_raw.split("\n"):
        name, raw_instr = raw[:-1].split("{")
        steps = []
        for s in raw_instr.split(","):
            xmas = re.search(r"^[xmas]", s)
            res = re.search(r":(.*)", s)
            num = re.search(r"[0-9]+", s)
            if xmas and res:
                steps.append(
                    (xmas.group(0), num.group(0), s,
                    eval(f"lambda {xmas.group(0)}: '{res.group(1)}' if {s.split(':')[0]} else None"))
                )
            else:
                steps.append(s)
        workflows[name] = steps

    ratings = []
    for r in ratings_raw.split("\n"):
        r = r.replace("=", ":")
        r = r.replace("x", "'x'").replace("m", "'m'").replace("a", "'a'").replace("s", "'s'")
        ratings.append(eval(r))
    return workflows, ratings


def first_star(data):
    workflows, ratings = parse_input(data)

    start = "in"
    current = start
    status = {k: None for k in [r for r, _ in enumerate(ratings)]}

    for r, rating in enumerate(ratings):
        while not status[r]:
            workflow = workflows[current]
            for curr_step in workflow:
                if isinstance(curr_step, tuple):
                    variable, _, _, function = curr_step
                    compare = rating[variable]
                    next_step = function(int(compare))
                    if not next_step:
                        continue
                    elif next_step in ("R", "A"):
                        status[r] = next_step
                        current = start
                        break
                    else:
                        current = next_step
                        break
                elif isinstance(curr_step, str):
                    if curr_step in ("R", "A"):
                        status[r] = curr_step
                        current = start
                        break
                    else:
                        current = curr_step
                        break
    return sum([sum(ratings[k].values()) for k, v in status.items() if v == "A"])


def split_interval(xmas, workflows, name, s):
    result = []
    curr_step = workflows[name][s]
    xmaso = copy.deepcopy(xmas)

    if isinstance(curr_step, tuple):
        var, thresh, rep, func = curr_step
        thresh = int(thresh)
        new_intv = []
        new_dest = []
        while xmas[var]:
            min_v, max_v = xmas[var].pop()
            if min_v < thresh < max_v:
                min_f, max_f = func(min_v), func(max_v)
                if "<" in rep:
                    new_intv += [(min_v, thresh - 1), (thresh, max_v)]
                elif ">" in rep:
                    new_intv += [(min_v, thresh), (thresh + 1, max_v)]
                new_dest += [min_f, max_f]
            else:
                new_intv += [(min_v, max_v)]
                new_dest += [(min_f, max_f)]

        for intv, dest in zip(new_intv, new_dest):
            xmasc = copy.deepcopy(xmaso)
            xmasc.update({var: [intv]})
            if dest in ("R", "A"):
                result += [(copy.deepcopy(xmasc), dest)]
            elif not dest:
                result += split_interval(copy.deepcopy(xmasc), workflows, name, s + 1)
            else:
                result += split_interval(copy.deepcopy(xmasc), workflows, dest, 0)

    elif isinstance(curr_step, str):
        if curr_step in ("R", "A"):
            result += [(copy.deepcopy(xmaso), curr_step)]
        elif not curr_step:
            result += split_interval(copy.deepcopy(xmaso), workflows, name, s + 1)
        else:
            result += split_interval(copy.deepcopy(xmaso), workflows, curr_step, 0)
    return result


def second_star(data):
    workflows, _ = parse_input(data)
    xmas = {"x": [(1, 4000)], "m": [(1, 4000)], "a": [(1, 4000)], "s": [(1, 4000)]}
    intervals = split_interval(xmas, workflows, "in", 0)
    accepted = [xmas for xmas, res in intervals if res == "A"]

    collect = []
    for xmas in accepted:
        scollect = []
        for vl in xmas.values():
            for v in vl:
                scollect.append(v[1] - v[0] + 1)
        collect.append(reduce(lambda x, y: x * y, scollect))
    return sum(collect)


if __name__ == "__main__":
    with open(f"data/2023/19.txt", "r") as f:
        data = f.read()

    #     data = """px{a<2006:qkq,m>2090:A,rfg}
    # pv{a>1716:R,A}
    # lnx{m>1548:A,A}
    # rfg{s<537:gd,x>2440:R,A}
    # qs{s>3448:A,lnx}
    # qkq{x<1416:A,crn}
    # crn{x>2662:A,R}
    # in{s<1351:px,qqz}
    # qqz{s>2770:qs,m<1801:hdj,R}
    # gd{a>3333:R,R}
    # hdj{m>838:A,pv}

    # {x=787,m=2655,a=1222,s=2876}
    # {x=1679,m=44,a=2067,s=496}
    # {x=2036,m=264,a=79,s=2244}
    # {x=2461,m=1339,a=466,s=291}
    # {x=2127,m=1623,a=2188,s=1013}"""

    print(first_star(data))
    print(second_star(data))
