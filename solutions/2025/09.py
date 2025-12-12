
def parse(data):
    coords = [(int(d.split(",")[0]), int(d.split(",")[1])) for d in data.split()]
    return coords


def first_star(data):
    coords = parse(data)
    areas = []
    for c1x, c1y in coords:
        for c2x, c2y in coords:
            areas.append((abs(c2y - c1y) + 1) * (abs(c2x - c1x) + 1))

    return max(areas)


def get_rectangle_details(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    corners = [
        (min_x, min_y), (max_x, min_y),
        (max_x, max_y), (min_x, max_y)
    ]

    n = lambda a, b: (b > a) - (a > b)

    segments = []
    for i in range(4):
        (sp_x, sp_y), (ep_x, ep_y) = corners[i], corners[(i + 1) % 4]
        nx, ny = n(sp_x, ep_x), n(sp_y, ep_y)
        segments.append(((sp_x + nx, sp_y + ny), (ep_x - nx, ep_y - ny)))

    return corners, segments


def do_segments_intersect(seg1, seg2):
    p1, p2 = seg1
    p3, p4 = seg2
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = p3; x4, y4 = p4

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return False

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    return (ua > 0 and ua < 1) and (ub > 0 and ub < 1)



def is_on_segment(point, segment):
    p, a, b = point, segment[0], segment[1]

    is_collinear = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) == 0
    if not is_collinear:
        return False

    in_x_bounds = min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
    in_y_bounds = min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

    return in_x_bounds and in_y_bounds

def is_point_in_polygon(point, polygon_segments):
    px, py = point

    for segment in polygon_segments:
        if is_on_segment(point, segment):
            return True

    winding_number = 0

    def get_quadrant(v):
        dx, dy = v[0] - px, v[1] - py
        if dx > 0 and dy >= 0: return 0
        if dx <= 0 and dy > 0: return 1
        if dx < 0 and dy <= 0: return 2
        return 3

    for p1, p2 in polygon_segments:
        quad1 = get_quadrant(p1)
        quad2 = get_quadrant(p2)
        delta = quad2 - quad1

        if delta == 3:
            winding_number -= 1
        elif delta == -3:
            winding_number += 1
        elif abs(delta) == 2:
            cross_product = (p2[0] - p1[0]) * (py - p1[1]) - (p2[1] - p1[1]) * (px - p1[0])
            if cross_product > 0:
                winding_number += 2
            else:
                winding_number -= 2
        else:
            winding_number += delta
    return winding_number != 0


def second_star(data):
    coords = parse(data)
    o_segments = list(zip(coords, coords[1:] + [coords[0]]))

    areas = []

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            c1, c2 = coords[i], coords[j]
            r_corners, r_segments = get_rectangle_details(c1, c2)
            is_invalid = False

            for r_seg in r_segments:
                for o_seg in o_segments:
                    if do_segments_intersect(r_seg, o_seg):
                        is_invalid = True
                        break
                if is_invalid:
                    break
            if is_invalid:
                continue

            (min_x, min_y), (max_x, max_y) = r_corners[0], r_corners[2]
            sample_points = [
                (min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y),
                ((min_x + max_x) / 2, min_y), ((min_x + max_x) / 2, max_y),
                (min_x, (min_y + max_y) / 2), (max_x, (min_y + max_y) / 2)
            ]

            for point in sample_points:
                if not is_point_in_polygon(point, o_segments):
                    is_invalid = True
                    break

            if is_invalid:
                continue

            (c1x, c1y), (c2x, c2y) = c1, c2
            area = (abs(c2y - c1y) + 1) * (abs(c2x - c1x) + 1)
            areas.append(area)
    return max(areas)


if __name__ == "__main__":
    with open(f"data/2025/09.txt", "r") as f:
        data = f.read()
        #         data = """7,1
        # 11,1
        # 11,7
        # 9,7
        # 9,5
        # 2,5
        # 2,3
        # 7,3"""

    print(first_star(data))
    print(second_star(data))
