import numpy as np

with open("input.txt", 'r') as f:
    raw = f.read().split('\n')

# Part 1
readings = np.array(raw).astype(int)


def get_dt_from_array(arr):
    past_readings = np.append(np.array([0]), arr[:-1])
    dreadings = arr - past_readings
    return dreadings


dreadings = get_dt_from_array(readings)[1:]
print(np.sum(dreadings > 0))

# Part 2
shift1 = np.append(np.array([0]), readings[:-1])
shift2 = np.append(np.array([0, 0]), readings[:-2])

window = readings + shift1 + shift2
dwindow = get_dt_from_array(window)[3:]
print(np.sum(dwindow > 0))


# Part 2 Method 2
def get_window_matrix(n, w_size):
    res = np.eye(n)
    for i in range(1, w_size):
        shifted = np.roll(np.eye(n), shift=i, axis=1)
        shifted[:, :i] = 0
        res += shifted
    return res


window_size = 3
mat = get_window_matrix(len(readings), window_size)
window_sums = mat @ readings
window_sums = window_sums[:-2]  # get rid of the last two "windows" that are not windows
print(np.sum(get_dt_from_array(window_sums)[1:] > 0))
# array slicing is for getting rid of no past value items, in this case first window
