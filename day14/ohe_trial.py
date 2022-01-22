import numpy as np

# slows to a crawl after 21 steps

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)

all_characters = np.unique(np.array([list(a) for a in raw_input[:, 0]]).flatten())
CLASS_COUNT = len(all_characters)

def char_to_ohe(ch):
    out = np.eye(CLASS_COUNT)[all_characters == ch].flatten()
    #print(f"ohe: {ch}-->{out}")
    return out
print(raw_input)

rules = {tuple(np.hstack([char_to_ohe(a[0]),char_to_ohe(a[1])])): char_to_ohe(b) for a, b in zip(raw_input[:, 0], raw_input[:, 2])}
starting_polymer = np.array([char_to_ohe(a) for a in open(input_file, "r").readline().rstrip()])


polymer = starting_polymer
steps=40
for i in range(steps):
    print(f"{i=}")
    shifted = np.roll(polymer,shift = -1, axis=0)
    reactions = np.hstack([polymer,shifted])[:-1]
    new_polymer = np.zeros((2 * len(polymer) - 1, CLASS_COUNT))
    new_polymer[0::2] = polymer
    new_polymer[1::2] = np.array([rules[tuple(x)] for x in reactions])
    polymer = new_polymer
hist = np.sum(polymer,axis=0)
print(hist)
print(all_characters)
print(hist.max()-hist.min())