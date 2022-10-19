from day16 import parse_literal_value, convert_hex_to_bin, read_operator_packet
import math


def read_packet(msg):
    # print(f"reading packet \n{msg}")
    version, type_id, body = msg[:3], msg[3:6], msg[6:]
    # print(f"version={int(version, 2)}")
    # print(f"type={int(type_id, 2)}")
    # print(f"{body:>{len(msg)}}")
    if int(type_id, 2) == 4:
        value, left = parse_literal_value(body)
        value = int(value, 2)
    else:
        subpackets, left = read_operator_packet(body, read_packet)
        match int(type_id, 2):
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


if __name__ == "__main__":
    input_file = "input.txt"
    with open(input_file, 'r') as f:
        raw_input = f.read()

    packet = convert_hex_to_bin(raw_input)
    ret, left = read_packet(packet)
    print(f"{ret=}")
