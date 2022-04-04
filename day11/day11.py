import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)
raw_input = np.array([[ch for ch in x] for x in raw_input], dtype=int)


def get_neighbourhood(loc, dims):
    # get the window around loc, not overstepping dims
    return slice(max(0, loc[0] - 1), min(dims[0], loc[0] + 2)), slice(max(0, loc[1] - 1), min(dims[1], loc[1] + 2))


def step(octopus_field):
    flash_tracker = np.zeros_like(octopus_field)
    octopus_field += 1
    while True:
        flashing_octopus = octopus_field > 9
        if not np.any(flashing_octopus):
            break
        loc = np.argwhere(flashing_octopus)[0]  # get first element >9
        flash_tracker[tuple(loc)] += 1
        octopus_field[get_neighbourhood(loc, octopus_field.shape)] += 1
        octopus_field[flash_tracker == 1] = 0  # set all flashed to 0
    return octopus_field


field = raw_input
flash_count = 0
step_count = 1
while True:
    # cond = i == 100 #part1
    cond = np.all(field == 0)  # part2
    if cond:
        break
    print(f"Step: {step_count}")
    field = step(field)
    flash_count += np.sum(field == 0)
    print(f"Total {flash_count} flashes")
    print(f"Flashed octopuses:\n{field == 0}")
    step_count += 1
