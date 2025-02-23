from collections import Counter


def parse(data):
    return data.strip().split("\n")


def most_common_bit(diag, i):
    freqs = Counter([d[i] for d in diag])
    if freqs["1"] != freqs["0"]:
        return max(freqs, key=freqs.get)
    else:
        return "1"


def least_common_bit(diag, i):
    freqs = Counter([d[i] for d in diag])
    if freqs["1"] != freqs["0"]:
        return min(freqs, key=freqs.get)
    else:
        return "0"


def first_star(data):
    diag = parse(data)
    gamma = "".join([most_common_bit(diag, i) for i in range(len(diag[0]))])
    epsilon = "".join([least_common_bit(diag, i) for i in range(len(diag[0]))])
    return int(gamma, 2) * int(epsilon, 2)


def second_star(data):
    diag = parse(data)
    for i in range(len(diag[0])):
        mcb  = most_common_bit(diag, i)
        diag = [d for d in diag if d[i] == mcb]
        if len(diag) == 1:
            ogr = diag[0]


    diag = parse(data)
    for i in range(len(diag[0])):
        lcb  = least_common_bit(diag, i)
        diag = [d for d in diag if d[i] == lcb]
        if len(diag) == 1:
            csr = diag[0]

    return int(ogr, 2) * int(csr, 2)


if __name__ == "__main__":
    with open(f"data/2021/03.txt", "r") as f:
        data = f.read()
        #         data = """
        # 00100
        # 11110
        # 10110
        # 10111
        # 10101
        # 01111
        # 00111
        # 11100
        # 10000
        # 11001
        # 00010
        # 01010
        # """

    print(first_star(data))
    print(second_star(data))
