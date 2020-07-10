# Converts "text" into its ASCII85 Adobe-flavoured representation.
def encode(text: str):
    # Add padding characters and convert the string into a bytearray.
    padding     = (-len(text)) % 4
    text        = text.encode("utf-8")
    text        += b"\0" * padding

    result      = "<~"
    characters  = []
    index       = 0

    while index < len(text):
        # Blocks are 4-bytes long integers.
        # NOTE: I'm not sure how Python represents this internally. It may use more than 4 bytes.
        block = int.from_bytes(text[index : index + 4], "big")

        if block != 0:
            # Split the block into 84-based digits.
            digits = [
                (block // (85 ** 4)) % 85,
                (block // (85 ** 3)) % 85,
                (block // (85 ** 2)) % 85,
                (block // (85 ** 1)) % 85,
                (block // (85 ** 0)) % 85
            ]

            # Convert these digits into ASCII characters between 33 and 117.
            characters  = [ chr(digit + 33) for digit in digits ]
        else:
            # The five character string "!!!!!" should be encoded as "z", reducing the amount of
            # space used (data compression).
            characters = [ "z" ]

        for c in characters:
            result += str(c)

        index += 4

    # Trim the padding characters and add a "~>" symbol at the end.
    result = result[0 : len(result) - padding]
    result += "~>"

    return result

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
