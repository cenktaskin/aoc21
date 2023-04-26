#!/usr/bin/env python

from pathlib import Path


def read_input(fname):
    with open(Path(__file__).parent.joinpath(fname), "r") as f:
        return f.read()


def parse_input(inp: str):
    return [int(i.split(": ")[1]) for i in inp.split("\n")[:-1]]


def main():
    input = parse_input(read_input("input.txt"))
    print(input)
    pos0, pos1 = [i - 1 for i in input]
    score0, score1 = 0, 0
    n = 0  # round
    print(f"Initial pos")
    print(f"{pos0=}")
    print(f"{pos1=}")
    while True:
        print(f"Round {n}")
        roll0 = 3 * (6 * n + 2)
        pos0 = (pos0 + roll0) % 10
        score0 += pos0 + 1
        print(f"{roll0=}")
        print(f"{pos0=},{score0=}")
        if score0 >= 1000:
            print("Player 0 won")
            roll_count = (n + 1) * 6 - 3
            loser_score = score1
            break
        roll1 = 3 * (6 * n + 5)
        pos1 = (pos1 + roll1) % 10
        score1 += pos1 + 1
        print(f"{roll1=}")
        print(f"{pos1=},{score1=}")
        if score1 >= 1000:
            print("Player 1 won")
            roll_count = (n + 1) * 6
            loser_score = score0
            break
        n += 1

    print(f"Result:{roll_count*loser_score}")


if __name__ == "__main__":
    main()
