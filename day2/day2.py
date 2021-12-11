import numpy as np

with open("input.txt", 'r') as f:
    raw_input = f.read().split('\n')


def map_commands(command):
    [dir, mag] = command.split(" ")
    return dir2coord[dir] * int(mag)


dir2coord = {"forward": np.array([1, 0]),
             "down": np.array([0, -1]),
             "up": np.array([0, 1])
             }

commands = np.array([map_commands(x) for x in raw_input])
result = np.sum(commands, axis=0)
# minus since coord frame is inverted, depth is positive in the quesiton
print(result[0] * -result[1])

# part 2
forward_commands = np.where(commands[:,0] > 0)[0]
depth = 0
for f_command in forward_commands:
    considered_aim = commands[:f_command]
    current_aim = np.sum(considered_aim, axis=0)[1]
    depth += current_aim * commands[f_command,0]
print(result[0] * -depth)