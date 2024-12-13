from collections import defaultdict
import numpy as np


AROUND = ((-1, 0), (0, -1), (1, 0), (0, 1))


def parse(data):
    garden = np.array([list(d) for d in data.strip().split()])
    plants = np.unique(garden)
    return garden, plants


def get_plot_coords(garden, loc, plant):
    stack = [loc]
    seen = set()

    nrows, ncols = garden.shape

    while stack:
        vr, vc = stack.pop()
        seen.add((vr, vc))

        next_plants = [
            (vr + ar, vc + ac) for ar, ac in AROUND
            if 0 <= vr + ar < nrows and 0 <= vc + ac < ncols
            and garden[vr + ar, vc + ac] == plant
        ]
        for nr, nc in next_plants:
            if (nr, nc) not in seen:
                stack.append((nr, nc))
    return seen


def get_areas_perimeters(garden, plots):
    areas = defaultdict(int)
    perimeters = defaultdict(int)

    nrows, ncols = garden.shape

    for plant, regions in plots.items():
        for i, r in enumerate(regions):
            areas[f"{plant}_{i}"] += len(r)
            for vr, vc in r:
                look = [
                    (vr + ar, vc + ac) for ar, ac in AROUND
                    if (0 <= vr + ar < nrows and 0 <= vc + ac < ncols and garden[vr + ar, vc + ac] != plant)
                    or ((vr + ar in (-1, nrows)) or (vc + ac in (-1, ncols)))
                ]
                perimeters[f"{plant}_{i}"] += len(look)
    return areas, perimeters


def get_plots(garden, plants):
    plots = defaultdict(list)
    for plant in plants:
        locs = list(zip(*np.where(garden == plant)))

        while locs:
            loc = locs.pop()
            seen = get_plot_coords(garden, loc, plant)
            plots[plant].append(list(seen))
            locs = list(set(locs) - seen)
    return plots


# if both coords are not on grid or different plant
OUTER_CORNERS = [
    ((-1, 0), (0, 1)),
    ((-1, 0), (0, -1)),
    ((1, 0), (0, 1)),
    ((1, 0), (0, -1)),
]

# if first two are same plant but third is different, cannot be off grid
INNER_CORNERS = [
    ((-1, 0), (0, 1), (-1, 1)),
    ((-1, 0), (0, -1), (-1, -1)),
    ((1, 0), (0, 1), (1, 1)),
    ((1, 0), (0, -1), (1, -1)),
]


def get_areas_sides(garden, plots):
    areas = defaultdict(int)
    sides = defaultdict(int)

    nrows, ncols = garden.shape

    for plant, regions in plots.items():
        for i, r in enumerate(regions):
            areas[f"{plant}_{i}"] += len(r)
            corners = 0
            for cr, cc in r:
                for (ar0, ac0), (ar1, ac1) in OUTER_CORNERS:
                    or0, oc0 = cr + ar0, cc + ac0
                    or1, oc1 = cr + ar1, cc + ac1
                    if (
                        ((not 0 <= or0 < nrows or not 0 <= oc0 < ncols) or garden[or0, oc0] != plant) and
                        ((not 0 <= or1 < nrows or not 0 <= oc1 < ncols) or garden[or1, oc1] != plant)
                    ):
                        corners += 1

                for (ar0, ac0), (ar1, ac1), (ar2, ac2) in INNER_CORNERS:
                    ir0, ic0 = cr + ar0, cc + ac0
                    ir1, ic1 = cr + ar1, cc + ac1
                    ir2, ic2 = cr + ar2, cc + ac2
                    if (
                        any(not 0 <= xr < nrows for xr in (ir0, ir1, ir2)) or
                        any(not 0 <= xc < ncols for xc in (ic0, ic1, ic2))
                    ):
                        continue
                    else:
                        if (
                            garden[ir0, ic0] == plant and
                            garden[ir1, ic1] == plant and
                            garden[ir2, ic2] != plant
                        ):
                            corners += 1
            sides[f"{plant}_{i}"] = corners
    return areas, sides


def first_star(data):
    garden, plants = parse(data)
    plots = get_plots(garden, plants)
    areas, perimeters = get_areas_perimeters(garden, plots)
    price = 0
    for p in areas.keys():
        price += areas[p] * perimeters[p]

    return price


def second_star(data):
    garden, plants = parse(data)
    plots = get_plots(garden, plants)
    areas, sides = get_areas_sides(garden, plots)
    price = 0
    for p in areas.keys():
        price += areas[p] * sides[p]

    return price


if __name__ == "__main__":
    with open(f"data/2024/12.txt", "r") as f:
        data = f.read()
        #         data = """
        # RRRRIICCFF
        # RRRRIICCCF
        # VVRRRCCFFF
        # VVRCCCJFFF
        # VVVVCJJCFE
        # VVIVCCJJEE
        # VVIIICJJEE
        # MIIIIIJJEE
        # MIIISIJEEE
        # MMMISSJEEE"""

    print(first_star(data))
    print(second_star(data))
