import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)
input_map = np.array([list(x) for x in raw_input], dtype=int)

adjacent_distances = np.array([(1, 0), (-1, 0), (0, -1), (0, 1)])


def get_neighbours(coord, borders):
    n = coord + adjacent_distances
    return n[np.bitwise_and.reduce(n >= 0, axis=1) & np.bitwise_and.reduce(n <= np.array(borders) - 1, axis=1)]


def draw_the_path(prevs, src, dst, map):
    path = np.zeros_like(prevs)
    while (dst != src) and (dst is not None):
        path[dst] = 1
        dst = prevs[dst]
    print(f"Shortest path \n {path} \n {np.sum(path * map)}")
    return path


def a_star(inp_map, src=(0, 0), dst=None, dijkstra=False):
    if dst is None:
        dst = tuple(t - 1 for t in inp_map.shape)
    visited = np.zeros_like(inp_map, dtype=bool)
    distances = visited + np.inf
    distances[src] = 0
    previous_node = np.zeros_like(inp_map, dtype=object) + np.nan

    width = np.arange(inp_map.shape[0])[::-1]
    manhattan_dst = np.zeros(inp_map.shape) + width + width.reshape(-1, 1)
    if dijkstra:
        manhattan_dst = 0

    while True:
        canditates = distances.copy() + manhattan_dst
        canditates[visited] = np.inf
        current_node = np.unravel_index(np.argmin(canditates), canditates.shape)
        print(f"Checking node {current_node} with cost {canditates[current_node]}")
        if current_node == dst or canditates[current_node] == np.inf:
            print(f"{np.sum(visited)} nodes have been visited")
            return draw_the_path(previous_node, src, dst, inp_map)

        for n in get_neighbours(current_node, inp_map.shape):
            neighb = tuple(n)
            if ~visited[neighb]:
                new_dist = inp_map[neighb] + distances[current_node]
                if new_dist < distances[neighb]:
                    distances[neighb] = new_dist
                    previous_node[neighb] = current_node

        visited[current_node] = True


def a_star_rolling(inp_map, src=(0, 0), dst=None, dijkstra=False):
    # as you hit and land on a new tile call a new a_star. No need to change the algorithm
    # since it can take any start posn. We always now the map, and we know the heuristics so its ok
    if dst is None:
        dst = tuple(t - 1 for t in inp_map.shape)
    visited = np.zeros_like(inp_map, dtype=bool)
    distances = visited + np.inf
    distances[src] = 0
    previous_node = np.zeros_like(inp_map, dtype=object) + np.nan

    width = np.arange(inp_map.shape[0])[::-1]
    manhattan_dst = np.zeros(inp_map.shape) + width + width.reshape(-1, 1)
    if dijkstra:
        manhattan_dst = 0

    while True:
        canditates = distances.copy() + manhattan_dst
        canditates[visited] = np.inf
        current_node = np.unravel_index(np.argmin(canditates), canditates.shape)
        print(f"Checking node {current_node} with cost {canditates[current_node]}")
        if ((current_node[0] % 100 == 0) or (current_node[1] % 100 == 0)) and (current_node[0]+current_node[1]>100):
            print("cuk")
            exit()

        if current_node == dst or canditates[current_node] == np.inf:
            print(f"{np.sum(visited)} nodes have been visited")
            return draw_the_path(previous_node, src, dst, inp_map)

        for n in get_neighbours(current_node, inp_map.shape):
            neighb = tuple(n)
            if ~visited[neighb]:
                new_dist = inp_map[neighb] + distances[current_node]
                if new_dist < distances[neighb]:
                    distances[neighb] = new_dist
                    previous_node[neighb] = current_node

        visited[current_node] = True


# shortest_path = a_star(input_map, initial_node)
# print(shortest_path)
# print(np.sum(shortest_path * input_map))

# part 2
new_map = np.vstack([np.hstack([input_map + i for i in range(5)]) + i for i in range(5)])
new_map[new_map > 9] -= 9  # one subtraction is enough since max increase is +8
#input_map = new_map  # uncomment to execute part 2
print(input_map.shape)
shortest_path = a_star(input_map)
