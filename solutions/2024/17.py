def combo(n):
    return {
        0:0, 1:1, 2:2, 3:3,
        4: register["A"],
        5: register["B"],
        6: register["C"],
    }[n]

def adv(n):
    global jump
    jump = True
    register["A"] = int(register["A"] / 2**combo(n))

def bxl(n):
    global jump
    jump = True
    register["B"] = register["B"] ^ n

def bst(n):
    global jump
    jump = True
    register["B"] = combo(n) % 8

def jnz(n):
    global ip, jump
    if register["A"] != 0:
        ip = n
        jump = False

def bxc(_):
    global jump
    jump = True
    register["B"] = register["B"] ^ register["C"]

def out(n):
    global jump
    jump = True
    output.append(combo(n) % 8)

def bdv(n):
    global jump
    jump = True
    register["B"] = int(register["A"] / 2**combo(n))

def cdv(n):
    global jump
    jump = True
    register["C"] = int(register["A"] / 2**combo(n))


instruction = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}

data = """Register A: 28422061
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,1,5,4,2,5,5,0,3,3,0"""

raw = dict(zip(["A", "B", "C", "P"], [d.split(" ")[-1] for d in data.split("\n") if d]))
register_ = dict()
for r in ["A", "B", "C"]:
    register_[r] = int(raw[r])

program = list(map(int, raw["P"].split(",")))

for i in range(1, 100000000):
    n = bin(i)[2:] + '11011010110111010111101'
    register = register_.copy()
    register["A"] = int(n, 2)
    ip = 0
    jump = True
    output = list()

    while ip < len(program):
        opc = program[ip]
        opr = program[ip + 1]
        instruction[opc](opr)
        if jump:
            ip += 2

        if output and output != program[:len(output)]:
            break

    if output == program:
        break
    elif output and output == program[:len(output)]:
        print(int(n, 2), output)


",".join(map(str, output)), n

# 23948989 [2, 4, 1, 1, 7, 5, 1, 5, 4]
# 820866749 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 829255357 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 837643965 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 3895022415549 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2, 5, 5, 0, 3]
# 34681347993277 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2, 5, 5, 0, 3, 3]

# 6 [2]
# 14 [2, 4]
# 332 [2, 4, 1]
# 23948989 [2, 4, 1, 1, 7, 5, 1, 5, 4]
# 23949245 [2, 4, 1, 1, 7, 5, 1, 5, 4]
# 820866749 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 820867005 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 829255357 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 829255613 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 837643965 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
# 837644221 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]

# 332                             101001100
# 23948989        1011011010110111010111101
# 820866749  110000111011010110111010111101

#                     1011011010110111010111101 [2, 4, 1, 1, 7, 5, 1, 5, 4]
#                110000111011010110111010111101 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
#                110001011011010110111010111101 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
#                110001111011010110111010111101 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2]
#    111000101011100001011011010110111010111101 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2, 5, 5, 0, 3]
# 111111000101011100001011011010110111010111101 [2, 4, 1, 1, 7, 5, 1, 5, 4, 2, 5, 5, 0, 3, 3]

def first_star(data):
    return "first answer goes here"


def second_star(data):
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/2024/17.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
