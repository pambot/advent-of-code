import math

# Possible values for unknown variables
a = 1/4
b = -3
c = 1/2

# Grid as list of lists
grid = [
    # Row 0
    [None, None, None, None, 6*c - 4*b, None, None, None, None, None, None, None, None],

    # Row 1
    [None, None, None, None, None, None, None, 8 - b, None, None, None, None, None],

    # Row 2
    [None, (a**b - 4)/(6*c + 1), None, (b + c)/(c - 1), None, None, b**2 - b/c, None, math.sqrt(30 + a)/c, None, (a + b)/(c - 3*a), None, None],

    # Row 3
    [None, None, None, None, (b - 3*a)/(a - c), None, None, 8*a - 2*b, None, b/(a - c), None, (b + 9)/math.sqrt(c - a), None],

    # Row 4
    [None, 18/(a*c + 1), None, None, None, c**b, None, None, None, None, (3 + b**2)/math.sqrt(3 + 2*c), None, None],

    # Row 5
    [None, None, None, b/(a**2 - c**2), None, None, None, None, None, None, None, None, math.sqrt(a + 2)/a],

    # Row 6
    [None, None, a**b - 12/a, None, 2*c + c/a, None, 4*a - 5*b, None, c + 2*a, None, b/(9*a - 5*c), None, None],

    # Row 7
    [(b**3 + 2*c)/(b + 2*c), None, None, None, None, None, None, None, None, b/(a - 1), None, None, None],

    # Row 8
    [None, None, (c - b)/(2*a), None, None, None, None, b/(a - c), None, None, None, (b + c)/(a - c), None],

    # Row 9
    [None, math.log(a, c), None, (c**2 - b)/a, None, (b - 1)**2, None, None, (43 - a*c)**(1/3)/a, None, None, None, None],

    # Row 10
    [None, None, (b - a)/(a - c), None, 11 - b, None, (b - 2*a)/(a - c), None, None, (c + 3)/a, None, 8*c - b/c, None],

    # Row 11
    [None, None, None, None, None, b**2, None, None, None, None, None, None, None],

    # Row 12
    [None, None, None, None, None, None, None, None, (2**b + 1)/(a*c), None, None, None, None]
]

# Grid with computed values (a=1/4, b=-3, c=1/2)
values = [
    [None, None, None, None,   15, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None,   11, None, None, None, None, None],
    [None,   15, None,    5, None, None,   15, None,   11, None,   11, None, None],
    [None, None, None, None,   15, None, None,    8, None,   12, None,   12, None],
    [None,   16, None, None, None,    8, None, None, None, None,    6, None, None],
    [None, None, None,   16, None, None, None, None, None, None, None, None,    6],
    [None, None,   16, None,    3, None,   16, None,    1, None,   12, None, None],
    [  13, None, None, None, None, None, None, None, None,    4, None, None, None],
    [None, None,    7, None, None, None, None,   12, None, None, None,   10, None],
    [None,    2, None,   13, None,   16, None, None,   14, None, None, None, None],
    [None, None,   13, None,   14, None,   14, None, None,   14, None,   10, None],
    [None, None, None, None, None,    9, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None,    9, None, None, None, None],
]

# Solved grid (N=16 subtiles)
solution = [
    [ 0,  5,  5,  5, 15, 15,  0, 11,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  5,  0, 15,  0, 11,  0,  0, 11, 11, 11],
    [15, 15, 15,  5,  0, 15, 15, 11, 11, 11, 11,  0, 11],
    [15, 16, 15, 15, 15, 15,  8,  8,  8, 12, 12, 12, 11],
    [15, 16,  0,  0,  8,  8,  8,  0,  8, 12,  6,  6,  6],
    [15, 16,  0, 16, 16, 16, 16,  0,  8, 12, 12,  0,  6],
    [ 0, 16, 16, 16,  3,  3, 16, 16,  1,  4, 12,  6,  6],
    [13, 13, 13, 13, 14,  3, 16,  4,  4,  4, 12, 10, 10],
    [ 7,  7,  7, 13, 14, 16, 16, 12, 12, 12, 12, 10,  0],
    [ 7,  2,  2, 13, 14, 16, 14, 14, 14, 14,  0, 10,  0],
    [ 7,  7, 13, 13, 14, 14, 14,  0,  9, 14, 14, 10, 10],
    [ 0,  7, 13,  9,  9,  9,  9,  0,  9, 14,  0,  0, 10],
    [ 0,  0, 13, 13, 13, 13,  9,  9,  9, 14, 10, 10, 10],
]
# Row sums: [56, 64, 135, 162, 93, 133, 115, 129, 138, 120, 139, 89, 123]
# Answer: min(56) * max(162) = 9072

rowsums = [sum(s) for s in solution]
print(min(rowsums) * max(rowsums))
