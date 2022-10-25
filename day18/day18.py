import numpy as np


# with open("input.txt", "r") as f:
#     a = f.readlines()

def check_topograpgy(inp_list):
    depth, max_depth, int_count = 0, 0, 0
    for element in inp_list:
        match element:
            case '[':
                depth += 1
            case ']':
                depth -= 1
            case "," | " ":
                continue
            case _:  # int
                int_count += 1
        if depth > max_depth:
            max_depth = depth
    return max_depth, int_count


def topography_template(d, w):
    return np.array(d * w * [np.nan]).reshape(d, w)


def read_topopgrahy(inp_list):
    max_depth, int_count = check_topograpgy(inp_list)
    mat = topography_template(max_depth, int_count)

    current_depth, current_int = -1, 0
    for element in inp_list:
        match element:
            case '[':
                current_depth += 1
            case ']':
                current_depth -= 1
            case "," | " ":
                continue
            case _:  # int
                mat[current_depth, current_int] = element
                current_int += 1
    return mat


def add(a, b):
    new_depth = max(a.shape[0], b.shape[0]) + 1
    new_width = a.shape[1] + b.shape[1]
    new_mat = topography_template(new_depth, new_width)
    new_mat[1:a.shape[0] + 1, :a.shape[1]] = a
    new_mat[1:b.shape[0] + 1, -b.shape[1]:] = b
    return new_mat


def explode(inp):
    a = inp[-1]  # last row
    exploding_ones = np.where(~np.isnan(a))
    print(exploding_ones)


raw_a = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
raw_a = "[1,2]"
raw_b = "[[3,4],5]"

a = read_topopgrahy(raw_a)
b = read_topopgrahy(raw_b)

print(f"{a=}")
print(f"{b=}")

sum = add(a, b)
print(f"{sum=}")
print(explode(sum))
