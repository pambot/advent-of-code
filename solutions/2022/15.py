import re


def extract_coords(data):
    sensor_locs = []
    beacon_locs = []
    for d in data.splitlines():
        n = tuple(map(int, re.findall(r"(-?\d+)", d)))
        sensor_locs.append((n[1], n[0]))
        beacon_locs.append((n[3], n[2]))
    return sensor_locs, beacon_locs


def first_star(data):
    row = 2_000_000    # row = 10
    sensor_locs, beacon_locs = extract_coords(data)
    beacon_coverage = set([b for b in beacon_locs if b[0] == row])
    range_coverage = set([s for s in sensor_locs if s[0] == row])
    for sensor, beacon in zip(sensor_locs, beacon_locs):
        sy, sx = sensor
        by, bx = beacon
        radius = abs(bx - sx) + abs(by - sy)
        if sy - radius <= row <= sy + radius:
            y_diff = abs(row - sy)
            for x in range(sx - radius + y_diff, sx + radius - y_diff + 1):
                range_coverage.add((row, x))
    coverage = range_coverage - beacon_coverage
    return len(coverage)


def check_in_range(check_coord, sensor_coord, radius):
    cy, cx = check_coord
    sy, sx = sensor_coord
    if abs(cy - sy) + abs(cx - sx) <= radius:
        return True
    else:
        return False


def trace_range(sensor_coord, radius):
    sy, sx = sensor_coord
    radius += 1
    trace_coords = []
    for y in range(sy - radius, sy + radius + 1):
        y_diff = abs(y - sy)
        x_diff = radius - y_diff
        trace_coords.extend([(y, sx - x_diff), (y, sx + x_diff)])
    return trace_coords


def second_star(data):
    c_min, c_max = 0, 4_000_000    # c_min, c_max = 0, 20
    sensor_locs, beacon_locs = extract_coords(data)
    radii = [
        abs(bx - sx) + abs(by - sy)
        for (sy, sx), (by, bx) in zip(sensor_locs, beacon_locs)
    ]
    trace_coords = []
    for sensor_coord, radius in zip(sensor_locs, radii):
        raw_coords = trace_range(sensor_coord, radius)
        filtered_coords = [
            (y, x) for y, x in raw_coords
            if c_min < x < c_max and c_min < y < c_max
        ]
        trace_coords.extend(filtered_coords)
    trace_coords = list(set(trace_coords))
    for trace_coord in trace_coords:
        c = 0
        for sensor_coord, radius in zip(sensor_locs, radii):
            if check_in_range(trace_coord, sensor_coord, radius):
                c += 1
        if c == 0:
            break
    ty, tx = trace_coord
    return tx * 4_000_000 + ty


if __name__ == "__main__":
    with open(f"data/2022/15.txt", "r") as f:
        data = f.read()

    example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

    print(first_star(data))
    print(second_star(data))
