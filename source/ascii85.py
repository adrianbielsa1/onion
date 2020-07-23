__pows_of_85 = [1, 85, 7225, 614125, 52200625]

# Converts an ASCII-based bytestream into its ASCII85-based representation,
# using Adobe's guidelines.
def encode(byte_data: bytes):
    # Calculate padding bytes required.
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

# Converts "text" into its actual, non ASCII-85 value.
def decode(text: str):
    # Strip leading and trailing symbols (<~ and ~>).
    text        = text[2 : len(text) - 2]

    # Add padding characters.
    padding     = (-len(text)) % 5
    text        += "u" * padding

    result      = ""
    characters  = ""
    index       = 0

    while index < len(text):
        if text[index].isspace():
            # Skip whitespace.
            index   += 1
        elif text[index] == "z":
            # The "z" character was originally a 4-null-characters block.
            result  += b"\0" * 4
            index   += 1
        else:
            characters  = characters + text[index]

            if len(characters) == 5:
                digits      = [ ord(character) - 33 for character in characters]
                digits      = [
                    digits[0] * (85 ** 4),
                    digits[1] * (85 ** 3),
                    digits[2] * (85 ** 2),
                    digits[3] * (85 ** 1),
                    digits[4] * (85 ** 0)
                ]

                block = int.from_bytes([0, 0, 0, 0], "big")

                for digit in digits:
                    block += digit

                for b in block.to_bytes(4, "big"):
                    result += chr(b)

                characters = ""

            index += 1

    # Trim the padding characters.
    result = result[0 : len(result) - padding]

    return result
