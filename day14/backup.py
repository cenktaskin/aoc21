import numpy as np

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)

all_characters = np.unique(np.array([list(a) for a in raw_input[:, 0]]).flatten())
starting_polymer = open(input_file, "r").readline().rstrip()
one_step_ahead = {a: a[0] + b + a[1] for a, b in zip(raw_input[:, 0], raw_input[:, -1])}

def calculate_from_parts(poly, step):
    res = ""
    for sli in slicer(poly):
        out = query_the_pair(sli, step)
        res = combine_slices(res, out)
    return res

def slicer(poly):
    return [poly[j:j + 2] for j in range(len(poly) - 1)]

def combine_slices(poly, slic):
    if poly == "":
        return slic
    else:
        return poly + slic[1:]

wikipedia = {hop+1: {} for hop in range(10)}
wikipedia[1] = one_step_ahead
print(wikipedia)
for i in range(2,5):
    for key in wikipedia[1].keys():
        val = wikipedia[i-1][key]
        print(f"{key}->{val}")
        res = ""
        for sli in slicer(val):
            out = wikipedia[i-1][sli]
            res = combine_slices(res, out)
        wikipedia[i][key] = res
        print(res)
