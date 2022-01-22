import logging
import sys

import numpy as np

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(stream_handler)

input_file = "test_input.txt"
raw_input = np.genfromtxt(input_file, skip_header=2, dtype=str)

reaction_table = {a: b for a, b in zip(raw_input[:, 0], raw_input[:, -1])}
starting_polymer = open(input_file, "r").readline().rstrip()
