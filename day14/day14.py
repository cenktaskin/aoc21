from collections import Counter

import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)
VOCAB = np.array(raw_input[:, 0])
PAIR_COUNT = len(VOCAB)
CHAR_VOCAB = np.array(list(Counter("".join(VOCAB)).keys()))
CHAR_COUNT = len(CHAR_VOCAB)


def pair_to_ohe(p):
    return np.eye(PAIR_COUNT)[VOCAB == p].flatten()


def poly_to_ohe(poly):
    return np.sum([pair_to_ohe(poly[j:j + 2]) for j in range(len(poly) - 1)], axis=0)


def pair_to_counts(p):
    return np.sum([np.eye(CHAR_COUNT)[CHAR_VOCAB == c].flatten() for c in p], axis=0)


def take_step(arr):
    new_arr = np.zeros_like(arr)
    avaliable_pairs = np.diag(arr)[arr > 0]
    for p in avaliable_pairs:
        multiplier = np.sum(p)
        new_arr += multiplier * reaction_table[tuple(p / multiplier)]
    return new_arr


bins = np.array([pair_to_counts(p) for p in VOCAB])

reaction_table = {tuple(pair_to_ohe(a)): poly_to_ohe(a[0] + b + a[1]) for a, b in
                  zip(raw_input[:, 0], raw_input[:, -1])}

starting_polymer = open(input_file, "r").readline().rstrip()
first_and_last = pair_to_counts(starting_polymer[0] + starting_polymer[-1])

p = poly_to_ohe(starting_polymer)
for i in range(40):
    p = take_step(p)

hist = (bins.T @ p + first_and_last) / 2
print(hist)
print(int(hist.max() - hist.min()))
