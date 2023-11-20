import logging
import re
import sys
from pathlib import Path

import numpy as np


def read_input(fname):
    with open(Path(__file__).parent.joinpath(fname), "r") as f:
        return f.read()


def parse_args(args: list) -> list:
    if "--debug" in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove("--debug")
    return args


def parse_input(inp: str):
    pat = r"=(\-*\w+)..(\-*\w+)"
    line_pattern = r"^(\w{2,3})\sx" + pat + ",y" + pat + ",z" + pat + "$"
    return re.findall(line_pattern, inp, re.MULTILINE)


def slice_mat(coord):
    return np.s_[
        coord[0] : coord[1] + 1,
        coord[2] : coord[3] + 1,
        coord[4] : coord[5] + 1,
    ]


def part1(input):
    mat = np.zeros((101, 101, 101), dtype=int)
    for flag, *coord in input:
        flag = int(flag == "on")
        coord = [int(c) + 50 for c in coord]
        logging.info(slice_mat(coord))
        mat[slice_mat(coord)] = flag
        logging.info(f"Current sum:{mat.sum()}")


def part2(input):
    pass


def main():
    input = parse_input(read_input("input.txt"))
    # part1(input)
    part2(input)


if __name__ == "__main__":
    parse_args(sys.argv)
    main()
