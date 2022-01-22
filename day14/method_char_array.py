from day14 import *


def show_dict(d):
    for k in d.keys():
        print(f"{k}->{d[k]}")


def calculate_iteratively(poly, table, step):
    poly = np.asarray(list(poly))
    print(f"Starting poly:{''.join(poly)}")
    for step in range(step):
        print(f"Step:{step + 1}")
        reactions = np.char.add(poly[:-1], poly[1:])
        new_poly = np.empty_like(reactions, shape=(2 * poly.shape[0] - 1))
        new_poly[::2] = poly
        new_poly[1::2] = [table[x] for x in reactions]
        poly = new_poly
        print(f"{''.join(poly)}")
    return ''.join(poly)


if __name__ == "__main__":
    show_dict(reaction_table)
    calculate_iteratively(starting_polymer, reaction_table, 10)
