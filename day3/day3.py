import numpy as np

with open("input.txt", 'r') as f:
    raw_input = np.array(f.read().split('\n'))

report = np.array(list(map(list, raw_input))).astype(int)
gamma_rate = np.array([np.argmax(np.bincount(report[:, x])) for x in range(report.shape[1])]).astype(str)
epsilon_rate = np.invert(gamma_rate.astype(bool)).astype(int).astype(str)


# print(int("".join(epsilon_rate),2)*int("".join(gamma_rate),2))

# part 2

def iterate_freq_element(arr, acc, oxy=True, debug=False):
    frequencies = np.bincount(arr[:, 0])
    dominant_nr = np.argmax(frequencies)
    if not ((frequencies[0] == frequencies[1]) ^ oxy):  # took me awhile, check the truth table of equality vs oxygen(or c02)
        dominant_nr = 1 - dominant_nr
    acc += str(dominant_nr)
    survivors = arr[arr[:, 0] == dominant_nr][:, 1:]  # slicing is to get rid of used col, before recursive call
    if debug:
        print(f"Calling this func with {len(arr)} entries")
        print(f"{frequencies=} \n{dominant_nr=} \nReduced to {survivors.shape[0]} entries")
    if survivors.shape[0] == 1:
        return acc + "".join(survivors.astype(str)[0])
    return iterate_freq_element(survivors, acc, oxy, debug)



oxygen_rating = iterate_freq_element(report, "", True)
print(oxygen_rating)
co2_rating = iterate_freq_element(report, "", False)
print(co2_rating)

print(int(oxygen_rating,2)*int(co2_rating,2))