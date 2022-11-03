import numpy as np


def nan_matrix(d, w):
    return np.array(d * w * [np.nan]).reshape(d, w)


def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.vstack([nan_matrix(1, a.shape[1] + b.shape[1]), np.hstack([a[:-1], b[:-1]])])


def read_topopgrahy(inp_list: str) -> np.ndarray:
    mat = nan_matrix(5, sum([a.isdigit() for a in inp_list]))
    current_depth, current_int = -1, 0
    for element in inp_list:
        match element:
            case "[":
                current_depth += 1
            case "]":
                current_depth -= 1
            case "," | " ":
                continue
            case _:  # int
                mat[current_depth, current_int] = element
                current_int += 1
    return mat


def explode(inp):
    notna_inp = ~np.isnan(inp)
    left, right = np.nonzero(notna_inp[-1])[0][:2]
    res = inp.copy()
    if left > 0:
        left_ngh_idx_y = np.nonzero(notna_inp[:, left - 1])
        res[left_ngh_idx_y, left - 1] += inp[-1, left]
    if right < inp.shape[1] - 1:
        right_ngb_idx_y = np.nonzero(notna_inp[:, right + 1])
        res[right_ngb_idx_y, right + 1] += inp[-1, right]
    new_col = nan_matrix(inp.shape[0], 1)
    new_col[3] = 0
    return np.hstack([res[:, :left], new_col, res[:, right + 1 :]])


def split(inp: np.ndarray) -> np.ndarray:
    split_canditates = np.argwhere(inp >= 10)
    to_be_split = split_canditates[np.argmin(split_canditates[:, 1])]
    val = inp[*to_be_split]
    inp[*to_be_split] = np.nan
    new_mat = np.hstack([inp[:, : to_be_split[1] + 1], inp[:, to_be_split[1] :]])
    new_mat[to_be_split[0] + 1, to_be_split[1]] = np.floor(val / 2)
    new_mat[to_be_split[0] + 1, to_be_split[1] + 1] = np.ceil(val / 2)
    return new_mat


def reduce_it(inp: np.ndarray) -> np.ndarray:
    print(f"Array to be reduced\n{inp}")
    if np.any(to_be_exploded := ~np.isnan(inp[-1])):
        print("Following entries on last row need exploding")
        print(to_be_exploded)
        return reduce_it(explode(inp))
    elif np.any(to_be_split := inp >= 10):
        print("Following entry need splitting")
        print(np.argwhere(to_be_split)[0])
        return reduce_it(split(inp))
    else:
        print("Reducing is complete, returning following")
        print(inp)
        return inp


def main():
    with open("day18/test5.txt", "r") as f:
        raw_numbers = f.read().splitlines()

    cumulative_sum = read_topopgrahy(raw_numbers[0])
    print(f"cumulative_sum")
    print(f"{cumulative_sum}")
    for line in raw_numbers[1:]:
        new_number = read_topopgrahy(line)
        print(f"{new_number=}")
        cumulative_sum = add(cumulative_sum, new_number)
        print(f"cumulative_sum")
        print(f"{cumulative_sum}")
        cumulative_sum = reduce_it(cumulative_sum)
        print(f"cumulative_sum")
        print(f"{cumulative_sum}")
        exit()


if __name__ == "__main__":
    main()
