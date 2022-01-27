from collections import Counter

import numpy as np

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)


def ohe(vocab, item):
    return np.eye(len(vocab))[vocab == item].flatten()


def poly_to_ohe(poly):
    return np.sum([ohe(pair_vocab, poly[j:j + 2]) for j in range(len(poly) - 1)], axis=0)


def pair_to_counts(ch_vocab, p):
    return np.sum([ohe(ch_vocab, c) for c in p], axis=0)


def take_step(arr):
    new_arr = np.zeros_like(arr)
    available_pairs = np.diag(arr)[arr > 0]
    for p in available_pairs:
        multiplier = np.sum(p)
        new_arr += multiplier * reaction_table[tuple(p / multiplier)]
    return new_arr


def poly_to_counts(vocab, pol, pol0):
    ch_vocab = np.array(list(Counter("".join(vocab)).keys()))
    bins = np.array([pair_to_counts(ch_vocab, p) for p in vocab])
    first_and_last = pair_to_counts(ch_vocab, pol0[0] + pol0[-1])
    return (bins.T @ pol + first_and_last) / 2


pair_vocab = np.array(raw_input[:, 0])

reaction_table = {tuple(poly_to_ohe(a)): poly_to_ohe(a[0] + b + a[1]) for a, b in
                  zip(raw_input[:, 0], raw_input[:, -1])}

starting_polymer = open(input_file, "r").readline().rstrip()
print(starting_polymer)

p = poly_to_ohe(starting_polymer)
print(p)
print(pair_vocab)
for i in range(40):
    p = take_step(p)
    print(f"Step {i}")
    print(p)

hist = poly_to_counts(pair_vocab, p, starting_polymer)
print(hist)
print(int(hist.max() - hist.min()))


d={a:b for a, b in zip(raw_input[:, 0], raw_input[:, -1])}
for k in d:
    print(f"{k}->{d[k]}")