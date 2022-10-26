import numpy as np


# with open("input.txt", "r") as f:
#     a = f.readlines()

# TODO: check_topograpgy gereksiz, derinlik en fazla her zaman 5, sabit tut
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


def nan_matrix(d, w):
    return np.array(d * w * [np.nan]).reshape(d, w)


def read_topopgrahy(inp_list):
    max_depth, int_count = check_topograpgy(inp_list)
    mat = nan_matrix(max_depth, int_count)

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
    new_mat = nan_matrix(new_depth, new_width)
    new_mat[1:a.shape[0] + 1, :a.shape[1]] = a
    new_mat[1:b.shape[0] + 1, -b.shape[1]:] = b
    return new_mat


def explode(inp):
    a = inp[-1]  # last row
    left, right = np.where(~np.isnan(a))[0][:2]
    # TODO: implement the case where there is no suitable number
    # TODO: don't modify the inp, use the res
    left_ngh_idx_y = np.where(~np.isnan(inp[:, left - 1]))
    inp[left_ngh_idx_y, left - 1] += inp[-1, left]
    right_ngb_idx_y = np.where(~np.isnan(inp[:, right + 1]))
    inp[right_ngb_idx_y, right + 1] += inp[-1, right]
    new_col = nan_matrix(inp.shape[0], 1)
    new_col[3] = 0
    return np.hstack([inp[:, :left], new_col, inp[:, right + 1:]])


def split(inp):
    print(np.where(inp > 10))
    print(inp)


raw_a = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
raw_a = "[1,2]"
raw_b = "[[3,4],5]"
raw_c = "[[[[4,3],4],4],[7,[[8,4],9]]]"
raw_d = "[1,1]"

a = read_topopgrahy(raw_a)
b = read_topopgrahy(raw_b)

# print(f"{a=}")
# print(f"{b=}")
#
# sum = add(a, b)
# print(f"{sum=}")
# print(explode(sum))

c = read_topopgrahy(raw_c)
d = read_topopgrahy(raw_d)
print(f"{c=}")
print(f"{d=}")
sum = add(c, d)
print(f"{sum=}")
res = explode(sum)
print(f"{res=}")
res = explode(res)
print(f"{res=}")
