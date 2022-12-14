import ast
import functools


def is_right_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        else:
            return left < right
    elif isinstance(left, int):
        return is_right_order([left], right)
    elif isinstance(right, int):
        return is_right_order(left, [right])
    elif isinstance(left, list) and isinstance(right, list):
        if left == right:
            return None
        elif left == []:
            return True
        elif right == []:
            return False
        else:
            l0 = left[0]
            r0 = right[0]
            check = is_right_order(l0, r0)
            if check in (True, False):
                return check
            elif check == None:
                return is_right_order(left[1:], right[1:])


def first_star(data):
    packet_pairs = [
        (ast.literal_eval(d.split("\n")[0]), ast.literal_eval(d.split("\n")[1]))
        for d in data.split("\n\n")
    ]
    index_sum = 0
    for i, (left, right) in enumerate(packet_pairs):
        if is_right_order(left, right) == True:
            index_sum += i + 1
    return index_sum


def comparator(left, right):
    if left == right:
        return 0
    elif is_right_order(left, right):
        return -1
    else:
        return 1


def second_star(data):
    packets = [ast.literal_eval(d) for d in data.split("\n") if d]
    dividers = [[[2]], [[6]]]
    packets += dividers
    packets = sorted(packets, key=functools.cmp_to_key(comparator))
    return (packets.index(dividers[0]) + 1) * (packets.index(dividers[1]) + 1)


if __name__ == "__main__":
    with open(f"data/2022/13.txt", "r") as f:
        data = f.read()

    assert is_right_order([1,1,3,1,1], [1,1,5,1,1]) == True
    assert is_right_order([[1],[2,3,4]], [[1],4]) == True
    assert is_right_order([9], [[8,7,6]]) == False
    assert is_right_order([[4,4],4,4], [[4,4],4,4,4]) == True
    assert is_right_order([7,7,7,7], [7,7,7]) == False
    assert is_right_order([], [3]) == True
    assert is_right_order([[[]]], [[]]) == False
    assert is_right_order([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]) == False

    assert is_right_order([[2]], [[2],[[[6],3,9,[1],2]],[[8,[0],0],9,2],[2,[[9,1]]],[]]) == True
    assert is_right_order([[6]], [[[6],5,[[6,9,9,0,10],8],6,[[3,6],7]]]) == True
    assert is_right_order(
        [[],[[3,[6],9,4,4],2]],
        [[],[[3,4],[8,3,[6,8,6],0],7,[6,2,[7]],10],[[2],[[10,2],[],[1,3],0,[9, 5,8,0,0]],1,[8,5,10],[5,4,1,1]],[0,[1],[8,4,[]],[6]]]
    ) == False

    print(first_star(data))
    print(second_star(data))
