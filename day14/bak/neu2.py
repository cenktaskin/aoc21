from day14 import *
from utils import *

one_step_ahead = {k: k[0] + reaction_table[k] + k[1] for k in reaction_table}


def query_the_pair(pair, at_step):
    logger.info(f"Checking {pair=} {at_step=}")
    if pair in wikipedia[at_step]:
        logger.debug(f"Recursive soln to {pair} at step {at_step} = {wikipedia[at_step][pair]}")
        return wikipedia[at_step][pair]
    else:
        half_age_status = query_the_pair(pair, at_step // 2)
        res = calculate_from_parts(half_age_status, at_step // 2)
        logger.info(f"Wikipedia updated {at_step=} for {pair}->{res}")
        wikipedia[at_step][pair] = res
        return res


def calculate_from_parts(poly, step):
    logger.debug(f"Calculating from parts {poly} using {step=}")
    res = ""
    for sli in slicer(poly):
        out = query_the_pair(sli, step)
        res = combine_slices(res, out)
    return res


def forecast_the_polymer(poly, any_step):
    if np.log2(any_step) % 1 == 0:
        return calculate_from_parts(poly, any_step)
    else:
        closest_hop = 2 ** int(np.log2(any_step))
        print("Closest even step", closest_hop)
        res = calculate_from_parts(poly, closest_hop)
        print("##########################")
        return forecast_the_polymer(res, any_step - closest_hop)


def forecast_the_polymer_neu(poly, any_step):
    next_hop = 2 ** int(np.ceil(np.log2(any_step)))
    logger.debug(f"Next hop: {next_hop}")
    res = calculate_from_parts(poly, next_hop)
    print("#######")
    return res[::2 ** (next_hop - any_step)]


def lay_fib_up_to(target_level):
    seq = [1, 2]
    while seq[-1] < target_level:
        seq.append(seq[-1] + seq[-2])
    return seq[:-1]


print(lay_fib_up_to(10))
exit()

logger.setLevel(logging.INFO)
import time

total_steps = 10
# hops = [2 ** x for x in range(int(np.log2(total_steps) + 1))]
hops = [2 ** x for x in range(int(np.ceil(np.log2(total_steps))) + 1)]
print(hops)
wikipedia = {hop: {} for hop in hops}
wikipedia[1] = one_step_ahead

start = time.time()

output = forecast_the_polymer(starting_polymer, total_steps)
hist, counts = np.unique(list(output), return_counts=True)
print(f"{hist}\n{counts}")
print(np.max(counts) - np.min(counts))
print(f"Took {time.time() - start}")

wikipedia = {hop: {} for hop in hops}
wikipedia[1] = one_step_ahead

start = time.time()

output = forecast_the_polymer_neu(starting_polymer, total_steps)
hist, counts = np.unique(list(output), return_counts=True)
print(f"{hist}\n{counts}")
print(np.max(counts) - np.min(counts))
print(f"Took {time.time() - start}")
