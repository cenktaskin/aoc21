import numpy as np

input_file = "input.txt"
raw_input = np.loadtxt(input_file, delimiter=",", dtype=int)
print(f"Input: {raw_input}")

part1_flag=False
if part1_flag:
    meeting_points = np.median(raw_input).astype(int)
    # Justificaiton for meeting point: https://math.stackexchange.com/a/113336
    print(f"Median: {meeting_points}")
    print(f"Total fuel: {np.sum(np.abs(raw_input-meeting_points))}")


# part 2
# tried to find analytical soln but stuck at
# 2*sum(rho-arr) + sum(sign(arr-rho)) = 0  # rho that satisfies this gets the min
# Probably a float so need rounding
test_rhos = np.arange(raw_input.max())
cost = lambda rho: np.sum(np.square(raw_input-rho) + np.abs(raw_input-rho))/2
meeting_point = np.argmin([cost(rho) for rho in test_rhos])
print(int(cost(meeting_point))) # has to be integer think about by-hand calc of cost
