from collections import Counter

import numpy as np

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)

all_characters = np.unique(np.array([list(a) for a in raw_input[:, 0]]).flatten())
CLASS_COUNT = len(all_characters)




# dynamic programming, keep in memory what happens to each 2 after 5 steps

one_step_ahead = {a: a[0] + b + a[1] for a, b in zip(raw_input[:, 0], raw_input[:, -1])}
starting_polymer = open(input_file, "r").readline().rstrip()


total_steps = 10
hops = [2**x for x in range(1,len(bin(total_steps))-2)]
wikipedia = {hop:{} for hop in hops}
wikipedia[1] = one_step_ahead

for key in one_step_ahead.keys():
    print(f"{key}-->{one_step_ahead[key]}")

def foresee_future(inp_pair, rules):
    poly = inp_pair
    for i in range(2):
        result = poly[0]
        for j in range(len(poly) - 1):
            if poly[j:j+2] in rules.keys():
                result += rules[poly[j:j + 2]][1:]
            else:
                get_from_wiki(poly[j:j+2],)
        poly = result
    return poly


def get_from_wiki(inp_pair, desired_depth):
    print(f"Called with {inp_pair} for {desired_depth}")
    if inp_pair not in wikipedia[desired_depth].keys():
        print("recursion")
        half_depth_res = get_from_wiki(inp_pair, desired_depth//2)
        print(f"Expanding wiki entry {inp_pair} for {desired_depth} using step {desired_depth//2}")
        val = foresee_future(inp_pair, wikipedia[desired_depth//2])
        print("Future",val)
        print(f"Saving {desired_depth} for {inp_pair} = {val}")
        wikipedia[desired_depth][inp_pair] = val
        print(wikipedia[desired_depth])
        print(f"Recursion to depth {desired_depth} is ended")
        return wikipedia[desired_depth][inp_pair]
    else:
        print("else "+wikipedia[desired_depth][inp_pair])
        return wikipedia[desired_depth][inp_pair]


print(get_from_wiki("NN",4))




exit()
poly = starting_polymer
print(f"{starting_polymer=}")
for step in hops:
    print(step)
    new_poly = poly[0]
    for j in range(len(poly) - 1):
        if poly[j:j+2] not in wikipedia[step].keys():
            pair = poly[j:j+2]
            print(f"Need to calculate {step} ahead for {pair}")
            wikipedia[step][pair] = expand_wiki_ahead(pair, wikipedia[step/2])
            print(wikipedia[step][pair])
        #new_poly += ten_step_ahead[poly[j:j + 2]][1:]
        #counts[poly[j:j + 2]] += 1
    #poly = new_poly
    #print(poly)

#hist = Counter(poly).most_common()
#print(hist)
#print(hist[0][1] - hist[-1][1])

#for key in counts.keys():
#    print(f"{key}:{counts[key]}")
