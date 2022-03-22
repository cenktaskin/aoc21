from pathlib import Path
import numpy as np

day = Path(__file__).stem
# print(day)

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)[0]
raw_input = "D2FE28"


def hex2bin(ch):
    diff = ord(ch) - ord(str(9))
    if ord(ch) >= 65:
        diff -= 7  # to make up for the chars between
    return bin(9 + diff)[2:].zfill(4)


msg = "".join([hex2bin(ch) for ch in raw_input])
print(msg)
pkg_version = int(msg[:3], 2)
pkg_type_id = int(msg[3:6], 2)
print(f"{pkg_version=}")
print(f"{pkg_type_id=}")
if pkg_type_id != 4:
    # operator
    print("I don't know")
else:
    print(len(msg) - 6)
    print(msg[6::4])
    result = int(msg[6:], 2)
