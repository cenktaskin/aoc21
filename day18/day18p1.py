import numpy as np

# with open("input.txt", "r") as f:
#     a = f.readlines()

a = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
a = "[1,2]"

depth, max_depth = 0, 0
for element in a:
    match element:
        case '[':
            depth += 1
        case ']':
            depth -= 1
        case "," | " ":
            continue
        case _:  # int
            continue
    if depth > max_depth:
        max_depth = depth

print(max_depth)