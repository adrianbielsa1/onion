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
