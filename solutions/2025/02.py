
def parse(data):
    return [list(map(int, d.split("-"))) for d in data.strip().split(",")]


def first_star(data):
    id_ranges = parse(data)
    invalids = 0
    for left, right in id_ranges:
        curr = left
        seen = set()
        while curr <= right:
            s_curr = str(curr)
            max_i = len(s_curr) // 2 if len(s_curr) % 2 == 0 else len(s_curr) // 2 + 1
            pref = s_curr[:max_i]
            check = int(pref + pref)
            if check not in seen and left <= check <= right:
                invalids += check
                seen.add(check)
            curr += 1
    return invalids


def second_star(data):
    id_ranges = parse(data)
    invalids = 0
    for left, right in id_ranges:
        curr = left
        seen = set()
        while curr <= right:
            s_curr = str(curr)
            max_i = len(s_curr) // 2
            for i in range(1, max_i + 1):
                pref = s_curr[:i]
                if len(s_curr) % i == 0:
                    check = pref * (len(s_curr) // i)
                    if check not in seen and check == s_curr:
                        invalids += int(check)
                        seen.add(check)
            curr += 1
    return invalids


if __name__ == "__main__":
    with open(f"data/2025/02.txt", "r") as f:
        data = f.read()
        #         data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
        # 1698522-1698528,446443-446449,38593856-38593862,565653-565659,
        # 824824821-824824827,2121212118-2121212124"""

    print(first_star(data))
    print(second_star(data))
