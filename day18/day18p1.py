import numpy as np

with open("input.txt", "r") as f:
    a = f.readlines()

a = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
a = "[1,2]"

sum = -1
for i in a:
    try:
        int(i)
        sum += 1
    except ValueError:
        continue


def add(a, b):
    return [a] + [b]


def read_input(a):
    depth = 0
    result = np.zeros(1) - 1
    for element in a:
        match element:
            case '[':
                depth += 1
            case ']':
                depth -= 1
            case "," | " ":
                continue
            case _:  # int
                if depth > result.shape[0]:
                    print("problem, new depth is deeper than current table")
                    result = np.vstack([result, np.zeros_like(result[0]) - 1])
                print(f"{depth=}")
                print(f"{element=}")
                new_col = np.zeros((result.shape[0], 1)) - 1
                new_col[depth - 1] = int(element)
                result = np.hstack([result, new_col])
                print(f"{result=}")
    result = result[:, 1:]
    result[result == -1] = np.nan
    print(f"{result}")


print(a)
read_input(a)


def check_depth(pair):
    print(f"checking {pair}")
    if isinstance(pair, list):
        print(f"disecting {pair}")
        return [max(check_depth(pair[0])) + 1, max(check_depth(pair[1])) + 1]
    else:
        print("not a list")
        return [0]


pair = None
