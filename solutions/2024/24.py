from operator import or_, and_, xor


def parse(data):
    inputs = {k.split(': ')[0]: int(k.split(': ')[1]) for k in data.strip().split('\n\n')[0].split('\n')}
    gates = {k.split(' -> ')[1]: k.split(' -> ')[0].split() for k in data.strip().split('\n\n')[1].split('\n')}

    for logic in gates.values():
        swap = {
            'OR': or_,
            'AND': and_,
            'XOR': xor
        }
        logic[1] = swap[logic[1]]
    return inputs, gates


def first_star(data):
    inputs, gates = parse(data)
    outputs = dict()
    def simulate(out, logic):
        i0, op, i1 = logic
        if out in outputs:
            result = outputs[out]
        elif i0[0] in 'xy' and i1[0] in 'xy':
            result = op(inputs[i0], inputs[i1])
        else:
            result = op(simulate(i0, gates[i0]), simulate(i1, gates[i1]))

        outputs[out] = result
        return result

    for out, logic in gates.items():
        outputs[out] = simulate(out, logic)

    zwires = {k: v for k, v in outputs.items() if k[0] == 'z'}
    return int("".join([str(v[1]) for v in sorted(zwires.items(), reverse=True)]), 2)


def second_star(data):
    return "second answer goes here"


if __name__ == "__main__":
    with open(f"data/2024/24.txt", "r") as f:
        data = f.read()

    print(first_star(data))
    print(second_star(data))
