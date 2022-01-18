import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)


class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.capital = False

    def add_connection(self, destination):
        self.connections.append(destination)

    def __str__(self):
        msg = f"Node {self.name} --> "
        for cnt in self.connections:
            msg += cnt.name + " "
        return msg


class Graph:
    def __init__(self):
        self.nodes = []
        self.node_names = []

    def add_node(self, nd):
        if nd in self.node_names:
            # print(f"{nd} is already in graph")
            return self.get_node(nd)
        else:
            new_node = Node(nd)
            if nd.isupper():
                new_node.capital = True
            # print(f"Creating new node {nd}")
            self.nodes.append(new_node)
            self.node_names.append(nd)
            return new_node

    def get_node(self, node_name):
        return self.nodes[np.where(np.array(self.node_names) == node_name)[0][0]]

    def __str__(self):
        msg = f"Graph with nodes:\n"
        for nd in self.nodes:
            msg += nd.name + " - "
        return msg[:-3]

graph = Graph()
for line in raw_input:
    [src, dst] = line.split('-')
    node0 = graph.add_node(src)
    node1 = graph.add_node(dst)
    node0.add_connection(node1)
    node1.add_connection(node0)


valid_paths = []
def walker(current_loc, path, lucky_small_cave):
    if current_loc == "end":
        print("Path ended!!!")
        valid_paths.append(path)
        return path
    else:
        print("Current loc", current_loc, "with path", path)
        print(graph.get_node(current_loc))
        print("Possible outways")
        for dst in graph.get_node(current_loc).connections:
            if not np.any(np.array(path) == dst.name) or dst.capital:
                print(f"Walking to {dst.name} from {current_loc}")
                new_path = path.copy()
                new_path.append(dst.name)
                walker(dst.name, new_path, lucky_small_cave)
            else:
                if lucky_small_cave and not np.any(np.array(['start', 'end']) == dst.name):
                    print(f"Lucky cave is {dst.name}")
                    print(f"Walking to {dst.name} from {current_loc}")
                    new_path = path.copy()
                    new_path.append(dst.name)
                    walker(dst.name, new_path, False)
                print("Path ended (to)", dst.name)

# for part 1 set 3rd argument False
walker('start', ['start'], False)
# print(valid_paths)
print(len(valid_paths))
