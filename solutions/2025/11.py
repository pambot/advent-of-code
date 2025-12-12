from functools import cache


def parse(data):
    return {d[:3]: d[4:].split() for d in data.split("\n")}


def first_star(data):
    D = parse(data)

    @cache
    def count_paths(start, finish):
        if start == finish:
            return 1
        else:
            path_count = 0
            for node in D[start]:
                path_count += count_paths(node, finish)
        return path_count

    return count_paths("you", "out")


def second_star(data):
    D = parse(data)

    @cache
    def count_paths(start, finish):
        if start == finish:
            return 1
        elif start not in D:
            return 0
        else:
            path_count = 0
            for node in D[start]:
                path_count += count_paths(node, finish)
        return path_count

    svr2dac = count_paths("svr", "dac")
    dac2fft = count_paths("dac", "fft")
    fft2out = count_paths("fft", "out")

    svr2fft = count_paths("svr", "fft")
    fft2dac = count_paths("fft", "dac")
    dac2out = count_paths("dac", "out")

    return max((
        svr2dac * dac2fft * fft2out,
        svr2fft * fft2dac * dac2out
    ))


if __name__ == "__main__":
    with open(f"data/2025/11.txt", "r") as f:
        data = f.read()
        #         data = """svr: aaa bbb
        # aaa: fft
        # fft: ccc
        # bbb: tty
        # tty: ccc
        # ccc: ddd eee
        # ddd: hub
        # hub: fff
        # eee: dac
        # dac: fff
        # fff: ggg hhh
        # ggg: out
        # hhh: out"""

    print(first_star(data))
    print(second_star(data))
