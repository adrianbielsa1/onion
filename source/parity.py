def count_bits_turned_on(byte: int):
    count = 0

    # MSB -> LSB (not included).
    for i in range(7, 0, -1):
        if byte & (2 ** i):
            count += 1

    return count

def get_data_carrying_bits(byte: int):
    # Resulting bit stream.
    result = ""

    # NOTE: All bits (except the LSB) must be analyzed since leading
    # 0 bits are also important. This cannot be achieved using
    # built-in functions like "bin" since they discard unimportant
    # zeros.
    # MSB -> LSB (not included).
    for i in range(7, 0, -1):
        if byte & (2 ** i):
            result += "1"
        else:
            result += "0"

    return result

def decode(byte_data: bytes):
    # Result of the operation.
    byte_result = bytearray()

    # Temporal bit stream which will be converted to bytes when possible.
    bit_stream = ""

    for b in byte_data:
        # Count all non-LSB non-zero bits and get the parity bit, which
        # is the LSB.
        bits_turned_on = count_bits_turned_on(b)
        parity_bit = b & 1

        # If the number of bits turned on is even, then the parity bit
        # should be 0, otherwise it must be 1.
        if (bits_turned_on % 2) == parity_bit:
            # This byte's parity bit is OK, get the data carrying bits,
            # which are the other 7 bits, and store them.
            data_bits = get_data_carrying_bits(b)
            bit_stream += data_bits

            while len(bit_stream) >= 8:
                # Convert the first 8 characters into a number,
                # effectively converting bits to an integer.
                byte_result.append(int(bit_stream[0 : 8], 2))

                # Discard first 8 characters.
                bit_stream = bit_stream[8 : len(bit_stream)]

    return byte_result
