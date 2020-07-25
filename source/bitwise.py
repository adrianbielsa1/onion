def encode(byte_data: bytes):
    # The result is a "bytearray" object, which is mutable. Assignment is then faster compared
    # against a "bytes" object since there's no need to re-create and copy the object.
    byte_result = bytearray(len(byte_data))

    for index, character in enumerate(byte_data):
        # Get the MSB and move it all the way to the right, making it the LSB.
        first_bit = (character & 128)
        first_bit = (first_bit >> 7)

        # NOTE: This is a small patch to deal with integer promotion in Python.
        # Left shifting causes the "int" object to go from 8 bits to 9 bits in size,
        # which, if the MSB is non-zero, yields a value greater than 255 (the
        # maximum "byte" object value). By making the MSB zero, integer
        # promotion still happens, but it doesn't affect the result.
        character = (character & 0b01111111)

        # Shift the character one bit to the left (discarding the MSB), then
        # replace the LSB with what was the MSB, effectively rotating the
        # bit stream to the left.
        character = (character << 1)
        character = (character | first_bit)

        # Flip odd bits (1, 3, 5, 7).
        character = (character ^ 0b01010101)

        # Copy the character to our result.
        byte_result[index] = character

    return byte_result

def decode(byte_data: bytes):
    # The result is a "bytearray" object, which is mutable. Assignment is then faster compared
    # against a "bytes" object since there's no need to re-create and copy the object.
    byte_result = bytearray(len(byte_data))

    for index, character in enumerate(byte_data):
        # Flip odd bits (1, 3, 5, 7) and shift to the right.
        character = (character ^ 0b01010101)

        # Get the last bit (LSB) and move it all the way to the left,
        # leaving zeroes at its right.
        last_bit = (character & 1)
        last_bit = (last_bit << 7)

        # Shift the character one bit to the right and replace the MSB with
        # the one that was the LSB. All other bits are untouched because
        # in "last_bit" the only non-zero bit is the MSB.
        character = (character >> 1)
        character = (character | last_bit)

        # Copy the character to our result.
        byte_result[index] = character

    return byte_result
