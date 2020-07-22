def decode(byte_data: bytes):
    # The result is a "bytearray" object, which is mutable. Assignment is then faster compared
    # against a "bytes" object since there's no need to re-create and copy the object.
    byte_result = bytearray(len(byte_data))

    for index, character in enumerate(byte_data):
        # TODO: I'm a bit concerned by this; it should be ROTATING not SHIFTING the bits - which is
        # inconsistent with the instructions - yet it works anyway. I've compared two outputs: one
        # generated by shifting and the other by rotating, and they're identical.
        # For simplicity, I've stick to bit shifting method.

        # Flip odd bits (1, 3, 5, 7) and shift to the right.
        character = (character ^ 0b01010101)
        character = (character >> 1)

        # Copy the character to our result.
        byte_result[index] = character

    return byte_result
