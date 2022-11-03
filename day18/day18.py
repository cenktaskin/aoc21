import numpy as np


def nan_matrix(d, w):
    return np.array(d * w * [np.nan]).reshape(d, w)


def read_topopgrahy(inp_list: str) -> np.ndarray:
    # max_depth, int_count = check_topograpgy(inp_list)
    mat = nan_matrix(max_depth := 5, sum([a.isdigit() for a in inp_list]))

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


def add(a: np.ndarray, b: np.ndarray):
    new_width = a.shape[1] + b.shape[1]
    new_mat = nan_matrix(new_depth := 5, new_width)
    new_mat[1:, :a.shape[1]] = a[:-1]
    new_mat[1:, -b.shape[1]:] = b[:-1]
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
    one2split = np.where(inp > 10)[0]
    val = inp[*one2split]
    inp[*one2split] = np.nan
    new_mat = np.hstack([inp[:, :one2split[1] + 1], inp[:, one2split[1]:]])
    new_mat[one2split[0] + 1, one2split[1]] = np.floor(val / 2)
    new_mat[one2split[0] + 1, one2split[1] + 1] = np.ceil(val / 2)
    return new_mat


# def reduce(inp):
#     while True:
#         if np.where(~np.isnan(inp[-1]))[0]:
#             inp = explode(inp)
#             continue
#
#     left=np.where(~np.isnan(inp[-1]))[0]
#     print(left)


if __name__ == "__main__":
    with open("test-input.txt", "r") as f:
        raw_numbers = f.read().splitlines()

    cumulative_sum = read_topopgrahy(raw_numbers[0])
    print(f"{cumulative_sum=}")
    for line in raw_numbers[1:]:
        new_number = read_topopgrahy(line)
        print(f"{new_number=}")
        cumulative_sum = add(cumulative_sum, new_number)
        print(f"{cumulative_sum=}")

