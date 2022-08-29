import numpy as np


def check_trajectory(v0, goal):
    x = np.array([0, 0])
    v = np.copy(v0)

    while np.all(x <= goal[1]):
        if np.all(x >= goal[0]):
            return True
        x += v
        v += np.array([-1, +1])
        if v[0] < 0:
            v[0] = 0
    return False


def check_deepest_curve(goal):
    min_v0x = int(np.ceil((-1 + (1 + 8 * goal[0, 0]) ** 0.5) / 2))
    for v0_x in range(min_v0x, goal[1, 0] + 1):
        for v0_y in range(-(goal[1, 1] + 1), goal[1, 1] + 1):
            v0 = np.array([v0_x, v0_y])
            if check_trajectory(v0, goal):
                return v0


def check_possible_v(goal):
    possible_vs = []
    min_v0x = int(np.ceil((-1 + (1 + 8 * goal[0, 0]) ** 0.5) / 2))
    for v0_x in range(min_v0x, goal[1, 0] + 1):
        for v0_y in range(-(goal[1, 1] + 1), goal[1, 1] + 1):
            v0 = np.array([v0_x, v0_y])
            if check_trajectory(v0, goal):
                possible_vs.append(v0)
    return possible_vs



if __name__ == "__main__":
    target = np.array([[201, -65], [230, -99]])
    target[:, 1] *= -1

    # part1
    best_shot = check_deepest_curve(target)
    print(f"{best_shot=}")
    ymin = best_shot[1] * (best_shot[1] - 1) / 2
    print(f"highest point {ymin}")

    # part 2
    v = check_possible_v(target)
    print(len(v))
