import math
import logging
import sys


def convert_hex_to_bin(msg):
    return "".join(f"{int(a, 16):0>4b}" for a in msg)


def parse_literal_value(msg):
    packet_len = len(msg)
    logging.debug(f"Parsing literal {msg}")
    binary_string = ""
    while True:
        header, four_bits, msg = msg[0], msg[1:5], msg[5:]
        logging.debug(f"{four_bits:>{packet_len - len(msg)}}")
        binary_string += four_bits
        if header == '0':
            break
    return binary_string, msg


def read_operator_packet(msg, read_func):
    logging.debug(f"reading operator packet \n{msg}")
    length_type_id, msg = int(msg[0]), msg[1:]
    logging.debug(f"{length_type_id=}")
    body_start_idx = 15 - length_type_id * 4
    subpacket_len, body = int(msg[:body_start_idx], 2), msg[body_start_idx:]
    logging.debug(f"subp_len_info:{subpacket_len}")
    logging.debug(f"{body:>{len(msg) + 1}}")
    subpackets = []
    length_read = 0
    while length_read != subpacket_len:
        initial_len = len(body)
        value, body = read_func(body)
        subpackets.append(value)
        match length_type_id:
            case 0:
                length_read += initial_len - len(body)
            case 1:
                length_read += 1
        logging.debug(f"subpkg read:{length_read}/{subpacket_len}")

    return subpackets, body


def read_packet(msg):
    logging.debug(f"reading packet \n{msg}")
    version, type_id, body = msg[:3], msg[3:6], msg[6:]
    logging.debug(f"version={int(version, 2)}")
    logging.debug(f"type={int(type_id, 2)}")
    logging.debug(f"{body:>{len(msg)}}")
    if int(type_id, 2) == 4:
        value, left = parse_literal_value(body)
        logging.debug(f"literal ret {value, left}")
        value = int(version, 2)
    else:
        subpackets, left = read_operator_packet(body, read_packet)
        value = sum(subpackets) + int(version, 2)
    return value, left


# def part1_value_calculator(subs, vers, _):
#     return sum(subs) + int(vers, 2)


def initiate_logger(level=logging.WARNING):
    logger = logging.getLogger('root')
    logger.setLevel(level)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
    logger.addHandler(stream_handler)


def main():
    input_file = "input.txt"
    with open(input_file, 'r') as f:
        raw_input = f.read()
    # raw_input = "A0016C880162017C3686B18A3D4780"

    initiate_logger()

    packet = convert_hex_to_bin(raw_input)
    ret, left = read_packet(packet)
    print(f"{ret=}")


if __name__ == "__main__":
    main()
