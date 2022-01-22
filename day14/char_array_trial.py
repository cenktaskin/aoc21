import numpy as np


def show_dict(d):
    for k in d.keys():
        print(f"{k}->{d[k]}")


def test_with_char_array(poly, table, step):
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
    input_file = "test_input.txt"
    raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)

    rules = {a: b for a, b in zip(raw_input[:, 0], raw_input[:, -1])}
    polymer0 = open(input_file, "r").readline().rstrip()

    show_dict(rules)
    test_with_char_array(polymer0, rules, 8)
