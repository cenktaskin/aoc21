from day14 import *

VOCAB = np.unique(np.array([list(a) for a in raw_input[:, 0]]).flatten())
CLASS_COUNT = len(VOCAB)


def char_to_ohe(ch):
    return np.eye(CLASS_COUNT)[VOCAB == ch].flatten()


def to_ohe(poly):
    return np.array([char_to_ohe(c) for c in poly])


def calculate_iteratively(poly, to_step):
    for i in range(to_step):
        print(f"Step:{i + 1}")
        shifted = np.roll(poly, shift=-1, axis=0)
        reactions = np.hstack([poly, shifted])[:-1]
        new_polymer = np.zeros((2 * len(poly) - 1, CLASS_COUNT))
        new_polymer[0::2] = poly
        new_polymer[1::2] = np.array([ohe_table[tuple(x)].flatten() for x in reactions])
        poly = new_polymer
    return poly


if __name__ == "__main__":
    ohe_table = {tuple(to_ohe(k).flatten()): to_ohe(reaction_table[k]) for k in reaction_table}

    polymer = calculate_iteratively(to_ohe(starting_polymer), 10)

    hist = np.sum(polymer, axis=0)
    print(hist)
    print(VOCAB)
    print(hist.max() - hist.min())
