import numpy as np
import string

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)

unique_nrs = raw_input[:, np.nonzero(raw_input[0] == "|")[0][0] + 1:]
lens = np.char.str_len(unique_nrs)
unique_lens = [2, 3, 4, 7]
counts = [(lens == l).astype(int) for l in unique_lens]


# print(np.sum(counts))

# part 2

def string_to_one_hot(inp):
    alphabet = np.array(list(string.ascii_lowercase[:7]))
    return np.sum([(alphabet == c).astype(int) for c in inp], axis=0)


def vect_to_digit(vect):
    return np.arange(10)[np.all(decoder == vect, axis=1)]


sum = 0
delimeter_ind = np.nonzero(raw_input[0] == "|")[0][0]
for line in raw_input:
    unique_nrs = line[:delimeter_ind]
    output_code = line[delimeter_ind + 1:]

    input_msg = np.array([string_to_one_hot(code) for code in unique_nrs])
    lengths = np.sum(input_msg, axis=1)
    nr1 = input_msg[lengths == 2]
    nr4 = input_msg[lengths == 4]
    nr7 = input_msg[lengths == 3]
    nr8 = input_msg[lengths == 7]
    # segA = nr7 - nr1
    # print(f"segA: {segA}")
    # check the unlit segment of group6 (group of codes with length 6). Only one member shares that one with nr1
    group6 = input_msg[lengths == 6]
    unlit_group6 = (group6 == 0).astype(int)
    which6, _ = np.nonzero(unlit_group6 * nr1)
    nr6 = group6[which6]
    segC = 1 - nr6
    segF = nr1 - segC
    leftover6 = group6[np.any(~((group6 - nr6) == 0), axis=1)]  # nr9 and nr0
    mask_nr9 = np.sum(leftover6 * nr4, axis=1) == 4
    nr9 = leftover6[mask_nr9]  # nr 0 has nr 4 completely
    nr0 = leftover6[~mask_nr9]
    # print(f"segC: {segC}")
    # print(f"segF: {segF}")
    # the one who missed segC from group5 is 5
    group5 = input_msg[lengths == 5]
    mask5 = np.all((group5 * segC) == 0, axis=1)
    nr5 = group5[mask5]
    left_over_group5 = group5[~mask5]  # nr2 and nr3
    nr3 = np.sum(left_over_group5 * segF, axis=1).reshape(1, -1) @ left_over_group5
    nr2 = (1 - np.sum(left_over_group5 * segF, axis=1)).reshape(1, -1) @ left_over_group5

    decoder = np.array([nr0, nr1, nr2, nr3, nr4, nr5, nr6, nr7, nr8, nr9]).reshape(10, -1)

    output_as_vect = np.array([string_to_one_hot(code) for code in output_code])
    each_digit = np.array([vect_to_digit(v) for v in output_as_vect]).flatten()
    output_nr = (each_digit @ np.array([10 ** x for x in range(4)])[::-1].reshape(-1, 1))[0]
    print(output_nr)
    sum += output_nr
print(sum)
