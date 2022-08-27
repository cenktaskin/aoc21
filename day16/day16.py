def hex2bin(ch):
    diff = ord(ch) - ord(str(9))
    if ord(ch) >= 65:
        diff -= 7  # to make up for the chars between
    return bin(9 + diff)[2:].zfill(4)

def convert_hex_to_bin(msg):
    while msg[-1] == '0':
        msg = msg[:-1]
    return "".join([hex2bin(ch) for ch in msg])


def parse_packet_header(msg):
    return msg[:3], msg[3:6], msg[6:]


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
    return msg, binary_string


def read_packet(msg, version_sum=0):
    print(msg)
    print("parsing header")
    version, type_id, body = parse_packet_header(msg)
    version_sum += int(version, 2)
    print(f"version:{int(version, 2)}")
    print(f"{body:>{len(msg)}}")
    if int(type_id, 2) == 4:
        print(f"literal")
        body, literal_string = parse_literal_value(body)
        print(f"return body {body}, {int(literal_string, 2)}")
        if len(body) == 0:
            print("done")
        elif len(body) < 4:
            if int(body, 2) == 0:
                print("just extra 0s, done")
    else:
        length_type_id, body = body[0], body[1:]
        match int(length_type_id, 2):
            case 0:
                print(f"length_type_id is 0")
                subpacket_length, body = int(body[:15], 2), body[15:]
                print(f"{subpacket_length=}")
                length_read = 0
                while length_read != subpacket_length:
                    left, version_sum = read_packet(body, version_sum)
                    length_read += len(body) - len(left)
                    body = left
            case 1:
                print(f"length_type_id is 1")
                subpacket_count, body = int(body[:11], 2), body[11:]
                print(f"{subpacket_count=}")
                for i in range(subpacket_count):
                    print(f"{i}th subpkg")
                    body, version_sum = read_packet(body, version_sum)
    return body, version_sum


if __name__ == "__main__":
    input_file = "input.txt"
    with open(input_file, 'r') as f:
        raw_input = f.read()

    packet = convert_hex_to_bin(raw_input)
    _, sum_of_vers = read_packet(packet)
    print(f"{sum_of_vers=}")
