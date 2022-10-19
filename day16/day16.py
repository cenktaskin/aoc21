def convert_hex_to_bin(msg):
    return "".join(f"{int(a, 16):0>4b}" for a in msg)


def parse_literal_value(msg):
    packet_len = len(msg)
    print(f"{msg}")
    binary_string = ""
    while True:
        header, four_bits, msg = msg[0], msg[1:5], msg[5:]
        print(f"{four_bits:>{packet_len - len(msg)}}")
        binary_string += four_bits
        if header == '0':
            break
    return binary_string, msg


def read_operator_packet(msg):
    print(f"reading operator packet \n{msg}")
    length_type_id, msg = int(msg[0]), msg[1:]
    print(f"{length_type_id=}")
    body_start_idx = 15 - length_type_id * 4
    subpacket_len, body = int(msg[:body_start_idx], 2), msg[body_start_idx:]
    print(f"subp_len_info:{subpacket_len}")
    print(f"{body:>{len(msg) + 1}}")
    subpackets = []
    length_read = 0
    while length_read != subpacket_len:
        initial_len = len(body)
        value, body = read_packet(body)
        subpackets.append(value)
        match length_type_id:
            case 0:
                length_read += initial_len - len(body)
            case 1:
                length_read += 1
        print(f"subpkg read:{length_read}/{subpacket_len}")

    return subpackets, body


def read_packet(msg):
    print(f"reading packet \n{msg}")
    version, type_id, body = msg[:3], msg[3:6], msg[6:]
    print(f"version={int(version, 2)}")
    print(f"type={int(type_id, 2)}")
    print(f"{body:>{len(msg)}}")
    if int(type_id, 2) == 4:
        value, left = parse_literal_value(body)
        print(f"literal ret {value, left}")
        value = int(version, 2)
    else:
        subpackets, left = read_operator_packet(body)
        value = sum(subpackets) + int(version, 2)
    return value, left


if __name__ == "__main__":
    input_file = "input.txt"
    with open(input_file, 'r') as f:
        raw_input = f.read()
    raw_input = "A0016C880162017C3686B18A3D4780"
    packet = convert_hex_to_bin(raw_input)
    ret, left = read_packet(packet)
    print(f"{ret=}")
