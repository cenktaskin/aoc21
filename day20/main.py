#!/usr/bin/env python

from pathlib import Path
import numpy as np


def read_input(fname):
    with open(Path(__file__).parent.joinpath(fname), "r") as f:
        return f.read()


def parse_input(inp: str):
    alg, img = inp.split("\n\n")
    img = img.replace("\n", "")
    return alg, np.array([int(ch == "#") for ch in img]).reshape(
        int(len(img) ** 0.5), -1
    )


def conv(mat, dec):
    bin_value = int("".join([str(i) for i in mat.reshape(-1)]), 2)
    return int(dec[bin_value] == "#")


def iterate(mat, decoder, surr):
    img = np.pad(mat, 2, constant_values=surr)
    res = np.zeros_like(img)

    for r in range(1, len(img) - 1):
        for c in range(1, len(img) - 1):
            res[r, c] = conv(img[r - 1 : r + 2, c - 1 : c + 2], decoder)

    res = res[1:-1, 1:-1]  # get rid of the padding that has not been convtd over
    new_surr = conv(np.zeros((3, 3), dtype=int) + surr, decoder)
    return res, new_surr


def main():
    input_file = "input.txt"
    raw_input = read_input(input_file)
    decoder, img = parse_input(raw_input)
    surr = 0
    for i in range(50):
        img, surr = iterate(img, decoder, surr)
    print(np.sum(img))


if __name__ == "__main__":
    main()
