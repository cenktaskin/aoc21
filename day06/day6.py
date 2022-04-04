import numpy as np

input_file = "input.txt"
raw_input = np.loadtxt(input_file, delimiter=",", dtype=int)


def a_day_in_the_sea(swarm):
    # part 1 func, gets the input as it sees, can't scale
    swarm -= 1
    birth_flag = swarm == -1
    swarm[birth_flag] = 6
    birth_count = np.sum(birth_flag, dtype=int)
    return np.concatenate([swarm, np.ones(birth_count, dtype=int) * 8])


def a_day_in_the_sea_but_smarter(swarm):
    birth_count = swarm[0]
    swarm = np.append(swarm[1:], 0)
    swarm[6] += birth_count
    swarm[8] += birth_count
    return swarm

bin_count = np.bincount(raw_input.astype(int))
swarm = np.pad(bin_count, (0, 9 - bin_count.shape[0]))

days = 80
for day in range(1, days + 1):
    swarm = a_day_in_the_sea_but_smarter(swarm)

print(f"After {days} days fish count: {np.sum(swarm)}")
