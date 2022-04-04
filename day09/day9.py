import itertools
import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)

height_map = np.array([np.array(list(line)) for line in raw_input]).astype(int)
map_padded = np.pad(height_map, (1, 1), mode='maximum')
shifts = np.array([np.roll(map_padded, s, axis=a) for a, s in itertools.product([0, 1], [-1, 1])])
local_minimas = np.sum(np.array([np.sign(map_padded - shift) for shift in shifts]), axis=0) == -4
print(np.sum(map_padded[local_minimas] + 1))

# part 2
mask = np.zeros_like(map_padded)
iter = np.nditer(map_padded, flags=["multi_index"])
last_class = 0
coincidents = []
for x in iter:
    # The algo from Spong Robotics book, connected components
    if x == 9:
        continue
    i, j = iter.multi_index
    if mask[i - 1, j] + mask[i, j - 1] == 0:
        last_class += 1
        mask[i, j] = last_class
    else:
        if (mask[i - 1, j] != 0) and (mask[i, j - 1] != 0):
            if mask[i - 1, j] != mask[i, j - 1]:
                mask[mask == max(mask[i - 1, j], mask[i, j - 1])
                     ] = min(mask[i - 1, j], mask[i, j - 1])
            mask[i, j] = min(mask[i - 1, j], mask[i, j - 1])
        else:
            mask[i, j] = mask[i, j - 1] + mask[i - 1, j]

basins = np.array([np.count_nonzero(mask == cl) for cl in np.unique(mask)])
print(np.prod(np.sort(basins[1:])[-3:]))
