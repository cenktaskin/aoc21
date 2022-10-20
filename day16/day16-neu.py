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


def read_operator_packet(msg, is_part1):
    length_type_id, msg = int(msg[0]), msg[1:]
    body_start_idx = 15 - length_type_id * 4
    subpacket_len, body = int(msg[:body_start_idx], 2), msg[body_start_idx:]
    subpackets = []
    length_read = 0
    while length_read != subpacket_len:
        initial_len = len(body)
        value, body = read_packet(body, is_part1)
        subpackets.append(value)
        match length_type_id:
            case 0:
                length_read += initial_len - len(body)
            case 1:
                length_read += 1

    return subpackets, body


def read_packet(msg, is_part1):
    version, type_id, body = msg[:3], int(msg[3:6], 2), msg[6:]
    if type_id == 4:
        value, left = parse_literal_value(body)
        if is_part1:
            value = version
        value = int(value, 2)
    else:
        subpackets, left = read_operator_packet(body, is_part1)
        if is_part1:
            subpackets.append(int(version, 2))
            type_id = 0

        match type_id:
            case 0:
                value = sum(subpackets)
            case 1:
                value = math.prod(subpackets)
            case 2:
                value = min(subpackets)
            case 3:
                value = max(subpackets)
            case 5:
                value = int(subpackets[0] > subpackets[1])
            case 6:
                value = int(subpackets[0] < subpackets[1])
            case 7:
                value = int(subpackets[0] == subpackets[1])

    return value, left

# TODO You can fix this script: Just merge the two reading functions I think they are overly specialized unnecessarily
def main():
    input_file = "input.txt"
    with open(input_file, 'r') as f:
        raw_input = f.read()
    test_inputs = ["D2FE28", "38006F45291200", "EE00D40C823060"]
    raw_input = test_inputs[0]

    packet = convert_hex_to_bin(raw_input)
    ret, _ = read_packet(packet, is_part1=True)
    print(f"{ret=}")


if __name__ == "__main__":
    main()
