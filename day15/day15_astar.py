import numpy as np

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)
input_map = np.array([list(x) for x in raw_input], dtype=int)
heuristic_map = np.arange(input_map.shape[1])[::-1] + np.arange(input_map.shape[0])[::-1].reshape((-1, 1))


class Node:
    map = input_map
    adjacent_distances = np.array([(1, 0), (-1, 0), (0, -1), (0, 1)])
    heuristics = heuristic_map

    def __init__(self, coords, via=None):
        self.coordinates = tuple(coords)
        self.via = via
        self.entry_cost = Node.map[self.coordinates]
        self.cost = None
        self.combined_cost = None

    def set_cost(self, val):
        self.cost = val
        self.combined_cost = self.cost + Node.heuristics[self.coordinates]

    def get_neighbours(self):
        n = self.coordinates + Node.adjacent_distances
        return n[
            np.bitwise_and.reduce(n >= 0, axis=1) & np.bitwise_and.reduce(n <= np.array(Node.map.shape) - 1, axis=1)]

    def __str__(self):
        return f"Node {self.coordinates} (via {self.via}) with cost:{self.cost}"


starting_node = Node((0, 0))
starting_node.set_cost(0)

queue = [starting_node]

end_goal_reached = False
been_to = np.zeros_like(input_map)
while not end_goal_reached:
    current_node = queue[0]
    print(f"Checking node {current_node}")
    neighbours = current_node.get_neighbours()
    print(f"Neighbours:")
    for n in neighbours:
        if been_to[tuple(n)]:
            print(f"We've been to {n}")
            continue
        new_node = Node(tuple(n), via=current_node.coordinates)
        new_node.set_cost(new_node.entry_cost + current_node.cost)
        queue.append(new_node)
        print(new_node)
    explored_node = queue.pop(0)
    been_to[explored_node.coordinates] = 1
    # Use the combined heuristic when you are reordering the queue
    # We haven't use the same node appearing in queue with different cost?
    # print([k.cost for k in queue])
    queue.sort(key=lambda x: x.cost)
    # print([k.cost for k in queue])
    print(f"Done with node at {current_node.coordinates}")
    if explored_node.coordinates == tuple(np.array(input_map.shape) - 1):
        end_goal_reached = True
        print(f"Visited {len(been_to)} nodes in total, lowest possible cost {explored_node.cost}")
