import numpy as np


def nan_matrix(d, w):
    return np.array(d * w * [np.nan]).reshape(d, w)


def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.vstack(
        [nan_matrix(1, a.shape[1] + b.shape[1]), np.hstack([a[:-1], b[:-1]])]
    )


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
    new_col = nan_matrix(5, 1)
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
    if np.any(~np.isnan(inp[-1])):
        return reduce_it(explode(inp))
    elif np.any(inp >= 10):
        return reduce_it(split(inp))
    else:
        return inp


def calculate_magnitude(inp: np.ndarray) -> int:
    while True:
        not_na = np.argwhere(~np.isnan(inp))
        elevation_canditates = np.argwhere(not_na[:, 0] == not_na[:, 0].max()).flatten()
        left, right = not_na[elevation_canditates[:2]]
        new_col = nan_matrix(5, 1)
        new_col[left[0] - 1] = inp[*left] * 3 + inp[*right] * 2
        res = np.hstack([inp[:, : left[1]], new_col, inp[:, right[1] + 1 :]])
        inp = res
        if left[0] == 0:
            return new_col[left[0] - 1][0]


def part1(raw_numbers):
    cumulative_sum = read_topopgrahy(raw_numbers[0])
    for line in raw_numbers[1:]:
        new_number = read_topopgrahy(line)
        cumulative_sum = add(cumulative_sum, new_number)
        cumulative_sum = reduce_it(cumulative_sum)
        print(f"cumulative_sum")
        print(f"{cumulative_sum}")
    result = calculate_magnitude(cumulative_sum)
    return result


def part2(raw_numbers):
    results = []
    for line_i in raw_numbers:
        nr1 = read_topopgrahy(line_i)
        for line_j in raw_numbers:
            if line_i == line_j:
                results.append(0)
            nr2 = read_topopgrahy(line_j)
            cumulative_sum = add(nr1, nr2)
            cumulative_sum = reduce_it(cumulative_sum)
            results.append(calculate_magnitude(cumulative_sum))
    return max(results)


def main():
    with open("day18/input.txt", "r") as f:
        raw_numbers = f.read().splitlines()

    # result = part1(raw_numbers)
    result = part2(raw_numbers)

    print(result)


if __name__ == "__main__":
    main()
