__pows_of_85 = [1, 85, 7225, 614125, 52200625]

# Converts an ASCII-based bytestream into its ASCII85-based representation,
# using Adobe's guidelines.
def encode(byte_data: bytes):
    # Calculate padding bytes required (must be a multiple of 4).
    padding = (-len(byte_data) % 4)

    # Duplicate the data and add padding null-characters at the end. Duplication is
    # implicit since "bytes" objects are immutable.
    byte_data += b"\0" * padding

    # Prepare the resulting buffer and add leading guard.
    byte_result = bytearray(b"<~")

    # Loop through the data in blocks of 4 bytes.
    for i in range(0, len(byte_data), 4):
        # Convert the 4-byte block into a number. This *SHOULD* be 32 bits long if
        # Python doesn't represent it differently.
        numeric_block = int.from_bytes(byte_data[i : i + 4], "big")

        if numeric_block != 0:
            # Non-zero blocks are stored as 5 characters long strings.
            for j in range(0, 5):
                # Convert each byte in the numeric block into a base 84 digit.
                base_84_digit = (numeric_block // __pows_of_85[4 - j]) % 85

                # Convert said digit into an ASCII character ordinal between "!" and "u",
                # and store it.
                byte_result.append(base_84_digit + 33)
        else:
            # A zero-block would be represented by the 5-characters string "!!!!!",
            # however, for the sake of compression, the "z" character is used instead.
            byte_result.append(122) # ord("z")

    # Ignore padding characters and add trailing guard.
    byte_result = byte_result[0 : len(byte_result) - padding]
    byte_result += b"~>"

    return byte_result

# Converts an ASCII85-based bytestream into its ASCII representation, using
# Adobe's guidelines.
def decode(byte_data: bytes):
    # TODO: See if this makes a copy, or simply moves a pointer ("bytes" objects are
    # immutable).
    # Remove leading (<~) and trailing (~>) guards.
    byte_data = byte_data[2 : len(byte_data) - 2]

    # Calculate padding bytes required (must be a multiple of 5).
    padding = (-len(byte_data) % 5)

    # Duplicate the data and add padding "u" characters at the end. Duplication is
    # implicit since "bytes" objects are immutable.
    byte_data += b"u" * padding

    # Prepare the resulting buffer.
    byte_result = bytearray()

    # Blocks are made of 5 non-consecutive, non-z and non-whitespace characters.
    numeric_block = 0
    numeric_block_length = 0

    # Analyze each ASCII character.
    for c in byte_data:
        if c == ord("z"): # c == 122:
            # The "z" character was originally a 4 null characters block.
            byte_result.append(b"\0\0\0\0")
        elif ord("!") <= c <= ord("u"): # 33 <= c <= 117:
            # Restore the original ASCII range (0 - 84 instead of 33 - 117) by subtracting
            # 33 and undo base 84 conversion using multiplication by a power of 85.
            c -= 33
            c *= __pows_of_85[4 - numeric_block_length]

            # Re-encode the character inside a 32-bit integer.
            numeric_block += c
            numeric_block_length += 1

            # The block is complete.
            if numeric_block_length == 5:
                # Split each byte from the 4 that make up the block.
                byte_result += numeric_block.to_bytes(4, "big")

                # Reset.
                numeric_block = 0
                numeric_block_length = 0
        else:
            # Other characters are ignored.
            pass

    # Trim padding characters.
    return byte_result[0 : len(byte_result) - padding]
