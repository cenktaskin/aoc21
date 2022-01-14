import numpy as np
from io import StringIO

input_file = "input.txt"
with open(input_file, 'r') as f:
    raw_input = f.read().replace(" -> ", ",")

coords = np.genfromtxt(StringIO(raw_input), delimiter=",").astype(int).reshape(-1, 2, 2)  # (#examples,start/end,x/y)
empty_table = np.zeros((coords.max() + 1, coords.max() + 1))

debug = False
for points in coords:
    if debug: print(f"{points=}")
    vect = np.subtract(points[1], points[0])
    points = np.sort(points, axis=0)
    points[-1, :] += 1  # adding one to end point so that we would encapsulate a col or row
    if np.any(vect == 0):  # straight check
        new_line = 1
    else:
        reversion_condition = (np.sign(vect[0] * vect[1]) == -1)
        new_line = np.eye(abs(vect)[0] + 1)
        if reversion_condition:  # check truth table, if only one axis is reverted than it is reverted diag
            new_line = np.fliplr(new_line)
    empty_table[slice(*points[:, 0]), slice(*points[:, 1])] += new_line
    if debug: print(f"{empty_table}"), input()

print(np.sum(empty_table >= 2))
