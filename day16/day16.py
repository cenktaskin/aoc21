def hex2bin(ch):
    diff = ord(ch) - ord(str(9))
    if ord(ch) >= 65:
        diff -= 7  # to make up for the chars between
    return bin(9 + diff)[2:].zfill(4)


def parse_literal_value(msg):
    PACKET_LEN = len(msg)
    print(f"literal \n{msg}")
    binary_string = ""
    while True:
        header, four_bits, msg = msg[0], msg[1:5], msg[5:]
        print(f"{four_bits:>{PACKET_LEN - len(msg)}}")
        binary_string += four_bits
        if header == '0':
            break
    return binary_string, msg


def parse_packet_header(msg):
    return int(msg[:3], 2), int(msg[3:6], 2), msg[6:]


def read_packet(bits):
    if len(bits) == 0:
        return 0
    PACKET_LEN = len(bits)
    print("new packet-------------------------------")
    print(bits)
    version, type_id, bits = parse_packet_header(bits)
    print(f"{version=},{type_id=}")
    print(f"{bits:>{PACKET_LEN}}")
    if type_id == 4:
        _, leftover = parse_literal_value(bits)
        print("literal leftover", {leftover})
        if len(leftover) > 0:
            if int(leftover, 2) == 0:
                leftover = ""
        read_packet(leftover)  # literal parsin can't call, only operators can call
    else:
        length_type_id, bits = int(bits[0]), bits[1:]
        print(f"{length_type_id=}")
        match length_type_id:
            case 0:
                length, bits = int(bits[:15], 2), bits[15:]
                print(f"{length=}")
                l = len(bits)
                print(f"{bits[:length]:>{PACKET_LEN - l + length}}")
                print(f"{bits[length:]:>{PACKET_LEN}}")
                read_packet(bits[:length])
                read_packet(bits[length:])
            case 1:
                length, bits = int(bits[:11], 2), bits[11:]
                print(f"subp count={length}")
                print(f"{bits:>{PACKET_LEN}}")
                for _ in range(length):
                    bits = read_packet(bits)


# don't delete what you have read just track

if __name__ == "__main__":
    input_file = "test_input.txt"
    with open(input_file, 'r') as f:
        raw_input = f.read()
    raw_input = "D2FE28"
    packet = "".join([hex2bin(ch) for ch in raw_input])
    val, rest = parse_literal_value(packet)
    print(f"{val=},{rest=}")