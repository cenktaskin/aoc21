#!/usr/bin/env python

from pathlib import Path

import numpy as np


def read_input(fname):
    with open(Path(__file__).parent.joinpath(fname), "r") as f:
        return f.read()


def parse_input(inp: str):
    return [int(i.split(": ")[1]) for i in inp.split("\n")[:-1]]


class DeterministicDice:
    def __init__(self):
        self.last_roll = 0

    def roll(self):
        self.last_roll += 1
        return self.last_roll


def part1(input):
    posn = [i - 1 for i in input]
    score = [0, 0]
    n = 0  # round
    print(f"Initial pos {posn=}")
    dice = DeterministicDice()
    i_player = 0
    while score[0] < 1000 and score[1] < 1000:
        for i in range(3):
            posn[i_player] = (posn[i_player] + dice.roll()) % 10
        score[i_player] += posn[i_player] + 1
        i_player = abs(i_player - 1)
        n += 1
    print(score[i_player] * n * 3)


def part2(input):
    quantum_mat = np.zeros(shape=(21, 10), dtype=int)  # scores X posn matrix
    # initialize a game
    initial_pos = 4
    quantum_mat[0, initial_pos] += 1
    # one turn
    pos_i = initial_pos  # position we're iterating (col)
    pnt_i = 0  # score we're iterating (row)
    count = quantum_mat[pnt_i, pos_i]
    distrb = [1, 3, 6, 7, 6, 3, 1] * count

    res_mat = np.zeros(shape=(21, 10), dtype=int)
    for move, count in zip(list(range(3, 9)), distrb):
        pos_new = (pos_i + move) % 10
        pnt_new = pos_i + 1 + pos_new
        res_mat[pnt_new, pos_new] += count
    # Rinse and repeat for each non-zero value on quantum_mat
    # At the end the res_mat is ready for new round
    # Ofc there should be two competing quantum_mats taking turns for each
    # player


def main():
    input = parse_input(read_input("test-input.txt"))
    # part1(input)
    part2(input)


if __name__ == "__main__":
    main()
