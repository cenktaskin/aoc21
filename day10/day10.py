import numpy as np

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)
unique_chars = np.unique([ord(c) for c in "".join(raw_input)])


def str_to_one_hot(msg):
    return np.array([np.eye(len(unique_chars))[unique_chars == ord(ch)].flatten() for ch in msg])


lens = [len(l) for l in raw_input]
code = np.zeros((len(lens), max(lens), len(unique_chars)))
for i in range(code.shape[0]):
    code[i, :len(raw_input[i])] += str_to_one_hot(raw_input[i])

print(np.sum(code, axis=1))
print(code[0])