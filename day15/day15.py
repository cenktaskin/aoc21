import numpy as np
import matplotlib.pyplot as plt
import time as t

# don't want to tire the computer so this solves in ~20 sec
t0 = t.time()
input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)
input_map = np.array([list(x) for x in raw_input], dtype=int)

#print(input_map)

adjacent_distances = np.array([(1, 0), (-1, 0), (0, -1), (0, 1)])


def get_neighbors(coord, borders):
    n = coord + adjacent_distances
    return n[np.bitwise_and.reduce(n >= 0, axis=1) & np.bitwise_and.reduce(n <= np.array(borders) - 1, axis=1)]

def iterate_a_node(queue, visited, input_map):
    # disect element to parts
    current_node_ind = np.argmin(queue[:, :1])
    current_node_coord = queue[current_node_ind, 1:3]
    current_cost = queue[current_node_ind, 0]
    #print(f"Current node {current_node_coord}")
    for neighbor in get_neighbors(current_node_coord, input_map.shape):
        if not visited[tuple(neighbor)]:
            #print(f"Checking neighbor at {neighbor}")
            entry_cost = input_map[tuple(neighbor)]
            new_entry = np.insert(np.array([neighbor, current_node_coord]).flatten(), 0, entry_cost+current_cost, axis=0)
            #print(f"New entry {new_entry}")
            already_explored = np.all(queue[:, 1:3] == new_entry[1:3], axis=1)
            if np.any(already_explored):
                old_ind = np.where(already_explored)[0][0]
                old_price = queue[old_ind,0]
                new_price = new_entry[0]
                #print(f"{old_price=}")
                #print(f"{new_price=}")
                if new_price < old_price:
                    #print("Found a better way")
                    queue[old_ind] = new_entry
            else:
                queue = np.vstack([queue, new_entry])
    #print(f"Done with {current_node_coord}")
    #print(f"{queue=}")
    visited[tuple(current_node_coord)] = True
    queue = np.delete(queue, current_node_ind, axis=0)

    if np.all(current_node_coord == np.array(input_map.shape) - 1):
        print(current_node_coord)
        print(current_cost)
        print("Done")
        # finished
        print(f"{t.time() - t0}")
        exit()
    #print(visited)
    #print("Queue after removal")
    #print(queue)
    #print("\n*********\n")
    return queue

part_2 = True
if part_2:
    new_map = np.vstack([np.hstack([input_map + i for i in range(5)]) + i for i in range(5)])
    new_map[new_map > 9] -= 9  # one subtraction is enough since max increase is +8
    input_map = new_map

visited = np.zeros_like(input_map, dtype=bool)
queue = np.array([0, 0, 0, -1, -1]).reshape(1,5)

#print(queue)

# element : [cost, y, x, prev_y, prev_x]
i=0
while True:
    queue = iterate_a_node(queue, visited, input_map)


    #i += 1
    #if i % 5000 == 0:
    #    plt.imshow(visited)
    #    plt.show(block=False)
    #    plt.pause(10 ** -250)
    #    plt.clf()

